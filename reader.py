
from utils import countdown, print_box

def enforce_reading(minutes: int):
    print_box("Reading Time", f"You must read for {minutes} minutes.\nUse any terminal-friendly material (e.g. 'man bash', local notes). Stay on this screen.")
    seconds = int(minutes * 60)
    countdown(seconds, label="Reading")
