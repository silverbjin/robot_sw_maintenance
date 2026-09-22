# 1회차 적용하기 — ROS 2 Humble + Gazebo Fortress LiDAR 유지보수

## 목표
Gazebo에서 LiDAR는 정상인데 RViz에 데이터가 보이지 않는 장애를 진단하고, 잘못된 bridge topic을 수정하여 복구한다.

## A. 최초 1회 환경 준비

### Windows 11 관리자 PowerShell
```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\windows\00_setup_wsl.ps1
```
Ubuntu-22.04를 처음 실행해 Linux 사용자 계정을 만든다.

### WSL2 Ubuntu 22.04
이 폴더를 **WSL 홈 디렉터리**(예: `~/ros2_humble_fortress_lidar_lab`)에 둔 후:
```bash
cd ~/ros2_humble_fortress_lidar_lab
./scripts/01_install_linux.sh
./scripts/02_build_lab.sh
```
새 터미널을 연다.

## B. 실습 시작

### 터미널 1 — Gazebo + RobotModel + RViz
```bash
ros2 launch maintenance_fortress_demo base_demo.launch.py
```
확인: Gazebo에는 로봇·장애물·LiDAR ray가 보이고, RViz에는 RobotModel/TF/Grid가 보인다.

### 터미널 2 — 의도적 오류 bridge
```bash
ros2 run maintenance_fortress_demo bridge_wrong.sh
```
이 bridge는 존재하지 않는 Gazebo 토픽 `/wrong_lidar_scan`을 사용한다.

> ros_gz_bridge 버전에 따라 `/scan` 이름 자체가 보일 수도 있고 안 보일 수도 있다. 핵심 판정은 **메시지가 수신되지 않는 것**이다.

## C. 6단계 진단

### 1) ROS 노드 확인
```bash
ros2 node list
```
판단: ROS 전체 장애인지 확인한다.

### 2) ROS `/scan` 확인
```bash
ros2 topic list | grep scan

timeout 4 ros2 topic echo /scan --once
```
정상 기대값이 아니라 **메시지 수신 실패**가 현재 장애 증거다.

### 3) Gazebo LiDAR 확인
```bash
ign topic -l | grep lidar

timeout 2 ign topic -e -t /lidar_scan
```
정상 결과: `/lidar_scan` 존재 + LaserScan 거리값 출력.

### 4) bridge 설정 비교
```bash
cat ~/ros2_humble_fortress_lidar_lab/maintenance_demo_ws/src/maintenance_fortress_demo/config/bridge_wrong.yaml
cat ~/ros2_humble_fortress_lidar_lab/maintenance_demo_ws/src/maintenance_fortress_demo/config/bridge_correct.yaml
```
핵심 차이:
```text
wrong   : /wrong_lidar_scan
correct : /lidar_scan
```

### 5) 정상 bridge로 복구
터미널 2에서 `Ctrl+C` 후:
```bash
ros2 run maintenance_fortress_demo bridge_correct.sh
```

### 6) 복구 재검증
터미널 3에서:
```bash
ros2 topic list | grep scan
ros2 topic echo /scan --once
ros2 topic hz /scan
```
`ros2 topic hz`는 평균 약 10 Hz를 확인한 뒤 `Ctrl+C`.

RViz에서 확인:
- LaserScan point 표시
- Gazebo 장애물의 **로봇을 향한 면**에 해당하는 스캔 반환
- Status 정상

종합 점검:
```bash
ros2 run maintenance_fortress_demo system_check.sh
```
모두 `[PASS]`이면 복구 완료.

## D. 유지보수 기록
```bash
cp ~/ros2_humble_fortress_lidar_lab/maintenance_demo_ws/src/maintenance_fortress_demo/records/maintenance_record_template.md ~/SIM-FORTRESS-LIDAR-001.md
code ~/SIM-FORTRESS-LIDAR-001.md
```
최소 기록: **증상 → 원인 → 조치 → 검증 결과 → 예방 조치**.

## E. 종료
각 실행 터미널에서 `Ctrl+C`. 남은 프로세스가 있으면:
```bash
pkill -f 'ign gazebo' || true
pkill -f ros_gz_bridge || true
pkill -f rviz2 || true
```

## 학생이 직접 이해해야 할 명령 6개
```bash
ros2 node list
ros2 topic list
ros2 topic echo /scan --once
ros2 topic hz /scan
ign topic -l
ign topic -e -t /lidar_scan
```

## 핵심 판단
```text
Gazebo /lidar_scan 없음       → Gazebo 센서 계층
Gazebo 정상, ROS 메시지 없음  → bridge 계층
ROS 메시지 정상, RViz 미표시  → TF / QoS / RViz 설정
```
