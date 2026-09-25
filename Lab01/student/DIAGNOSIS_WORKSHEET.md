# 학생용 Diagnosis Worksheet

| 단계 | 확인 명령 | 관찰 결과 | PASS/FAIL | 다음 판단 |
|---|---|---|---|---|
| ROS graph | `ros2 node list` | | | |
| ROS scan | `ros2 topic echo /scan --once` | | | |
| Gazebo topic | `ign topic -l \| grep lidar` | | | |
| Gazebo data | `ign topic -e -t /lidar_scan` | | | |
| Bridge config | `diff bridge_wrong.yaml bridge_correct.yaml` | | | |
| Recovery | `ros2 topic echo /scan --once` | | | |
| Rate | `ros2 topic hz /scan` | | | |
| System check | `ros2 run maintenance_fortress_demo system_check.sh` | | | |

## 최종 판단

- 증상:
- 정상으로 확인한 계층:
- 비정상 경계:
- 원인:
- 조치:
- 재검증 결과:
- 예방 조치:
