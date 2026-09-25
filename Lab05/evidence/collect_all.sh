#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RESULTS_DIR="${RESULTS_DIR:-$ROOT/results/$(date +%Y%m%d_%H%M%S)}"
export RESULTS_DIR
mkdir -p "$RESULTS_DIR"
bash "$ROOT/evidence/collect_system_baseline.sh"
bash "$ROOT/evidence/collect_ros_baseline.sh"
if [[ -n "${REPO_DIR:-}" ]]; then
  export REPO_DIR
  bash "$ROOT/evidence/collect_git_baseline.sh"
else
  echo 'SKIP Git baseline: set REPO_DIR to the lab Git repository.' >&2
  cat > "$RESULTS_DIR/03_git_baseline.txt" <<'EOF'
=== GIT BASELINE ===
NOT_EXECUTED: REPO_DIR was not provided.
EOF
fi
bash "$ROOT/evidence/collect_runtime_topics.sh"
(
  cd "$RESULTS_DIR"
  sha256sum 01_system_baseline.txt 02_ros_baseline.txt 03_git_baseline.txt 04_runtime_topics.txt > manifest.sha256
)
echo "Evidence directory: $RESULTS_DIR"
