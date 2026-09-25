from setuptools import setup
from glob import glob
import os

package_name = 'myagv_bringup'

setup(
    name=package_name,
    version='1.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Course Instructor',
    maintainer_email='instructor@example.invalid',
    description='Safe baseline state publisher for Session 5 upgrade-preparation training.',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'status_publisher = myagv_bringup.status_publisher:main',
        ],
    },
)
