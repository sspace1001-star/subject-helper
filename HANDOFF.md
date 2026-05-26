# HANDOFF.md

에이전트 간 업무 인수인계 로그.

## 2026-05-26 - 서울대 농경제 l7·참고 표시

상태: 완료
담당: Composer

목표:
- F·G열 `제2외국어/한문`이 핵심 l7로 잘못 표시되던 문제 수정

변경:
- scripts/update_from_excel.py: `제2외국어/…`는 core·rec 파싱 제외
- index.html: 한문(l7) 편제 추가, 참고 태그 flex gap, I열만 있을 때 안내 문구
- data/depts.json: 해당 행 core/rec 비움, ref m3·m5·m4·m6 유지

검증:
- seoul 농경제사회학부: core=[], ref=['m3','m5','m4','m6']

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

## 2026-05-26 - 배당표 업로드 2칸 (2026/2025)

상태: 완료
담당: Composer

목표:
- 교육과정 편제표를 배당표 엑셀 업로드로 갱신, 초기값은 기존 docs·HTML 유지

변경:
- app.py: POST /api/upload/curriculum/2026|2025, GET /api/data subjects
- index.html: 업로드 UI 2개, SUBJECTS_LIVE 서버 덮어쓰기
- data/depts.json: subjects 2026/2025 시드

검증:
- subjects 각 103칸, 배포 완료

## 2026-05-26 - 43학과·7계열 하드코딩 제거 (엑셀 전용)

상태: 완료
담당: Composer

목표:
- 에이전트가 만든 DEPT_DATA.series / MATCH_KEYWORDS 제거, 모든 선택·데이터를 univIndex(엑셀)만 사용

변경:
- index.html: DEPT_DATA·MATCH_KEYWORDS 블록 삭제, __global__ 전국 모집단위
- scripts/update_from_excel.py: build_global_index, depts.json은 univIndex만
- app.py, README, CLAUDE.md

검증:
- globalUnits=697, univIndex=45(전국+대학44)

## 2026-05-26 - 전체 대학 엑셀 모집단위 직접 표시 (univIndex)

상태: 완료
담당: Composer

목표:
- 43학과 매칭 없이 엑셀 행 전체를 대학별 단과대·모집단위로 표시

변경:
- scripts/update_from_excel.py: build_univ_index, data/depts.json.univIndex
- app.py, excel_to_depts.py, index.html UNIV_INDEX 연동
- D/E 없는 대학(가톨릭대·중앙대 등)은 모집단위만 1단계 선택

검증:
- 조선대 63개, 서울대 74개, 가톨릭대 33개(단과대 구분 없음)

## 2026-05-26 - 대학 선택 시 엑셀 단과대·모집단위 표시

상태: 완료
담당: Composer

목표:
- 조선대 등 D열 단과대(공과대학)를 계열 선택에 반영, E열 모집단위를 학과 선택에 표시

변경:
- scripts/update_from_excel.py: parse_unit_columns, sources.unitGroup
- index.html: 대학 선택 시 collectExcelGroups/Units, getDeptInfo 엑셀 모드
- data/depts.json 재생성

검증:
- 조선대 unitGroup 12개(공과대학 등), 기계공학과 → 공과대학

## 2026-05-26 - 계열·학과 드롭다운 동적 필터

상태: 완료
담당: Composer

목표:
- 데이터 있는 계열·학과만 목록에 표시, 대학 선택 시 해당 대학 데이터 있는 항목만

변경:
- 파일: index.html — deptHasVisibleData, collectSeriesOptions, collectDeptOptions, populateSeries/Depts

검증:
- 전체: 계열 7개 중 7, 학과 40 (국제관계·음악·무용 제외)
- 인하대: 계열 4, 학과 14

## 2026-05-26 - 대학 드롭다운 동적 생성

상태: 완료
담당: Composer

목표:
- 엑셀 sources에 있는 전체 대학(인하대 등)을 희망 진로 선택에 표시

변경:
- 파일: index.html — sel-univ 하드코딩 10개 제거, collectUnivOptions/populateUnivSelect 추가

검증:
- data/depts.json sources 기준 대학 43개 목록 생성

남은 작업:
- 없음

