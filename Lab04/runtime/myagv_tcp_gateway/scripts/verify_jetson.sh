#!/usr/bin/env bash
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG="${JETSON_GATEWAY_CONFIG:-$ROOT/config/jetson.env}"
MYAGV_WS="${MYAGV_WS:-$HOME/myagv_ros2}"
FAIL=0

# shellcheck disable=SC1091
source /opt/ros/galactic/setup.bash
if [[ -f "$MYAGV_WS/install/local_setup.bash" ]]; then
  # shellcheck disable=SC1090
  source "$MYAGV_WS/install/local_setup.bash"
fi
if [[ -f "$CONFIG" ]]; then
  # shellcheck disable=SC1090
  source "$CONFIG"
else
  echo "[FAIL] missing config: $CONFIG"; FAIL=1
fi

echo "=== Jetson / Galactic verification ==="
[[ "${ROS_DISTRO:-}" == "galactic" ]] && echo "[OK] ROS_DISTRO=galactic" || { echo "[FAIL] ROS_DISTRO=${ROS_DISTRO:-unset}"; FAIL=1; }

if [[ -e /dev/ttyS0 ]]; then echo "[OK] /dev/ttyS0"; else echo "[WARN] /dev/ttyS0 not found"; fi
if compgen -G '/dev/ttyUSB*' >/dev/null; then echo "[OK] LiDAR candidate: $(ls /dev/ttyUSB* 2>/dev/null | tr '\n' ' ')"; else echo "[WARN] /dev/ttyUSB* not found"; fi

NODES="$(ros2 node list 2>/dev/null || true)"
if grep -q '/myagv_tcp_gateway_jetson' <<<"$NODES"; then echo "[OK] Jetson gateway ROS node"; else echo "[FAIL] Jetson gateway ROS node not found"; FAIL=1; fi

TOPICS="$(ros2 topic list 2>/dev/null || true)"
for topic in /cmd_vel /odom /imu /scan; do
  if grep -qx "$topic" <<<"$TOPICS"; then echo "[OK] topic $topic"; else echo "[FAIL] topic $topic missing"; FAIL=1; fi
done
for topic in /voltage /voltage_backup; do
  if grep -qx "$topic" <<<"$TOPICS"; then echo "[OK] optional topic $topic"; else echo "[WARN] optional topic $topic not found"; fi
done

PORT="${GATEWAY_PORT:-5000}"
if ss -lnt 2>/dev/null | grep -qE ":${PORT}[[:space:]]"; then echo "[OK] TCP port $PORT listening"; else echo "[FAIL] TCP port $PORT not listening"; FAIL=1; fi

if pgrep -af 'jetson_gateway.py' >/dev/null; then echo "[OK] jetson_gateway.py process"; else echo "[FAIL] jetson_gateway.py process missing"; FAIL=1; fi

exit "$FAIL"
