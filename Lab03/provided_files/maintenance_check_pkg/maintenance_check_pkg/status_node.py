import rclpy
from rclpy.node import Node


class StatusNode(Node):
    def __init__(self):
        super().__init__('status_node')
        self.get_logger().info('Maintenance environment check started.')
        self.get_logger().info('ROS 2 environment is ready.')


def main(args=None):
    rclpy.init(args=args)
    node = StatusNode()
    rclpy.spin_once(node, timeout_sec=1.0)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
