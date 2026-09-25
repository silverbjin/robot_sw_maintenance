# 학생용 Quick Start — LiDAR Bridge 장애 진단

## 1. PowerShell — Container 시작

```powershell
docker pull silverbjin/ros2-humble-fortress-lab:1.0
docker compose up -d
docker compose ps
```

브라우저:

```text
http://localhost:6080/vnc.html
Password: student
```

Container Desktop에서 Terminator를 실행합니다.

## 2. 환경 확인

```bash
ros2 run maintenance_fortress_demo check_environment.sh
```

`Environment READY` 확인.

## 3. Terminator 4분할

```text
T1: Gazebo + RViz
T2: Bridge
T3: ROS 2 진단
T4: Gazebo 진단
```

## 4. T1 — World 실행

```bash
ros2 launch maintenance_fortress_demo base_demo.launch.py
```

## 5. T2 — 장애 주입

```bash
ros2 run maintenance_fortress_demo bridge_wrong.sh
```

## 6. T3 — ROS 2 확인

```bash
ros2 node list
ros2 topic list | grep scan
timeout 4 ros2 topic echo /scan --once
```

## 7. T4 — Gazebo 확인

```bash
ign topic -l | grep lidar
timeout 3 ign topic -e -t /lidar_scan
```

Gazebo 데이터가 정상인데 ROS `/scan` 메시지가 없으면 bridge 계층을 조사합니다.

## 8. Bridge 비교

```bash
PKG=$(ros2 pkg prefix maintenance_fortress_demo)/share/maintenance_fortress_demo
diff "$PKG/config/bridge_wrong.yaml" "$PKG/config/bridge_correct.yaml"
```

## 9. 복구

T2에서 `Ctrl+C` 후:

```bash
ros2 run maintenance_fortress_demo bridge_correct.sh
```

## 10. 재검증

```bash
ros2 topic echo /scan --once
ros2 topic hz /scan
```

`ros2 topic hz` 확인 후 `Ctrl+C`.

```bash
ros2 run maintenance_fortress_demo system_check.sh
```

## 11. 기록

```bash
cp $(ros2 pkg prefix maintenance_fortress_demo)/share/maintenance_fortress_demo/records/maintenance_record_template.md \
  ~/student_work/SIM-FORTRESS-LIDAR-001.md
```

자세한 절차: [`../docs/03_SLIDE_LAB_GUIDE.md`](../docs/03_SLIDE_LAB_GUIDE.md)
