from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

from scripts.excel_to_depts import build_depts_from_excel


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
DATA_FILE = DATA_DIR / "depts.json"

app = Flask(__name__, static_folder=None)


def non_empty_count(depts: dict) -> int:
    return sum(
        1
        for info in depts.values()
        if info.get("core") or info.get("rec") or info.get("ref") or info.get("comment")
    )


def save_data(depts: dict, source_name: str) -> dict:
    DATA_DIR.mkdir(exist_ok=True)
    payload = {
        "updatedAt": datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S %Z"),
        "source": source_name,
        "nonEmpty": non_empty_count(depts),
        "depts": depts,
    }
    DATA_FILE.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return payload


@app.get("/")
def index():
    return send_from_directory(ROOT, "index.html")


@app.get("/api/data")
def data():
    if not DATA_FILE.exists():
        return jsonify({"depts": None})
    return jsonify(json.loads(DATA_FILE.read_text(encoding="utf-8")))


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
        depts = build_depts_from_excel(target)
        payload = save_data(depts, file.filename)
        return jsonify(payload)
    except Exception as exc:
        bad = UPLOAD_DIR / f"failed-{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
        shutil.move(target, bad)
        return jsonify({"error": str(exc)}), 400


@app.get("/<path:path>")
def static_files(path: str):
    return send_from_directory(ROOT, path)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
