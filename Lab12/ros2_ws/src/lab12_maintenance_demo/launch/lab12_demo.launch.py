from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    share = get_package_share_directory('lab12_maintenance_demo')
    params = os.path.join(share, 'config', 'config.yaml')
    return LaunchDescription([
        Node(
            package='lab12_maintenance_demo',
            executable='lidar_publisher',
            name='lab12_lidar_publisher',
            output='screen',
            parameters=[params],
        ),
        Node(
            package='lab12_maintenance_demo',
            executable='monitor',
            name='lab12_monitor',
            output='screen',
            parameters=[params],
        ),
    ])
