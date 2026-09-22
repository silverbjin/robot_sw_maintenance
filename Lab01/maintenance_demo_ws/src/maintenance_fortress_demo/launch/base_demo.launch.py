from pathlib import Path
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node


gui_config = str(
    Path.home() / '.ignition/gazebo/6/gui.config'
)

def generate_launch_description():
    share = Path(get_package_share_directory('maintenance_fortress_demo'))
    world = share / 'worlds' / 'lidar_demo.sdf'
    urdf = (share / 'urdf' / 'maintenance_robot.urdf').read_text()
    rviz = share / 'rviz' / 'lidar_demo.rviz'

    return LaunchDescription([
        ExecuteProcess(cmd=['ign', 'gazebo', '-r', str(world), '--gui-config', gui_config], output='screen'),
        #ExecuteProcess(cmd=['ign', 'gazebo', '-r', str(world), '--gui-config', '/home/jinho/.ignition/gazebo/6/gui.config'], output='screen'),
        Node(package='robot_state_publisher', executable='robot_state_publisher',
             parameters=[{'robot_description': urdf}], output='screen'),
        Node(package='rviz2', executable='rviz2', arguments=['-d', str(rviz)], output='screen'),
    ])
