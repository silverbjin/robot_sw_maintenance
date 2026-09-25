import rclpy
from rclpy.node import Node
from diagnostic_msgs.msg import DiagnosticArray, DiagnosticStatus, KeyValue
from std_msgs.msg import String


class MyAGVMonitorNode(Node):
    """Observe /myagv/status and publish a small diagnostic summary."""

    def __init__(self):
        super().__init__('myagv_monitor_node')
        self.last_status_time = None
        self.last_status_text = 'NONE'

        self.subscription = self.create_subscription(
            String, '/myagv/status', self.status_callback, 10
        )
        self.diagnostics_publisher = self.create_publisher(
            DiagnosticArray, '/diagnostics', 10
        )
        self.timer = self.create_timer(2.0, self.publish_diagnostics)

        self.get_logger().info(
            'myAGV monitor node started. Waiting for /myagv/status ...'
        )

    def status_callback(self, msg):
        self.last_status_time = self.get_clock().now()
        self.last_status_text = msg.data
        self.get_logger().info(f'received: {msg.data}')

    def publish_diagnostics(self):
        now = self.get_clock().now()

        if self.last_status_time is None:
            age_sec = -1.0
            healthy = False
        else:
            age_sec = (now - self.last_status_time).nanoseconds / 1e9
            healthy = age_sec < 3.0

        array = DiagnosticArray()
        array.header.stamp = now.to_msg()

        status = DiagnosticStatus()
        status.name = 'myagv_monitor/status'
        status.hardware_id = 'myagv_JN_2023'
        status.level = DiagnosticStatus.OK if healthy else DiagnosticStatus.WARN
        status.message = (
            'Robot status stream is healthy'
            if healthy
            else 'No recent /myagv/status message'
        )
        status.values = [
            KeyValue(key='last_status', value=self.last_status_text),
            KeyValue(key='age_sec', value=f'{age_sec:.2f}'),
        ]

        array.status = [status]
        self.diagnostics_publisher.publish(array)


def main(args=None):
    rclpy.init(args=args)
    node = MyAGVMonitorNode()
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
