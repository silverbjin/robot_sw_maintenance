#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PACKAGES_DIR="$ROOT_DIR/packages"
DEB="$PACKAGES_DIR/libogrenextmain2.2.5_2.2.5+dfsg3-0ubuntu2_amd64.deb"
OGRE_PLUGIN="/usr/lib/x86_64-linux-gnu/OGRE-Next/RenderSystem_GL3Plus.so"
BACKUP_DIR="$HOME/.local/share/gazebo_fortress_wsl2_setup/backup"

echo "========================================"
echo " Patched Ogre-Next Installer"
echo "========================================"

if [[ ! -f "$DEB" ]]; then
    echo "FAIL: patched .deb를 찾을 수 없습니다."
    echo "Expected: $DEB"
    echo
    echo "강사가 빌드한 파일을 packages/에 복사한 뒤 다시 실행하십시오."
    exit 1
fi

echo
echo "[1/6] Package architecture"
DEB_ARCH="$(dpkg-deb -f "$DEB" Architecture)"
echo "Package architecture: $DEB_ARCH"
if [[ "$DEB_ARCH" != "amd64" ]]; then
    echo "FAIL: amd64 package가 아닙니다."
    exit 1
fi

echo
echo "[2/6] Package checksum"
if grep -Eq '^[0-9a-fA-F]{64}[[:space:]]+\*?libogrenextmain2\.2\.5_.*\.deb$' "$PACKAGES_DIR/SHA256SUMS" 2>/dev/null; then
    (cd "$PACKAGES_DIR" && sha256sum -c SHA256SUMS)
else
    echo "WARNING: 유효한 SHA256SUMS가 없습니다."
    echo "강사는 배포 전에 scripts/99_prepare_distribution.sh를 실행하십시오."
fi

echo
echo "[3/6] Current Ogre"
dpkg-query -W -f='${Package} ${Version}\n' libogrenextmain2.2.5 || true

echo
echo "[4/6] Backup current GL3Plus plugin"
mkdir -p "$BACKUP_DIR"
if [[ -f "$OGRE_PLUGIN" ]]; then
    TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
    BACKUP="$BACKUP_DIR/RenderSystem_GL3Plus.so.$TIMESTAMP"
    cp "$OGRE_PLUGIN" "$BACKUP"
    echo "Backup: $BACKUP"
fi

echo
echo "[5/6] Installing patched Ogre package"
sudo dpkg -i "$DEB"
sudo ldconfig

echo
echo "[6/6] Verify patch"
if strings "$OGRE_PLUGIN" | grep -q 'glCopyImageSubDataNV'; then
    echo "PASS: glCopyImageSubDataNV detected."
else
    echo "FAIL: patched GL3Plus renderer를 확인할 수 없습니다."
    exit 1
fi

echo
echo "Installation completed."
