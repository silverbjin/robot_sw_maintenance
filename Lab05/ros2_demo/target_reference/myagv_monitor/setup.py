from setuptools import setup
package_name='myagv_monitor'
setup(name=package_name, version='1.1.0', packages=[package_name],
      data_files=[('share/ament_index/resource_index/packages',['resource/'+package_name]),('share/'+package_name,['package.xml'])],
      install_requires=['setuptools'], zip_safe=True,
      maintainer='Course Instructor', maintainer_email='instructor@example.invalid',
      description='Instructor-only Session 6 target reference.', license='Apache-2.0',
      entry_points={'console_scripts':['monitor = myagv_monitor.monitor:main']})
