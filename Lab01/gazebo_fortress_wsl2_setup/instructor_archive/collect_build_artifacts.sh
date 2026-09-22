#!/usr/bin/env bash
set -euo pipefail

SRC="${1:-$HOME/ogre_wslg_fix}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DST="$HERE/collected"

mkdir -p "$DST"

copy_if_exists() {
    local src="$1"
    local dst="$2"
    if [[ -f "$src" ]]; then
        cp -a "$src" "$dst"
        echo "COPIED: $src"
    else
        echo "SKIP:   $src (not found)"
    fi
}

copy_if_exists "$SRC/backup/RenderSystem_GL3Plus.so" \
               "$DST/RenderSystem_GL3Plus.so.original"
copy_if_exists "$SRC/ogre-next_2.2.5+dfsg3-0ubuntu2_amd64.buildinfo" \
               "$DST/ogre-next_2.2.5+dfsg3-0ubuntu2_amd64.buildinfo"
copy_if_exists "$SRC/ogre-next_2.2.5+dfsg3-0ubuntu2_amd64.changes" \
               "$DST/ogre-next_2.2.5+dfsg3-0ubuntu2_amd64.changes"

if [[ -f "$SRC/libogrenextmain2.2.5_2.2.5+dfsg3-0ubuntu2_amd64.deb" ]]; then
    sha256sum "$SRC/libogrenextmain2.2.5_2.2.5+dfsg3-0ubuntu2_amd64.deb" \
      > "$DST/libogrenextmain2.2.5.sha256"
    echo "HASHED: patched .deb"
fi

echo
echo "Collected artifacts: $DST"
ls -lah "$DST"
