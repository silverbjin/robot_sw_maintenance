# 선택 실습 — 실제 YDLIDAR를 ROS 2 Humble에서 사용하기

기본 LAB-11~15는 Mock LiDAR를 사용합니다. 이 문서는 **실제 LiDAR 하드웨어가 준비된 강사용 선택 경로**입니다. 학생 기본 실습의 진단 흐름을 하드웨어 준비 문제와 분리하기 위해, 장비가 없거나 설정이 불확실하면 Mock 경로를 유지합니다.

## 1. 왜 기존 myAGV Galactic 패키지를 그대로 사용하지 않는가?

Elephant Robotics의 `myagv_ros2` 저장소는 `galactic-JN` 사용 예에서 Jetson Nano / JetPack 4.6 / ROS 2 Galactic 환경을 안내하고 `ydlidar_ros2_driver`를 포함합니다. 이번 과정은 Ubuntu 22.04 + ROS 2 Humble을 기준으로 하므로, 전체 Galactic workspace를 그대로 복제하는 대신 **공식 YDLIDAR Humble 드라이버를 외부 의존성으로 사용**합니다.

참고:
- https://github.com/elephantrobotics/myagv_ros2
- https://github.com/elephantrobotics/myagv_plus_ros2

Elephant Robotics의 `myagv_plus_ros2`는 Jetson Orin Nano + Ubuntu 22.04 + ROS 2 Humble 소프트웨어 환경을 명시하고 있어 본 과정의 기준 환경과 방향이 일치합니다.

## 2. 공식 YDLIDAR Humble 드라이버 준비

YDLIDAR 공식 ROS 2 드라이버 README는 Humble/Jazzy 계열에서 `humble` 브랜치를 사용하도록 안내합니다.

```bash
cd ~/ydlidar_ros2_ws/src
git clone -b humble https://github.com/YDLIDAR/ydlidar_ros2_driver.git
```

공식 드라이버는 `YDLidar-SDK`에 의존합니다. SDK 설치/빌드는 공식 저장소 절차를 따릅니다.

- Driver: https://github.com/YDLIDAR/ydlidar_ros2_driver
- SDK: https://github.com/YDLIDAR/YDLidar-SDK

빌드 예:

```bash
cd ~/ydlidar_ros2_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

## 3. 실제 장비에서 반드시 강사가 확인할 값

`optional_hardware/myagv_lidar_bringup/config/ydlidar_humble.yaml`은 **템플릿**입니다. 다음 값은 실제 LiDAR 모델의 매뉴얼/동작 상태를 기준으로 **강사가 확인**해야 합니다.

| 파라미터 | 확인 이유 |
|---|---|
| `port` | `/dev/ydlidar`, `/dev/ttyUSB0` 등 실제 장치 경로가 다를 수 있음 |
| `baudrate` | 모델별 통신 속도가 다를 수 있음 |
| `sample_rate` | 모델별 지원 sample rate가 다름 |
| `lidar_type` / `device_type` | 실제 LiDAR 모델 계열에 따라 달라짐 |
| `isSingleChannel` | 모델별 통신 방식 차이 |
| `frequency` | 실제 장비의 지원 주기와 일치해야 함 |
| `range_min` / `range_max` | 장비 사양에 맞춰야 함 |

**정확한 실제 LiDAR 모델을 확인하지 않은 상태에서는 위 템플릿 값이 장비에 맞다고 가정하지 않습니다.**

## 4. 장치 확인

```bash
ls -l /dev/ydlidar /dev/ttyUSB* 2>/dev/null
```

공식 YDLIDAR 패키지는 serial alias 생성용 startup script도 제공하지만, 강의장 운영 정책에 따라 udev/권한 설정을 사전에 완료하는 것을 권장합니다.

## 5. 선택 패키지를 학생 Workspace에 추가

실제 하드웨어 실습을 진행할 때만 선택 wrapper를 ROS 2 workspace로 복사하고 다시 빌드합니다.

```bash
cd <Lab07_Upgrade_Verification_패키지_루트>
cp -a optional_hardware/myagv_lidar_bringup ros2_ws/src/
source /opt/ros/humble/setup.bash
source ~/ydlidar_ros2_ws/install/setup.bash
cd ros2_ws
colcon build --symlink-install
source install/setup.bash
cd ..
```

## 6. 기본 `/scan`으로 실행

공식 드라이버는 LaserScan을 기본적으로 `scan` Topic에 발행합니다.

```bash
ros2 launch myagv_lidar_bringup ydlidar_humble.launch.py output_topic:=/scan
```

확인:

```bash
ros2 topic echo /scan --once
ros2 topic hz /scan
```

## 7. LAB-07의 v1.3 변경을 하드웨어로 재현

wrapper의 `output_topic` remap을 이용해 실제 드라이버의 `/scan`을 `/lidar/scan`으로 바꿀 수 있습니다.

```bash
ros2 launch myagv_lidar_bringup ydlidar_humble.launch.py output_topic:=/lidar/scan
```

그 상태에서 Navigation 측이 `/scan`을 계속 기다리도록 구성하면 Mock 실습과 동일한 **Topic mismatch 개념**을 관찰할 수 있습니다.

```mermaid
flowchart LR
  A[Real YDLIDAR] --> B[Official Humble Driver]
  B -->|remap| C[/lidar/scan]
  D[Navigation Subscriber] --> E[/scan]
  C -. mismatch .- E
```

## 8. 장비가 정상 동작하지 않으면

이 회차의 학습목표는 serial/SDK 문제 해결이 아니라 업그레이드 후 검증 절차입니다. 다음 문제가 발생하면 수업 본 실습은 Mock으로 전환합니다.

- 장치 파일 미검출
- 권한 문제
- SDK/driver 빌드 실패
- 모델 파라미터 불확실
- 모터/전원/케이블 문제

```bash
ros2 launch maintenance_lidar_demo lab_current.launch.py
```

Mock과 실제 하드웨어는 모두 `sensor_msgs/msg/LaserScan`을 기준으로 진단하므로 이후 학습 절차는 동일하게 유지할 수 있습니다.

## 9. 검증 범위 주의

이 패키지의 하드웨어 경로는 **선택용 bringup wrapper와 설정 템플릿**입니다. 실제 장치가 연결되어 실행 시험을 통과하기 전에는 **실제 하드웨어에서 검증되었다고 간주하지 않습니다**.
