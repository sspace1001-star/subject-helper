from __future__ import annotations

from pathlib import Path

from scripts.update_from_excel import (
    DOCS,
    build_course_to_id,
    build_global_index,
    build_univ_index,
    load_recommendation_rows,
)

GLOBAL_KEY = "__global__"


def build_depts_from_excel(path: Path | None = None) -> dict:
    source = path or next(item for item in DOCS.glob("*.xlsx") if "2028" in item.name)
    rows = load_recommendation_rows(source)
    course_to_id = build_course_to_id()
    univ_index = build_univ_index(rows, course_to_id)
    univ_index[GLOBAL_KEY] = build_global_index(rows, course_to_id)
    return univ_index
