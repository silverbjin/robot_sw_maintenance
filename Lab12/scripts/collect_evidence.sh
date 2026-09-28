#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/common.sh"
source_ros

OUT="$LAB_ROOT/evidence"
mkdir -p "$OUT"

printenv ROS_DISTRO > "$OUT/E01_environment.txt"
ros2 node list > "$OUT/E02_node_list.txt"
ros2 topic list > "$OUT/E03_topic_list.txt"
(timeout 6s ros2 topic hz /lidar_scan || true) > "$OUT/E04_topic_hz.txt" 2>&1
(
  cd "$LAB_ROOT"
  git status --short
) > "$OUT/E05_git_status.txt"
(
  cd "$LAB_ROOT"
  git diff -- ros2_ws/src/lab12_maintenance_demo/config/config.yaml
) > "$OUT/E06_git_diff.txt"
(
  cd "$LAB_ROOT"
  git log --oneline --decorate -5
) > "$OUT/E07_git_log.txt"
(timeout 5s ros2 topic echo /lab12/function_status --once || true) > "$OUT/E08_function_status.txt" 2>&1

node_pass=FAIL
if grep -qx '/lab12_lidar_publisher' "$OUT/E02_node_list.txt" && grep -qx '/lab12_monitor' "$OUT/E02_node_list.txt"; then
  node_pass=PASS
fi

topic_pass=FAIL
if grep -qx '/lidar_scan' "$OUT/E03_topic_list.txt" && grep -q 'average rate:' "$OUT/E04_topic_hz.txt"; then
  topic_pass=PASS
fi

function_pass=FAIL
if grep -q 'FUNCTION_TEST=PASS' "$OUT/E08_function_status.txt"; then
  function_pass=PASS
fi

cat > "$OUT/evidence_summary.md" <<EOF2
# LAB12 Evidence Summary

| Evidence | 항목 | 판정/요약 |
|---|---|---|
| E01 | ROS 2 환경 | $(cat "$OUT/E01_environment.txt" | tr '\n' ' ') |
| E02 | 핵심 노드 | $node_pass |
| E03/E04 | LiDAR 토픽/통신 | $topic_pass |
| E05/E06 | Git 변경 상태 | 복구 변경 여부 확인 필요 |
| E07 | Git 기준선/이력 | stable-2026-08 포함 여부 확인 |
| E08 | 기능 상태 | $function_pass |

## 최종 기능 판정

- NODE_STATUS: $node_pass
- TOPIC_STATUS: $topic_pass
- FUNCTION_TEST: $function_pass
EOF2

echo "[PASS] Evidence collected in: $OUT"
echo "Open: $OUT/evidence_summary.md"
