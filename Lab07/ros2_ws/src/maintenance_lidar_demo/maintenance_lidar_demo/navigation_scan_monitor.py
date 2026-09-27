#!/usr/bin/env python3
"""Monitor LaserScan reception and expose the controlled timeout symptom."""

from dataclasses import dataclass


@dataclass
class TimeoutTracker:
    timeout_sec: float
    last_scan_sec: float = 0.0

    def __post_init__(self) -> None:
        if self.timeout_sec <= 0.0:
            raise ValueError("timeout_sec must be > 0")

    def mark_scan(self, now_sec: float) -> None:
        self.last_scan_sec = now_sec

    def evaluate(self, now_sec: float) -> bool:
        return (now_sec - self.last_scan_sec) > self.timeout_sec


def main(args=None) -> None:
    import rclpy
    from rclpy.node import Node
    from sensor_msgs.msg import LaserScan

    class NavigationScanMonitor(Node):
        def __init__(self) -> None:
            super().__init__("navigation_scan_monitor")
            self.declare_parameter("scan_topic", "/scan")
            self.declare_parameter("timeout_sec", 1.0)
            topic = str(self.get_parameter("scan_topic").value)
            timeout_sec = float(self.get_parameter("timeout_sec").value)
            now = self.get_clock().now().nanoseconds / 1e9
            self.tracker = TimeoutTracker(timeout_sec=timeout_sec, last_scan_sec=now)
            self.timed_out = False
            self.subscription = self.create_subscription(LaserScan, topic, self.on_scan, 10)
            self.timer = self.create_timer(0.25, self.check_timeout)
            self.get_logger().info(f"Navigation monitor subscribing to {topic}")

        def now_sec(self) -> float:
            return self.get_clock().now().nanoseconds / 1e9

        def on_scan(self, _msg: LaserScan) -> None:
            self.tracker.mark_scan(self.now_sec())
            if self.timed_out:
                self.get_logger().info("Laser scan data recovered")
                self.timed_out = False

        def check_timeout(self) -> None:
            if self.tracker.evaluate(self.now_sec()) and not self.timed_out:
                self.get_logger().warn("Laser scan data timeout")
                self.timed_out = True

    rclpy.init(args=args)
    node = NavigationScanMonitor()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
