from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

BASE_NODES = ['controller_manager', 'motor_driver', 'sensor_node', 'state_publisher', 'tf_publisher']

def configure(context):
    scenario = LaunchConfiguration('scenario').perform(context)
    if scenario not in ('normal', 'missing_sensor'):
        raise RuntimeError(f'unsupported scenario: {scenario}')
    nodes = [n for n in BASE_NODES if not (scenario == 'missing_sensor' and n == 'sensor_node')]
    return [
        Node(
            package='lab08_training_demo',
            executable='training_component',
            name=n,
            output='screen',
        ) for n in nodes
    ]

def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('scenario', default_value='normal', description='normal or missing_sensor'),
        OpaqueFunction(function=configure),
    ])
