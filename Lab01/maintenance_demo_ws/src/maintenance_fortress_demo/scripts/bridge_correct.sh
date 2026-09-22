#!/usr/bin/env bash
set -euo pipefail

set +u
source /opt/ros/humble/setup.bash
set -u

# 정상: Gazebo 실제 LiDAR 토픽 /lidar_scan을 ROS /scan으로 remap한다.
echo "[OK] Gazebo topic /lidar_scan -> ROS /scan"
exec ros2 run ros_gz_bridge parameter_bridge \
  '/lidar_scan@sensor_msgs/msg/LaserScan[ignition.msgs.LaserScan' \
  --ros-args -r /lidar_scan:=/scan
