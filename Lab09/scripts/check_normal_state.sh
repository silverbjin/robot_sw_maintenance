#!/usr/bin/env bash
set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"
load_lab09_config || exit $?
source_ros_environment || exit $?

printf '%s\n' '=== Lab09 Normal-State Check ==='
"$SCRIPT_DIR/check_lidar_state.sh"
lidar_rc=$?

printf '\n[4/4] RViz CHECK\n'
rviz_rc=0
if [[ "$CHECK_RVIZ" == "1" ]]; then
  rviz_nodes="$(ros2 node list 2>/dev/null || true)"
  if grep -Eq "$RVIZ_NODE_PATTERN" <<<"$rviz_nodes"; then
    printf 'PASS: an RViz-related node is present.\n'
  else
    printf 'FAIL: no RViz-related node was detected.\n'
    rviz_rc=13
  fi
else
  printf 'MANUAL: visually confirm that LaserScan is displayed in RViz 2.\n'
fi

if [[ $lidar_rc -ne 0 ]]; then
  exit "$lidar_rc"
fi
exit "$rviz_rc"
