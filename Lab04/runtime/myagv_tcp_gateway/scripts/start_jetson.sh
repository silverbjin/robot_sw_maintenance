#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG="${JETSON_GATEWAY_CONFIG:-$ROOT/config/jetson.env}"
MYAGV_WS="${MYAGV_WS:-$HOME/myagv_ros2}"

# shellcheck disable=SC1091
source /opt/ros/galactic/setup.bash
if [[ -f "$MYAGV_WS/install/local_setup.bash" ]]; then
  # shellcheck disable=SC1090
  source "$MYAGV_WS/install/local_setup.bash"
fi
[[ -f "$CONFIG" ]] || { echo "ERROR: missing $CONFIG. Run install_jetson.sh first." >&2; exit 1; }
cd "$ROOT"
exec python3 "$ROOT/jetson/jetson_gateway.py" --config "$CONFIG"
