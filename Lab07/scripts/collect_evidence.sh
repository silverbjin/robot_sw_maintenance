#!/usr/bin/env bash
set -u
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
ROOT=$(cd "$SCRIPT_DIR/.." && pwd)
LAB=${1:-}
case "$LAB" in
  LAB11|LAB12|LAB13|LAB14|LAB15) ;;
  *) echo "Usage: $0 {LAB11|LAB12|LAB13|LAB14|LAB15}" >&2; exit 2 ;;
esac
DEST="$ROOT/evidence/$LAB"
mkdir -p "$DEST"
STAMP=$(date '+%Y-%m-%dT%H:%M:%S%z')
printf 'LAB=%s\ncollected_at=%s\n' "$LAB" "$STAMP" > "$DEST/collection_meta.txt"

capture() {
  local name=$1; shift
  {
    echo "+ $*"
    "$@"
    rc=$?
    echo "exit_code=$rc"
  } > "$DEST/$name.txt" 2>&1
  return 0
}

case "$LAB" in
  LAB11)
    capture git_status git status --short --branch
    capture active_config cat "$ROOT/ros2_ws/src/maintenance_lidar_demo/config/lab_active.yaml"
    ;;
  LAB12)
    capture node_list ros2 node list
    capture topic_list ros2 topic list
    capture scan_info ros2 topic info /scan -v
    capture lidar_scan_once timeout 5s ros2 topic echo /lidar/scan --once
    ;;
  LAB13)
    capture git_log git log --oneline --decorate --graph -5
    capture git_diff git diff v1.2..v1.3
    ;;
  LAB14)
    capture git_status git status --short --branch
    capture active_config cat "$ROOT/ros2_ws/src/maintenance_lidar_demo/config/lab_active.yaml"
    ;;
  LAB15)
    capture node_list ros2 node list
    capture lidar_info ros2 topic info /lidar/scan -v
    capture lidar_scan_once timeout 5s ros2 topic echo /lidar/scan --once
    capture verify "$ROOT/scripts/verify_result.sh"
    ;;
esac

echo "Evidence collected: $DEST"
