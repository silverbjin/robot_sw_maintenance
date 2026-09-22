# Distribution Manifest

## Student-facing files

```text
gazebo_fortress_wsl2_setup/
├── README.md
├── PATCH_INFO.md
├── troubleshooting.md
├── MANIFEST.md
├── packages/
│   ├── README.md
│   └── SHA256SUMS
└── scripts/
    ├── 00_precheck.sh
    ├── 01_install_ogre_patch.sh
    ├── 02_check_gpu.sh
    ├── 03_verify_gazebo.sh
    ├── 99_prepare_distribution.sh
    └── env_gazebo.sh
```

`packages/`에는 강사가 다음 파일을 별도로 추가해야 합니다.

```text
libogrenextmain2.2.5_2.2.5+dfsg3-0ubuntu2_amd64.deb
```

## Instructor-only files

```text
instructor_archive/
├── README.md
├── BUILD_NOTES.md
├── PATCH_SOURCE.md
└── collect_build_artifacts.sh
```

실제 `.buildinfo`, `.changes`, 원본 `RenderSystem_GL3Plus.so`는 사용자의 기존 `~/ogre_wslg_fix`에서 `collect_build_artifacts.sh`로 수집합니다.
