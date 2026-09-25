from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    control_node = Node(
        package='myagv_control',
        executable='control_node',
        name='myagv_control_node',
        output='screen',
    )

    return LaunchDescription([control_node])
