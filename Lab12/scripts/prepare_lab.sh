#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/common.sh"

source_ros
cd "$LAB_ROOT"

if [ ! -d .git ]; then
  git init -q
  git config user.name "Lab12 Student"
  git config user.email "lab12-student@example.local"

  # Initial known-good baseline: config already contains /dev/ttyUSB1.
  git add .
  git commit -q -m "baseline: known-good Lab12 runtime"
  git tag stable-2026-08

  # Create a historical regression commit.
  python3 - "$CONFIG" <<'PY'
from pathlib import Path
import sys
p = Path(sys.argv[1])
s = p.read_text()
s = s.replace('lidar_port: /dev/ttyUSB1', 'lidar_port: /dev/ttyUSB0', 1)
p.write_text(s)
PY
  git add "$CONFIG"
  git commit -q -m "regression: incorrect LiDAR port setting"

  # Student starts after repair, but before the repair is committed.
  python3 - "$CONFIG" <<'PY'
from pathlib import Path
import sys
p = Path(sys.argv[1])
s = p.read_text()
s = s.replace('lidar_port: /dev/ttyUSB0', 'lidar_port: /dev/ttyUSB1', 1)
p.write_text(s)
PY
else
  echo "[INFO] Existing Git repository detected; Git scenario initialization skipped."
fi

mkdir -p "$LAB_ROOT/evidence"
rm -f "$LAB_ROOT/evidence"/E*.txt "$LAB_ROOT/evidence/evidence_summary.md" 2>/dev/null || true

cd "$WS"
colcon build --symlink-install

echo
echo "[PASS] Lab12 student environment prepared."
echo "Known-good tag: stable-2026-08"
echo "Working tree intentionally contains the recovered lidar_port change."
echo "Next: bash scripts/start_lab.sh"
