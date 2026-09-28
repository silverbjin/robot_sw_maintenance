#!/usr/bin/env bash
set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=common.sh
source "$SCRIPT_DIR/common.sh"
load_lab09_config || exit $?
source_ros_environment || exit $?
require_command ros2 || exit $?
require_command timeout || exit $?

node_status=FAIL
topic_status=FAIL
data_status=FAIL
exit_code=0

printf '%s\n' '======================================='
printf '%s\n' ' Lab09 LiDAR State Check'
printf '%s\n' '======================================='
printf '\n[1/3] NODE CHECK\n'
if node_is_present; then
  node_status=PASS
  printf 'PASS: expected LiDAR-related node is present\n'
else
  printf 'FAIL: expected LiDAR-related node was not detected\n'
  exit_code=10
fi

printf '\n[2/3] TOPIC CHECK\n'
if topic_is_present; then
  topic_status=PASS
  printf 'PASS: %s topic exists\n' "$SCAN_TOPIC"
else
  printf 'FAIL: %s topic was not detected\n' "$SCAN_TOPIC"
  [[ $exit_code -eq 0 ]] && exit_code=11
fi

printf '\n[3/3] DATA CHECK\n'
if [[ "$topic_status" == PASS ]] && topic_has_data; then
  data_status=PASS
  printf 'PASS: messages were observed on %s during the observation window\n' "$SCAN_TOPIC"
else
  printf 'FAIL: no messages were observed on %s during the observation window\n' "$SCAN_TOPIC"
  [[ $exit_code -eq 0 ]] && exit_code=12
fi

printf '\n---------------------------------------\n'
printf 'RESULT\n\n'
printf 'Node  : %s\n' "$node_status"
printf 'Topic : %s\n' "$topic_status"
printf 'Data  : %s\n' "$data_status"
printf '%s\n' '---------------------------------------'
printf '\nSuggested problem area:\n'
if [[ "$node_status" == FAIL ]]; then
  printf 'Program execution / node startup\n'
elif [[ "$topic_status" == FAIL ]]; then
  printf 'Topic creation / configuration\n'
elif [[ "$data_status" == FAIL ]]; then
  printf 'Sensor / Driver / Communication\n'
else
  printf 'No LiDAR data-path anomaly detected\n'
fi
printf '\nUse the observed results to find the matching FAQ entry.\n'
exit "$exit_code"
