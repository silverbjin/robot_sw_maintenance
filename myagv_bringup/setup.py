import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'myagv_bringup'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Training Maintainer',
    maintainer_email='training@example.com',
    description='Educational myAGV bringup package for ROS 2 Humble',
    license='Apache-2.0',
)
