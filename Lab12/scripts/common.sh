#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
WS="$LAB_ROOT/ros2_ws"
CONFIG="$WS/src/lab12_maintenance_demo/config/config.yaml"

source_ros() {
  if [ -f /opt/ros/humble/setup.bash ]; then
    # shellcheck disable=SC1091
    source /opt/ros/humble/setup.bash
  else
    echo "[ERROR] /opt/ros/humble/setup.bash not found. ROS 2 Humble is required." >&2
    return 1
  fi
  if [ -f "$WS/install/setup.bash" ]; then
    # shellcheck disable=SC1091
    source "$WS/install/setup.bash"
  fi
}
