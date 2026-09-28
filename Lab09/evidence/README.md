# Evidence 저장 폴더

`collect_evidence.sh`를 실행하면 시간별 세션 폴더가 생성된다.

예:

```text
evidence/
└── 20260927-143000_lab09/
    ├── system_info.txt
    ├── node_list.txt
    ├── topic_list.txt
    ├── topic_info.txt
    ├── scan_hz.txt
    ├── lidar_state.txt
    ├── normal_state.txt
    ├── summary.txt
    ├── SHA256SUMS
    └── result_report.md
```

`SHA256SUMS`는 원본 Evidence 파일의 무결성 확인용이다. 학생이 편집하는 `result_report.md`는 해시 대상에서 제외된다.
