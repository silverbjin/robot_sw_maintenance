#!/usr/bin/env bash
set -u

STAGE="${1:-}"
REPO="${2:-$HOME/robot_sw_maintenance}"
OUT_ROOT="${3:-$HOME/Lab06_evidence}"

if [[ ! "$STAGE" =~ ^(baseline|upgrade|rollback)$ ]]; then
  echo "Usage: $0 <baseline|upgrade|rollback> [repo_root] [output_root]"
  exit 2
fi

if [[ ! -d "$REPO/.git" ]]; then
  echo "ERROR: Git repository not found: $REPO"
  exit 1
fi

WS="$REPO/Lab06/ros2_ws"
if [[ ! -d "$WS/src" ]]; then
  echo "ERROR: Lab06 workspace not found: $WS"
  exit 1
fi

STAMP="$(date +%Y%m%d_%H%M%S)"
OUT="$OUT_ROOT/${STAMP}_${STAGE}"
mkdir -p "$OUT"

branch="$(git -C "$REPO" branch --show-current 2>/dev/null || true)"
commit="$(git -C "$REPO" rev-parse HEAD 2>/dev/null || true)"
head_tag="$(git -C "$REPO" describe --tags --exact-match HEAD 2>/dev/null || true)"
status_short="$(git -C "$REPO" status --porcelain 2>/dev/null || true)"

{
  echo "stage=$STAGE"
  echo "timestamp=$(date --iso-8601=seconds)"
  echo "repo=$REPO"
  echo "branch=${branch:-DETACHED}"
  echo "commit=$commit"
  echo "head_tag=${head_tag:-NONE}"
  echo "working_tree_clean=$([[ -z "$status_short" ]] && echo true || echo false)"
} > "$OUT/git_facts.txt"

git -C "$REPO" status > "$OUT/git_status.txt" 2>&1 || true
git -C "$REPO" log --oneline --decorate -8 > "$OUT/git_log.txt" 2>&1 || true
git -C "$REPO" log --graph --oneline --decorate --all -12 > "$OUT/git_graph.txt" 2>&1 || true
git -C "$REPO" tag > "$OUT/git_tags.txt" 2>&1 || true

find "$WS/src" -mindepth 1 -maxdepth 1 -type d -printf '%f\n' | sort > "$OUT/source_packages.txt"

python3 - "$WS" "$OUT/package_versions.json" <<'PY'
from pathlib import Path
import json, sys, xml.etree.ElementTree as ET
ws = Path(sys.argv[1])
out = Path(sys.argv[2])
data = {}
for p in sorted((ws/"src").glob("*/package.xml")):
    root = ET.parse(p).getroot()
    data[root.findtext("name")] = root.findtext("version")
out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
PY

{
  echo "uname:"
  uname -a
  echo
  echo "lsb_release:"
  lsb_release -a 2>&1 || true
  echo
  echo "ROS_DISTRO(env before sourcing): ${ROS_DISTRO:-UNSET}"
} > "$OUT/system.txt"

ros_available=false
install_available=false
installed_myagv_monitor=false

if [[ -f /opt/ros/humble/setup.bash ]]; then
  # shellcheck disable=SC1091
  source /opt/ros/humble/setup.bash
  ros_available=true
fi

if [[ -f "$WS/install/setup.bash" ]]; then
  # shellcheck disable=SC1090
  source "$WS/install/setup.bash"
  install_available=true
fi

if command -v ros2 >/dev/null 2>&1; then
  ros2 pkg list | grep '^myagv_' | sort > "$OUT/installed_myagv_packages.txt" 2>&1 || true
  if ros2 pkg prefix myagv_monitor >/dev/null 2>&1; then
    installed_myagv_monitor=true
  fi

  ros2 node list > "$OUT/ros2_nodes.txt" 2>&1 || true
  ros2 topic list > "$OUT/ros2_topics.txt" 2>&1 || true
  timeout 4s ros2 topic echo /myagv/status --once > "$OUT/myagv_status_once.txt" 2>&1 || true
else
  echo "ros2 command unavailable" > "$OUT/installed_myagv_packages.txt"
  echo "ros2 command unavailable" > "$OUT/ros2_nodes.txt"
  echo "ros2 command unavailable" > "$OUT/ros2_topics.txt"
  echo "ros2 command unavailable" > "$OUT/myagv_status_once.txt"
fi

monitor_source=false
[[ -d "$WS/src/myagv_monitor" ]] && monitor_source=true

cat > "$OUT/facts.json" <<EOF
{
  "stage": "$STAGE",
  "branch": "${branch:-}",
  "commit": "$commit",
  "head_tag": "${head_tag:-}",
  "working_tree_clean": $([[ -z "$status_short" ]] && echo true || echo false),
  "monitor_source_present": $monitor_source,
  "ros_available": $ros_available,
  "install_available": $install_available,
  "installed_myagv_monitor": $installed_myagv_monitor
}
EOF

(
  cd "$OUT"
  sha256sum *.txt *.json 2>/dev/null | grep -v 'SHA256SUMS.txt' > SHA256SUMS.txt || true
)

echo "Evidence saved: $OUT"
