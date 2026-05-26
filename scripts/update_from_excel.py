from __future__ import annotations

import json
import re
import subprocess
from collections import OrderedDict
from pathlib import Path

import openpyxl
from openpyxl.utils.cell import range_boundaries
from zipfile import ZipFile
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
DOCS = ROOT / "docs"

AREA_KEY = {
    "국 어": "korean",
    "수 학": "math",
    "영 어": "english",
    "사 회": "society",
    "과 학": "science",
    "체 육": "pe",
    "예 술": "arts",
    "기술": "tech",
    "제2외국어": "second",
    "교 양": "career",
}

PREFIX = {
    "korean": "k",
    "math": "m",
    "english": "e",
    "history": "h",
    "society": "s",
    "science": "sc",
    "pe": "p",
    "arts": "a",
    "tech": "t",
    "second": "l",
    "career": "c",
}

TYPE_MAP = {"공통": "il", "일반": "il", "진로": "jin", "융합": "fus"}

FIXED_IDS = {
    "공통국어1": "k1",
    "공통국어2": "k2",
    "문학": "k3",
    "화법과 언어": "k4",
    "매체 의사소통": "k5",
    "독서 토론과 글쓰기": "k6",
    "독서와 작문": "k7",
    "언어생활 탐구": "k8",
    "주제 탐구 독서": "k9",
    "문학과 영상": "k10",
    "공통수학1": "m1",
    "공통수학2": "m2",
    "대수": "m3",
    "확률과 통계": "m4",
    "미적분Ⅰ": "m5",
    "기하": "m6",
    "미적분Ⅱ": "m7",
    "인공지능 수학": "m8",
    "경제 수학": "m9",
    "수학과제 탐구": "m10",
    "수학과 문화": "m11",
    "실용 통계": "m12",
    "고급 대수": "m13",
    "공통영어1": "e1",
    "공통영어2": "e2",
    "영어Ⅰ": "e3",
    "영어Ⅱ": "e4",
    "영어 독해와 작문": "e5",
    "영미 문학 읽기": "e6",
    "영어 발표와 토론": "e7",
    "심화 영어 독해와 작문": "e8",
    "한국사1": "h1",
    "한국사2": "h2",
    "통합사회1": "s1",
    "통합사회2": "s2",
    "현대사회와 윤리": "s3",
    "세계시민과 지리": "s4",
    "사회와 문화": "s5",
    "세계사": "s6",
    "경제": "s7",
    "윤리와 사상": "s8",
    "도시의 미래 탐구": "s9",
    "한국지리 탐구": "s10",
    "인문학과 윤리": "s11",
    "사회문제 탐구": "s12",
    "역사로 탐구하는 현대 세계": "s13",
    "여행지리": "s14",
    "금융과 경제생활": "s15",
    "윤리문제 탐구": "s16",
    "통합과학1": "sc1",
    "통합과학2": "sc2",
    "과학탐구실험1": "sc3",
    "과학탐구실험2": "sc4",
    "물리학": "sc5",
    "화학": "sc6",
    "생명과학": "sc7",
    "지구과학": "sc8",
    "역학과 에너지": "sc9",
    "물질과 에너지": "sc10",
    "세포와 물질대사": "sc11",
    "행성우주과학": "sc12",
    "전자기와 양자": "sc13",
    "화학 반응의 세계": "sc14",
    "생물의 유전": "sc15",
    "지구시스템과학": "sc16",
    "기후변화와 환경생태": "sc17",
    "융합과학 탐구": "sc18",
    "고급 물리학": "sc19",
    "고급 화학": "sc20",
    "고급 생명과학": "sc21",
    "고급 지구과학": "sc22",
    "체육1": "p1",
    "체육2": "p2",
    "스포츠 문화": "p3",
    "스포츠 과학": "p4",
    "스포츠 생활1": "p5",
    "스포츠 생활2": "p6",
    "음악": "a1",
    "미술": "a2",
    "음악 연주와 창작": "a3",
    "미술 창작": "a4",
    "음악 감상과 비평": "a5",
    "미술과 매체": "a6",
    "정보": "t1",
    "인공지능 기초": "t2",
    "컴퓨터 시스템 일반": "t3",
    "데이터 과학": "t4",
    "소프트웨어와 생활": "t5",
    "정보과학": "t6",
    "일본어": "l1",
    "중국어": "l2",
    "일본어 회화": "l3",
    "중국어 회화": "l4",
    "일본 문화": "l5",
    "중국 문화": "l6",
    "진로와 직업": "c1",
    "논술": "c2",
}

