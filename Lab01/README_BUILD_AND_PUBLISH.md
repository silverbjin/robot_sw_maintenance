# silverbjin/ros2-humble-fortress-lab:1.0 — Build / Push / Offline Export

## 목표

학생 온라인 시작:

```powershell
docker pull silverbjin/ros2-humble-fortress-lab:1.0
docker compose up -d
```

브라우저: `http://localhost:6080/vnc.html`  
VNC password: `student`

인터넷 제한 강의장:

```powershell
docker load -i .\ros2-humble-fortress-lab-1.0.tar
docker compose up -d
```

## 강사용 생성 순서

1. Docker Desktop 실행(WSL 2 backend / Linux containers).
2. `.\scripts\01_build.ps1`
3. `.\scripts\02_smoke_test.ps1`
4. 브라우저에서 noVNC 접속 및 `check_environment.sh` 확인.
5. Gazebo → wrong bridge → correct bridge → `system_check.sh` 실제 검증.
6. `docker login`
7. `.\scripts\03_push.ps1`
8. 별도 PC에서 `docker pull silverbjin/ros2-humble-fortress-lab:1.0` 확인.
9. `.\scripts\04_export_offline.ps1`로 `ros2-humble-fortress-lab-1.0.tar` 생성.
10. `.\scripts\05_verify_offline.ps1`로 `docker load` 재검증.

## 오프라인 파일 무결성

```powershell
Get-FileHash .\ros2-humble-fortress-lab-1.0.tar -Algorithm SHA256
```

## 수업의 핵심

```text
장애 관찰 → ROS 계층 → Gazebo 계층 → 정상/비정상 경계 → bridge 수정 → 재검증 → 유지보수 기록
```
