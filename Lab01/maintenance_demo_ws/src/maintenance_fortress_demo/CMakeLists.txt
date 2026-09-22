cmake_minimum_required(VERSION 3.8)
project(maintenance_fortress_demo)
find_package(ament_cmake REQUIRED)

install(DIRECTORY launch worlds urdf rviz config records
  DESTINATION share/${PROJECT_NAME})

install(PROGRAMS
  scripts/bridge_wrong.sh
  scripts/bridge_correct.sh
  scripts/check_gazebo.sh
  scripts/check_ros.sh
  scripts/system_check.sh
  DESTINATION lib/${PROJECT_NAME})

ament_package()
