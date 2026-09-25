#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 STUDENT_ID"
  exit 2
fi

STUDENT_ID="$1"
if [[ ! "$STUDENT_ID" =~ ^[A-Za-z0-9._-]+$ ]]; then
  echo "ERROR: STUDENT_ID may contain only letters, numbers, ., _, -"
  exit 2
fi

BASE_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
OUT="$BASE_DIR/evidence"
mkdir -p "$OUT/logs" "$OUT/screenshots" "$OUT/submissions"
TS="$(date +%Y%m%d_%H%M%S)"
TMP="$OUT/submissions/${STUDENT_ID}_${TS}"
mkdir -p "$TMP"

cp -a "$OUT/logs" "$TMP/" 2>/dev/null || true
cp -a "$OUT/screenshots" "$TMP/" 2>/dev/null || true

if [[ -f "$BASE_DIR/reports/05_result_report_template.md" ]]; then
  cp "$BASE_DIR/reports/05_result_report_template.md" "$TMP/"
fi

(
  cd "$OUT/submissions"
  zip -qr "${STUDENT_ID}_${TS}.zip" "${STUDENT_ID}_${TS}"
)
rm -rf "$TMP"

echo "Created: $OUT/submissions/${STUDENT_ID}_${TS}.zip"
