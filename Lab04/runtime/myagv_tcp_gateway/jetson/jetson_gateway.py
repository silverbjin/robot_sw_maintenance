#!/usr/bin/env python3
"""Jetson Nano / ROS 2 Galactic side of the myAGV TCP gateway."""
from __future__ import annotations

import argparse
import math
import queue
import signal
import socket
import sys
import threading
import time
from collections import deque
from pathlib import Path
from typing import Any

# Make direct execution from jetson/ work without installing a Python package.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from common.config import GatewayConfig
from common.protocol import NDJSONBuffer, ProtocolError, VelocityLimits, encode_message
from common.scan_health import summarize_scan
from jetson.session import JetsonProtocolSession
from jetson.watchdog import GatewayWatchdog

try:
    import rclpy
    from rclpy.node import Node
    from geometry_msgs.msg import Twist
    from nav_msgs.msg import Odometry
    from sensor_msgs.msg import Imu, LaserScan
except ImportError as exc:  # pragma: no cover - exercised on robot, not build container
    raise SystemExit(
        "ROS 2 Python packages are unavailable. Source ROS 2 Galactic before running: "
        "source /opt/ros/galactic/setup.bash"
    ) from exc


def _yaw_from_quaternion(q: Any) -> float:
    siny_cosp = 2.0 * (q.w * q.z + q.x * q.y)
    cosy_cosp = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
    return math.atan2(siny_cosp, cosy_cosp)


