# HANDOFF.md

에이전트 간 업무 인수인계 로그.

## 작성 규칙
- 새 항목은 항상 `## YYYY-MM-DD HH:mm KST - 작업명` 형식으로 문서 최상단에 추가한다.
- 세션 시작 시 최신 항목 2개만 먼저 읽는다.
- 완료/진행/차단 상태를 사실만 기록한다.
- 추측, 잡담, 장문 배경 설명은 쓰지 않는다.

## 항목 양식
```md
## YYYY-MM-DD HH:mm KST - 작업명

상태: 완료 | 진행중 | 차단
담당: 에이전트명 또는 세션 식별자

목표:
- 

변경:
- 파일: 내용

검증:
- 명령:
- 결과:

남은 작업:
- 

차단/주의:
- 
```

## 2026-05-26 14:37 KST - 편제표 과목명 열 기준 명시

상태: 완료
담당: Codex

목표:
- 편제표 B열/D열 역할 명확화

변경:
- 파일: README.md
  - B열은 교과군 참고용, D열은 실제 과목명이라고 명시
- 파일: HANDOFF.md
  - 동일 기준 기록

검증:
- 명령: sed -n '219,275p' scripts/update_from_excel.py
- 결과: B열은 area, D열은 name으로 사용 확인
- 명령: .venv/bin/python scripts/audit_excel_mapping.py
- 결과: curriculum_subjects_2026=103, app_subjects_2026=103, curriculum_subjects_2025=103, app_subjects_2025=103, bad_ids=[], ref_count=273, comment_nonempty=[]

남은 작업:
- 없음

차단/주의:
- 없음

## 2026-05-26 14:36 KST - 편제표 학점 셀 기준 파싱

상태: 완료
담당: Codex

목표:
- 1/2학년 이수 과목은 학점/선택학점 값이 들어간 학기 칸만 개설 과목으로 반영
- 2026/2025 편제표를 각각 해당 엑셀 원본에서 생성

변경:
- 파일: scripts/update_from_excel.py
  - 편제표 G~L 학기 칸 병합 학점 셀 전파
  - 학점/선택학점 값이 있는 학기 칸만 SUBJECTS에 추가
  - SUBJECTS_2026은 2026학년도 1학년 엑셀에서 생성
  - SUBJECTS_2025는 2025학년도 2학년 엑셀에서 생성
- 파일: scripts/audit_excel_mapping.py
  - 2026/2025 편제표를 각각 검증
- 파일: index.html
  - SUBJECTS_2026 103개, SUBJECTS_2025 103개로 재생성
- 파일: README.md
  - 편제표 파싱 기준 갱신

검증:
- 명령: .venv/bin/python scripts/update_from_excel.py
- 결과: subjects_2026=103, subjects_2025=103, depts=43
- 명령: .venv/bin/python scripts/audit_excel_mapping.py
- 결과: curriculum_subjects_2026=103, app_subjects_2026=103, curriculum_subjects_2025=103, app_subjects_2025=103, bad_ids=[], ref_count=273, comment_nonempty=[]

남은 작업:
- 없음

차단/주의:
- 없음

## 2026-05-26 14:32 KST - H열 ref 반영

상태: 완료
담당: Codex

목표:
- 권장과목 엑셀 H열 비고를 참고(ref)로 반영

변경:
- 파일: scripts/update_from_excel.py
  - H열 값 로드 및 병합값 전파
  - H열 문장 안 과목명 포함 매칭을 ref로 반영
  - ref 출력 누락 버그 수정
- 파일: scripts/audit_excel_mapping.py
  - ref 비어 있음 검증 제거
  - ref_count 출력 추가
- 파일: index.html
  - 재생성 반영
- 파일: README.md
  - H열 ref 기준 문서화

검증:
- 명령: .venv/bin/python scripts/update_from_excel.py
- 결과: subjects=99, depts=43, empty=언론,국제관계,미술,음악,무용
- 명령: .venv/bin/python scripts/audit_excel_mapping.py
- 결과: curriculum_subjects=99, app_subjects=99, bad_ids=[], ref_count=273, comment_nonempty=[]

남은 작업:
- 없음

차단/주의:
- 없음

## 2026-05-26 14:30 KST - 모집단위 D/E 구조 반영

상태: 완료
담당: Codex

목표:
- 모집단위 D/E 열을 E 학과명 기준으로 해석

