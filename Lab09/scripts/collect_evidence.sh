#!/usr/bin/env bash
set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"
load_lab09_config || exit $?
source_ros_environment || exit $?
require_command ros2 || exit $?
require_command timeout || exit $?

label="${1:-session}"
label="$(printf '%s' "$label" | tr -cs 'A-Za-z0-9._-' '_')"
timestamp="$(date '+%Y%m%d-%H%M%S')"
session_dir="$EVIDENCE_DIR/${timestamp}_${label}"
mkdir -p "$session_dir"

{
  printf 'captured_at=%s\n' "$(date --iso-8601=seconds)"
  printf 'hostname=%s\n' "$(hostname)"
  printf 'uname=%s\n' "$(uname -a)"
  printf 'ROS_DISTRO=%s\n' "${ROS_DISTRO:-unknown}"
  printf 'LAB09_MODE=%s\n' "$LAB09_MODE"
  printf 'SCAN_TOPIC=%s\n' "$SCAN_TOPIC"
  printf 'LIDAR_NODE_EXACT=%s\n' "$LIDAR_NODE_EXACT"
} > "$session_dir/system_info.txt"

ros2 node list > "$session_dir/node_list.txt" 2>&1 || true
ros2 topic list > "$session_dir/topic_list.txt" 2>&1 || true
ros2 topic info "$SCAN_TOPIC" --verbose > "$session_dir/topic_info.txt" 2>&1 || true
timeout "${DATA_OBSERVE_SEC}s" ros2 topic hz "$SCAN_TOPIC" > "$session_dir/scan_hz.txt" 2>&1 || true

"$SCRIPT_DIR/check_lidar_state.sh" > "$session_dir/lidar_state.txt" 2>&1
lidar_rc=$?
"$SCRIPT_DIR/check_normal_state.sh" > "$session_dir/normal_state.txt" 2>&1
normal_rc=$?

{
  printf 'session=%s\n' "$(basename "$session_dir")"
  printf 'lidar_state_exit_code=%s\n' "$lidar_rc"
  printf 'normal_state_exit_code=%s\n' "$normal_rc"
  if grep -q 'Node  : PASS' "$session_dir/lidar_state.txt"; then printf 'Node=PASS\n'; else printf 'Node=FAIL\n'; fi
  if grep -q 'Topic : PASS' "$session_dir/lidar_state.txt"; then printf 'Topic=PASS\n'; else printf 'Topic=FAIL\n'; fi
  if grep -q 'Data  : PASS' "$session_dir/lidar_state.txt"; then printf 'Data=PASS\n'; else printf 'Data=FAIL\n'; fi
} > "$session_dir/summary.txt"

(
  cd "$session_dir"
  find . -maxdepth 1 -type f ! -name SHA256SUMS ! -name result_report.md -printf '%P\0' \
    | sort -z \
    | xargs -0 -r sha256sum > SHA256SUMS
)

# Generate the editable student report only after hashing the raw Evidence.
# The report is intentionally excluded from SHA256SUMS because the learner edits it.
require_command python3 || exit $?
report_path="$(python3 "$SCRIPT_DIR/create_result_report.py" "$session_dir")" || exit $?

printf 'Evidence saved: %s\n' "$session_dir"
printf 'Result report prepared: %s\n' "$report_path"
exit 0
