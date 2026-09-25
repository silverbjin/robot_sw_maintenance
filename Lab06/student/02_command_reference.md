# Lab06 명령어 Reference

| 구분 | 명령어 | 목적 |
|---|---|---|
| 자료 받기 | `git clone --filter=blob:none --sparse <repo>` | Sparse Clone 시작 |
| Lab06 선택 | `git sparse-checkout set Lab06` | Lab06만 Working Tree에 표시 |
| Git 상태 | `git status` | 변경/Branch 상태 확인 |
| 이력 | `git log --oneline -5` | 최근 Commit 확인 |
| Tag | `git tag` | Baseline Tag 확인 |
| Target | `git switch release-v2` | Upgrade 대상 적용 |
| Dependency | `rosdep install --from-paths src --ignore-src -r -y` | 의존성 확인/설치 |
| Build | `colcon build --symlink-install` | Workspace Build |
| Source | `source install/setup.bash` | 새 Overlay 반영 |
| 실행 | `ros2 run myagv_monitor monitor_node` | 신규 모듈 최소 실행 |
| Rollback | `git switch --detach pre-upgrade-v1` | Baseline Source 복원 |
| Clean | `rm -rf build install log` | 기존 Build 결과 제거 |

## `rm -rf` 사용 규칙

반드시 먼저:

```bash
pwd
```

로 현재 위치가 `.../Lab06/ros2_ws`인지 확인합니다.
