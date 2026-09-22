# Gazebo Fortress + WSL2 Ogre2 Setup

## 1. 목적

이 배포본은 다음 환경에서 Gazebo Fortress의 Ogre2 렌더링을 안정적으로 사용하기 위한 실습용 설정 패키지입니다.

- Windows 11
- WSL2 / WSLg
- Ubuntu 22.04
- ROS 2 Humble
- Gazebo Fortress / Ignition Gazebo 6
- Ogre-Next 2.2.5
- NVIDIA GPU + Mesa D3D12

특정 WSLg / Mesa D3D12 환경에서는 Ubuntu 22.04의 Ogre-Next 2.2.5가 다음 오류로 종료될 수 있습니다.

```text
OGRE EXCEPTION(9:UnimplementedException)
in GL3PlusTextureGpu::copyTo
```

이 실습에서는 Ogre 2.3으로 올리지 않고, Gazebo Fortress가 기대하는 Ogre-Next 2.2.5 ABI를 유지한 채 `GL_NV_copy_image` fallback 수정만 backport한 패키지를 사용합니다.

> 중요: 이 배포본에는 patched `.deb` 파일이 포함되어 있지 않습니다. 강사가 빌드한 아래 파일을 `packages/`에 직접 복사해야 합니다.
>
> `libogrenextmain2.2.5_2.2.5+dfsg3-0ubuntu2_amd64.deb`

---

## 2. 배포 디렉터리 준비

강사가 빌드한 패키지를 복사합니다.

```bash
cp ~/ogre_wslg_fix/libogrenextmain2.2.5_2.2.5+dfsg3-0ubuntu2_amd64.deb \
  ./packages/
```

SHA-256을 생성합니다.

```bash
./scripts/99_prepare_distribution.sh
```

검증:

```bash
cd packages
sha256sum -c SHA256SUMS
cd ..
```

---

## 3. 학생 설치 순서

### STEP 1 — 사전 점검

```bash
chmod +x scripts/*.sh
./scripts/00_precheck.sh
```

### STEP 2 — patched Ogre 설치

```bash
./scripts/01_install_ogre_patch.sh
```

### STEP 3 — NVIDIA GPU 경로 확인

```bash
./scripts/02_check_gpu.sh
```

정상 예:

```text
OpenGL renderer string: D3D12 (NVIDIA ...)
```

### STEP 4 — Gazebo Ogre2 검증

```bash
./scripts/03_verify_gazebo.sh
```

Gazebo `shapes.sdf`에서 도형들이 최소 20~30초 이상 안정적으로 표시되는지 확인합니다.

정상 기준:

- ground plane 표시
- box / sphere / cylinder 표시
- white / black / gray blank screen 없음
- 심한 flicker 없음
- `GL3PlusTextureGpu::copyTo` crash 없음

---

## 4. ROS 2 실습 환경 적용

새 터미널에서 다음 파일을 `source` 합니다.

```bash
source scripts/env_gazebo.sh
```

현재 renderer 확인:

```bash
glxinfo -B | grep -E 'Device|OpenGL renderer|OpenGL version'
```

그 다음 ROS 2 workspace를 실행합니다.

```bash
cd ~/ros2_humble_fortress_lidar_lab/maintenance_demo_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 launch maintenance_fortress_demo base_demo.launch.py
```

### Launch 파일의 GUI config 주의

Gazebo GUI가 회색 빈 화면으로 뜨는 경우, 프로젝트 SDF의 `<gui>` 설정 대신 정상 `gui.config`를 강제해야 할 수 있습니다.

Python launch에서는 `~`를 문자열로 직접 넘기지 말고 `Path.home()`으로 절대 경로를 만듭니다.

```python
from pathlib import Path

gui_config = str(Path.home() / '.ignition/gazebo/6/gui.config')

ExecuteProcess(
    cmd=[
        'ign', 'gazebo', '-r', str(world),
        '--gui-config', gui_config,
    ],
    output='screen',
)
```

---

## 5. LiDAR 확인

```bash
ign topic -l | grep lidar
```

```bash
timeout 3 ign topic -e -t /lidar_scan
```

거리 데이터가 출력되면 정상입니다.

---

## 6. 정상 실습 환경에서 사용하지 않는 변수

다음은 문제 분리 과정에서 사용했던 진단용 설정입니다. 정상 실습 baseline에서는 사용하지 않습니다.

```text
LIBGL_ALWAYS_SOFTWARE
LIBGL_DRI3_DISABLE
MESA_GL_VERSION_OVERRIDE
QT_QPA_PLATFORM
```

`env_gazebo.sh`는 이 값들이 남아 있으면 자동으로 해제합니다.

---

## 7. 원복

Ubuntu 공식 Ogre 패키지로 되돌리려면:

```bash
sudo apt update
sudo apt install --reinstall libogrenextmain2.2.5
sudo ldconfig
```

자세한 내용은 `troubleshooting.md`를 참고하십시오.
