# Docker Desktop 설치 가이드 — 사전 준비

> 이 문서는 수업 전에 1회만 수행합니다. ROS 2와 Gazebo는 Windows에 직접 설치하지 않습니다.

## 1. PowerShell 열기

Windows 시작 메뉴에서 **PowerShell**을 실행합니다.

## 2. WSL 2 확인 및 업데이트

```powershell
wsl --version
wsl --status
wsl --update
```

업데이트 후 필요하면:

```powershell
wsl --shutdown
```

Docker Desktop은 Windows에서 Linux container를 실행하기 위해 WSL 2 backend를 사용합니다. 별도의 Ubuntu 배포판을 학생이 직접 실행할 필요는 없습니다.

## 3. Docker Desktop 설치

Docker 공식 사이트에서 **Docker Desktop for Windows**를 설치합니다.

설치 후 Docker Desktop을 실행하고 다음을 확인합니다.

```text
Settings → General → Use WSL 2 based engine
```

지원 환경에서는 기본값으로 활성화되어 메뉴가 보이지 않을 수도 있습니다.

> 이번 실습에서는 Ubuntu WSL 내부에 `docker.io` 또는 Docker Engine을 별도로 설치하지 않습니다.

## 4. 설치 확인

새 PowerShell을 열고:

```powershell
docker version
```

`Client`와 `Server`가 모두 출력되는지 확인합니다.

다음 테스트도 실행합니다.

```powershell
docker run --rm hello-world
```

`Hello from Docker!`가 보이면 준비 완료입니다.

## 5. 실습 image 준비

```powershell
docker pull silverbjin/ros2-humble-fortress-lab:1.0
```

확인:

```powershell
docker image ls silverbjin/ros2-humble-fortress-lab
```

## 완료 기준

```text
[PASS] docker version에서 Client / Server 확인
[PASS] hello-world 실행
[PASS] silverbjin/ros2-humble-fortress-lab:1.0 image 확인
```
