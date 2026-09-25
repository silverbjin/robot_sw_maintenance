# 실습용 ROS 2 / Gazebo 명령 가이드

> 이 문서의 명령은 **브라우저로 접속한 Container Desktop의 Terminator**에서 실행합니다. Windows PowerShell에 입력하지 않습니다.

## 환경 확인

```bash
ros2 run maintenance_fortress_demo check_environment.sh
```

용도: ROS 2 Humble, Gazebo, RViz2, ros_gz_bridge, 실습 package, DISPLAY가 준비되었는지 확인합니다.

## ROS 2 계층

### 노드 목록

```bash
ros2 node list
```

용도: ROS graph 전체가 살아 있는지 확인합니다.

### scan 관련 topic 확인

```bash
ros2 topic list | grep scan
```

용도: `/scan` 이름이 ROS graph에 존재하는지 확인합니다.

### 실제 LaserScan 메시지 확인

```bash
timeout 4 ros2 topic echo /scan --once
```

용도: `/scan`에서 **실제 데이터가 수신되는지** 확인합니다. Topic 이름만 존재하는 것은 정상 판정 근거가 아닙니다.

### 발행 주기 확인

```bash
ros2 topic hz /scan
```

용도: 복구 후 약 10 Hz 수준으로 지속 발행되는지 확인합니다. 확인 후 `Ctrl+C`로 종료합니다.

## Gazebo 계층

### LiDAR topic 확인

```bash
ign topic -l | grep lidar
```

정상 예:

```text
/lidar_scan
```

### LiDAR 실제 데이터 확인

```bash
timeout 3 ign topic -e -t /lidar_scan
```

`ranges:` 값이 출력되면 Gazebo sensor와 Gazebo Transport가 데이터를 만들고 있는 것입니다. `inf`는 해당 방향의 측정 범위 안에 장애물이 없다는 의미로 정상일 수 있습니다.

## Bridge 계층

### 의도적 장애 실행

```bash
ros2 run maintenance_fortress_demo bridge_wrong.sh
```

### 설정 비교

```bash
PKG=$(ros2 pkg prefix maintenance_fortress_demo)/share/maintenance_fortress_demo
diff "$PKG/config/bridge_wrong.yaml" "$PKG/config/bridge_correct.yaml"
```

핵심 차이:

```text
wrong   : /wrong_lidar_scan
correct : /lidar_scan
```

### 정상 bridge 실행

기존 bridge 터미널에서 `Ctrl+C` 후:

```bash
ros2 run maintenance_fortress_demo bridge_correct.sh
```

## 최종 자동 점검

```bash
ros2 run maintenance_fortress_demo system_check.sh
```

`SYSTEM STATUS: PASS`이면 Gazebo → bridge → ROS 데이터 경로가 복구된 것입니다.