변경:
- 파일: scripts/update_from_excel.py
  - D/E 병합 행은 병합값을 E 학과명으로 전파해 사용
  - D/E 분리 행은 E값을 실제 학과/단과대 모집단위로 사용
  - C/D/E/F/G 병합 셀 값 전파
- 파일: index.html
  - 재생성 반영
- 파일: README.md
  - D/E 모집단위 해석 기준 추가
  - core/rec 빈 학과 목록 갱신

검증:
- 명령: .venv/bin/python scripts/update_from_excel.py
- 결과: subjects=99, depts=43, empty=언론,국제관계,미술,음악,무용
- 명령: .venv/bin/python scripts/audit_excel_mapping.py
- 결과: curriculum_subjects=99, app_subjects=99, bad_ids=[], ref_nonempty=[], comment_nonempty=[]

남은 작업:
- 없음

차단/주의:
- 없음

## 2026-05-26 14:28 KST - 수학 괄호 세부 과목 매핑

상태: 완료
담당: Codex

목표:
- `수학(확률, 미적분)` 같은 표현에서 괄호 안 과목을 개별 과목으로 매핑

변경:
- 파일: scripts/update_from_excel.py
  - `확률` → `확률과 통계`
  - `미적분` → `미적분Ⅰ`, `미적분Ⅱ`
  - 별칭 하나가 여러 과목 ID로 확장되도록 처리
- 파일: index.html
  - 엑셀 재생성 반영
- 파일: README.md
  - 괄호 안 수학 세부 과목 매핑 기준 추가

검증:
- 명령: .venv/bin/python scripts/update_from_excel.py
- 결과: subjects=99, depts=43
- 명령: .venv/bin/python scripts/audit_excel_mapping.py
- 결과: curriculum_subjects=99, app_subjects=99, bad_ids=[], ref_nonempty=[], comment_nonempty=[]

남은 작업:
- 없음

차단/주의:
- 없음

## 2026-05-26 14:26 KST - 병합 권장과목 core 처리

상태: 완료
담당: Codex

목표:
- F/G 권장과목 영역 병합 셀 값을 모두 core로 반영

변경:
- 파일: scripts/update_from_excel.py
  - F/G 병합 셀 메타 추적
  - 병합된 G열 값도 rec가 아니라 core에 추가
- 파일: README.md
  - 병합 권장과목은 모두 core 처리한다고 문서화
- 파일: index.html
  - 재생성 반영

검증:
- 명령: .venv/bin/python scripts/update_from_excel.py
- 결과: subjects=99, depts=43
- 명령: .venv/bin/python scripts/audit_excel_mapping.py
- 결과: curriculum_subjects=99, app_subjects=99, bad_ids=[], ref_nonempty=[], comment_nonempty=[]

남은 작업:
- 없음

차단/주의:
- 없음

## 2026-05-26 14:25 KST - 권장과목 병합 셀 처리 보정

상태: 완료
담당: Codex

목표:
- 권장과목 엑셀 F/G/D/C 병합 셀 누락 방지

변경:
- 파일: scripts/update_from_excel.py
  - Sheet1 XML mergeCell 범위 직접 파싱
  - C/D/F/G 병합 범위 하위 셀에 좌상단 값 전파
  - F:G 가로 병합은 좌상단 F열 값으로 core 처리
- 파일: README.md
  - 병합 셀 처리 기준 문서화

검증:
- 명령: .venv/bin/python scripts/update_from_excel.py
- 결과: subjects=99, depts=43
- 명령: .venv/bin/python scripts/audit_excel_mapping.py
- 결과: curriculum_subjects=99, app_subjects=99, bad_ids=[], ref_nonempty=[], comment_nonempty=[]

남은 작업:
- 없음

차단/주의:
- openpyxl 일반 모드는 원본 스타일 오류로 실패하여 read_only + XML mergeCell 파싱 사용

## 2026-05-26 14:21 KST - 엑셀 기준 데이터 정정

상태: 완료
담당: Codex

목표:
- 입시 데이터에서 비엑셀 기반 core/rec/ref/comment 제거
- 편제표와 권장과목을 엑셀 기준으로 재생성

변경:
- 파일: index.html
  - SUBJECTS_2026 99개를 2026 편제표 기준으로 재생성
  - SUBJECTS_2025는 SUBJECTS_2026 복제 유지
  - DEPT_DATA core/rec를 권장과목 엑셀 F/G열 직접 매핑으로 재생성
  - ref/comment 전부 빈 값
  - 같은 과목 ID가 여러 학기 칸에 있을 때 모두 하이라이트되도록 data-id 기반 처리
