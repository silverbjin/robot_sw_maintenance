import math

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan


class Lab12LidarPublisher(Node):
    def __init__(self):
        super().__init__('lab12_lidar_publisher')
        self.declare_parameter('lidar_port', '/dev/ttyUSB1')
        self.declare_parameter('expected_lidar_port', '/dev/ttyUSB1')
        self.declare_parameter('publish_rate_hz', 10.0)

        self.lidar_port = str(self.get_parameter('lidar_port').value)
        self.expected_port = str(self.get_parameter('expected_lidar_port').value)
        self.rate_hz = float(self.get_parameter('publish_rate_hz').value)

        self.publisher = self.create_publisher(LaserScan, '/lidar_scan', 10)
        self.timer = self.create_timer(1.0 / max(self.rate_hz, 1.0), self.publish_scan)

        if self.lidar_port == self.expected_port:
            self.get_logger().info(
                f'LiDAR configuration OK: port={self.lidar_port}, rate={self.rate_hz:.1f} Hz'
            )
        else:
            self.get_logger().error(
                f'LiDAR configuration mismatch: configured={self.lidar_port}, '
                f'expected={self.expected_port}. No scan data will be published.'
            )

    def publish_scan(self):
        if self.lidar_port != self.expected_port:
            return

        msg = LaserScan()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'laser'
        msg.angle_min = -math.pi
        msg.angle_max = math.pi
        msg.angle_increment = math.pi / 180.0
        msg.time_increment = 0.0
        msg.scan_time = 1.0 / self.rate_hz
        msg.range_min = 0.12
        msg.range_max = 12.0
        count = int(round((msg.angle_max - msg.angle_min) / msg.angle_increment)) + 1
        msg.ranges = [2.0 + 0.2 * math.sin(i * 0.12) for i in range(count)]
        msg.intensities = [50.0] * count
        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = Lab12LidarPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
