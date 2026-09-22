# 학생용 초간단 실행 순서

```bash
cd ~/ros2_humble_fortress_lidar_lab
./scripts/01_install_linux.sh      # 최초 1회
./scripts/02_build_lab.sh          # 최초 또는 소스 변경 후
```

터미널 1:
```bash
ros2 launch maintenance_fortress_demo base_demo.launch.py
```

터미널 2:
```bash
ros2 run maintenance_fortress_demo bridge_wrong.sh
```

터미널 3 진단:
```bash
ros2 node list
ros2 topic list | grep scan
timeout 4 ros2 topic echo /scan --once
ign topic -l | grep lidar
timeout 2 ign topic -e -t /lidar_scan
```

터미널 2: `Ctrl+C`, 이후
```bash
ros2 run maintenance_fortress_demo bridge_correct.sh
```

터미널 3 재검증:
```bash
ros2 topic echo /scan --once
ros2 topic hz /scan
ros2 run maintenance_fortress_demo system_check.sh
```
