from setuptools import find_packages, setup

package_name = 'myagv_control'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Training Maintainer',
    maintainer_email='training@example.com',
    description='Safe educational myAGV status publisher',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'control_node = myagv_control.control_node:main',
        ],
    },
)
