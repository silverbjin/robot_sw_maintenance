#!/usr/bin/env bash
set -euo pipefail

set +u
source /opt/ros/humble/setup.bash
set -u

# 의도적 장애: Gazebo에는 /wrong_lidar_scan 이 없으므로 /scan에 데이터가 오지 않는다.
echo "[FAULT] Gazebo topic /wrong_lidar_scan -> ROS /scan"
exec ros2 run ros_gz_bridge parameter_bridge \
  '/wrong_lidar_scan@sensor_msgs/msg/LaserScan[ignition.msgs.LaserScan' \
  --ros-args -r /wrong_lidar_scan:=/scan
