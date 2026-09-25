#!/usr/bin/env bash
set -euo pipefail
if [[ $# -ne 3 ]]; then
  echo 'Usage: finalize_evidence.sh <results-dir> <completed-upgrade-plan.md> <completed-go-no-go.md>' >&2
  exit 2
fi
DIR="$1"; PLAN="$2"; DECISION="$3"
[[ -d "$DIR" ]] || { echo "ERROR: results directory not found: $DIR" >&2; exit 2; }
[[ -s "$PLAN" ]] || { echo "ERROR: completed Upgrade Plan not found/empty: $PLAN" >&2; exit 2; }
[[ -s "$DECISION" ]] || { echo "ERROR: completed GO/NO-GO file not found/empty: $DECISION" >&2; exit 2; }
for f in 01_system_baseline.txt 02_ros_baseline.txt 03_git_baseline.txt 04_runtime_topics.txt; do
  [[ -s "$DIR/$f" ]] || { echo "ERROR: base Evidence missing: $DIR/$f" >&2; exit 1; }
done
cp "$PLAN" "$DIR/05_upgrade_plan.md"
cp "$DECISION" "$DIR/06_go_no_go.md"
(
  cd "$DIR"
  sha256sum \
    01_system_baseline.txt 02_ros_baseline.txt 03_git_baseline.txt \
    04_runtime_topics.txt 05_upgrade_plan.md 06_go_no_go.md > manifest.sha256
)
echo "Finalized Evidence: $DIR"
