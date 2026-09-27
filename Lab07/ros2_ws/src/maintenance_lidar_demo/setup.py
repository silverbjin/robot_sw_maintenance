from glob import glob
from setuptools import find_packages, setup

package_name = 'maintenance_lidar_demo'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
        ('share/' + package_name + '/config', glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Course Instructor',
    maintainer_email='instructor@example.com',
    description='Deterministic ROS 2 LiDAR upgrade verification training package.',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'mock_lidar_publisher = maintenance_lidar_demo.mock_lidar_publisher:main',
            'navigation_scan_monitor = maintenance_lidar_demo.navigation_scan_monitor:main',
        ],
    },
)
