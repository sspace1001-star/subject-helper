from __future__ import annotations

import json
import subprocess
from pathlib import Path

import openpyxl
from update_from_excel import load_curriculum


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def load_app() -> tuple[dict, dict, dict]:
    script = """
const fs=require('fs');
const html=fs.readFileSync('index.html','utf8');
const subj2026=html.match(/const SUBJECTS_2026 = ([\\s\\S]*?);\\n\\n\\/\\* 2025/)[1];
const subj2025=html.match(/const SUBJECTS_2025 = ([\\s\\S]*?);\\n\\n\\/\\* =========================================================\\n   학과별 권장교과 데이터/)[1];
const data=html.match(/const DEPT_DATA = ([\\s\\S]*?);\\n\\n\\/\\* =========================================================\\n   상태/)[1];
console.log(JSON.stringify({subjects2026:Function('return '+subj2026)(), subjects2025:Function('return '+subj2025)(), deptData:Function('return '+data)()}));
"""
    data = json.loads(subprocess.check_output(["node", "-e", script], cwd=ROOT, text=True))
    return data["subjects2026"], data["subjects2025"], data["deptData"]


def curriculum_count(year: str) -> int:
    return sum(len(values) for values in load_curriculum(year).values())


def main() -> None:
    subjects_2026, subjects_2025, dept_data = load_app()
    app_subjects_2026 = [item for items in subjects_2026.values() for item in items]
    app_subjects_2025 = [item for items in subjects_2025.values() for item in items]
    app_ids = {item["id"] for item in app_subjects_2026 + app_subjects_2025}
    dept_items = dept_data["depts"].items()

    bad_ids = []
    bad_comment = []
    for dept, info in dept_items:
        for field in ("core", "rec", "ref"):
            for subject_id in info[field]:
                if subject_id not in app_ids:
                    bad_ids.append((dept, field, subject_id))
        if info["comment"]:
            bad_comment.append(dept)

    expected_2026 = curriculum_count("2026")
    expected_2025 = curriculum_count("2025")
    print(f"curriculum_subjects_2026={expected_2026}")
    print(f"app_subjects_2026={len(app_subjects_2026)}")
    print(f"curriculum_subjects_2025={expected_2025}")
    print(f"app_subjects_2025={len(app_subjects_2025)}")
    print(f"departments={len(dept_data['depts'])}")
    print(f"bad_ids={bad_ids}")
    print(f"ref_count={sum(len(info['ref']) for info in dept_data['depts'].values())}")
    print(f"comment_nonempty={bad_comment}")

    if (
        len(app_subjects_2026) != expected_2026
        or len(app_subjects_2025) != expected_2025
        or bad_ids
        or bad_comment
    ):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
