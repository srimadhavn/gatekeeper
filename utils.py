
import json, os, sys, time, datetime as dt, shutil, textwrap

def expand(path: str) -> str:
    return os.path.expanduser(os.path.expandvars(path))

def clear():
    # Clear screen for most terminals
    os.system('clear' if os.name != 'nt' else 'cls')

def pause(msg="Press Enter to continue..."):
    try:
        input(msg)
    except KeyboardInterrupt:
        print("\nDetected interrupt. In strict mode this will count as a failure.")
        raise

def countdown(seconds: int, label="Time left"):
    try:
        for remaining in range(seconds, -1, -1):
            mins, secs = divmod(remaining, 60)
            print(f"\r{label}: {mins:02d}:{secs:02d}", end="", flush=True)
            time.sleep(1)
        print()
    except KeyboardInterrupt:
        print("\nTimer interrupted. In strict mode this will count as failure.")
        raise

def print_box(title: str, body: str = ""):
    lines = [title] + ([] if not body else body.splitlines())
    width = max(len(l) for l in lines) + 4
    print("+" + "-"*(width-2) + "+")
    for l in lines:
        print("| " + l.ljust(width-4) + " |")
    print("+" + "-"*(width-2) + "+")

def ensure_dir(path: str):
    p = expand(path)
    os.makedirs(p, exist_ok=True)
    return p

def write_file(path: str, content: str):
    p = expand(path)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)

def timestamp():
    return dt.datetime.now().isoformat(timespec="seconds")
