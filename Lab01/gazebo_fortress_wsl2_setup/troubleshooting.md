# Troubleshooting

## 1. `GL3PlusTextureGpu::copyTo` 오류

### 증상

```text
OGRE EXCEPTION(9:UnimplementedException)
in GL3PlusTextureGpu::copyTo
```

### 확인

```bash
strings /usr/lib/x86_64-linux-gnu/OGRE-Next/RenderSystem_GL3Plus.so \
  | grep glCopyImageSubDataNV
```

출력이 없다면 patched Ogre runtime이 설치되지 않은 것입니다.

```bash
./scripts/01_install_ogre_patch.sh
```

설치 후 다시 확인합니다.

---

## 2. NVIDIA 대신 Intel GPU가 선택됨

확인:

```bash
glxinfo -B | grep -E 'Device|OpenGL renderer|OpenGL version'
```

문제 예:

```text
D3D12 (Intel(R) Iris(R) Xe Graphics)
```

NVIDIA 강제 선택:

```bash
export MESA_D3D12_DEFAULT_ADAPTER_NAME=NVIDIA
```

다시 확인:

```bash
glxinfo -B | grep -E 'Device|OpenGL renderer|OpenGL version'
```

정상 예:

```text
D3D12 (NVIDIA ...)
```

---

## 3. Gazebo GUI가 회색 빈 화면으로 표시됨

`shapes.sdf`는 정상인데 프로젝트 world에서 회색 화면만 나타나는 경우에는 GUI configuration을 확인합니다.

기본 설정 파일:

```text
~/.ignition/gazebo/6/gui.config
```

직접 확인:

```bash
ls -l ~/.ignition/gazebo/6/gui.config
```

프로젝트 world를 직접 시험할 때:

```bash
ign gazebo -v 4 -r /path/to/world.sdf \
  --gui-config "$HOME/.ignition/gazebo/6/gui.config"
```

이 명령에서 정상화되면 Ogre2 자체가 아니라 프로젝트의 `<gui>` / GUI plugin 구성 문제가 원인입니다.

### ROS 2 Python launch 주의

다음처럼 사용하지 마십시오.

```python
'~/.ignition/gazebo/6/gui.config'
```

`ExecuteProcess`는 shell의 `~` 확장을 자동으로 수행하지 않습니다.

올바른 방법:

```python
from pathlib import Path

gui_config = str(Path.home() / '.ignition/gazebo/6/gui.config')
```

---

## 4. `XMLError`가 발생함

### 메시지 예

```text
Failed to load file [~/.ignition/gazebo/6/gui.config]: XMLError
```

이 경우 실제 XML 오류가 아니라 `~`가 확장되지 않은 경로 문제일 수 있습니다.

확인:

```bash
ls "$HOME/.ignition/gazebo/6/gui.config"
```

launch에서는 반드시 절대 경로로 전달하십시오.

---

## 5. Software rendering이 남아 있음

확인:

```bash
env | grep -E 'LIBGL_ALWAYS_SOFTWARE|LIBGL_DRI3_DISABLE|MESA_GL_VERSION_OVERRIDE|QT_QPA_PLATFORM'
```

정상 baseline에서는 다음 값을 제거합니다.

```bash
unset LIBGL_ALWAYS_SOFTWARE
unset LIBGL_DRI3_DISABLE
unset MESA_GL_VERSION_OVERRIDE
unset QT_QPA_PLATFORM
```

그 후 NVIDIA 경로를 지정합니다.

```bash
export MESA_D3D12_DEFAULT_ADAPTER_NAME=NVIDIA
```

---

## 6. `shapes.sdf`부터 분리 진단

프로젝트를 바로 디버깅하지 말고 먼저 Gazebo 기본 world를 확인합니다.

```bash
source scripts/env_gazebo.sh
ign gazebo -v 4 shapes.sdf
```

### `shapes.sdf`도 실패

그래픽 runtime / Ogre / WSLg 계층을 점검합니다.

### `shapes.sdf`는 성공하지만 프로젝트만 실패

다음을 확인합니다.

1. GUI config
2. SDF `<gui>` 설정
3. 프로젝트 resource path
4. project-specific rendering / sensor plugin

---

## 7. LiDAR 확인

```bash
ign topic -l | grep lidar
```

```bash
timeout 3 ign topic -e -t /lidar_scan
```

GUI와 sensor rendering은 별도 경로일 수 있으므로 두 항목을 각각 확인합니다.

---

## 8. 공식 Ogre 패키지로 원복

```bash
sudo apt update
sudo apt install --reinstall libogrenextmain2.2.5
sudo ldconfig
```

원복 확인:

```bash
dpkg-query -W -f='${Package} ${Version}\n' libogrenextmain2.2.5
```
