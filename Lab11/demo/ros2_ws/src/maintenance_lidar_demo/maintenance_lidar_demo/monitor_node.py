#!/usr/bin/env python3
"""Lightweight monitor node for the Lab11 LaserScan demo."""

from collections import deque

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan


class MonitorNode(Node):
    def __init__(self) -> None:
        super().__init__('myagv_monitor')
        self._timestamps = deque(maxlen=30)
        self._last_report_ns = 0
        self.create_subscription(LaserScan, '/scan', self._on_scan, 10)
        self.get_logger().info('myagv_monitor started; watching /scan rate')

    def _on_scan(self, _msg: LaserScan) -> None:
        now_ns = self.get_clock().now().nanoseconds
        self._timestamps.append(now_ns)
        if len(self._timestamps) < 4:
            return
        if now_ns - self._last_report_ns < 3_000_000_000:
            return
        self._last_report_ns = now_ns
        elapsed = (self._timestamps[-1] - self._timestamps[0]) / 1e9
        if elapsed <= 0:
            return
        rate = (len(self._timestamps) - 1) / elapsed
        if rate < 8.0:
            self.get_logger().warning(f'/scan rate LOW: {rate:.2f} Hz (baseline ≈ 10 Hz)')
        else:
            self.get_logger().info(f'/scan rate OK: {rate:.2f} Hz')


def main(args=None) -> None:
    rclpy.init(args=args)
    node = MonitorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
