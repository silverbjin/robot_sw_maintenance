from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='maintenance_lidar_demo',
            executable='lidar_node',
            name='lidar_node',
            output='screen',
            parameters=[{'publish_rate_hz': 10.0}],
        ),
        Node(
            package='maintenance_lidar_demo',
            executable='monitor_node',
            name='myagv_monitor',
            output='screen',
        ),
    ])
