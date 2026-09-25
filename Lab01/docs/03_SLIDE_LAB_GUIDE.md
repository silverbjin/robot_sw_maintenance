# 슬라이드 단위 실습 가이드 — Slides 11~16

## 실습 시작 전

PowerShell:

```powershell
docker compose up -d
```

브라우저에서 `http://localhost:6080/vnc.html` 접속 → 비밀번호 `student` → Terminator 4분할.

```text
┌─────────────────────┬─────────────────────┐
│ T1 Gazebo + RViz    │ T2 Bridge           │
├─────────────────────┼─────────────────────┤
│ T3 ROS 2 진단       │ T4 Gazebo 진단      │
└─────────────────────┴─────────────────────┘
```

---

## Slide 11 — 장애 관찰

### T1

```bash
ros2 launch maintenance_fortress_demo base_demo.launch.py
```

### T2

```bash
ros2 run maintenance_fortress_demo bridge_wrong.sh
```

### 관찰

- Gazebo: 로봇·장애물·LiDAR world 실행
- RViz: RobotModel은 보이지만 LaserScan은 정상 표시되지 않음

### 기록

> 아직 원인을 확정하지 않는다. 먼저 계층별 증거를 확인한다.

---

## Slide 12 — ROS 2 계층 확인

### T3

```bash
ros2 node list
ros2 topic list | grep scan
timeout 4 ros2 topic echo /scan --once
```

### 판정

- ROS node가 존재 → ROS 전체 장애는 아님
- `/scan` 메시지가 없음 → ROS sensor data 경로에 이상 존재

> `/scan` 이름이 보이는 것과 실제 메시지가 들어오는 것은 다릅니다.

---

## Slide 13 — Gazebo 계층 확인

### T4

```bash
ign topic -l | grep lidar
timeout 3 ign topic -e -t /lidar_scan
```

### 정상 기대값

```text
/lidar_scan 존재
ranges: ... 값 출력
```

### 판정

```text
Gazebo /lidar_scan 정상
ROS /scan 메시지 없음
→ 정상/비정상 경계는 bridge 주변
```

---

## Slide 14 — Bridge 원인 특정

### T3 또는 T4

```bash
PKG=$(ros2 pkg prefix maintenance_fortress_demo)/share/maintenance_fortress_demo
diff "$PKG/config/bridge_wrong.yaml" "$PKG/config/bridge_correct.yaml"
```

### 발견해야 할 차이

```diff
- gz_topic_name: "/wrong_lidar_scan"
+ gz_topic_name: "/lidar_scan"
```

### 원인

`ros_gz_bridge`가 실제 Gazebo LiDAR topic이 아닌 잘못된 topic을 참조하고 있음.

---

## Slide 15 — 최소 수정과 재검증

### T2

`Ctrl+C`로 잘못된 bridge만 종료한 뒤:

```bash
ros2 run maintenance_fortress_demo bridge_correct.sh
```

### T3

```bash
ros2 topic echo /scan --once
ros2 topic hz /scan
```

`ros2 topic hz` 확인 후 `Ctrl+C`.

### 최종 자동 점검

```bash
ros2 run maintenance_fortress_demo system_check.sh
```

정상:

```text
SYSTEM STATUS: PASS
```

### 화면 검증

RViz에서 LaserScan point가 표시되는지 확인합니다.

---

## Slide 16 — 유지보수 기록

```bash
cp $(ros2 pkg prefix maintenance_fortress_demo)/share/maintenance_fortress_demo/records/maintenance_record_template.md \
  ~/student_work/SIM-FORTRESS-LIDAR-001.md
```

기록 항목:

```text
증상 → 진단 증거 → 원인 → 조치 → 재검증 → 예방 조치
```

예방 조치 예:

> 다음 실행부터 `system_check.sh`로 Gazebo sensor → bridge → ROS topic 상태를 확인한다.

---

## 완료 조건

```text
[ ] /lidar_scan 데이터 확인
[ ] 잘못된 bridge mapping 발견
[ ] /scan 메시지 복구
[ ] /scan 발행 주기 확인
[ ] RViz LaserScan 확인
[ ] SYSTEM STATUS: PASS
[ ] 유지보수 기록 작성
```
