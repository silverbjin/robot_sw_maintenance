from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import SetRemap


def generate_launch_description():
    own_share = Path(get_package_share_directory('myagv_lidar_bringup'))
    upstream_share = Path(get_package_share_directory('ydlidar_ros2_driver'))

    params_file = LaunchConfiguration('params_file')
    output_topic = LaunchConfiguration('output_topic')

    upstream_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(str(upstream_share / 'launch' / 'ydlidar_launch.py')),
        launch_arguments={'params_file': params_file}.items(),
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'params_file',
            default_value=str(own_share / 'config' / 'ydlidar_humble.yaml'),
            description='YDLIDAR ROS 2 parameter file.',
        ),
        DeclareLaunchArgument(
            'output_topic',
            default_value='/scan',
            description='Remapped LaserScan output topic. Use /lidar/scan to reproduce the v1.3 topic change.',
        ),
        GroupAction([
            SetRemap(src='/scan', dst=output_topic),
            upstream_launch,
        ]),
    ])
