#!/usr/bin/env python3
from storage import read
from datetime import datetime, timedelta
from collections import Counter
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from theme import Theme

console = Console()

def heat_cell(val:int) -> str:
    # 0 none, 1 low, 2 med, 3+ high
    if val <= 0: return "░"
    if val == 1: return "▒"
    if val == 2: return "▓"
    return "█"

def heatmap_grid(logs, days=35, cols=7):
    """Return rows of recent days (left older → right newer)"""
    today = datetime.now().date()
    buckets = []
    for i in range(days):
        d = today - timedelta(days=(days-1-i))
        count = sum(1 for e in logs if datetime.fromisoformat(e["time"]).date() == d)
        buckets.append(heat_cell(count))
    # shape into rows
    rows = []
    for r in range(0, days, cols):
        rows.append(" ".join(buckets[r:r+cols]))
    return "\n".join(rows)

def stats():
    settings = read("settings")
    Theme.set(settings.get("theme","tokyo"))

    answers = read("answers")
    sessions = read("sessions")
    state = read("state")

    streak = state.get("streak", 0)
    total = len(sessions)

    correct_dsa = sum(1 for a in answers if a["type"]=="dsa" and a["correct"])
    total_dsa = sum(1 for a in answers if a["type"]=="dsa")
    correct_sql = sum(1 for a in answers if a["type"]=="sql" and a["correct"])
    total_sql = sum(1 for a in answers if a["type"]=="sql")

    console.print(Panel.fit(
        f"{Theme.C('header')}🔥 Streak:{Theme.C('fg')} {streak} days",
        border_style=Theme._current["border"]
    ))

    console.print(f"\n{Theme.C('accent')}Last 35 Days Heatmap:{Theme.C('fg')}")
    console.print(heatmap_grid(sessions, 35, 7))
    console.print("[dim]░ none  ▒ low  ▓ med  █ high[/dim]\n")

    tbl = Table(show_header=True, header_style=f"bold {Theme._current['header']}")
    tbl.add_column("Metric"); tbl.add_column("Value", justify="right")
    tbl.add_row("Total Sessions", str(total))
    tbl.add_row("DSA Accuracy", f"{correct_dsa}/{total_dsa}")
    tbl.add_row("SQL Accuracy", f"{correct_sql}/{total_sql}")
    console.print(tbl)

    tag_perf = Counter(); tag_total = Counter()
    for a in answers:
        for t in a["tags"]:
            tag_total[t]+=1
            if a["correct"]: tag_perf[t]+=1

    console.print(f"\n{Theme.C('accent')}Topic Performance:{Theme.C('fg')}")
    if not tag_total:
        console.print("[dim]Answer more questions to see topic data.[/dim]")
        return
    for t in sorted(tag_total):
        rate = int(100*tag_perf[t]/tag_total[t]) if tag_total[t] else 0
        filled = rate // 10
        bar = "█" * filled + "░" * (10 - filled)
        console.print(f"{t:14}: {bar} {rate}%")

if __name__ == "__main__":
    stats()
