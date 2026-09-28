# 학생용 패키지 구성

```text
Lab12_Student/
├── README.md
├── docs/
│   ├── 01_lab_flow.md
│   ├── 02_evidence_capture_guide.md
│   └── 03_student_package_manifest.md
├── scenario/
│   ├── case_card.md
│   └── failure_log.txt
├── ros2_ws/
│   └── src/lab12_maintenance_demo/
│       ├── package.xml
│       ├── setup.py
│       ├── setup.cfg
│       ├── config/config.yaml
│       ├── launch/lab12_demo.launch.py
│       └── lab12_maintenance_demo/
│           ├── lidar_publisher.py
│           └── monitor.py
├── scripts/
│   ├── common.sh
│   ├── prepare_lab.sh
│   ├── start_lab.sh
│   ├── check_runtime.sh
│   ├── collect_evidence.sh
│   └── reset_evidence.sh
├── student/
│   └── 01_student_workbook.md
├── reports/
│   ├── README.md
│   ├── 02_maintenance_result_report.md
│   └── 03_operations_followup.md
└── evidence/
    └── README.md
```

## 제외한 강사용 항목

학생용 패키지에는 다음을 포함하지 않습니다.

- 장애 주입 스크립트
- 복구 정답 스크립트
- Workbook 정답
- 결과 보고서 정답
- 강사용 운영 가이드
- 평가 정답/채점 기준
