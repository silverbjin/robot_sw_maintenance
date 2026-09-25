"""Safe ROS 2 status publisher used by the Session 5 baseline lab.

This node publishes simulated maintenance state only and exposes no hardware-control interface.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class StatusPublisher(Node):
    def __init__(self) -> None:
        super().__init__('myagv_status_publisher')
        self._system_pub = self.create_publisher(String, '/myagv/system_state', 10)
        self._battery_pub = self.create_publisher(String, '/myagv/battery_state', 10)
        self._network_pub = self.create_publisher(String, '/myagv/network_state', 10)
        self._timer = self.create_timer(1.0, self._publish_status)
        self.get_logger().info('Session 5 safe baseline status publisher started.')

    def _publish_status(self) -> None:
        system = String(); system.data = 'READY'
        battery = String(); battery.data = '82'
        network = String(); network.data = 'CONNECTED'
        self._system_pub.publish(system)
        self._battery_pub.publish(battery)
        self._network_pub.publish(network)


def main(args=None) -> None:
    rclpy.init(args=args)
    node = StatusPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
