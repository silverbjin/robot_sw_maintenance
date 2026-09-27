#!/usr/bin/env python3
"""Deterministic LaserScan publisher used by the LAB-07 maintenance exercise."""

import math
from typing import Dict, List


def scan_geometry(sample_count: int = 360) -> Dict[str, float]:
    if sample_count < 2:
        raise ValueError("sample_count must be >= 2")
    angle_min = -math.pi
    angle_max = math.pi
    return {
        "angle_min": angle_min,
        "angle_max": angle_max,
        "angle_increment": (angle_max - angle_min) / (sample_count - 1),
        "range_min": 0.12,
        "range_max": 8.0,
    }


def generate_ranges(sample_count: int = 360, phase: int = 0) -> List[float]:
    """Return deterministic, plausible ranges for classroom use."""
    geometry = scan_geometry(sample_count)
    values = []
    for index in range(sample_count):
        angle = (2.0 * math.pi * index / sample_count) + (phase * 0.03)
        distance = 2.2 + 0.55 * math.sin(angle) + 0.20 * math.sin(3.0 * angle)
        values.append(round(min(geometry["range_max"], max(geometry["range_min"], distance)), 4))
    return values


def main(args=None) -> None:
    import rclpy
    from rclpy.node import Node
    from sensor_msgs.msg import LaserScan

    class MockLidarPublisher(Node):
        def __init__(self) -> None:
            super().__init__("lidar_node")
            self.declare_parameter("scan_topic", "/scan")
            self.declare_parameter("frequency_hz", 10.0)
            self.declare_parameter("frame_id", "laser_frame")
            self.declare_parameter("sample_count", 360)

            topic = str(self.get_parameter("scan_topic").value)
            frequency_hz = float(self.get_parameter("frequency_hz").value)
            self.frame_id = str(self.get_parameter("frame_id").value)
            self.sample_count = int(self.get_parameter("sample_count").value)
            if frequency_hz <= 0.0:
                raise ValueError("frequency_hz must be > 0")
            self.period = 1.0 / frequency_hz
            self.geometry = scan_geometry(self.sample_count)
            self.phase = 0
            self.publisher = self.create_publisher(LaserScan, topic, 10)
            self.timer = self.create_timer(self.period, self.publish_scan)
            self.get_logger().info(
                f"Mock LiDAR publishing {topic} at {frequency_hz:.1f} Hz (frame={self.frame_id})"
            )

        def publish_scan(self) -> None:
            msg = LaserScan()
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.header.frame_id = self.frame_id
            msg.angle_min = self.geometry["angle_min"]
            msg.angle_max = self.geometry["angle_max"]
            msg.angle_increment = self.geometry["angle_increment"]
            msg.time_increment = self.period / max(1, self.sample_count - 1)
            msg.scan_time = self.period
            msg.range_min = self.geometry["range_min"]
            msg.range_max = self.geometry["range_max"]
            msg.ranges = generate_ranges(self.sample_count, self.phase)
            self.phase += 1
            self.publisher.publish(msg)

    rclpy.init(args=args)
    node = MockLidarPublisher()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