차단/주의:
- 대학 선택은 sources 매칭만 필터; 계열·학과 목록은 기존 43개 고정

## 2026-05-26 16:05 KST - 엑셀 전체 재파싱·배포

상태: 완료
담당: Composer

목표:
- 2028 엑셀 기준 초기 데이터 재생성 후 서버 반영

변경:
- 명령: scripts/update_from_excel.py → index.html DEPT_DATA/SUBJECTS 갱신
- 파일: data/depts.json, data/uploads/latest.xlsx 재생성
- 서버: deploy_oci.sh, subject-helper 재시작

검증:
- 명령: curl 서버 /api/data
- 결과: nonEmpty 40, source 2028 권장과목 xlsx

남은 작업:
- 없음

차단/주의:
- 편제표 xlsx에 없는 한문(l7)은 SUBJECTS에 수동 유지

## 2026-05-26 15:52 KST - 운영 주소 univref 로 변경

상태: 완료
담당: Composer

목표:
- 학생 안내 URL에 univref 이름 반영

변경:
- 서버: nginx 메인 vhost `univref.152-69-239-29.sslip.io` (HTTP → gunicorn)
- 서버: 구 주소(152.69.239.29, nip.io) → univref HTTP로 301
- 서버: HTTPS는 기존 `152.69.239.29.nip.io` 인증서만 유지
- 파일: README.md, scripts/deploy_oci.sh, scripts/nginx-subject-helper.conf

검증:
- 명령: curl http://univref.152-69-239-29.sslip.io/
- 결과: HTTP 200

남은 작업:
- univref 호스트 HTTPS (LE 한도 해제 후 certbot 또는 학교 도메인)

차단/주의:
- univref.duckdns.org 는 타 IP 사용 중
- nip.io/sslip.io 신규 LE 발급 주간 한도 초과 (2026-05-26)

## 2026-05-26 15:48 KST - nginx HTTPS (nip.io) 연동

상태: 완료
담당: Composer

목표:
- 포트 번호 없이 HTTPS로 학생 접속 가능하게 정리

변경:
- 서버: nginx 80/443 → gunicorn:5001 리버스 프록시
- 서버: Let's Encrypt 인증서 (152.69.239.29.nip.io), certbot 자동 갱신
- OCI 보안목록·iptables 80/443 개방
- 파일: README.md, scripts/deploy_oci.sh URL 갱신

검증:
- 명령: curl https://152.69.239.29.nip.io/ 및 /api/data
- 결과: HTTPS 200, API nonEmpty 40

남은 작업:
- 학교 전용 도메인(CNAME) 연결 시 certbot -d 로 인증서 교체

차단/주의:
- sslip.io 는 LE 발급 한도 초과로 nip.io 사용
- IP만으로는 HTTPS 인증서 이름 불일치 가능 → nip.io URL 안내

## 2026-05-26 15:42 KST - OCI vm-1-6 Flask 배포

상태: 완료
담당: Composer

목표:
- oracle-bot-vm-1-6에 subject-helper Flask 운영 배포

변경:
- 파일: requirements.txt — gunicorn 추가
- 파일: scripts/deploy_oci.sh — rsync + pip + systemctl 재시작
- 파일: README.md — 운영 URL·재배포 명령
- 서버: 152.69.239.29 예약 IP, OCI 보안목록·iptables 5001 개방
- 서버: ~/subject-helper, .venv, nodejs, systemd subject-helper

검증:
- 명령: curl http://152.69.239.29:5001/ 및 /api/data
- 결과: HTTP 200, nonEmpty 40

남은 작업:
- HTTPS(443) 또는 도메인 연결 선택

차단/주의:
- 접속 URL에 포트 :5001 필요

## 2026-05-26 15:28 KST - Flask 공용 저장 업로드 서버 추가

상태: 완료
담당: Codex

목표:
- 선생님이 엑셀 업로드하면 같은 반 학생들이 같은 데이터를 보도록 서버 저장 구조 추가

변경:
- 파일: app.py
  - Flask 앱 추가
  - `GET /api/data`: 저장 데이터 조회
  - `POST /api/upload`: 엑셀 저장 후 파싱 결과를 `data/depts.json`에 저장
  - `/`: index.html 제공
