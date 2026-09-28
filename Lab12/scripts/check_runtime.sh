#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/common.sh"
source_ros

echo "=== ROS 2 distribution ==="
printenv ROS_DISTRO || true

echo
echo "=== Required nodes ==="
ros2 node list | grep -E '^/lab12_(lidar_publisher|monitor)$' || true

echo
echo "=== Required topics ==="
ros2 topic list | grep -E '^/(lidar_scan|lab12/function_status)$' || true

echo
echo "=== Function status ==="
timeout 5s ros2 topic echo /lab12/function_status --once || true

echo
echo "=== Git working tree ==="
cd "$LAB_ROOT"
git status --short || true
