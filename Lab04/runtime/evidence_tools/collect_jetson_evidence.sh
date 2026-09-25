#!/usr/bin/env bash
set -u

BASE_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
OUT_DIR="${EVIDENCE_DIR:-$BASE_DIR/evidence/logs}"
mkdir -p "$OUT_DIR"
TS="$(date +%Y%m%d_%H%M%S)"
OUT="$OUT_DIR/E01_E02_jetson_${TS}.txt"

# Best effort: source expected Galactic environments when present.
if [[ -f /opt/ros/galactic/setup.bash ]]; then
  # shellcheck disable=SC1091
  source /opt/ros/galactic/setup.bash
fi
if [[ -f "$HOME/myagv_ros2/install/local_setup.bash" ]]; then
  # shellcheck disable=SC1090
  source "$HOME/myagv_ros2/install/local_setup.bash"
fi

{
  echo "# Ch04 Jetson Evidence"
  echo "timestamp=$(date --iso-8601=seconds 2>/dev/null || date)"
  echo "hostname=$(hostname)"
  echo "ROS_DISTRO=${ROS_DISTRO:-unset}"
  echo

  echo "## Device"
  ls -l /dev/ttyS0 2>&1 || true
  ls -l /dev/ttyUSB* 2>&1 || true
  ls -l /dev/ydlidar 2>&1 || true
  echo

  echo "## Nodes"
  timeout 5 ros2 node list 2>&1 || true
  echo

  echo "## Topics"
  timeout 5 ros2 topic list 2>&1 || true
  echo

  echo "## /scan info"
  timeout 5 ros2 topic info /scan 2>&1 || true
  echo

  echo "## /scan hz sample"
  timeout 6 ros2 topic hz /scan 2>&1 || true
  echo

  echo "## /odom once"
  timeout 4 ros2 topic echo --once /odom 2>&1 || true
  echo

  echo "## /imu once"
  timeout 4 ros2 topic echo --once /imu 2>&1 || true
  echo

  echo "## /voltage once"
  timeout 4 ros2 topic echo --once /voltage 2>&1 || true
  echo

  echo "## Gateway process"
  pgrep -af jetson_gateway.py 2>&1 || true
  echo

  echo "## Listening ports"
  ss -lntp 2>&1 | grep -E '(:5000|jetson_gateway)' || true
} > "$OUT"

echo "Saved: $OUT"
