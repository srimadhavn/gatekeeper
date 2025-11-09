
import os, textwrap
from utils import ensure_dir, expand, write_file, timestamp, print_box

def write_journal(journal_dir: str, min_lines: int = 10):
    print_box("Journal", f"Write {min_lines}+ lines reflecting on what you read.\nFinish with a blank line on its own.")
    lines = []
    while True:
        try:
            line = input("> ")
        except KeyboardInterrupt:
            print("\nInterrupt not allowed during journal in strict mode.")
            continue
        if line.strip() == "" and len(lines) >= min_lines:
            break
        lines.append(line)
    out_dir = ensure_dir(journal_dir)
    fname = os.path.join(out_dir, f"{timestamp().replace(':','-')}.md")
    content = "# Reading Journal\n\n" + "\n".join(lines) + "\n"
    write_file(fname, content)
    return fname
