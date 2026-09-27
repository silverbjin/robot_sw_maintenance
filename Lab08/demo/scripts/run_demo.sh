#!/usr/bin/env bash
set -euo pipefail
SCENARIO="${1:-normal}"
case "$SCENARIO" in normal|missing_sensor) ;; *) echo "usage: $0 normal|missing_sensor" >&2; exit 2;; esac
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WS="$(cd "$SCRIPT_DIR/../ros2_ws" && pwd)"
source /opt/ros/humble/setup.bash
if [[ ! -f "$WS/install/setup.bash" ]]; then echo "[ERROR] Demo not built. Run: $SCRIPT_DIR/build_demo.sh" >&2; exit 3; fi
source "$WS/install/setup.bash"
echo "[INFO] scenario=$SCENARIO"
echo "[INFO] Keep this terminal open. Students inspect from another terminal."
exec ros2 launch lab08_training_demo training_demo.launch.py scenario:="$SCENARIO"
