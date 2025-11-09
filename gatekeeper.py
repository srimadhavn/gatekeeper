#!/usr/bin/env python3
import signal, sys, time
from datetime import date
from storage import init_storage, read, write
from dsa_engine import DSAEngine
from sql_engine import SQLEngine
from logger import log_answer, log_session
from reader import enforce_reading
from journal import write_journal
from utils import clear
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from theme import Theme

console = Console()
init_storage()

def settings(): return read("settings")

def load_state(): return read("state")
def save_state(state): write("state", state)

def unlock():
    state = load_state()
    before = state.get("streak",0)
    state["locked"] = False
    today = str(date.today())
    if state.get("last_unlock_date") != today:
        state["streak"] = before + 1
        state["last_unlock_date"] = today
    save_state(state)
    after = state["streak"]
    streak_popup(before, after)

def lock():
    state = load_state(); state["locked"] = True; save_state(state)

def streak_popup(before:int, after:int):
    if after > before:
        console.print("\a", end="")  # terminal bell
        pct = min(100, after*10)   # fun pseudo XP
        console.print(Panel.fit(
            f"{Theme.C('success')}🔥 Streak Up!  +1 day\n"
            f"{Theme.C('fg')}XP: ",
            border_style=Theme._current["success"]
        ), end="")
        # animate bar
        width = pct//10
        console.print("")  # newline
        for i in range(width+1):
            bar = "█"*i + "░"*(10-i)
            console.print(f"\r{Theme.C('fg')}{bar} {i*10:>3}%", end="")
            time.sleep(0.05)
        console.print("")  # newline

def header():
    console.print(Panel.fit(
        f"{Theme.C('header')}Gatekeeper Terminal[/]\n"
        f"{Theme.C('fg')}Solve to unlock. Strict mode active.",
        border_style=Theme._current["border"]
    ))

def main():
    Theme.set(settings().get("theme","tokyo"))

    def on_interrupt(sig, frame):
        console.print(f"\n{Theme.C('warning')}⚠️  Interrupted — challenge failed.")
        sys.exit(1)
    signal.signal(signal.SIGINT, on_interrupt)

    if settings().get("strict_mode", True):
        lock()
    clear()
    header()

    dsa = DSAEngine(); sql = SQLEngine()

    # --- DSA ---
    q = dsa.get_random()
    console.print(Panel.fit(
        f"{Theme.C('accent')}🧠 DSA Challenge\n\n{Theme.C('fg')}{q['question']}",
        title=f"{Theme.C('header')}Step 1 of 3[/]", border_style=Theme._current["border"]
    ))
    if q["type"] == "mcq":
        for k,v in q["options"].items():
            console.print(f"{Theme.C('fg')}{k}) {v}")
    ans = Prompt.ask(f"{Theme.C('success')}\nYour Answer")
    ok = dsa.check(q, ans)
    log_answer("dsa", q["id"], q["tags"], ok)

    if ok:
        unlock(); log_session("pass_dsa", load_state()["streak"]); clear()
        console.print(Panel.fit(
            f"{Theme.C('success')}✅ Access Granted\n\n{Theme.C('fg')}DSA Passed\n🔥 Streak: {load_state()['streak']}",
            border_style=Theme._current["success"]
        ))
        return

    console.print(f"\n{Theme.C('error')}❌ DSA failed → SQL challenge.")

    # --- SQL ---
    sq = sql.get_random()
    console.print(Panel.fit(
        f"{Theme.C('accent')}🧾 SQL Challenge\n\n{Theme.C('fg')}{sq['prompt']}\n\n[i]Submit SQL, end with '.'[/i]",
        title=f"{Theme.C('header')}Step 2 of 3[/]", border_style=Theme._current["border"]
    ))
    lines = []
    while True:
        line = input("> ")
        if line.strip() == ".": break
        lines.append(line)
    user_sql = "\n".join(lines)
    ok_sql = sql.check(sq, user_sql)
    log_answer("sql", sq["id"], sq["tags"], ok_sql)

    if ok_sql:
        unlock(); log_session("pass_sql", load_state()["streak"]); clear()
        console.print(Panel.fit(
            f"{Theme.C('success')}✅ Access Granted\n\n{Theme.C('fg')}SQL Passed\n🔥 Streak: {load_state()['streak']}",
            border_style=Theme._current["success"]
        ))
        return

    console.print(f"\n{Theme.C('error')}❌ SQL failed → Reading + Journal required.")

    # --- Reading + Journal ---
    mins = settings().get("reading_minutes", 10)
    enforce_reading(mins)
    path = write_journal("~/Gatekeeper/journal", settings().get("journal_min_lines",10))

    unlock(); log_session("pass_journal", load_state()["streak"]); clear()
    console.print(Panel.fit(
        f"{Theme.C('success')}✅ Access Granted\n\n{Theme.C('fg')}Reflection Complete\n"
        f"🔥 Streak: {load_state()['streak']}\n📘 Saved: {path}",
        border_style=Theme._current["success"]
    ))

if __name__ == "__main__":
    main()
