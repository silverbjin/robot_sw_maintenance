#!/usr/bin/env bash
set -u
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
python3 "$SCRIPT_DIR/collect_evidence.py" --profile developer --output-dir "$ROOT_DIR/results"
rc=$?
if [[ $rc -eq 10 ]]; then
  echo "[INFO] NOT_READY는 수집 도구 오류가 아니라 점검 항목 중 FAIL이 있다는 의미입니다."
fi
exit $rc
