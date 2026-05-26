from __future__ import annotations

from pathlib import Path

from update_from_excel import (
    DOCS,
    load_curriculum,
    load_recommendation_rows,
    normalize_course_text,
    token_to_ids,
)
from write_ref_to_excel import set_inline_string, write_i_column


def clean(value: object) -> str:
    return " ".join(str(value or "").split())


def first_items(values: list[str], limit: int) -> list[str]:
    return list(dict.fromkeys(values))[:limit]


def build_course_maps() -> tuple[dict[str, str], dict[str, str]]:
    subjects = []
    for year in ("2026", "2025"):
        subjects.extend(item for values in load_curriculum(year).values() for item in values)
    course_to_id = {}
    id_to_name = {}
    for item in subjects:
        course_to_id.setdefault(item["name"], item["id"])
        id_to_name[item["id"]] = item["name"]
    return course_to_id, id_to_name


def mapped_names(value: object, course_to_id: dict[str, str], id_to_name: dict[str, str]) -> list[str]:
    names = []
    for token in normalize_course_text(value):
        names.extend(id_to_name[subject_id] for subject_id in token_to_ids(token, course_to_id))
    return first_items(names, 4)


def build_comment(row: dict[str, object], course_to_id: dict[str, str], id_to_name: dict[str, str]) -> str:
    university = clean(row["university"])
    unit = clean(row["unit"])
    core = mapped_names(row["core"], course_to_id, id_to_name)
    rec = [] if row["rec_merged"] else mapped_names(row["rec"], course_to_id, id_to_name)
    ref = mapped_names(row["ref"], course_to_id, id_to_name)

    parts = []
    if core:
        parts.append(f"핵심은 {', '.join(core)}입니다")
    if rec:
        parts.append(f"추가 권장은 {', '.join(rec)}입니다")
    if ref:
        parts.append(f"비고상 참고는 {', '.join(ref)}입니다")
    if not parts:
        return ""

    subject = f"{university} {unit}".strip()
    return f"{subject}: " + ". ".join(parts) + "."


def build_row_comment_values() -> dict[int, str]:
    workbook = next(path for path in DOCS.glob("*.xlsx") if "2028" in path.name)
    rows = load_recommendation_rows(workbook)
    course_to_id, id_to_name = build_course_maps()
    values = {}
    for index, row in enumerate(rows, 5):
        comment = build_comment(row, course_to_id, id_to_name)
        if comment:
            values[index] = comment
    return values


def main() -> None:
    path = next(path for path in DOCS.glob("*.xlsx") if "2028" in path.name)
    row_values = build_row_comment_values()
    write_j_column(path, row_values)
    print(f"written_rows={len(row_values)}")
    print(path)


def write_j_column(path: Path, row_values: dict[int, str]) -> None:
    import shutil
    import tempfile
    from zipfile import ZIP_DEFLATED, ZipFile
    from xml.etree import ElementTree as ET

    from write_ref_to_excel import NS

    with ZipFile(path) as source:
        root = ET.fromstring(source.read("xl/worksheets/sheet1.xml"))
        dimension = root.find(f"{{{NS}}}dimension")
        if dimension is not None:
            dimension.set("ref", "A1:J1362")
        sheet_data = root.find(f"{{{NS}}}sheetData")
        rows = {int(row.attrib["r"]): row for row in sheet_data.findall(f"{{{NS}}}row")}

        set_inline_string(rows[3], "J3", "앱 comment")
        set_inline_string(rows[4], "J4", "코멘트 초안")

        for row_num, row in rows.items():
            for cell in list(row.findall(f"{{{NS}}}c")):
                if cell.attrib.get("r") == f"J{row_num}" and row_num >= 5:
                    row.remove(cell)

        for row_num, value in row_values.items():
            set_inline_string(rows[row_num], f"J{row_num}", value)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp:
            temp_path = Path(temp.name)
        with ZipFile(temp_path, "w", ZIP_DEFLATED) as target:
            for item in source.infolist():
                data = ET.tostring(root, encoding="utf-8", xml_declaration=True) if item.filename == "xl/worksheets/sheet1.xml" else source.read(item.filename)
                target.writestr(item, data)

    shutil.move(temp_path, path)


if __name__ == "__main__":
    main()
