#!/usr/bin/env bash
# Shared Lab09 shell helpers. Source this file; do not execute it directly.

LAB09_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LAB09_CONFIG="${LAB09_CONFIG:-$LAB09_ROOT/config/lab09_config.env}"

load_lab09_config() {
  if [[ ! -f "$LAB09_CONFIG" ]]; then
    echo "ERROR: Lab09 config not found: $LAB09_CONFIG" >&2
    return 2
  fi
  # shellcheck disable=SC1090
  source "$LAB09_CONFIG"

  : "${LAB09_MODE:=mock}"
  : "${SCAN_TOPIC:=/scan}"
  : "${LIDAR_NODE_EXACT:=/lab09_mock_lidar}"
  : "${LIDAR_NODE_PATTERN:=lab09_mock_lidar}"
  : "${DATA_OBSERVE_SEC:=4}"
  : "${CHECK_RVIZ:=0}"
  : "${RVIZ_NODE_PATTERN:=rviz2}"
  : "${EVIDENCE_DIR:=evidence}"

  if [[ "$EVIDENCE_DIR" != /* ]]; then
    EVIDENCE_DIR="$LAB09_ROOT/$EVIDENCE_DIR"
  fi
}

source_ros_environment() {
  if [[ "${LAB09_SKIP_ROS_SOURCE:-0}" == "1" ]]; then
    return 0
  fi

  if [[ -n "${ROS_SETUP_FILE:-}" && -f "$ROS_SETUP_FILE" ]]; then
    # shellcheck disable=SC1090
    source "$ROS_SETUP_FILE"
  elif ! command -v ros2 >/dev/null 2>&1; then
    echo "ERROR: ros2 command not found and ROS_SETUP_FILE is unavailable." >&2
    return 3
  fi

  local workspace_setup="${WORKSPACE_SETUP_FILE:-}"
  if [[ -z "$workspace_setup" && -n "${WORKSPACE_SETUP_REL:-}" ]]; then
    workspace_setup="$LAB09_ROOT/$WORKSPACE_SETUP_REL"
  fi
  if [[ -n "$workspace_setup" && -f "$workspace_setup" ]]; then
    # shellcheck disable=SC1090
    source "$workspace_setup"
  fi
}

require_command() {
  local name="$1"
  if ! command -v "$name" >/dev/null 2>&1; then
    echo "ERROR: required command not found: $name" >&2
    return 4
  fi
}

node_is_present() {
  local output
  output="$(ros2 node list 2>/dev/null || true)"
  if [[ -n "${LIDAR_NODE_EXACT:-}" ]]; then
    grep -Fxq "$LIDAR_NODE_EXACT" <<<"$output"
  else
    grep -Eq "$LIDAR_NODE_PATTERN" <<<"$output"
  fi
}

topic_is_present() {
  ros2 topic list 2>/dev/null | grep -Fxq "$SCAN_TOPIC"
}

topic_has_data() {
  local output
  output="$(timeout "${DATA_OBSERVE_SEC}s" ros2 topic hz "$SCAN_TOPIC" 2>&1 || true)"
  grep -Eq 'average rate:[[:space:]]*[0-9]' <<<"$output"
}
