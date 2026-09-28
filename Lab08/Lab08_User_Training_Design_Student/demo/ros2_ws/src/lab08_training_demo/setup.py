from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'lab08_training_demo'
setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Instructor',
    maintainer_email='instructor@example.com',
    description='Lab08 instructor-provided training demo.',
    license='Apache-2.0',
    entry_points={'console_scripts': ['training_component = lab08_training_demo.component_node:main']},
)
