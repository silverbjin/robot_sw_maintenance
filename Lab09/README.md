# Lab09 Student Package

9회차 **ROS 2 로봇 사용자 문제 대응 실습** 학생 배포본입니다.

## 진행 순서

```text
1. workbook/01_student_workbook.md
2. 상태 확인
3. workbook/02_faq.md
4. 사용자 허용 조치 선택
5. 복구 여부 재검증
6. ./scripts/collect_evidence.sh lab09
7. `./scripts/verify_evidence.sh <세션폴더>`로 Evidence 확인
8. 생성된 result_report.md 작성
```

## 시작

```bash
cd Lab09_Student
source /opt/ros/humble/setup.bash
echo $ROS_DISTRO
./scripts/check_lidar_state.sh
```

교육자가 별도의 workspace setup 명령을 제공하면 그 지시를 따르십시오.

## 중요

- 원인을 추측하지 말고 Evidence를 확인합니다.
- 설정/코드/드라이버/OS를 임의로 변경하지 않습니다.
- 해결되지 않으면 Evidence와 수행 조치를 정리하여 REPORT 합니다.
