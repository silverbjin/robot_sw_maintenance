#!/usr/bin/env bash
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MYAGV_WS="${MYAGV_WS:-$HOME/myagv_ros2}"
mkdir -p "$ROOT/logs"
OUT="$ROOT/logs/jetson_$(date +%Y%m%d_%H%M%S).txt"
# shellcheck disable=SC1091
source /opt/ros/galactic/setup.bash
if [[ -f "$MYAGV_WS/install/local_setup.bash" ]]; then source "$MYAGV_WS/install/local_setup.bash"; fi
{
  echo "# myAGV TCP Gateway - Jetson evidence"
  date -Is
  echo "ROS_DISTRO=${ROS_DISTRO:-unset}"
  echo; echo "## Devices"; ls -l /dev/ttyS0 /dev/ttyUSB* 2>&1 || true
  echo; echo "## Processes"; pgrep -af '[j]etson_gateway.py' || true
  echo; echo "## Nodes"; ros2 node list 2>&1 || true
  echo; echo "## Topics"; ros2 topic list 2>&1 || true
  echo; echo "## /scan rate (5s)"; timeout 5 ros2 topic hz /scan 2>&1 || true
  echo; echo "## /odom sample"; timeout 3 ros2 topic echo --once /odom 2>&1 || true
  echo; echo "## /imu sample"; timeout 3 ros2 topic echo --once /imu 2>&1 || true
  echo; echo "## Listening sockets"; ss -lntp 2>&1 || true
} > "$OUT"
echo "Saved: $OUT"
