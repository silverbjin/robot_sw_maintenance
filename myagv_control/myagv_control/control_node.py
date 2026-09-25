import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MyAGVControlNode(Node):
    """Educational stand-in for the myAGV runtime.

    This node intentionally does NOT send motor or serial commands.
    It only publishes a status message for upgrade/rollback practice.
    """

    def __init__(self):
        super().__init__('myagv_control_node')
        self.publisher_ = self.create_publisher(String, '/myagv/status', 10)
        self.timer_ = self.create_timer(1.0, self.publish_status)
        self.seq_ = 0
        self.get_logger().info('myAGV control node started (baseline-v1).')

    def publish_status(self):
        self.seq_ += 1
        msg = String()
        msg.data = f'state=READY; seq={self.seq_}; source=myagv_control'
        self.publisher_.publish(msg)
        self.get_logger().info(f'publish: {msg.data}')


def main(args=None):
    rclpy.init(args=args)
    node = MyAGVControlNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
