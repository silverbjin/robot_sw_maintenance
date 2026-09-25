#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG="${DESKTOP_GATEWAY_CONFIG:-$ROOT/config/desktop.env}"
# shellcheck disable=SC1091
source /opt/ros/humble/setup.bash
[[ -f "$CONFIG" ]] || { echo "ERROR: missing $CONFIG. Run install_desktop.sh first." >&2; exit 1; }
cd "$ROOT"
exec python3 "$ROOT/desktop/desktop_gateway.py" --config "$CONFIG"
