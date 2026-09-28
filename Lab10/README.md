# Lab10 — 사용자 피드백 기반 교육 개선 실습 패키지

## 목적

슬라이드 10~15의 시연 사례를 학생이 그대로 따라 하며 다음 흐름을 수행하도록 구성한 배포 패키지입니다.

> 피드백 수집 → 문제 유형 분류 → 원인 분석 → 개선안 결정 → 교육·매뉴얼 수정 → 개선 효과 재평가

이번 실습의 중심은 ROS 2 명령 자체가 아니라 **사용자 행동과 Evidence를 근거로 교육·매뉴얼 개선안을 작성하는 판단 과정**입니다.

## 슬라이드 ↔ 실습 매핑

| 슬라이드 | 실습 | 핵심 활동 | 산출물 |
|---|---|---|---|
| 10 | LAB10-1 | 6단계 개선 프로세스 확인 | 프로세스 체크시트 |
| 11 | LAB10-2 | 사용자 행동을 사실 중심으로 기록 | 행동 사실 기록표 |
| 12 | LAB10-3 | Evidence 확인·해석 | Evidence 분석표 |
| 13 | LAB10-4 | 문제 분류와 원인 가설 | 원인 가설표 |
| 14 | LAB10-5 | 교육·매뉴얼 개선안 설계 | 개선안 초안 |
| 15 | LAB10-6 | 동일 기준으로 재평가 | 효과 평가·최종 판단 |

## 배포 원칙

- `student/` : 학생에게 처음부터 배포해도 되는 자료
- `instructor/` : 강사용 정답, Evidence 원본, 순차 공개 자료, 운영 스크립트
- Evidence는 교육용 샘플입니다. 실제 장비 실습 시에는 강사가 `instructor/demo/capture_live_evidence.sh`를 이용해 환경에 맞는 자료로 교체할 수 있습니다.
- 실제 myAGV가 ROS 2 Galactic이고 교육 PC가 Humble인 분리 환경이라면 DDS 직접 연결을 전제로 하지 말고, 본 Evidence Pack 또는 기존 Gateway/브리지 실습 구조를 사용하십시오.

## 권장 사용 순서

1. 학생에게 `student/` 배포
2. `student/workbook/Lab10_workbook.md`의 LAB10-1~2 수행
3. 강사가 `instructor/evidence/`를 E01부터 순차 공개
4. LAB10-3~5 수행
5. 강사가 `instructor/release/evaluation_after.csv` 공개
6. LAB10-6 수행 및 `student/templates/improvement_plan_template.md`로 최종 제출
7. 강사가 `instructor/answer_key/instructor_answer_key.md`와 `instructor/operation/instructor_guide.md`로 평가

## 검증

```bash
python3 instructor/demo/verify_package.py
```

정상이라면 `PASS: Lab10 package validation`이 출력됩니다.
