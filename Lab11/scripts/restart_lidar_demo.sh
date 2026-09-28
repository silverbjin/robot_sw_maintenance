#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/common.sh"
source_ros

if [[ ! -f "$WS_DIR/install/setup.bash" ]]; then
  echo "[ERROR] 먼저 scripts/build_demo.sh 를 실행하세요." >&2
  exit 1
fi

# 최소 범위 복구: monitor는 유지하고 lidar_node만 재시작한다.
stop_pid_file "$LIDAR_PID_FILE"
nohup ros2 run maintenance_lidar_demo lidar_node --ros-args -p publish_rate_hz:=10.0 \
  >"$LOG_DIR/lidar_node.log" 2>&1 &
echo $! > "$LIDAR_PID_FILE"
sleep 2

echo "[OK] lidar_node only restarted at default 10 Hz."
echo "[NEXT] 동일한 기준으로 재검증: timeout 5 ros2 topic hz /scan"
