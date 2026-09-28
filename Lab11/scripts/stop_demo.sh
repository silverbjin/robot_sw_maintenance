#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/common.sh"
stop_pid_file "$LIDAR_PID_FILE"
stop_pid_file "$MONITOR_PID_FILE"
echo "[OK] Lab11 demo stopped."
