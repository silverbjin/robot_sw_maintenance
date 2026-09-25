#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RESULTS_DIR="${RESULTS_DIR:-$ROOT/results/$(date +%Y%m%d_%H%M%S)}"
REPO_DIR="${REPO_DIR:-$PWD}"
mkdir -p "$RESULTS_DIR"
OUT="$RESULTS_DIR/03_git_baseline.txt"
if [[ ! -d "$REPO_DIR" ]] || ! git -C "$REPO_DIR" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "ERROR: Git repository not found at: $REPO_DIR" >&2
  exit 2
fi
{
  echo '=== GIT BASELINE ==='
  echo "timestamp=$(date -Is)"
  echo "repo=$(git -C "$REPO_DIR" rev-parse --show-toplevel)"
  echo "branch=$(git -C "$REPO_DIR" branch --show-current)"
  echo "head=$(git -C "$REPO_DIR" rev-parse HEAD)"
  echo
  echo '[status]'
  git -C "$REPO_DIR" status --short --branch
  echo
  echo '[recent commits]'
  git -C "$REPO_DIR" log --oneline -5
  echo
  echo '[tags]'
  git -C "$REPO_DIR" tag --list
  echo
  echo '[pre-upgrade-v1]'
  if git -C "$REPO_DIR" rev-parse -q --verify refs/tags/pre-upgrade-v1 >/dev/null; then
    git -C "$REPO_DIR" show --no-patch --decorate --oneline pre-upgrade-v1
  else
    echo 'NOT_FOUND: pre-upgrade-v1'
  fi
} > "$OUT"
cat "$OUT"
echo "Saved: $OUT" >&2
