from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    config = str(Path(get_package_share_directory('maintenance_lidar_demo')) / 'config' / 'v13_broken.yaml')
    return LaunchDescription([
        Node(
            package='maintenance_lidar_demo',
            executable='mock_lidar_publisher',
            name='lidar_node',
            output='screen',
            parameters=[config],
        ),
        Node(
            package='maintenance_lidar_demo',
            executable='navigation_scan_monitor',
            name='navigation_scan_monitor',
            output='screen',
            parameters=[config],
        ),
    ])