class JetsonGatewayNode(Node):
    def __init__(self, config: GatewayConfig):
        super().__init__("myagv_tcp_gateway_jetson")
        self.cfg = config
        self._limits = VelocityLimits(
            config.max_linear_x,
            config.max_linear_y,
            config.max_angular_z,
        )
        self._watchdog = GatewayWatchdog(
            heartbeat_timeout=config.heartbeat_timeout_sec,
            command_timeout=config.command_timeout_sec,
        )
        self._events: queue.Queue = queue.Queue()
        self._outgoing: queue.Queue = queue.Queue(maxsize=100)
        self._network_ready = threading.Event()
        self._shutdown = threading.Event()
        self._state_lock = threading.Lock()

        self._latest_odom = None
        self._latest_imu = None
        self._voltage = None
        self._voltage_backup = None
        self._scalar_subscriptions = {}
        self._last_scan_ranges = []
        self._last_scan_frame = ""
        self._last_scan_monotonic = None
        self._scan_times = deque(maxlen=20)

        self._cmd_pub = self.create_publisher(Twist, "/cmd_vel", 10)
        self.create_subscription(Odometry, "/odom", self._odom_cb, 10)
        self.create_subscription(Imu, "/imu", self._imu_cb, 10)
        self.create_subscription(LaserScan, "/scan", self._scan_cb, 10)

        self.create_timer(0.05, self._control_tick)
        self.create_timer(config.state_period_sec, self._state_tick)
        self.create_timer(config.scan_health_period_sec, self._scan_health_tick)
        self.create_timer(1.0, self._discover_scalar_topics)

        self._network_thread = threading.Thread(
            target=self._server_loop,
            name="myagv-gateway-tcp-server",
            daemon=True,
        )
        self._network_thread.start()
        self._publish_zero("startup")
        self.get_logger().info(
            f"Jetson gateway listening on {config.gateway_bind_host}:{config.gateway_port}; "
            f"limits=({config.max_linear_x}, {config.max_linear_y}, {config.max_angular_z})"
        )

    # ---------- ROS callbacks ----------
    def _odom_cb(self, msg: Odometry) -> None:
        p = msg.pose.pose.position
        yaw = _yaw_from_quaternion(msg.pose.pose.orientation)
        data = {
            "x": float(p.x),
            "y": float(p.y),
            "yaw": float(yaw),
            "linear_x": float(msg.twist.twist.linear.x),
            "linear_y": float(msg.twist.twist.linear.y),
            "angular_z": float(msg.twist.twist.angular.z),
            "frame_id": str(msg.header.frame_id),
            "child_frame_id": str(msg.child_frame_id),
        }
        with self._state_lock:
            self._latest_odom = data

    def _imu_cb(self, msg: Imu) -> None:
        data = {
            "angular_z": float(msg.angular_velocity.z),
            "linear_accel_x": float(msg.linear_acceleration.x),
            "linear_accel_y": float(msg.linear_acceleration.y),
            "linear_accel_z": float(msg.linear_acceleration.z),
            "frame_id": str(msg.header.frame_id),
        }
        with self._state_lock:
            self._latest_imu = data

    def _scan_cb(self, msg: LaserScan) -> None:
        now = time.monotonic()
        with self._state_lock:
            self._last_scan_ranges = list(msg.ranges)
            self._last_scan_frame = str(msg.header.frame_id)
            self._last_scan_monotonic = now
            self._scan_times.append(now)

    def _discover_scalar_topics(self) -> None:
        wanted = {"/voltage": "voltage", "/voltage_backup": "voltage_backup"}
        try:
            topic_map = dict(self.get_topic_names_and_types())
        except Exception as exc:  # pragma: no cover
            self.get_logger().warning(f"topic discovery failed: {exc}")
            return

        for topic, attr_name in wanted.items():
            if topic in self._scalar_subscriptions:
                continue
            types = topic_map.get(topic, [])
            if not types:
                continue
            try:
                from rosidl_runtime_py.utilities import get_message

                msg_type = get_message(types[0])
            except Exception as exc:  # pragma: no cover
                self.get_logger().warning(f"cannot resolve {topic} type {types[0]}: {exc}")
                continue

            def callback(msg, target=attr_name, topic_name=topic):
                raw = getattr(msg, "data", None)
                if isinstance(raw, bool) or not isinstance(raw, (int, float)):
                    self.get_logger().warning(
                        f"{topic_name} has non-scalar data; ignoring value type {type(raw).__name__}"
                    )
                    return
                value = float(raw)
                if not math.isfinite(value):
                    return
                with self._state_lock:
                    setattr(self, "_" + target, value)

            sub = self.create_subscription(msg_type, topic, callback, 10)
            self._scalar_subscriptions[topic] = sub
            self.get_logger().info(f"subscribed dynamically to {topic} ({types[0]})")

    # ---------- State publication to TCP ----------
    def _queue_outgoing(self, message_type: str, fields: dict) -> None:
        if not self._network_ready.is_set():
            return
        item = (message_type, fields)
        try:
            self._outgoing.put_nowait(item)
        except queue.Full:
            try:
                self._outgoing.get_nowait()
            except queue.Empty:
                pass
            try:
                self._outgoing.put_nowait(item)
            except queue.Full:
                pass

    def _state_tick(self) -> None:
        with self._state_lock:
            fields = {
                "odom": dict(self._latest_odom) if self._latest_odom is not None else None,
                "imu": dict(self._latest_imu) if self._latest_imu is not None else None,
                "voltage": self._voltage,
                "voltage_backup": self._voltage_backup,
            }
        self._queue_outgoing("STATE", fields)

    def _scan_health_tick(self) -> None:
        now = time.monotonic()
        with self._state_lock:
            ranges = list(self._last_scan_ranges)
            frame = self._last_scan_frame
            last = self._last_scan_monotonic
            times = list(self._scan_times)
        age = (now - last) if last is not None else self.cfg.scan_stale_sec + 1.0
        hz = 0.0
        if len(times) >= 2 and times[-1] > times[0]:
            hz = (len(times) - 1) / (times[-1] - times[0])
        fields = summarize_scan(
            ranges,
            frame,
            hz,
            age,
            stale_after_sec=self.cfg.scan_stale_sec,
        )
        self._queue_outgoing("SCAN_HEALTH", fields)

    # ---------- Safety/control ----------
    def _publish_twist(self, command: dict) -> None:
        msg = Twist()
        msg.linear.x = float(command["linear_x"])
        msg.linear.y = float(command["linear_y"])
        msg.angular.z = float(command["angular_z"])
        self._cmd_pub.publish(msg)

    def _publish_zero(self, reason: str) -> None:
        msg = Twist()
        for _ in range(3):
            self._cmd_pub.publish(msg)
        self.get_logger().warning(f"STOP published: {reason}")

    def _control_tick(self) -> None:
        now = time.monotonic()
        while True:
            try:
                event = self._events.get_nowait()
            except queue.Empty:
                break
            kind = event[0]
            if kind == "connect":
                self._watchdog.on_connect(event[1])
                self._publish_zero("new_connection")
            elif kind == "heartbeat":
                self._watchdog.on_heartbeat(event[1])
            elif kind == "command":
                command, when = event[1], event[2]
                decision = self._watchdog.on_valid_command(when)
                if decision.command_allowed:
                    self._publish_twist(command)
                else:
                    self.get_logger().warning("command blocked while gateway is fail-safe stopped")
            elif kind == "stop":
                decision = self._watchdog.on_stop(event[1])
                if decision.stop_required:
                    self._publish_zero(decision.reason or "stop")
            elif kind == "disconnect":
                decision = self._watchdog.on_disconnect(event[1])
                if decision.stop_required:
                    self._publish_zero(decision.reason or "disconnect")

        decision = self._watchdog.tick(now)
        if decision.stop_required:
            self._publish_zero(decision.reason or "watchdog")

    # ---------- TCP server ----------
    def _drain_outgoing(self, conn: socket.socket, session: JetsonProtocolSession) -> None:
        while True:
            try:
                message_type, fields = self._outgoing.get_nowait()
            except queue.Empty:
                return
            conn.sendall(encode_message(session.make_outbound(message_type, **fields)))

    def _clear_outgoing(self) -> None:
        while True:
            try:
                self._outgoing.get_nowait()
            except queue.Empty:
                return

    def _server_loop(self) -> None:  # pragma: no cover - integration/hardware path
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.cfg.gateway_bind_host, self.cfg.gateway_port))
        server.listen(1)
        server.settimeout(0.5)
        try:
            while not self._shutdown.is_set():
                try:
                    conn, address = server.accept()
                except socket.timeout:
                    continue
                except OSError:
                    if self._shutdown.is_set():
                        break
                    raise

                self.get_logger().info(f"desktop connected from {address[0]}:{address[1]}")
                self._events.put(("connect", time.monotonic()))
                self._network_ready.clear()
                self._clear_outgoing()
                session = JetsonProtocolSession(self._limits)
                buffer = NDJSONBuffer(self.cfg.max_line_bytes)
                conn.settimeout(self.cfg.socket_timeout_sec)
                close_requested = False
                try:
                    while not self._shutdown.is_set() and not close_requested:
                        data = None
                        try:
                            data = conn.recv(4096)
                            if data == b"":
                                break
                        except socket.timeout:
                            pass

                        if data:
                            try:
                                messages = buffer.feed(data)
                            except ProtocolError as exc:
                                err = session.make_outbound(
                                    "ERROR", code="INVALID_FRAME", message=str(exc)
                                )
                                conn.sendall(encode_message(err))
                                messages = []

                            for message in messages:
                                result = session.handle(message, time.monotonic())
                                for outbound in result.outbound:
                                    conn.sendall(encode_message(outbound))
                                if session.hello_ok:
                                    self._network_ready.set()
                                if result.heartbeat:
                                    self._events.put(("heartbeat", time.monotonic()))
                                if result.command_is_fresh and result.command is not None:
                                    self._events.put(("command", result.command, time.monotonic()))
                                if result.stop:
                                    self._events.put(("stop", time.monotonic()))
                                if result.close_connection:
                                    close_requested = True
                                    break

                        if self._network_ready.is_set():
                            self._drain_outgoing(conn, session)
                except (ConnectionError, BrokenPipeError, OSError) as exc:
                    self.get_logger().warning(f"TCP session ended: {exc}")
                finally:
                    self._network_ready.clear()
                    self._clear_outgoing()
                    try:
                        conn.shutdown(socket.SHUT_RDWR)
                    except OSError:
                        pass
                    conn.close()
                    self._events.put(("disconnect", time.monotonic()))
                    self.get_logger().warning("desktop disconnected")
        finally:
            server.close()

    def shutdown_gateway(self) -> None:
        if self._shutdown.is_set():
            return
        self._shutdown.set()
        self._network_ready.clear()
        self._publish_zero("gateway_shutdown")
        self._network_thread.join(timeout=2.0)

    def destroy_node(self):
        self.shutdown_gateway()
        return super().destroy_node()


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, help="Path to Jetson gateway .env file")
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    cfg = GatewayConfig.from_env(args.config)
    rclpy.init(args=None)
    node = JetsonGatewayNode(cfg)

    stop_requested = threading.Event()

    def request_stop(signum, frame):
        del signum, frame
        stop_requested.set()

    signal.signal(signal.SIGTERM, request_stop)
    try:
        while rclpy.ok() and not stop_requested.is_set():
            rclpy.spin_once(node, timeout_sec=0.2)
    except KeyboardInterrupt:
        pass
    finally:
        node.shutdown_gateway()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
