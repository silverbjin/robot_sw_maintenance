# Git Repository 프로젝트 구조

## 권장 구조

```text
ros2-humble-fortress-lab/
├─ README.md
├─ README_BUILD_AND_PUBLISH.md
├─ compose.yaml
├─ Dockerfile
├─ .gitignore
│
├─ docs/
│  ├─ 00_DOCKER_DESKTOP_SETUP.md
│  ├─ 01_DOCKER_COMMAND_GUIDE.md
│  ├─ 02_ROS2_COMMAND_GUIDE.md
│  ├─ 03_SLIDE_LAB_GUIDE.md
│  ├─ 04_PROJECT_STRUCTURE.md
│  └─ 05_INSTRUCTOR_GUIDE.md
│
├─ docker/
│  └─ start-desktop.sh
│
├─ scripts/
│  ├─ 01_build.ps1
│  ├─ 02_smoke_test.ps1
│  ├─ 03_push.ps1
│  ├─ 04_export_offline.ps1
│  └─ 05_verify_offline.ps1
│
├─ student/
│  ├─ README.md
│  └─ DIAGNOSIS_WORKSHEET.md
│
└─ maintenance_demo_ws/
   └─ src/
      └─ maintenance_fortress_demo/
         ├─ CMakeLists.txt
         ├─ package.xml
         ├─ config/
         │  ├─ bridge_wrong.yaml
         │  └─ bridge_correct.yaml
         ├─ launch/
         │  └─ base_demo.launch.py
         ├─ records/
         │  └─ maintenance_record_template.md
         ├─ rviz/
         │  └─ lidar_demo.rviz
         ├─ scripts/
         │  ├─ bridge_wrong.sh
         │  ├─ bridge_correct.sh
         │  ├─ check_environment.sh
         │  └─ system_check.sh
         ├─ urdf/
         │  └─ maintenance_robot.urdf
         └─ worlds/
            └─ lidar_demo.sdf
```

## Git에 포함할 것

- Dockerfile / compose.yaml
- Docker startup·build·smoke test 스크립트
- ROS 2 package source
- 학생·강사 Markdown 문서
- bridge wrong/correct 설정
- RViz / URDF / SDF

## Git에 포함하지 않을 것

```text
maintenance_demo_ws/build/
maintenance_demo_ws/install/
maintenance_demo_ws/log/
student_work/
*.tar
*.zip
```

Docker image archive `ros2-humble-fortress-lab-1.0.tar`는 크기가 크므로 Git repository가 아니라 USB, 사내 파일 서버 또는 별도 Release 자산으로 배포하는 것을 권장합니다.

## Image 이름

모든 문서·스크립트·compose에서 다음 이름으로 통일합니다.

```text
silverbjin/ros2-humble-fortress-lab:1.0
```

최종 확인 예:

```powershell
Get-ChildItem -Recurse -File | Select-String "physicalai/ros2-humble-fortress-lab"
```

결과가 없으면 이전 namespace가 남아 있지 않은 것입니다.
