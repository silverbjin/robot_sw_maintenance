#!/usr/bin/env bash
set -u
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG="${DESKTOP_GATEWAY_CONFIG:-$ROOT/config/desktop.env}"
mkdir -p "$ROOT/logs"
OUT="$ROOT/logs/desktop_$(date +%Y%m%d_%H%M%S).txt"
# shellcheck disable=SC1091
source /opt/ros/humble/setup.bash
[[ -f "$CONFIG" ]] && source "$CONFIG"
{
  echo "# myAGV TCP Gateway - Desktop evidence"
  date -Is
  echo "ROS_DISTRO=${ROS_DISTRO:-unset}"
  echo "ROBOT_IP=${ROBOT_IP:-unset}"
  echo "GATEWAY_PORT=${GATEWAY_PORT:-unset}"
  echo; echo "## IP"; ip addr 2>&1 || true
  echo; echo "## Ping"; ping -c 4 "${ROBOT_IP:-127.0.0.1}" 2>&1 || true
  echo; echo "## Processes"; pgrep -af '[d]esktop_gateway.py' || true
  echo; echo "## Nodes"; ros2 node list 2>&1 || true
  echo; echo "## Gateway topics"; ros2 topic list 2>&1 | grep '^/gateway/' || true
  echo; echo "## Connected"; timeout 3 ros2 topic echo --once /gateway/connected 2>&1 || true
  echo; echo "## Status"; timeout 3 ros2 topic echo --once /gateway/status 2>&1 || true
  echo; echo "## Scan health"; timeout 3 ros2 topic echo --once /gateway/scan_health 2>&1 || true
} > "$OUT"
echo "Saved: $OUT"
