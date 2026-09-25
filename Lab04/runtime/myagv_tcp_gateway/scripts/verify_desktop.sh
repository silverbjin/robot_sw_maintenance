#!/usr/bin/env bash
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG="${DESKTOP_GATEWAY_CONFIG:-$ROOT/config/desktop.env}"
FAIL=0

# shellcheck disable=SC1091
source /opt/ros/humble/setup.bash
if [[ -f "$CONFIG" ]]; then
  # shellcheck disable=SC1090
  source "$CONFIG"
else
  echo "[FAIL] missing config: $CONFIG"; exit 1
fi

echo "=== Desktop / Humble verification ==="
[[ "${ROS_DISTRO:-}" == "humble" ]] && echo "[OK] ROS_DISTRO=humble" || { echo "[FAIL] ROS_DISTRO=${ROS_DISTRO:-unset}"; FAIL=1; }

if ping -c 2 -W 2 "$ROBOT_IP" >/dev/null 2>&1; then echo "[OK] ping $ROBOT_IP"; else echo "[FAIL] ping $ROBOT_IP"; FAIL=1; fi

if pgrep -af 'desktop_gateway.py' >/dev/null; then
  echo "[OK] desktop_gateway.py process"
else
  echo "[FAIL] desktop_gateway.py process missing"; FAIL=1
  if command -v nc >/dev/null 2>&1; then
    nc -z -w 2 "$ROBOT_IP" "${GATEWAY_PORT:-5000}" >/dev/null 2>&1 && echo "[OK] raw TCP port reachable" || echo "[WARN] raw TCP port not reachable"
  fi
fi

NODES="$(ros2 node list 2>/dev/null || true)"
if grep -q '/myagv_tcp_gateway_desktop' <<<"$NODES"; then echo "[OK] Desktop gateway ROS node"; else echo "[FAIL] Desktop gateway ROS node not found"; FAIL=1; fi

TOPICS="$(ros2 topic list 2>/dev/null || true)"
for topic in /gateway/cmd_vel /gateway/connected /gateway/status /gateway/odom /gateway/imu /gateway/scan_health; do
  if grep -qx "$topic" <<<"$TOPICS"; then echo "[OK] topic $topic"; else echo "[FAIL] topic $topic missing"; FAIL=1; fi
done

echo "--- one connection-status sample ---"
timeout 3 ros2 topic echo --once /gateway/connected 2>/dev/null || echo "[WARN] no /gateway/connected sample within 3 s"
echo "--- one gateway-status sample ---"
timeout 3 ros2 topic echo --once /gateway/status 2>/dev/null || echo "[WARN] no /gateway/status sample within 3 s"

exit "$FAIL"
