from setuptools import find_packages, setup

package_name = 'myagv_monitor'

setup(
    name=package_name,
    version='2.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Training Maintainer',
    maintainer_email='training@example.com',
    description='Monitoring module introduced in Lab06 release-v2',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'monitor_node = myagv_monitor.monitor_node:main',
        ],
    },
)
