#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class TrainingComponent(Node):
    def __init__(self):
        super().__init__('training_component')
        self.pub = self.create_publisher(String, '~/status', 10)
        self.timer = self.create_timer(1.0, self.tick)
        self.get_logger().info(f'{self.get_name()} started for Lab08 training')

    def tick(self):
        msg = String()
        msg.data = f'{self.get_name()}:READY'
        self.pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = TrainingComponent()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
