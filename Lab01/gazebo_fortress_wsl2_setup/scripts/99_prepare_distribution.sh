#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PACKAGES_DIR="$ROOT_DIR/packages"
DEB="$PACKAGES_DIR/libogrenextmain2.2.5_2.2.5+dfsg3-0ubuntu2_amd64.deb"

if [[ ! -f "$DEB" ]]; then
    echo "FAIL: $DEB 를 찾을 수 없습니다."
    echo "강사가 빌드한 patched .deb를 packages/에 복사하십시오."
    exit 1
fi

cd "$PACKAGES_DIR"
sha256sum "$(basename "$DEB")" > SHA256SUMS
sha256sum -c SHA256SUMS

echo
echo "Distribution package checksum prepared:"
cat SHA256SUMS
