#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC_PKG="$ROOT_DIR/provided_files/maintenance_check_pkg"
WS="$HOME/robot_ws"
mkdir -p "$WS/src"
if [ -d "$WS/src/maintenance_check_pkg" ]; then
  echo "maintenance_check_pkg already exists: $WS/src/maintenance_check_pkg"
  echo "No overwrite performed."
  exit 0
fi
cp -r "$SRC_PKG" "$WS/src/"
echo "Copied maintenance_check_pkg to $WS/src/"
echo "Next:"
echo "  source /opt/ros/humble/setup.bash"
echo "  cd ~/robot_ws"
echo "  colcon list"
echo "  colcon build --packages-select maintenance_check_pkg"
