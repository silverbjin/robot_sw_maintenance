# maintenance_check_pkg

강사가 학생에게 제공하는 ROS 2 Humble 설치/Overlay 검증용 패키지입니다.

## 학생 배치 위치

```bash
~/robot_ws/src/maintenance_check_pkg
```

## 빌드

```bash
source /opt/ros/humble/setup.bash
cd ~/robot_ws
colcon build --packages-select maintenance_check_pkg
```

## Overlay 적용

```bash
source ~/robot_ws/install/setup.bash
```

## 실행

```bash
ros2 run maintenance_check_pkg status_node
```

정상 출력 예시:

```text
[INFO] [status_node]: Maintenance environment check started.
[INFO] [status_node]: ROS 2 environment is ready.
```
