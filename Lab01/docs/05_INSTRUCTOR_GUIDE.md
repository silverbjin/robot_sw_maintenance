# 강사용 운영 가이드

## 1. 수업 전 점검

PowerShell에서 repository root로 이동한 후:

```powershell
docker pull silverbjin/ros2-humble-fortress-lab:1.0
.\scripts\02_smoke_test.ps1
```

확인:

```text
Container status : running
Restart count    : 0
Smoke test PASS
```

브라우저:

```text
http://localhost:6080/vnc.html
Password: student
```

Container Desktop의 Terminator에서:

```bash
ros2 run maintenance_fortress_demo check_environment.sh
```

`Environment READY` 확인.

## 2. 수업 전 기능 검증

### 정상 world 실행

```bash
ros2 launch maintenance_fortress_demo base_demo.launch.py
```

### 의도적 장애

```bash
ros2 run maintenance_fortress_demo bridge_wrong.sh
```

다른 터미널:

```bash
timeout 3 ign topic -e -t /lidar_scan
timeout 4 ros2 topic echo /scan --once
```

기대 결과:

```text
Gazebo /lidar_scan : 데이터 정상
ROS /scan          : 메시지 없음
```

### 복구

```bash
ros2 run maintenance_fortress_demo bridge_correct.sh
```

재검증:

```bash
ros2 topic echo /scan --once
ros2 topic hz /scan
ros2 run maintenance_fortress_demo system_check.sh
```

최종 기대값:

```text
SYSTEM STATUS: PASS
```

## 3. 슬라이드별 강사 포인트

| Slide | 강사 질문 | 학생이 찾아야 할 것 |
|---|---|---|
| 11 | “RViz에 안 보인다고 센서 고장이라고 말할 수 있는가?” | 아직 확정 불가 |
| 12 | “ROS 전체가 죽었는가?” | node는 살아 있음, `/scan` message는 없음 |
| 13 | “Gazebo sensor는 데이터를 만들고 있는가?” | `/lidar_scan` 정상 |
| 14 | “정상/비정상 경계는 어디인가?” | bridge mapping |
| 15 | “최소 변경으로 무엇만 재시작할 것인가?” | bridge만 재시작 |
| 16 | “해결 경험을 어떻게 예방 절차로 바꿀 것인가?” | 기록 + `system_check.sh` |

## 4. 정답 핵심

```text
실제 Gazebo topic : /lidar_scan
잘못된 설정       : /wrong_lidar_scan
원인               : ros_gz_bridge topic mapping 오류
조치               : correct bridge로 교체 후 bridge만 재시작
```

## 5. 흔한 오판 방지

- `/scan` 이름이 보이는 것만으로 PASS 판정하지 않음.
- RViz 화면만 보고 Gazebo sensor 정상/비정상을 확정하지 않음.
- 문제 발생 시 전체 ROS/Gazebo를 재설치하지 않음.
- 조치 후 반드시 **message + rate + RViz + system_check**를 재검증함.

## 6. 수업 중 Docker 장애 시

PowerShell:

```powershell
docker compose ps
docker logs --tail 100 ros2-humble-fortress-lab
```

Container가 불안정하면:

```powershell
docker compose down
docker compose up -d
```

Docker 자체 문제 해결은 수업 핵심과 분리하고, 가능하면 강사가 사전 준비 시간에 처리합니다.

## 7. 권장 시연 시간

```text
Slide 11 장애 관찰       1.5분
Slide 12 ROS 진단        1.5분
Slide 13 Gazebo 진단     1.5분
Slide 14 원인 특정       1.5분
Slide 15 복구·재검증     2.0분
Slide 16 기록            1.5분
합계                     약 9.5분
```
