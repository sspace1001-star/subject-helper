from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
from xml.etree import ElementTree as ET

from update_from_excel import DOCS, ROOT, load_recommendation_rows, matches


NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
ET.register_namespace("", NS)


def load_app_data() -> tuple[dict[str, dict], dict[str, str]]:
    script = """
const fs=require('fs');
const html=fs.readFileSync('index.html','utf8');
const subj2026=html.match(/const SUBJECTS_2026 = ([\\s\\S]*?);\\n\\n\\/\\* 2025/)[1];
const subj2025=html.match(/const SUBJECTS_2025 = ([\\s\\S]*?);\\n\\n\\/\\* =========================================================\\n   학과별 권장교과 데이터/)[1];
const data=html.match(/const DEPT_DATA = ([\\s\\S]*?);\\n\\n\\/\\* =========================================================\\n   상태/)[1];
const subjects=[...Object.values(Function('return '+subj2026)()).flat(), ...Object.values(Function('return '+subj2025)()).flat()];
const names=Object.fromEntries(subjects.map(s=>[s.id,s.name]));
const deptData=Function('return '+data)();
console.log(JSON.stringify({depts:deptData.depts, names}));
"""
    data = json.loads(subprocess.check_output(["node", "-e", script], cwd=ROOT, text=True))
    return data["depts"], data["names"]


def ordered_unique(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))


def build_row_ref_values() -> dict[int, str]:
    workbook = next(path for path in DOCS.glob("*.xlsx") if "2028" in path.name)
    rows = load_recommendation_rows(workbook)
    depts, subject_names = load_app_data()
    values = {}

    for index, row in enumerate(rows, 5):
        unit = str(row["unit"] or "")
        refs = []
        for dept, info in depts.items():
            if not matches(unit, dept):
                continue
            refs.extend(subject_names[subject_id] for subject_id in info["ref"])
        names = ordered_unique(refs)
        if names:
            values[index] = ", ".join(names)

    return values


def cell_text(cell) -> str:
    inline = cell.find(f"{{{NS}}}is/{{{NS}}}t")
    if inline is not None and inline.text:
        return inline.text
    value = cell.find(f"{{{NS}}}v")
    return value.text if value is not None and value.text else ""


def set_inline_string(row, ref: str, value: str) -> None:
    for cell in list(row.findall(f"{{{NS}}}c")):
        if cell.attrib.get("r") == ref:
            row.remove(cell)
            break

    cell = ET.Element(f"{{{NS}}}c", {"r": ref, "t": "inlineStr"})
    inline = ET.SubElement(cell, f"{{{NS}}}is")
    text = ET.SubElement(inline, f"{{{NS}}}t")
    text.text = value

    cells = row.findall(f"{{{NS}}}c")
    insert_at = len(cells)
    for pos, existing in enumerate(cells):
        existing_ref = existing.attrib.get("r", "")
        existing_col = "".join(ch for ch in existing_ref if ch.isalpha())
        if existing_col > "I":
            insert_at = pos
            break
    row.insert(insert_at, cell)


def write_i_column(path: Path, row_values: dict[int, str]) -> None:
    with ZipFile(path) as source:
        sheet_xml = source.read("xl/worksheets/sheet1.xml")
        root = ET.fromstring(sheet_xml)
        sheet_data = root.find(f"{{{NS}}}sheetData")
        rows = {int(row.attrib["r"]): row for row in sheet_data.findall(f"{{{NS}}}row")}

        set_inline_string(rows[3], "I3", "앱 ref")
        set_inline_string(rows[4], "I4", "참고과목")

        for row_num, row in rows.items():
            for cell in list(row.findall(f"{{{NS}}}c")):
                if cell.attrib.get("r") == f"I{row_num}" and row_num >= 5:
                    row.remove(cell)

        for row_num, value in row_values.items():
            set_inline_string(rows[row_num], f"I{row_num}", value)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp:
            temp_path = Path(temp.name)
        with ZipFile(temp_path, "w", ZIP_DEFLATED) as target:
            for item in source.infolist():
                data = ET.tostring(root, encoding="utf-8", xml_declaration=True) if item.filename == "xl/worksheets/sheet1.xml" else source.read(item.filename)
                target.writestr(item, data)

    shutil.move(temp_path, path)


def main() -> None:
    path = next(path for path in DOCS.glob("*.xlsx") if "2028" in path.name)
    row_values = build_row_ref_values()
    write_i_column(path, row_values)
    print(f"written_rows={len(row_values)}")
    print(path)


if __name__ == "__main__":
    main()
