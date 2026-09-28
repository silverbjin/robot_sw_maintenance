import time

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String


class Lab12Monitor(Node):
    def __init__(self):
        super().__init__('lab12_monitor')
        self.declare_parameter('scan_topic', '/lidar_scan')
        self.declare_parameter('status_topic', '/lab12/function_status')
        self.declare_parameter('scan_timeout_sec', 2.0)

        scan_topic = str(self.get_parameter('scan_topic').value)
        status_topic = str(self.get_parameter('status_topic').value)
        self.timeout_sec = float(self.get_parameter('scan_timeout_sec').value)

        self.last_scan_monotonic = None
        self.scan_count = 0
        self.subscription = self.create_subscription(LaserScan, scan_topic, self.on_scan, 10)
        self.status_publisher = self.create_publisher(String, status_topic, 10)
        self.timer = self.create_timer(1.0, self.publish_status)
        self.get_logger().info(f'Monitoring {scan_topic}; publishing status on {status_topic}')

    def on_scan(self, _msg):
        self.last_scan_monotonic = time.monotonic()
        self.scan_count += 1

    def publish_status(self):
        healthy = (
            self.last_scan_monotonic is not None
            and (time.monotonic() - self.last_scan_monotonic) <= self.timeout_sec
        )
        msg = String()
        if healthy:
            msg.data = (
                'NODE_STATUS=PASS;TOPIC_STATUS=PASS;'
                f'SCAN_COUNT={self.scan_count};FUNCTION_TEST=PASS'
            )
        else:
            msg.data = (
                'NODE_STATUS=PASS;TOPIC_STATUS=FAIL;'
                f'SCAN_COUNT={self.scan_count};FUNCTION_TEST=FAIL'
            )
        self.status_publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = Lab12Monitor()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