- 파일: scripts/excel_to_depts.py
  - 업로드 엑셀 파일을 DEPT_DATA.depts 구조로 변환
- 파일: scripts/update_from_excel.py
  - 외부 엑셀 경로를 받아 학과 매핑 생성 가능하도록 수정
- 파일: index.html
  - 업로드를 브라우저 메모리 처리 대신 `/api/upload` 서버 저장으로 변경
  - 페이지 시작 시 `/api/data` 저장 데이터 자동 로드
- 파일: requirements.txt
  - Flask 추가
- 파일: .gitignore
  - data/ 제외
- 파일: README.md
  - 서버 업로드 운영 방식 문서화

검증:
- 명령: .venv/bin/python app.py
- 결과: http://127.0.0.1:5001 서버 실행
- 명령: curl -F file=@docs/2028...xlsx http://127.0.0.1:5001/api/upload
- 결과: 업로드 성공, source 저장, nonEmpty=40
- 명령: curl http://127.0.0.1:5001/api/data
- 결과: 저장 데이터 조회 성공, 경제 데이터 존재

남은 작업:
- 운영 서버 배포 환경 선택 필요

차단/주의:
- GitHub Pages만으로는 공용 저장 불가. Flask 앱을 Render/Railway/Fly.io/교내 서버 등 Python 서버에 배포해야 함

## 2026-05-26 15:18 KST - 브라우저 엑셀 업로드 파싱 UI 추가

상태: 완료
담당: Codex

목표:
- 선생님이 수정한 2028 권장과목 엑셀을 화면에서 업로드해 즉시 파싱하는 구조 추가

변경:
- 파일: index.html
  - SheetJS `xlsx@0.18.5` CDN 추가
  - 사이드바 `엑셀 데이터 업로드` 카드 추가
  - 업로드된 엑셀의 C/D/E/F/G/H/J 열과 병합 셀을 브라우저에서 파싱
  - 업로드 데이터로 `DEPT_DATA.depts` 런타임 교체
  - 대학 선택 필터/하이라이트/코멘트 표시가 업로드 데이터에 즉시 적용
  - 국민대 선택 옵션 추가
- 파일: README.md
  - 브라우저 업로드 운영 방식 문서화

검증:
- 명령: node script syntax compile
- 결과: script_ok 0, script_ok 1
- 명령: node DEPT_DATA 추출
- 결과: 43개 학과, 경제 sources=19
- 명령: .venv/bin/python scripts/audit_excel_mapping.py
- 결과: curriculum_subjects_2026=103, app_subjects_2026=103, curriculum_subjects_2025=103, app_subjects_2025=103, bad_ids=[], ref_count=290, comment_count=40

남은 작업:
- 없음

차단/주의:
- 업로드는 서버 저장 없음. 새로고침하면 배포 기본 데이터로 복귀
- 배포 기본 데이터 갱신은 로컬 스크립트 실행 후 커밋/푸시 필요

## 2026-05-26 15:13 KST - 코멘트 없음 표시 제거

상태: 완료
담당: Codex

목표:
- 코멘트/대학 매칭 데이터가 없으면 별도 안내 문구를 표시하지 않음

변경:
- 파일: index.html
  - "선택한 대학의 엑셀 매칭 데이터가 없습니다." 메시지 제거
  - comment가 있을 때만 코멘트 박스 표시

검증:
- 명령: node 문자열 확인
- 결과: message_removed, korea_econ_sources=0
- 명령: .venv/bin/python scripts/audit_excel_mapping.py
- 결과: curriculum_subjects_2026=103, app_subjects_2026=103, curriculum_subjects_2025=103, app_subjects_2025=103, bad_ids=[], ref_count=290, comment_count=40

남은 작업:
- 없음

차단/주의:
- 없음

## 2026-05-26 15:11 KST - 대학 선택 필터 적용

상태: 완료
담당: Codex

목표:
- 고려대 선택 시 국민대 등 다른 대학 코멘트가 표시되는 문제 수정

변경:
- 파일: scripts/update_from_excel.py
  - 학과별 `sources` 추가
  - source별 대학 key, 대학명, 모집단위, comment, core, rec, ref 저장
