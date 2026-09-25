# ROS 2 Demo — Session 5 Baseline

이 데모는 실제 myAGV 하드웨어를 구동하지 않는다. `myagv_bringup`의 교육용 상태 노드가 다음 토픽만 1 Hz로 발행한다.

- `/myagv/system_state` → `READY`
- `/myagv/battery_state` → `82`
- `/myagv/network_state` → `CONNECTED`

## 준비

```bash
bash ros2_demo/setup_demo_workspace.sh
cd ~/lab05_ros2_ws
```

ROS 2 Humble이 설치된 환경이라면:

```bash
source /opt/ros/humble/setup.bash
colcon build --packages-select myagv_bringup
source install/setup.bash
ros2 launch myagv_bringup baseline_demo.launch.py
```

5회차에서는 `pre-upgrade-v1` 기준점만 사용한다. Target 구현으로 이동하지 않는다.
