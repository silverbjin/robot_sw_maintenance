#!/usr/bin/env bash
set -euo pipefail
if [ ! -f /opt/ros/humble/setup.bash ]; then
  echo "FAIL: /opt/ros/humble/setup.bash not found"
  exit 1
fi
source /opt/ros/humble/setup.bash
echo "ROS_DISTRO=${ROS_DISTRO:-<not set>}"
ros2 --help >/dev/null
echo "PASS: ros2 CLI"
if [ -f "$HOME/robot_ws/install/setup.bash" ]; then
  source "$HOME/robot_ws/install/setup.bash"
  if ros2 pkg prefix maintenance_check_pkg >/dev/null 2>&1; then
    echo "PASS: maintenance_check_pkg visible"
    echo "Prefix: $(ros2 pkg prefix maintenance_check_pkg)"
  else
    echo "INFO: maintenance_check_pkg not visible"
  fi
else
  echo "INFO: ~/robot_ws/install/setup.bash not found"
fi
