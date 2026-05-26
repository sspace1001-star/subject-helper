# CLAUDE.md

## 프로젝트 개요
숭문고 2028 대입 과목선택 도우미. index.html 단일 파일. 담당교사: 김경선

## 데이터 구조
- SUBJECTS_2026 / SUBJECTS_2025: 편제표 과목 목록
- DEPT_DATA.series: 계열 → 학과 매핑
- DEPT_DATA.depts: 학과별 권장교과 (core/rec/ref)

## 작업 규칙
- 외부 라이브러리 추가 금지 (단일 파일 유지)
- 과목 ID는 기존 형식 유지 (k1, m3, sc5 등)
- 한국어 UI 유지
- 세션 시작 시 HANDOFF.md 최신 항목 2개만 먼저 읽고 업무 상태를 파악
- 작업 인수인계는 HANDOFF.md 최상단에 지정 양식으로 기록