COURSE_ALIASES = {
    "영어독해와 작문": ["영어 독해와 작문"],
    "생물과 유전": ["생물의 유전"],
    "확률": ["확률과 통계"],
    "미적분": ["미적분Ⅰ", "미적분Ⅱ"],
}

MATCH_KEYWORDS = {
    "국어국문": ["국어국문"],
    "사학": ["사학"],
    "철학": ["철학"],
    "심리": ["심리"],
    "교육": ["교육"],
    "사회": ["사회학"],
    "언론": ["언론"],
    "경제": ["경제"],
    "경영": ["경영"],
    "법학": ["법학"],
    "행정": ["행정"],
    "국제관계": ["국제관계"],
    "사회복지": ["사회복지"],
    "수학": ["수학"],
    "물리": ["물리"],
    "화학": ["화학"],
    "생명과학": ["생명과학"],
    "컴퓨터": ["컴퓨터"],
    "전기전자": ["전기전자", "전자전기"],
    "기계": ["기계"],
    "화공": ["화공", "화학공학"],
    "건축": ["건축"],
    "의예": ["의예", "의학"],
    "치의예": ["치의예", "치의학"],
    "한의예": ["한의예", "한의학"],
    "약학": ["약학"],
    "간호": ["간호"],
    "수의예": ["수의예", "수의학"],
    "국어교육": ["국어교육"],
    "수학교육": ["수학교육"],
    "영어교육": ["영어교육"],
    "과학교육": ["과학교육"],
    "사회교육": ["사회교육"],
    "체육교육": ["체육교육"],
    "미술": ["미술"],
    "음악": ["음악"],
    "체육": ["체육"],
    "디자인": ["디자인"],
    "무용": ["무용"],
    "농학": ["농학", "농업"],
    "식품영양": ["식품영양"],
    "산림": ["산림"],
    "환경생태": ["환경생태", "생태환경"],
}

GENERIC_TEXT = (
    "진로 및 적성",
    "전 과목",
    "교과목 선택",
)


def clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip())


def get_area(raw: str) -> str | None:
    for key, area in AREA_KEY.items():
        if key in raw:
            return area
    return None


def load_curriculum(year: str) -> OrderedDict[str, list[dict[str, object]]]:
    path = next(p for p in DOCS.glob("*.xlsx") if year in p.name)
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = next(wb[name] for name in wb.sheetnames if "입학생" in name)
    values = load_curriculum_values(ws)
    subjects: OrderedDict[str, list[dict[str, object]]] = OrderedDict(
        (key, []) for key in PREFIX
    )

    for row in range(7, 106):
        area = get_area(clean(values.get((row, 2))))
        name = clean(values.get((row, 4)))
        typ = clean(values.get((row, 3)))
        if not name or typ not in TYPE_MAP or not area:
            continue

        subject_area = "history" if name.startswith("한국사") else area
        for col in range(7, 13):
            if values.get((row, col)) is None:
                continue
            subjects[subject_area].append(
                {
                    "id": FIXED_IDS[name],
                    "name": name,
                    "type": TYPE_MAP[typ],
                    "grade": (col - 7) // 2 + 1,
                    "sem": (col - 7) % 2 + 1,
                }
            )

    return subjects


def load_curriculum_values(ws) -> dict[tuple[int, int], object]:
    values = {}
    for row in range(1, ws.max_row + 1):
        for col in (2, 3, 4, 7, 8, 9, 10, 11, 12):
            values[(row, col)] = ws.cell(row, col).value

    for merged_range in ws.merged_cells.ranges:
        min_col, min_row, max_col, max_row = range_boundaries(str(merged_range))
        if not set(range(min_col, max_col + 1)) & {2, 3, 4, 7, 8, 9, 10, 11, 12}:
            continue
        source = values.get((min_row, min_col))
        if source is None:
            continue
        for row in range(min_row, max_row + 1):
            for col in range(min_col, max_col + 1):
                if col in {2, 3, 4, 7, 8, 9, 10, 11, 12} and values.get((row, col)) is None:
                    values[(row, col)] = source
    return values


def js_value(value: object, indent: int = 2) -> str:
    sp = " " * indent
    if isinstance(value, dict):
        parts = []
        for key, val in value.items():
            parts.append(f"{sp}{key}: {js_value(val, indent + 2)}")
        return "{\n" + ",\n".join(parts) + "\n" + " " * (indent - 2) + "}"
    if isinstance(value, list):
        if not value:
            return "[]"
        if isinstance(value[0], dict):
            lines = []
            for item in value:
                fields = ", ".join(
                    [
                        f"id:'{item['id']}'",
                        f"name:'{item['name']}'",
                        f"type:'{item['type']}'",
                        f"grade:{item['grade']}",
                        f"sem:{item['sem']}",
                    ]
                )
                lines.append(f"{sp}{{ {fields} }}")
            return "[\n" + ",\n".join(lines) + "\n" + " " * (indent - 2) + "]"
        return "[" + ",".join(f"'{item}'" for item in value) + "]"
    return json.dumps(value, ensure_ascii=False)


