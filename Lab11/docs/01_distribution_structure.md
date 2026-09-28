# ① 최종 배포 파일/디렉토리 구조

```text
Lab11_maintenance_procedure/
├── README.md
├── docs/
│   └── 01_distribution_structure.md
├── demo/
│   └── ros2_ws/
│       └── src/
│           └── maintenance_lidar_demo/
│               ├── package.xml
│               ├── setup.py
│               ├── setup.cfg
│               ├── resource/
│               │   └── maintenance_lidar_demo
│               ├── launch/
│               │   └── lab11_demo.launch.py
│               └── maintenance_lidar_demo/
│                   ├── __init__.py
│                   ├── lidar_node.py
│                   └── monitor_node.py
├── scripts/
│   ├── common.sh
│   ├── build_demo.sh
│   ├── start_demo.sh
│   ├── stop_demo.sh
│   ├── restart_lidar_demo.sh
│   ├── check_system.sh
│   └── collect_evidence.sh
├── student/
│   ├── Lab11_Workbook.md
│   ├── Lab11_Result_Report.md
│   └── evidence/
│       └── .gitkeep
└── instructor/
    ├── Instructor_Guide.md
    ├── answer_key.md
    ├── inject_slow_scan.sh
    └── reset_demo.sh
```

## 슬라이드와 파일의 대응

| 슬라이드 | 학생 행동 | 주 사용 파일 | Evidence |
|---|---|---|---|
| Slide 12 | `/scan` 이상 최초 확인 | `Lab11_Workbook.md` | `evidence_01_fault.txt/png` |
| Slide 13 | Node/Topic/Data/Resource 비교 | `check_system.sh`, Workbook | `evidence_02_system.txt/png` |
| Slide 14 | Publisher 확인 + 최소 복구 | `restart_lidar_demo.sh` | `evidence_03_connection.txt/png` |
| Slide 15 | 복구 전·후 + 지속성 검증 | Workbook, Report | `evidence_04_recovery.txt/png` |

## 배포 원칙

- 학생은 ROS 2 코드를 작성하지 않는다.
- 학생은 상태 확인 명령과 Workbook 판단·기록에 집중한다.
- 장애 주입은 강사만 수행한다.
- 복구는 전체 재부팅이 아니라 `lidar_node`만 재시작한다.
- 복구 완료는 `/scan` 존재가 아니라 정상 기준(약 10 Hz) 충족 및 지속성으로 판단한다.
