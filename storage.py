import os, json
from pathlib import Path

BASE = Path.home() / ".gatekeeper"

FILES = {
    "state": "state.json",
    "answers": "answers.json",
    "sessions": "sessions.json",
    "dsa": "questions_dsa.json",
    "sql": "questions_sql.json",
    "settings": "settings.json"   # NEW
}

DEFAULTS = {
    "state": {"locked": True, "streak": 0, "last_unlock_date": None},
    "answers": [],
    "sessions": [],
    "dsa": [],
    "sql": [],
    "settings": {                  # NEW
        "theme": "tokyo",
        "reading_minutes": 10,
        "journal_min_lines": 10,
        "strict_mode": True
    }
}

def init_storage():
    BASE.mkdir(exist_ok=True)
    for key, file in FILES.items():
        p = BASE / file
        if not p.exists():
            data = DEFAULTS[key]
            p.write_text(json.dumps(data, indent=2) if key!="answers" or key!="sessions" else "[]")
            if key in ("answers","sessions"):
                p.write_text("[]")
            else:
                p.write_text(json.dumps(DEFAULTS[key], indent=2))

def read(file_key):
    with open(BASE / FILES[file_key], "r", encoding="utf-8") as f:
        return json.load(f)

def write(file_key, data):
    with open(BASE / FILES[file_key], "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