def load_depts() -> dict[str, dict[str, object]]:
    script = """
const fs=require('fs');
const html=fs.readFileSync('index.html','utf8');
const data=html.match(/const DEPT_DATA = ([\\s\\S]*?);\\n\\n\\/\\* =========================================================\\n   상태/)[1];
console.log(JSON.stringify(Function('return '+data)().depts));
"""
    return json.loads(subprocess.check_output(["node", "-e", script], cwd=ROOT, text=True))


def normalize_course_text(text: object) -> list[str]:
    raw = clean(text)
    if not raw or raw == "-" or any(marker in raw for marker in GENERIC_TEXT):
        return []
    raw = raw.replace("Ⅰ", "I").replace("Ⅱ", "II")
    raw = raw.replace("미적분II", "미적분Ⅱ").replace("미적분I", "미적분Ⅰ")
    raw = re.sub(r"[\[\]\(\)]", ",", raw)
    raw = re.sub(r"또는|및|/|·|\\n|-일반선택:|-진로선택:", ",", raw)
    tokens = []
    for token in raw.split(","):
        token = clean(token).strip(": ")
        if not token or token in {"국어", "영어", "수학", "사회", "과학", "기술", "가정", "제2외국어", "한문"}:
            continue
        tokens.extend(COURSE_ALIASES.get(token, [token]))
    return tokens


def matches(unit: str, dept: str) -> bool:
    keywords = MATCH_KEYWORDS[dept]
    return any(keyword in unit for keyword in keywords)


def ordered_unique(values: list[str]) -> list[str]:
    return list(OrderedDict((value, None) for value in values))


def load_dept_mapping(course_to_id: dict[str, str], depts: dict[str, dict[str, object]]) -> dict[str, dict[str, object]]:
    path = next(p for p in DOCS.glob("*.xlsx") if "2028" in p.name)
    rows = load_recommendation_rows(path)
    result = {}

    for dept, info in depts.items():
        core_ids: list[str] = []
        rec_ids: list[str] = []
        ref_ids: list[str] = []
        comments: list[str] = []
        for row in rows:
            unit = clean(row["unit"])
            if not matches(unit, dept):
                continue
            for token in normalize_course_text(row["core"]):
                core_ids.extend(token_to_ids(token, course_to_id))
            target = core_ids if row["rec_merged"] else rec_ids
            for token in normalize_course_text(row["rec"]):
                target.extend(token_to_ids(token, course_to_id))
            for token in normalize_course_text(row["ref"]):
                ref_ids.extend(token_to_ids(token, course_to_id))
            comment = clean(row["comment"])
            if comment:
                comments.append(comment)
        core = ordered_unique(core_ids)
        rec = [item for item in ordered_unique(rec_ids) if item not in set(core)]
        ref = ordered_unique(ref_ids)
        result[dept] = {
            "comment": " ".join(ordered_unique(comments)[:2]),
            "core": core,
            "rec": rec,
            "ref": ref,
        }
    return result


def token_to_ids(token: str, course_to_id: dict[str, str]) -> list[str]:
    subject_id = course_to_id.get(token)
    if subject_id:
        return [subject_id]
    matched = []
    for course_name, course_id in course_to_id.items():
        if course_name in token:
            matched.append(course_id)
    return matched


def load_recommendation_rows(path: Path) -> list[dict[str, object]]:
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb["Sheet1"]
    values = {}
    merged_recommendation_cells = set()
    for row_num, row in enumerate(ws.iter_rows(min_row=5, values_only=True), 5):
        for col in (3, 4, 5, 6, 7, 8, 10):
            values[(row_num, col)] = row[col - 1] if len(row) >= col else None

    merge_ranges = read_sheet1_merge_ranges(path)
    for ref in merge_ranges:
        min_col, min_row, max_col, max_row = range_boundaries(ref)
        if not set(range(min_col, max_col + 1)) & {3, 4, 5, 6, 7, 8, 10}:
            continue
        source = values.get((min_row, min_col))
        if source is None:
            continue
        for row_num in range(max(min_row, 5), max_row + 1):
            for col in range(min_col, max_col + 1):
                if col in {6, 7}:
                    merged_recommendation_cells.add((row_num, col))
                if col in {3, 4, 5, 6, 7, 8, 10} and values.get((row_num, col)) is None:
                    values[(row_num, col)] = source

    rows = []
    for row_num in range(5, ws.max_row + 1):
        unit_detail = clean(values.get((row_num, 5)))
        rows.append(
            {
                "university": values.get((row_num, 3)),
                "unit": unit_detail or values.get((row_num, 4)),
                "core": values.get((row_num, 6)),
                "rec": values.get((row_num, 7)),
                "ref": values.get((row_num, 8)),
                "comment": values.get((row_num, 10)),
                "core_merged": (row_num, 6) in merged_recommendation_cells,
                "rec_merged": (row_num, 7) in merged_recommendation_cells,
            }
        )
    return rows


