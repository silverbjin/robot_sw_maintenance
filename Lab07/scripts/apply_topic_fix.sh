#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
ROOT=$(cd "$SCRIPT_DIR/.." && pwd)
cd "$ROOT"
ACTIVE="ros2_ws/src/maintenance_lidar_demo/config/lab_active.yaml"
[[ -f "$ACTIVE" ]] || { echo "ERROR: $ACTIVE missing; prepare/reset the lab first." >&2; exit 3; }
python3 - "$ACTIVE" <<'PY'
from pathlib import Path
import sys
path = Path(sys.argv[1])
text = path.read_text(encoding='utf-8')
needle = '    scan_topic: /scan\n'
replacement = '    scan_topic: /lidar/scan\n'
count = text.count(needle)
if count != 1:
    raise SystemExit(f'ERROR: expected exactly one subscriber /scan entry, found {count}; refusing ambiguous edit.')
path.write_text(text.replace(needle, replacement, 1), encoding='utf-8')
PY
INSTALLED="$ROOT/ros2_ws/install/maintenance_lidar_demo/share/maintenance_lidar_demo/config/lab_active.yaml"
if [[ -e "$INSTALLED" && "$(readlink -f "$ACTIVE")" != "$(readlink -f "$INSTALLED")" ]]; then cp "$ACTIVE" "$INSTALLED"; fi
echo "Applied v1.3 topic fix: navigation subscriber -> /lidar/scan"
