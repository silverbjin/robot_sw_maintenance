#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RESULTS_DIR="${RESULTS_DIR:-$ROOT/results/$(date +%Y%m%d_%H%M%S)}"
mkdir -p "$RESULTS_DIR"
OUT="$RESULTS_DIR/02_ros_baseline.txt"
{
  echo '=== ROS 2 BASELINE ==='
  echo "timestamp=$(date -Is)"
  echo "ROS_DISTRO=${ROS_DISTRO:-NOT_SET}"
  if command -v ros2 >/dev/null 2>&1; then
    echo "ros2_command=$(command -v ros2)"
    echo 'ros2_available=YES'
  else
    echo 'ros2_available=NO'
    echo 'hint=source /opt/ros/humble/setup.bash, then run this collector again'
  fi
  if [[ -d /opt/ros/humble ]]; then echo 'humble_install_dir=FOUND'; else echo 'humble_install_dir=NOT_FOUND'; fi
} > "$OUT"
cat "$OUT"
echo "Saved: $OUT" >&2
