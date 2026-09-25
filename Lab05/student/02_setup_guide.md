# 실습용 Setup Guide

## 1. 사전 준비

Master 패키지를 Ubuntu 22.04 / ROS 2 Humble 환경에 배치한다.

```bash
cd Lab05
```

셸 문법을 먼저 확인한다.

```bash
find . -name '*.sh' -print0 | xargs -0 -n1 bash -n
```

## 2. 데모 Git 저장소 준비

```bash
bash ros2_demo/setup_demo_workspace.sh
cd ~/lab05_ros2_ws
```

확인:

```bash
git status
git log --oneline -5
git tag
git show --no-patch --decorate pre-upgrade-v1
```

예상:

- `pre-upgrade-v1` Tag 존재
- Working Tree clean
- Commit 메시지에 `Session 5 stable baseline`

## 3. ROS 2 데모 Build — ROS 2 Humble이 설치된 경우

```bash
source /opt/ros/humble/setup.bash
cd ~/lab05_ros2_ws
colcon build --packages-select myagv_bringup
source install/setup.bash
```

실행:

```bash
ros2 launch myagv_bringup baseline_demo.launch.py
```

다른 터미널:

```bash
source /opt/ros/humble/setup.bash
source ~/lab05_ros2_ws/install/setup.bash
ros2 topic list
ros2 topic echo /myagv/system_state --once
```

예상 토픽:

- `/myagv/system_state`
- `/myagv/battery_state`
- `/myagv/network_state`

이 데모는 상태 토픽만 발행하며 실제 모터를 제어하지 않는다.

## 4. Evidence 사전 점검

```bash
REPO_DIR=~/lab05_ros2_ws RESULTS_DIR=/tmp/lab05_evidence_test \
  bash evidence/collect_all.sh
bash evidence/validate_evidence.sh --base /tmp/lab05_evidence_test
```
