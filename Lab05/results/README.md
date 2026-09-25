# results

실습 중 생성되는 Evidence를 저장한다.

권장 최종 구조:

```text
results/<run_id>/
├── 01_system_baseline.txt
├── 02_ros_baseline.txt
├── 03_git_baseline.txt
├── 04_runtime_topics.txt
├── 05_upgrade_plan.md
├── 06_go_no_go.md
└── manifest.sha256
```

1~4는 `evidence/collect_all.sh`로 수집한다.  
Upgrade Plan과 GO/NO-GO Checklist를 작성한 뒤 다음 명령으로 5~6을 복사하고 checksum을 갱신한다.

```bash
bash evidence/finalize_evidence.sh \
  results/<run_id> \
  reports/06_upgrade_plan_template.md \
  reports/07_go_no_go_checklist.md
```

실제 수업에서는 강사가 지정한 run directory를 사용한다.
