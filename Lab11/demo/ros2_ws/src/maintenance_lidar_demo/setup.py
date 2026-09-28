from setuptools import find_packages, setup

package_name = 'maintenance_lidar_demo'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/lab11_demo.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Lab Instructor',
    maintainer_email='instructor@example.invalid',
    description='Deterministic LaserScan maintenance demo for Lab11.',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'lidar_node = maintenance_lidar_demo.lidar_node:main',
            'monitor_node = maintenance_lidar_demo.monitor_node:main',
        ],
    },
)
