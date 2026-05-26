from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

from scripts.excel_to_curriculum import build_curriculum_from_excel
from scripts.excel_to_depts import GLOBAL_KEY, build_depts_from_excel
from scripts.update_from_excel import curriculum_to_dict, load_curriculum


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
CURRICULUM_DIR = DATA_DIR / "curriculum"
DATA_FILE = DATA_DIR / "depts.json"


app = Flask(__name__, static_folder=None)


def now_kst() -> str:
    return datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")


def read_payload() -> dict:
    if not DATA_FILE.exists():
        return {}
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def write_payload(payload: dict) -> dict:
    DATA_DIR.mkdir(exist_ok=True)
    DATA_FILE.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return payload


def subject_slot_count(subjects: dict | None) -> int:
    if not subjects:
        return 0
    return sum(len(items) for items in subjects.values())


def default_subjects() -> dict[str, dict]:
    return {
        "2026": curriculum_to_dict(load_curriculum("2026")),
        "2025": curriculum_to_dict(load_curriculum("2025")),
    }


def ensure_payload() -> dict:
    payload = read_payload()
    if payload.get("univIndex") and payload.get("subjects"):
        return payload

    subjects = payload.get("subjects") or default_subjects()
    if not payload.get("univIndex"):
        try:
            rec_path = next(
                p
                for p in [
                    UPLOAD_DIR / "latest.xlsx",
                    *sorted(ROOT.joinpath("docs").glob("*2028*.xlsx"), reverse=True),
                ]
                if p.exists() and not p.name.startswith("~$")
            )
            univ_index = build_depts_from_excel(rec_path)
            source = rec_path.name
        except StopIteration:
            univ_index = {}
            source = ""
        payload = {
            "updatedAt": now_kst(),
            "source": source,
            "unitCount": len(univ_index.get(GLOBAL_KEY, {}).get("groups", {}).get("", [])),
            "univIndex": univ_index,
            "subjects": subjects,
        }
    else:
        payload.setdefault("subjects", subjects)
    return write_payload(payload)


@app.get("/")
def index():
    return send_from_directory(ROOT, "index.html")


@app.get("/api/data")
def data():
    payload = ensure_payload()
    return jsonify(payload)


@app.post("/api/upload/curriculum/<year>")
def upload_curriculum(year: str):
    if year not in {"2026", "2025"}:
        return jsonify({"error": "year must be 2026 or 2025"}), 400
    file = request.files.get("file")
    if not file or not file.filename:
        return jsonify({"error": "file required"}), 400
    if not file.filename.lower().endswith((".xlsx", ".xls")):
        return jsonify({"error": "xlsx only"}), 400

    CURRICULUM_DIR.mkdir(parents=True, exist_ok=True)
    target = CURRICULUM_DIR / f"{year}.xlsx"
    file.save(target)

    try:
        subjects = build_curriculum_from_excel(target)
        payload = ensure_payload()
        payload.setdefault("subjects", {})
        payload["subjects"][year] = subjects
        payload["updatedAt"] = now_kst()
        payload[f"curriculum{year}At"] = payload["updatedAt"]
        write_payload(payload)
        return jsonify(
            {
                "year": year,
                "slotCount": subject_slot_count(subjects),
                "subjects": subjects,
                "updatedAt": payload["updatedAt"],
            }
        )
    except Exception as exc:
        failed = CURRICULUM_DIR / f"failed-{year}-{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
        if target.exists():
            shutil.move(target, failed)
        return jsonify({"error": str(exc)}), 400


@app.post("/api/upload")
def upload():
    file = request.files.get("file")
    if not file or not file.filename:
        return jsonify({"error": "file required"}), 400
    if not file.filename.lower().endswith((".xlsx", ".xls")):
        return jsonify({"error": "xlsx only"}), 400

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    target = UPLOAD_DIR / "latest.xlsx"
    file.save(target)

    try:
        univ_index = build_depts_from_excel(target)
        payload = ensure_payload()
        payload["source"] = file.filename
        payload["unitCount"] = len(univ_index.get(GLOBAL_KEY, {}).get("groups", {}).get("", []))
        payload["univIndex"] = univ_index
        payload["updatedAt"] = now_kst()
        write_payload(payload)
        return jsonify(payload)
    except Exception as exc:
        bad = UPLOAD_DIR / f"failed-{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
        if target.exists():
            shutil.move(target, bad)
        return jsonify({"error": str(exc)}), 400


@app.get("/<path:path>")
def static_files(path: str):
    return send_from_directory(ROOT, path)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
