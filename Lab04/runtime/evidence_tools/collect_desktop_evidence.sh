#!/usr/bin/env bash
set -u

BASE_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
OUT_DIR="${EVIDENCE_DIR:-$BASE_DIR/evidence/logs}"
mkdir -p "$OUT_DIR"
TS="$(date +%Y%m%d_%H%M%S)"
OUT="$OUT_DIR/E03_E04_desktop_${TS}.txt"

if [[ -f /opt/ros/humble/setup.bash ]]; then
  # shellcheck disable=SC1091
  source /opt/ros/humble/setup.bash
fi

{
  echo "# Ch04 Desktop Evidence"
  echo "timestamp=$(date --iso-8601=seconds 2>/dev/null || date)"
  echo "hostname=$(hostname)"
  echo "ROS_DISTRO=${ROS_DISTRO:-unset}"
  echo

  echo "## IP"
  ip -brief addr 2>&1 || ip addr 2>&1 || true
  echo

  echo "## Gateway process"
  pgrep -af desktop_gateway.py 2>&1 || true
  echo

  echo "## /gateway/connected once"
  timeout 4 ros2 topic echo --once /gateway/connected 2>&1 || true
  echo

  echo "## /gateway/status once"
  timeout 4 ros2 topic echo --once /gateway/status 2>&1 || true
  echo

  echo "## /gateway/odom once"
  timeout 4 ros2 topic echo --once /gateway/odom 2>&1 || true
  echo

  echo "## /gateway/imu once"
  timeout 4 ros2 topic echo --once /gateway/imu 2>&1 || true
  echo

  echo "## /gateway/voltage once"
  timeout 4 ros2 topic echo --once /gateway/voltage 2>&1 || true
  echo

  echo "## /gateway/scan_health once"
  timeout 4 ros2 topic echo --once /gateway/scan_health 2>&1 || true
} > "$OUT"

echo "Saved: $OUT"
