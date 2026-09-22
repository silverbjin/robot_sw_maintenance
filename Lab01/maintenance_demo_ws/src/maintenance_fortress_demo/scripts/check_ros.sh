#!/usr/bin/env bash
set +u
source /opt/ros/humble/setup.bash
set -u

echo "=== ROS 2 /scan ==="
ros2 topic list | grep -E '^/scan$' || echo '[INFO] /scan topic not listed on this bridge build'
if timeout 4 ros2 topic echo /scan --once >/tmp/scan_once.txt 2>/dev/null; then
  echo '[PASS] LaserScan message received'
  sed -n '1,18p' /tmp/scan_once.txt
else
  echo '[FAIL] No LaserScan message received within 4 sec'
  exit 1
fi
