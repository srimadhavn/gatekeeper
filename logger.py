from datetime import datetime
from storage import read, write

def log_answer(qtype, qid, tags, correct):
    logs = read("answers")
    logs.append({
        "time": datetime.now().isoformat(),
        "type": qtype,
        "id": qid,
        "tags": tags,
        "correct": correct
    })
    write("answers", logs)

def log_session(result, streak):
    logs = read("sessions")
    logs.append({
        "time": datetime.now().isoformat(),
        "result": result,
        "streak": streak
    })
    write("sessions", logs)
