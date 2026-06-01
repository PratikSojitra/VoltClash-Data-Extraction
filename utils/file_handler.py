import json
from pathlib import Path

DATA_FILE = Path("data/defenses.json")
CHANGES_FILE = Path("data/changes.json")


def load_json(file_path):
    if not file_path.exists():
        return {}

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    if not content.strip():
        return {}

    try:
        return json.loads(content)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {file_path}: {exc}") from exc


def save_json(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)