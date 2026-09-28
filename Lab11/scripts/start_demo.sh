#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/common.sh"
source_ros

if [[ ! -f "$WS_DIR/install/setup.bash" ]]; then
  echo "[ERROR] 먼저 scripts/build_demo.sh 를 실행하세요." >&2
  exit 1
fi

if ! pid_running "$LIDAR_PID_FILE"; then
  nohup ros2 run maintenance_lidar_demo lidar_node --ros-args -p publish_rate_hz:=10.0 \
    >"$LOG_DIR/lidar_node.log" 2>&1 &
  echo $! > "$LIDAR_PID_FILE"
fi

if ! pid_running "$MONITOR_PID_FILE"; then
  nohup ros2 run maintenance_lidar_demo monitor_node \
    >"$LOG_DIR/monitor_node.log" 2>&1 &
  echo $! > "$MONITOR_PID_FILE"
fi

sleep 2

echo "[OK] Lab11 demo started."
echo "     lidar_node PID : $(cat "$LIDAR_PID_FILE")"
echo "     monitor PID    : $(cat "$MONITOR_PID_FILE")"
echo "     expected /scan : ≈ 10 Hz"
echo
echo "검증: timeout 5 ros2 topic hz /scan"
