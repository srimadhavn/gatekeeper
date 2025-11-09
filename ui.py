#!/usr/bin/env python3
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from theme import Theme
from storage import read
import subprocess, os, sys

console = Console()

def run(cmd):
    proc = subprocess.run([sys.executable, cmd], check=False)
    return proc.returncode

def main():
    settings = read("settings")
    Theme.set(settings.get("theme","tokyo"))

    while True:
        console.clear()
        console.print(Panel.fit(
            f"{Theme.C('header')}Gatekeeper Dashboard[/]\n{Theme.C('fg')}Choose an action:",
            border_style=Theme._current["border"]
        ))
        console.print(
            f"{Theme.C('accent')}1.{Theme.C('fg')} Start Challenge\n"
            f"{Theme.C('accent')}2.{Theme.C('fg')} Stats\n"
            f"{Theme.C('accent')}3.{Theme.C('fg')} Add Question\n"
            f"{Theme.C('accent')}4.{Theme.C('fg')} Review Mistakes (enter tag in next step)\n"
            f"{Theme.C('accent')}5.{Theme.C('fg')} Daily (enter tag)\n"
            f"{Theme.C('accent')}6.{Theme.C('fg')} Switch Theme (tokyo/matrix/light)\n"
            f"{Theme.C('accent')}7.{Theme.C('fg')} Toggle Strict Mode\n"
            f"{Theme.C('accent')}0.{Theme.C('fg')} Exit"
        )
        choice = Prompt.ask(f"\n{Theme.C('success')}Your choice", choices=["0","1","2","3","4","5","6","7"])

        proj = os.path.dirname(__file__)
        if choice == "0":
            break
        elif choice == "1":
            run(os.path.join(proj, "gatekeeper.py"))
        elif choice == "2":
            run(os.path.join(proj, "stats.py")); input("\nPress Enter…")
        elif choice == "3":
            run(os.path.join(proj, "add_question.py"))
        elif choice == "4":
            tag = Prompt.ask(f"{Theme.C('accent')}Enter tag (e.g., dp, bst, sql)")
            subprocess.run([sys.executable, os.path.join(proj,"review.py"), tag])
            input("\nPress Enter…")
        elif choice == "5":
            tag = Prompt.ask(f"{Theme.C('accent')}Enter tag (e.g., dp, bst, sql)")
            subprocess.run([sys.executable, os.path.join(proj,"daily.py"), tag])
            input("\nPress Enter…")
        elif choice == "6":
            from storage import write
            new_t = Prompt.ask(f"{Theme.C('accent')}Theme", choices=["tokyo","matrix","light"])
            s = read("settings"); s["theme"] = new_t; write("settings", s)
            Theme.set(new_t)
        elif choice == "7":
            from storage import write
            s = read("settings"); s["strict_mode"] = not s.get("strict_mode", True); write("settings", s)
            console.print(f"{Theme.C('warning')}Strict mode is now {'ON' if s['strict_mode'] else 'OFF'}")
            input("\nPress Enter…")

if __name__ == "__main__":
    main()
