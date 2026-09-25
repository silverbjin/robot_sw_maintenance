"""Instructor-only reference for Session 6. Not distributed to students."""
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Monitor(Node):
    def __init__(self):
        super().__init__('myagv_monitor')
        self.create_subscription(String, '/myagv/system_state', self._cb, 10)
    def _cb(self, msg):
        self.get_logger().info(f'system_state={msg.data}')

def main(args=None):
    rclpy.init(args=args); node=Monitor()
    try: rclpy.spin(node)
    except KeyboardInterrupt: pass
    finally: node.destroy_node(); rclpy.shutdown()
