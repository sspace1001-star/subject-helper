from __future__ import annotations

from pathlib import Path

from scripts.update_from_excel import (
    DOCS,
    build_course_to_id,
    load_dept_mapping,
    load_depts,
)


def build_depts_from_excel(path: Path | None = None) -> dict:
    source = path or next(item for item in DOCS.glob("*.xlsx") if "2028" in item.name)
    depts = load_depts()
    return load_dept_mapping(build_course_to_id(), depts, source)