- 파일: index.html
  - `getDeptInfo()` 추가
  - 대학 선택값이 있으면 해당 대학 sources만 합산해 하이라이트/안내 표시
  - 선택 대학 매칭 데이터가 없으면 다른 대학 데이터 대신 "선택한 대학의 엑셀 매칭 데이터가 없습니다." 표시

검증:
- 명령: node 데이터 추출
- 결과: `경제` + `korea` sources=0, `경제` + `국민` sources=1
- 명령: .venv/bin/python scripts/audit_excel_mapping.py
- 결과: curriculum_subjects_2026=103, app_subjects_2026=103, curriculum_subjects_2025=103, app_subjects_2025=103, bad_ids=[], ref_count=290, comment_count=40

남은 작업:
- 없음

차단/주의:
- 고려대 경제는 현재 엑셀 매칭 source 없음

## 2026-05-26 15:04 KST - 2028 엑셀 J열 comment 초안 기록

상태: 완료
담당: Codex

목표:
- 레퍼런스 사이트처럼 학과 선택 시 코멘트가 나오도록 2028 엑셀 J열에 코멘트 초안 생성
- J열 코멘트를 앱 data comment로 사용

변경:
- 파일: docs/2028학년도 권역별 대학별 권장과목(반영과목).xlsx
  - J3: 앱 comment
  - J4: 코멘트 초안
  - J5~J1362: 대학/모집단위/F/G/H/I 기반 코멘트 초안 기록
- 파일: scripts/write_comments_to_excel.py
  - J열 코멘트 초안 생성 스크립트 추가
- 파일: scripts/update_from_excel.py
  - J열 comment 로드
  - 미적분Ⅱ 정규화 오류 수정
- 파일: scripts/audit_excel_mapping.py
  - comment_count 출력 추가
- 파일: index.html
  - comment 반영 재생성
- 파일: README.md
  - I/J열 보조 데이터 생성 방법 추가

검증:
- 명령: .venv/bin/python scripts/write_comments_to_excel.py
- 결과: written_rows=788
- 명령: .venv/bin/python scripts/update_from_excel.py
- 결과: subjects_2026=103, subjects_2025=103, depts=43
- 명령: .venv/bin/python scripts/audit_excel_mapping.py
- 결과: curriculum_subjects_2026=103, app_subjects_2026=103, curriculum_subjects_2025=103, app_subjects_2025=103, bad_ids=[], ref_count=290, comment_count=39
- 명령: openpyxl read_only J열 샘플 확인
- 결과: J3=앱 comment, J4=코멘트 초안, J25 값 확인

남은 작업:
- 없음

차단/주의:
- J열 코멘트는 자동 생성 초안임. 선생님 검수/수정 필요

## 2026-05-26 14:56 KST - 2028 엑셀 I열 ref 기록

상태: 완료
담당: Codex

목표:
- docs/2028학년도 권역별 대학별 권장과목 엑셀 I열에 현재 앱 ref 참고과목 기록

변경:
- 파일: docs/2028학년도 권역별 대학별 권장과목(반영과목).xlsx
  - I3: 앱 ref
  - I4: 참고과목
  - I5~I1362: 현재 index.html DEPT_DATA.ref 과목명을 모집단위 매칭 행에 기록
- 파일: scripts/write_ref_to_excel.py
  - 현재 앱 ref를 과목명으로 변환해 엑셀 I열에 쓰는 스크립트 추가

검증:
- 명령: .venv/bin/python scripts/write_ref_to_excel.py
- 결과: written_rows=637
- 명령: XML 직접 확인
- 결과: I열 비어있지 않은 셀 639개(I3/I4 포함)
- 명령: openpyxl read_only 로딩 확인
- 결과: I3=앱 ref, I4=참고과목, I19 값 확인
- 명령: .venv/bin/python scripts/audit_excel_mapping.py
- 결과: curriculum_subjects_2026=103, app_subjects_2026=103, curriculum_subjects_2025=103, app_subjects_2025=103, bad_ids=[], ref_count=273, comment_nonempty=[]

남은 작업:
- 없음

차단/주의:
- docs/는 .gitignore 대상이라 배포 커밋에는 포함되지 않음

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
