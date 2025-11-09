
import json, os
from utils import expand, ensure_dir

DEFAULT_STATE = {
    "locked": True,
    "last_attempt": None,
    "streak": 0,
    "last_unlock_date": None
}

class Locker:
    def __init__(self, state_path: str):
        self.state_path = expand(state_path)
        os.makedirs(os.path.dirname(self.state_path), exist_ok=True)
        if not os.path.exists(self.state_path):
            self._write(DEFAULT_STATE.copy())

    def _read(self):
        with open(self.state_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write(self, state):
        with open(self.state_path, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)

    def is_locked(self) -> bool:
        return self._read().get("locked", True)

    def lock(self):
        s = self._read()
        s["locked"] = True
        self._write(s)

    def unlock(self):
        s = self._read()
        s["locked"] = False
        from datetime import date
        today = str(date.today())
        if s.get("last_unlock_date") == today:
            s["streak"] = s.get("streak", 0)  # already counted
        else:
            s["streak"] = s.get("streak", 0) + 1
            s["last_unlock_date"] = today
        self._write(s)

    def streak(self) -> int:
        return self._read().get("streak", 0)

    def set_attempt_now(self):
        import datetime as dt
        s = self._read()
        s["last_attempt"] = dt.datetime.now().isoformat(timespec="seconds")
        self._write(s)
