#!/usr/bin/env python3
"""Instructor-provided low-speed motion test for the Desktop/Humble gateway.

The tool publishes only on /gateway/cmd_vel, waits for a live gateway connection,
and always publishes repeated zero-velocity commands before it exits.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from common.config import GatewayConfig

try:
    import rclpy
    from rclpy.node import Node
    from geometry_msgs.msg import Twist
    from std_msgs.msg import Bool, String
except ImportError as exc:  # pragma: no cover - requires sourced ROS 2 Humble
    raise SystemExit(
        "ROS 2 Python packages are unavailable. Source ROS 2 Humble first: "
        "source /opt/ros/humble/setup.bash"
    ) from exc


class LowSpeedTestNode(Node):
    def __init__(self) -> None:
        super().__init__("myagv_gateway_low_speed_test")
        self.publisher = self.create_publisher(Twist, "/gateway/cmd_vel", 10)
        self.connected = False
        self.last_status = ""
        self.create_subscription(Bool, "/gateway/connected", self._connected_cb, 10)
        # Desktop gateway emits HEARTBEAT_OK repeatedly. This makes the connection
        # gate reliable even when this test node starts after the first Bool message.
        self.create_subscription(String, "/gateway/status", self._status_cb, 10)

    def _connected_cb(self, msg: Bool) -> None:
        self.connected = bool(msg.data)

    def _status_cb(self, msg: String) -> None:
        self.last_status = msg.data
        try:
            payload = json.loads(msg.data)
        except (TypeError, json.JSONDecodeError):
            return
        state = payload.get("state")
        if state in {"CONNECTED", "HEARTBEAT_OK"}:
            self.connected = True
        elif state == "DISCONNECTED":
            self.connected = False

    def wait_until_connected(self, timeout_sec: float) -> bool:
        end = time.monotonic() + timeout_sec
        while rclpy.ok() and time.monotonic() < end:
            rclpy.spin_once(self, timeout_sec=0.1)
            if self.connected:
                return True
        return False

    def publish_motion(
        self,
        *,
        linear_x: float = 0.0,
        linear_y: float = 0.0,
        angular_z: float = 0.0,
        duration_sec: float,
        rate_hz: float,
    ) -> None:
        msg = Twist()
        msg.linear.x = float(linear_x)
        msg.linear.y = float(linear_y)
        msg.angular.z = float(angular_z)
        period = 1.0 / rate_hz
        end = time.monotonic() + duration_sec
        while rclpy.ok() and time.monotonic() < end:
            if not self.connected:
                raise RuntimeError("Gateway connection was lost during the motion test")
            self.publisher.publish(msg)
            rclpy.spin_once(self, timeout_sec=0.0)
            time.sleep(period)

    def publish_stop(self, *, duration_sec: float = 1.0, rate_hz: float = 10.0) -> None:
        """Publish repeated zero Twist so STOP does not depend on human timing."""
        msg = Twist()
        period = 1.0 / rate_hz
        end = time.monotonic() + duration_sec
        while rclpy.ok() and time.monotonic() < end:
            self.publisher.publish(msg)
            rclpy.spin_once(self, timeout_sec=0.0)
            time.sleep(period)


def _confirm(label: str) -> None:
    input(f"\n{label}\nConfirm the area is clear, then press ENTER to continue... ")


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        default=str(Path.home() / "myagv_tcp_gateway/config/desktop.env"),
        help="Desktop gateway env file used to enforce the same velocity limits",
    )
    parser.add_argument("--linear", type=float, default=0.03, help="Test linear speed in m/s")
    parser.add_argument("--angular", type=float, default=0.10, help="Test angular speed in rad/s")
    parser.add_argument("--move-seconds", type=float, default=1.0, help="Duration of each motion step")
    parser.add_argument("--rate", type=float, default=10.0, help="Command publication rate in Hz")
    parser.add_argument("--connect-timeout", type=float, default=5.0, help="Seconds to wait for gateway status")
    return parser.parse_args(argv)


def _validate_args(args, cfg: GatewayConfig) -> None:
    if args.rate <= 0.0 or args.move_seconds <= 0.0 or args.connect_timeout <= 0.0:
        raise SystemExit("--rate, --move-seconds, and --connect-timeout must be > 0")
    if abs(args.linear) > cfg.max_linear_x:
        raise SystemExit(
            f"--linear {args.linear} exceeds configured MAX_LINEAR_X={cfg.max_linear_x}"
        )
    if abs(args.angular) > cfg.max_angular_z:
        raise SystemExit(
            f"--angular {args.angular} exceeds configured MAX_ANGULAR_Z={cfg.max_angular_z}"
        )


def main(argv=None) -> int:
    args = parse_args(argv)
    cfg = GatewayConfig.from_env(args.config)
    _validate_args(args, cfg)

    rclpy.init(args=None)
    node = LowSpeedTestNode()
    try:
        print("Waiting for /gateway/connected or HEARTBEAT_OK ...")
        if not node.wait_until_connected(args.connect_timeout):
            raise SystemExit(
                "Gateway is not connected. Start/verify the Desktop gateway before motion testing."
            )

        print("Gateway connection confirmed.")
        print(
            f"Limits: |linear| <= {cfg.max_linear_x:.3f} m/s, "
            f"|angular| <= {cfg.max_angular_z:.3f} rad/s"
        )

        _confirm("STEP 0 — initial STOP")
        node.publish_stop(rate_hz=args.rate)

        _confirm(f"STEP 1 — low-speed FORWARD ({args.linear:+.3f} m/s)")
        node.publish_motion(
            linear_x=args.linear,
            duration_sec=args.move_seconds,
            rate_hz=args.rate,
        )
        node.publish_stop(rate_hz=args.rate)

        _confirm(f"STEP 2 — low-speed REVERSE ({-args.linear:+.3f} m/s)")
        node.publish_motion(
            linear_x=-args.linear,
            duration_sec=args.move_seconds,
            rate_hz=args.rate,
        )
        node.publish_stop(rate_hz=args.rate)

        _confirm(f"STEP 3 — low-speed ROTATE ({args.angular:+.3f} rad/s)")
        node.publish_motion(
            angular_z=args.angular,
            duration_sec=args.move_seconds,
            rate_hz=args.rate,
        )
        node.publish_stop(rate_hz=args.rate)

        print("\nLow-speed sequence finished. Final STOP is being held.")
        return 0
    except KeyboardInterrupt:
        print("\nInterrupted by user; forcing STOP.")
        return 130
    except RuntimeError as exc:
        print(f"\nABORT: {exc}; forcing STOP.", file=sys.stderr)
        return 2
    finally:
        try:
            node.publish_stop(duration_sec=1.0, rate_hz=args.rate)
        except Exception as exc:  # best effort during shutdown
            print(f"Warning: final STOP publish failed: {exc}", file=sys.stderr)
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    raise SystemExit(main())
