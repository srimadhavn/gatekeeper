
# Gatekeeper OS Shell (Strict Mode)

Earn access to your terminal by learning first.  
Stages:
1. DSA challenge (MCQ or short answer)
2. If wrong → SQL prompt
3. If wrong → Mandatory reading timer + journal (10+ lines)
4. Unlock

## Quick Start

```bash
cd gatekeeper_os_shell
python3 -m venv .venv && source .venv/bin/activate  # optional
python3 init_db.py     # seeds questions.db
./install.sh           # adds strict hook to your ~/.bashrc and/or ~/.zshrc
# Open a NEW terminal
```

If you interrupt (`Ctrl+C`), strict mode escalates punishment and can close the shell.

### Where things live
- Config: `config.json`
- DB: `questions.db`
- State: `~/.gatekeeper/state.json`
- Journals: `~/Gatekeeper/journal/*.md`

### Remove / Disable
Comment out or delete the lines added by `install.sh` in your shell rc file.

### Add Questions
Open `init_db.py` and add to `DSA` and `SQL`, then re-run `python3 init_db.py`.

### Roadmap
- GUI/browser lock
- LeetCode integration
- Streak dashboard
