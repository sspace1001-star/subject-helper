from __future__ import annotations

from pathlib import Path

from scripts.update_from_excel import curriculum_to_dict, load_curriculum_from_path


def build_curriculum_from_excel(path: Path) -> dict[str, list[dict[str, object]]]:
    return curriculum_to_dict(load_curriculum_from_path(path))