def read_sheet1_merge_ranges(path: Path) -> list[str]:
    ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    with ZipFile(path) as archive:
        root = ET.fromstring(archive.read("xl/worksheets/sheet1.xml"))
    return [node.attrib["ref"] for node in root.findall(".//m:mergeCell", ns)]


def format_subjects(name: str, subjects: OrderedDict[str, list[dict[str, object]]]) -> str:
    lines = [f"const {name} = {{"]
    for area, items in subjects.items():
        lines.append(f"  {area}: [")
        for item in items:
            lines.append(
                "    { "
                f"id:'{item['id']}', name:'{item['name']}', type:'{item['type']}', "
                f"grade:{item['grade']}, sem:{item['sem']} "
                "},"
            )
        lines.append("  ],")
    lines.append("};")
    return "\n".join(lines)


def format_depts(depts: dict[str, dict[str, object]]) -> str:
    lines = ["  depts: {"]
    for dept, info in depts.items():
        lines.append(
            f"    '{dept}': {{ comment:{json.dumps(info['comment'], ensure_ascii=False)}, "
            f"core:{js_value(info['core'])}, rec:{js_value(info['rec'])}, ref:{js_value(info['ref'])} }},"
        )
    lines.append("  },")
    return "\n".join(lines)


def main() -> None:
    html = INDEX.read_text(encoding="utf-8")
    subjects_2026 = load_curriculum("2026")
    subjects_2025 = load_curriculum("2025")
    flat_subjects = [item for values in subjects_2026.values() for item in values]
    course_to_id = OrderedDict()
    for item in flat_subjects + [item for values in subjects_2025.values() for item in values]:
        course_to_id.setdefault(item["name"], item["id"])
    depts = load_depts()
    mapped_depts = load_dept_mapping(course_to_id, depts)

    html = re.sub(
        r"const SUBJECTS_2026 = \{[\s\S]*?const SUBJECTS_2025 = [\s\S]*?\n\n/\* =========================================================\n   학과별 권장교과 데이터",
        format_subjects("SUBJECTS_2026", subjects_2026)
        + "\n\n/* 2025 입학생 — 2025학년도 입학생 편제 */\n"
        + format_subjects("SUBJECTS_2025", subjects_2025)
        + "\n\n/* =========================================================\n   학과별 권장교과 데이터",
        html,
    )
    html = re.sub(
        r"  depts: \{[\s\S]*?\n  \},\n\};",
        format_depts(mapped_depts) + "\n};",
        html,
    )
    html = html.replace(
        'id="cell-${s.id}" data-id="${s.id}"',
        'data-id="${s.id}"',
    )
    html = html.replace(
        "const el = document.getElementById('cell-'+id);\n    if (el) el.classList.add('hl-core');",
        "document.querySelectorAll(`[data-id=\"${id}\"]`).forEach(el => el.classList.add('hl-core'));",
    )
    html = html.replace(
        "const el = document.getElementById('cell-'+id);\n    if (el) { el.classList.remove('hl-core'); el.classList.add('hl-rec'); }",
        "document.querySelectorAll(`[data-id=\"${id}\"]`).forEach(el => { el.classList.remove('hl-core'); el.classList.add('hl-rec'); });",
    )
    html = html.replace(
        "const el = document.getElementById('cell-'+id);\n    if (el && !el.classList.contains('hl-core') && !el.classList.contains('hl-rec')) {\n      el.classList.add('hl-ref');\n    }",
        "document.querySelectorAll(`[data-id=\"${id}\"]`).forEach(el => {\n      if (!el.classList.contains('hl-core') && !el.classList.contains('hl-rec')) el.classList.add('hl-ref');\n    });",
    )
    INDEX.write_text(html, encoding="utf-8")

    print(f"subjects_2026={len(flat_subjects)}")
    print(f"subjects_2025={sum(len(values) for values in subjects_2025.values())}")
    print(f"depts={len(mapped_depts)}")
    print("empty=" + ",".join(k for k, v in mapped_depts.items() if not v["core"] and not v["rec"]))


if __name__ == "__main__":
    main()
