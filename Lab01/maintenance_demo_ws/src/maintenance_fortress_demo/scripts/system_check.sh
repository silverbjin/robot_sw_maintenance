#!/usr/bin/env bash
set +u
source /opt/ros/humble/setup.bash
set -u

FAIL=0
pass(){ echo "[PASS] $*"; }
fail(){ echo "[FAIL] $*"; FAIL=1; }

echo '============================================='
echo ' ROS 2 Humble + Gazebo Fortress System Check'
echo '============================================='
[ "${ROS_DISTRO:-}" = humble ] && pass 'ROS_DISTRO=humble' || fail 'ROS_DISTRO is not humble'
pgrep -f 'ign gazebo' >/dev/null && pass 'Gazebo Fortress process running' || fail 'Gazebo process not found'
ign topic -l 2>/dev/null | grep -q '^/lidar_scan$' && pass 'Gazebo /lidar_scan exists' || fail 'Gazebo /lidar_scan missing'
ros2 topic list 2>/dev/null | grep -q '^/scan$' && pass 'ROS /scan exists' || fail 'ROS /scan missing'
if timeout 4 ros2 topic echo /scan --once >/dev/null 2>&1; then pass 'LaserScan message received'; else fail 'LaserScan message not received'; fi
if timeout 4 ros2 topic hz /scan 2>/dev/null | grep -q 'average rate'; then pass 'LaserScan is publishing repeatedly'; else fail 'LaserScan rate not confirmed'; fi
exit "$FAIL"
