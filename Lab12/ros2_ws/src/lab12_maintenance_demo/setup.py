from setuptools import find_packages, setup

package_name = 'lab12_maintenance_demo'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/lab12_demo.launch.py']),
        ('share/' + package_name + '/config', ['config/config.yaml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Lab12 Instructor',
    maintainer_email='lab@example.com',
    description='Mock LiDAR maintenance reporting demo',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'lidar_publisher = lab12_maintenance_demo.lidar_publisher:main',
            'monitor = lab12_maintenance_demo.monitor:main',
        ],
    },
)
