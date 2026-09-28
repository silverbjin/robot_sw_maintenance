#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WS_DIR="$ROOT_DIR/demo/ros2_ws"
RUNTIME_DIR="$ROOT_DIR/.runtime"
LOG_DIR="$RUNTIME_DIR/logs"
LIDAR_PID_FILE="$RUNTIME_DIR/lidar_node.pid"
MONITOR_PID_FILE="$RUNTIME_DIR/monitor_node.pid"

mkdir -p "$RUNTIME_DIR" "$LOG_DIR"

source_ros() {
  if [[ -f /opt/ros/humble/setup.bash ]]; then
    # shellcheck disable=SC1091
    source /opt/ros/humble/setup.bash
  else
    echo "[ERROR] /opt/ros/humble/setup.bash 를 찾을 수 없습니다." >&2
    return 1
  fi
  if [[ -f "$WS_DIR/install/setup.bash" ]]; then
    # shellcheck disable=SC1090
    source "$WS_DIR/install/setup.bash"
  fi
}

pid_running() {
  local pid_file="$1"
  [[ -f "$pid_file" ]] || return 1
  local pid
  pid="$(cat "$pid_file")"
  kill -0 "$pid" 2>/dev/null
}

stop_pid_file() {
  local pid_file="$1"
  if pid_running "$pid_file"; then
    local pid
    pid="$(cat "$pid_file")"
    kill "$pid" 2>/dev/null || true
    for _ in {1..20}; do
      kill -0 "$pid" 2>/dev/null || break
      sleep 0.1
    done
    kill -9 "$pid" 2>/dev/null || true
  fi
  rm -f "$pid_file"
}
