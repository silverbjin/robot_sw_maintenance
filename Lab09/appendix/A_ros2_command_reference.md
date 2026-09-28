# 부록 A — ROS 2 명령어 간단 해설

| 명령 | 목적 | 핵심 확인 |
|---|---|---|
| `ros2 node list` | 실행 중인 Node 확인 | 관련 Node 존재 여부 |
| `ros2 topic list` | Topic 목록 확인 | `/scan` 존재 여부 |
| `ros2 topic list \| grep scan` | scan 관련 Topic 필터링 | `/scan` 존재 여부 |
| `ros2 topic hz /scan` | 메시지 수신 주기 확인 | 실제 Data 수신 여부 |
| `ros2 topic info /scan --verbose` | Publisher/Subscriber 상세 확인 | 통신 구조 Evidence |
| `echo $ROS_DISTRO` | 현재 ROS 배포판 확인 | `humble` 등 |

## 중요한 구분

```text
Topic 존재 ≠ Data 수신
Data 정상 ≠ RViz 표시 정상
```

따라서 항상:

```text
NODE → TOPIC → DATA → RViz
```

순서로 확인합니다.