- 파일: scripts/update_from_excel.py
  - 엑셀 원본 기반 재생성 스크립트 추가
- 파일: scripts/audit_excel_mapping.py
  - 편제표 수, bad id, ref/comment 비움 검증 추가
- 파일: README.md
  - 실제 매핑 기준으로 수정
- 파일: requirements.txt
  - openpyxl 의존성 기록

검증:
- 명령: .venv/bin/python scripts/update_from_excel.py
- 결과: subjects=99, depts=43
- 명령: .venv/bin/python scripts/audit_excel_mapping.py
- 결과: curriculum_subjects=99, app_subjects=99, bad_ids=[], ref_nonempty=[], comment_nonempty=[]

남은 작업:
- 없음

차단/주의:
- core/rec 빈 학과: 국어국문, 사학, 철학, 심리, 사회, 언론, 행정, 국제관계, 사회복지, 수의예, 국어교육, 수학교육, 영어교육, 과학교육, 사회교육, 체육교육, 미술, 음악, 무용
- 빈 이유: 매칭 행 없음 또는 F/G열이 일반 문구·교과군이라 특정 과목 ID로 변환하지 않음

## 2026-05-26 14:14 KST - 엑셀 데이터 반영 오딧

상태: 완료
담당: Codex

목표:
- README/HANDOFF 기준과 엑셀 원본, index.html 데이터 대조

변경:
- 파일: requirements.txt
  - openpyxl 의존성 추가
- 파일: .venv
  - requirements.txt 설치

검증:
- 명령: .venv/bin/python 엑셀 파싱
- 결과: 권장과목 엑셀 Sheet1 1362행, C/D/F/G 구조 확인
- 명령: node index.html 데이터 추출
- 결과: SUBJECTS_2026 91개, DEPT_DATA.depts 43개 확인

남은 작업:
- SUBJECTS_2026 누락 과목 반영 여부 결정
- DEPT_DATA 매핑 재생성 스크립트 보존 및 재검증
- README/HANDOFF의 부정확한 설명 수정

차단/주의:
- 현재 데이터는 엑셀 정확 반영으로 보기 어려움
- docs 폴더에 HANDOFF가 언급한 Python 파싱 스크립트 없음

## 2026-05-26 17:30 KST - 엑셀 기반 권장과목 매핑 및 문서화

상태: 완료
담당: Claude Sonnet 4.6

목표:
- core/rec 데이터를 임의 생성에서 엑셀 실제 데이터 기반으로 전면 교체
- 매핑 방법 문서화

변경:
- index.html: DEPT_DATA.depts 전 학과 core/rec 교체 (엑셀 파싱 기반), ref 전부 []
- README.md: 엑셀 매핑 방법·데이터 구조 전면 재작성

검증:
- 명령: git log --oneline -3
- 결과: f4f23ce docs: README 매핑 설명, c5977b5 feat: 엑셀 기반 권장과목 교체

남은 작업:
- ref 학과별 입력 (교사 직접, 엑셀 근거 없음)
- 엑셀 데이터 없는 학과 core/rec 입력: 심리, 언론, 수학교육, 과학교육, 사회교육, 체육교육, 음악, 무용

차단/주의:
- 오매칭 방지 처리: 화학과↔중국어문화학과, 의과대학↔수의과대학 (블랙리스트 적용)
- 엑셀 핵심과목/권장과목 열이 "진로 및 적성 고려 이수" 등 일반문구인 경우 제외 처리
- 파싱 스크립트: docs/ 폴더 내 Python 코드 (index.html에 미포함, 대화 내 실행)

## 2026-05-26 14:04 KST - 핸드오프 체계 생성

상태: 완료
담당: Codex

목표:
- 에이전트 간 업무 인수인계 파일 생성
- 세션 시작 시 최신 2개 항목만 읽도록 지침 추가

변경:
- 파일: HANDOFF.md
  - 인수인계 작성 규칙과 항목 양식 추가
- 파일: CLAUDE.md
  - 세션 시작 시 HANDOFF.md 최신 2개 항목 확인 규칙 추가

검증:
- 명령: sed -n '1,220p' HANDOFF.md
- 결과: 작성 규칙, 항목 양식, 최신 항목 확인
- 명령: sed -n '1,160p' CLAUDE.md
- 결과: 핸드오프 읽기/작성 규칙 확인

남은 작업:
- 없음

차단/주의:
- 없음
