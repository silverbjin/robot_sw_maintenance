#!/usr/bin/env bash
set -euo pipefail
echo "=== Gazebo Transport LiDAR ==="
ign topic -l | grep -E '^/lidar_scan$' || { echo '[FAIL] /lidar_scan not found'; exit 1; }
echo '[PASS] /lidar_scan exists'
echo 'Message sample (2 sec):'
timeout 2 ign topic -e -t /lidar_scan || true
