# maintenance_check_pkg

학생은 이 패키지의 소스 코드를 작성하지 않습니다.

## 배치

```bash
mkdir -p ~/robot_ws/src
cp -r maintenance_check_pkg ~/robot_ws/src/
```

## 빌드

```bash
source /opt/ros/humble/setup.bash
cd ~/robot_ws
colcon build --packages-select maintenance_check_pkg
```

## Overlay

```bash
source ~/robot_ws/install/setup.bash
```

## 실행

```bash
ros2 run maintenance_check_pkg status_node
```

정상 결과:

```text
Maintenance environment check started.
ROS 2 environment is ready.
```
