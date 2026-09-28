#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
find "$ROOT/evidence" -maxdepth 1 -type f \( -name 'E*.txt' -o -name 'E*.png' -o -name 'evidence_summary.md' \) -delete
printf '[PASS] Evidence outputs removed.\n'
