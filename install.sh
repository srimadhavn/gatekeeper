#!/usr/bin/env bash
set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOK='python3 "$PROJECT_DIR/gatekeeper.py" || exit'

echo "Installing Gatekeeper hook into ~/.bashrc and ~/.zshrc (if they exist)."

if [ -f "$HOME/.bashrc" ]; then
  if ! grep -Fq 'gatekeeper.py' "$HOME/.bashrc"; then
    {
      echo ""
      echo "# ---- Gatekeeper OS Shell (strict mode) ----"
      echo "$HOOK"
      echo "# -------------------------------------------"
    } >> "$HOME/.bashrc"
    echo "Added hook to .bashrc"
  else
    echo "Hook already present in .bashrc"
  fi
fi

if [ -f "$HOME/.zshrc" ]; then
  if ! grep -Fq 'gatekeeper.py' "$HOME/.zshrc"; then
    {
      echo ""
      echo "# ---- Gatekeeper OS Shell (strict mode) ----"
      echo "$HOOK"
      echo "# -------------------------------------------"
    } >> "$HOME/.zshrc"
    echo "Added hook to .zshrc"
  else
    echo "Hook already present in .zshrc"
  fi
fi

echo "Done. Open a NEW terminal to see Gatekeeper in action."
