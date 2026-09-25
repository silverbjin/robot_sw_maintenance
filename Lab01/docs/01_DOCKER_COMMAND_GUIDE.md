# 실습용 Docker 명령 가이드

> 아래 명령은 **Windows PowerShell**에서 실행합니다. Docker를 깊게 배우는 것이 아니라 실습 환경을 열고 닫는 데 필요한 명령만 사용합니다.

## 1. 현재 폴더 확인

```powershell
Get-Location
```

## 2. 실습 폴더로 이동

예:

```powershell
cd C:\Users\Jinho\Downloads\ros2_humble_fortress_lab_docker_1.0
```

`compose.yaml`이 보이는지 확인합니다.

```powershell
dir
```

## 3. Docker image 받기

```powershell
docker pull silverbjin/ros2-humble-fortress-lab:1.0
```

- `docker pull`: Docker Hub에서 실습 image를 내려받습니다.
- `:1.0`: 수업에서 사용할 image 버전입니다.

## 4. Container 시작

```powershell
docker compose up -d
```

- `compose up`: `compose.yaml` 설정으로 container를 만듭니다.
- `-d`: PowerShell을 계속 사용할 수 있도록 백그라운드에서 실행합니다.

## 5. 상태 확인

```powershell
docker compose ps
```

정상 기준:

```text
STATUS: Up ... (healthy)
PORTS : 0.0.0.0:6080->6080/tcp
```

## 6. 브라우저 접속

주소창:

```text
http://localhost:6080/vnc.html
```

VNC 비밀번호:

```text
student
```

Container Desktop이 나타나면 **Terminator**를 실행합니다.

## 7. 문제가 있을 때 로그 확인

```powershell
docker logs --tail 100 ros2-humble-fortress-lab
```

## 8. 실습 종료

Container 중지·삭제:

```powershell
docker compose down
```

다음 수업에서 다시 시작:

```powershell
docker compose up -d
```

## 온라인이 제한된 강의장

강사가 제공한 `ros2-humble-fortress-lab-1.0.tar`가 있다면:

```powershell
docker load -i .\ros2-humble-fortress-lab-1.0.tar
docker compose up -d
```

이 경우 `docker pull`은 필요하지 않습니다.
