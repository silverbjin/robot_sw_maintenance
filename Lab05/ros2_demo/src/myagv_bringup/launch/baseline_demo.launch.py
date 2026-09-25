from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='myagv_bringup',
            executable='status_publisher',
            name='myagv_status_publisher',
            output='screen',
        )
    ])
