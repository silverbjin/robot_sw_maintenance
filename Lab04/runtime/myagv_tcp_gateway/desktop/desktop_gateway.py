#!/usr/bin/env python3
"""Desktop PC / ROS 2 Humble side of the myAGV TCP gateway."""
from __future__ import annotations

import argparse
import json
import math
import queue
import signal
import socket
import sys
import threading
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from common.config import GatewayConfig
from common.protocol import (
    NDJSONBuffer,
    PROTOCOL_VERSION,
    ProtocolError,
    VelocityLimits,
    encode_message,
    make_message,
    validate_cmd_vel,
)
from desktop.session import DesktopProtocolSession, DesktopSessionState

try:
    import rclpy
    from rclpy.node import Node
    from geometry_msgs.msg import Twist
    from nav_msgs.msg import Odometry
    from sensor_msgs.msg import Imu
    from std_msgs.msg import Bool, Float32, String
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "ROS 2 Python packages are unavailable. Source ROS 2 Humble before running: "
        "source /opt/ros/humble/setup.bash"
    ) from exc


class DesktopGatewayNode(Node):
    def __init__(self, config: GatewayConfig):
        super().__init__("myagv_tcp_gateway_desktop")
        self.cfg = config
        self._limits = VelocityLimits(
            config.max_linear_x,
            config.max_linear_y,
            config.max_angular_z,
        )
        self._session_state = DesktopSessionState()
        self._session_lock = threading.Lock()
        self._events: queue.Queue = queue.Queue(maxsize=200)
        self._shutdown = threading.Event()
        self._ready = threading.Event()
        self._socket_lock = threading.Lock()
        self._socket = None

        self._odom_pub = self.create_publisher(Odometry, "/gateway/odom", 10)
        self._imu_pub = self.create_publisher(Imu, "/gateway/imu", 10)
        self._voltage_pub = self.create_publisher(Float32, "/gateway/voltage", 10)
        self._scan_health_pub = self.create_publisher(String, "/gateway/scan_health", 10)
        self._connected_pub = self.create_publisher(Bool, "/gateway/connected", 10)
        self._status_pub = self.create_publisher(String, "/gateway/status", 10)
        self.create_subscription(Twist, "/gateway/cmd_vel", self._cmd_cb, 10)
        self.create_timer(0.05, self._event_tick)

        self._network_thread = threading.Thread(
            target=self._client_loop,
            name="myagv-gateway-tcp-client",
            daemon=True,
        )
        self._network_thread.start()
        self._publish_connected(False)
        self._publish_status("STARTING", detail=f"robot={config.robot_ip}:{config.gateway_port}")

    def _cmd_cb(self, msg: Twist) -> None:
        temp = make_message(
            "CMD_VEL",
            0,
            linear_x=float(msg.linear.x),
            linear_y=float(msg.linear.y),
            angular_z=float(msg.angular.z),
        )
        try:
            normalized = validate_cmd_vel(temp, self._limits)
        except ProtocolError as exc:
            self.get_logger().error(f"dropping invalid local command: {exc}")
            self._publish_status("INVALID_LOCAL_COMMAND", detail=str(exc))
            return

        with self._session_lock:
            accepted = self._session_state.set_command(
                normalized["linear_x"],
                normalized["linear_y"],
                normalized["angular_z"],
            )
        if not accepted:
            self.get_logger().warning("dropping command because gateway session is not ready")

    def _put_event(self, kind: str, payload=None) -> None:
        try:
            self._events.put_nowait((kind, payload))
        except queue.Full:
            try:
                self._events.get_nowait()
            except queue.Empty:
                pass
            try:
                self._events.put_nowait((kind, payload))
            except queue.Full:
                pass

    def _event_tick(self) -> None:
        while True:
            try:
                kind, payload = self._events.get_nowait()
            except queue.Empty:
                return
            if kind == "connected":
                self._publish_connected(bool(payload))
                self._publish_status("CONNECTED" if payload else "DISCONNECTED")
            elif kind == "state":
                self._publish_state(payload)
            elif kind == "scan_health":
                msg = String()
                msg.data = json.dumps(payload, separators=(",", ":"), allow_nan=False)
                self._scan_health_pub.publish(msg)
            elif kind == "error":
                self._publish_status("ERROR", detail=str(payload))
                self.get_logger().error(str(payload))
            elif kind == "heartbeat":
                self._publish_status("HEARTBEAT_OK")

    def _publish_connected(self, connected: bool) -> None:
        msg = Bool()
        msg.data = bool(connected)
        self._connected_pub.publish(msg)

    def _publish_status(self, state: str, *, detail: str = "") -> None:
        msg = String()
        msg.data = json.dumps(
            {"state": state, "detail": detail, "timestamp": time.time()},
            separators=(",", ":"),
            allow_nan=False,
        )
        self._status_pub.publish(msg)

    def _publish_state(self, state: dict) -> None:
        stamp = self.get_clock().now().to_msg()
        odom = state.get("odom")
        if isinstance(odom, dict):
            msg = Odometry()
            msg.header.stamp = stamp
            msg.header.frame_id = str(odom.get("frame_id") or "odom")
            msg.child_frame_id = str(odom.get("child_frame_id") or "base_link")
            msg.pose.pose.position.x = float(odom.get("x", 0.0))
            msg.pose.pose.position.y = float(odom.get("y", 0.0))
            yaw = float(odom.get("yaw", 0.0))
            msg.pose.pose.orientation.z = math.sin(yaw / 2.0)
            msg.pose.pose.orientation.w = math.cos(yaw / 2.0)
            msg.twist.twist.linear.x = float(odom.get("linear_x", 0.0))
            msg.twist.twist.linear.y = float(odom.get("linear_y", 0.0))
            msg.twist.twist.angular.z = float(odom.get("angular_z", 0.0))
            self._odom_pub.publish(msg)

        imu = state.get("imu")
        if isinstance(imu, dict):
            msg = Imu()
            msg.header.stamp = stamp
            msg.header.frame_id = str(imu.get("frame_id") or "imu_link")
            msg.orientation_covariance[0] = -1.0
            msg.angular_velocity.z = float(imu.get("angular_z", 0.0))
            msg.linear_acceleration.x = float(imu.get("linear_accel_x", 0.0))
            msg.linear_acceleration.y = float(imu.get("linear_accel_y", 0.0))
            msg.linear_acceleration.z = float(imu.get("linear_accel_z", 0.0))
            self._imu_pub.publish(msg)

        voltage = state.get("voltage")
        if isinstance(voltage, (int, float)) and not isinstance(voltage, bool) and math.isfinite(float(voltage)):
            msg = Float32()
            msg.data = float(voltage)
            self._voltage_pub.publish(msg)

    def _next_message(self, seq_box: list, message_type: str, **fields):
        seq_box[0] += 1
        return make_message(message_type, seq_box[0], **fields)

    def _send(self, sock: socket.socket, message: dict) -> None:
        sock.sendall(encode_message(message))

    def _client_loop(self) -> None:  # pragma: no cover - integration/hardware path
        backoff = self.cfg.reconnect_min_sec
        while not self._shutdown.is_set():
            sock = None
            try:
                sock = socket.create_connection(
                    (self.cfg.robot_ip, self.cfg.gateway_port),
                    timeout=max(1.0, self.cfg.socket_timeout_sec * 5.0),
                )
                sock.settimeout(self.cfg.socket_timeout_sec)
                with self._socket_lock:
                    self._socket = sock
                with self._session_lock:
                    self._session_state.on_connect()
                proto = DesktopProtocolSession()
                buf = NDJSONBuffer(self.cfg.max_line_bytes)
                seq_box = [0]
                self._send(
                    sock,
                    self._next_message(
                        seq_box,
                        "HELLO",
                        protocol_version=PROTOCOL_VERSION,
                        role="desktop",
                    ),
                )
                last_heartbeat = 0.0
                backoff = self.cfg.reconnect_min_sec
                close_requested = False

                while not self._shutdown.is_set() and not close_requested:
                    now = time.monotonic()
                    if self._ready.is_set() and now - last_heartbeat >= self.cfg.heartbeat_period_sec:
                        self._send(sock, self._next_message(seq_box, "HEARTBEAT"))
                        last_heartbeat = now

                    if self._ready.is_set():
                        with self._session_lock:
                            command = self._session_state.take_command_for_send()
                        if command is not None:
                            if (
                                command["linear_x"] == 0.0
                                and command["linear_y"] == 0.0
                                and command["angular_z"] == 0.0
                            ):
                                self._send(sock, self._next_message(seq_box, "STOP"))
                            else:
                                self._send(sock, self._next_message(seq_box, "CMD_VEL", **command))

                    data = None
                    try:
                        data = sock.recv(4096)
                        if data == b"":
                            break
                    except socket.timeout:
                        pass

                    if data:
                        try:
                            messages = buf.feed(data)
                        except ProtocolError as exc:
                            self._put_event("error", f"invalid frame from Jetson: {exc}")
                            messages = []
                        for message in messages:
                            result = proto.handle(message)
                            if result.hello_ack:
                                with self._session_lock:
                                    self._session_state.on_hello_ack()
                                self._ready.set()
                                self._put_event("connected", True)
                            if result.heartbeat_ack:
                                self._put_event("heartbeat", None)
                            if result.state_message is not None:
                                self._put_event("state", result.state_message)
                            if result.scan_health is not None:
                                self._put_event("scan_health", result.scan_health)
                            if result.error:
                                self._put_event("error", result.error)
                            if result.close_connection:
                                close_requested = True
                                break
            except (ConnectionError, OSError) as exc:
                self._put_event("error", f"gateway connection failed: {exc}")
            finally:
                if sock is not None:
                    if self._ready.is_set():
                        try:
                            # Best effort; Jetson disconnect watchdog is the final safety authority.
                            self._send(sock, make_message("STOP", 2_147_483_647))
                        except Exception:
                            pass
                    try:
                        sock.close()
                    except OSError:
                        pass
                with self._socket_lock:
                    self._socket = None
                self._ready.clear()
                with self._session_lock:
                    self._session_state.on_disconnect()
                self._put_event("connected", False)

            if not self._shutdown.is_set():
                time.sleep(backoff)
                backoff = min(self.cfg.reconnect_max_sec, backoff * 1.5)

    def shutdown_gateway(self) -> None:
        if self._shutdown.is_set():
            return
        self._shutdown.set()
        with self._socket_lock:
            sock = self._socket
        if sock is not None:
            try:
                sock.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
        self._network_thread.join(timeout=2.0)

    def destroy_node(self):
        self.shutdown_gateway()
        return super().destroy_node()


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, help="Path to Desktop gateway .env file")
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    cfg = GatewayConfig.from_env(args.config)
    rclpy.init(args=None)
    node = DesktopGatewayNode(cfg)
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
