#!/usr/bin/env python3
"""Educational LaserScan publisher with a runtime-adjustable publish rate."""

import math
from typing import List

import rclpy
from rcl_interfaces.msg import SetParametersResult
from rclpy.node import Node
from sensor_msgs.msg import LaserScan


class LidarDemoNode(Node):
    def __init__(self) -> None:
        super().__init__('lidar_node')
        self.declare_parameter('publish_rate_hz', 10.0)
        self.declare_parameter('frame_id', 'laser_frame')
        self.declare_parameter('sample_count', 360)

        self.publisher = self.create_publisher(LaserScan, '/scan', 10)
        self._timer = None
        self._rate_hz = self._validated_rate(
            float(self.get_parameter('publish_rate_hz').value)
        )
        self._create_timer(self._rate_hz)
        self.add_on_set_parameters_callback(self._on_parameters)
        self.get_logger().info(
            f'Lab11 lidar_node started: /scan at {self._rate_hz:.1f} Hz'
        )

    @staticmethod
    def _validated_rate(value: float) -> float:
        if not math.isfinite(value) or value <= 0.0 or value > 50.0:
            raise ValueError('publish_rate_hz must be > 0 and <= 50 Hz')
        return value

    def _create_timer(self, rate_hz: float) -> None:
        if self._timer is not None:
            self.destroy_timer(self._timer)
        self._timer = self.create_timer(1.0 / rate_hz, self._publish_scan)

    def _on_parameters(self, params: List) -> SetParametersResult:
        for parameter in params:
            if parameter.name == 'publish_rate_hz':
                try:
                    new_rate = self._validated_rate(float(parameter.value))
                except (TypeError, ValueError) as exc:
                    return SetParametersResult(successful=False, reason=str(exc))
                self._rate_hz = new_rate
                self._create_timer(new_rate)
                self.get_logger().warning(
                    f'/scan publish rate changed to {new_rate:.1f} Hz'
                )
        return SetParametersResult(successful=True)

    def _publish_scan(self) -> None:
        sample_count = max(16, int(self.get_parameter('sample_count').value))
        msg = LaserScan()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = str(self.get_parameter('frame_id').value)
        msg.angle_min = -math.pi
        msg.angle_max = math.pi
        msg.angle_increment = (msg.angle_max - msg.angle_min) / sample_count
        msg.time_increment = 0.0
        msg.scan_time = 1.0 / self._rate_hz
        msg.range_min = 0.12
        msg.range_max = 12.0

        # Deterministic synthetic obstacle profile. No hardware is controlled.
        ranges = []
        for index in range(sample_count):
            angle = msg.angle_min + index * msg.angle_increment
            distance = 3.0 + 0.35 * math.sin(angle * 3.0)
            if abs(angle) < 0.25:
                distance = 1.4
            ranges.append(float(distance))
        msg.ranges = ranges
        msg.intensities = [50.0] * sample_count
        self.publisher.publish(msg)


def main(args=None) -> None:
    rclpy.init(args=args)
    node = LidarDemoNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
