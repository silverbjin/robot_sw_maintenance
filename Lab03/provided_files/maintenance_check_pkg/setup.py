from setuptools import find_packages, setup

package_name = 'maintenance_check_pkg'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Instructor',
    maintainer_email='instructor@example.com',
    description='Minimal ROS 2 package for installation and overlay verification lab.',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'status_node = maintenance_check_pkg.status_node:main',
        ],
    },
)
