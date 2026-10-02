#!/bin/bash
# Double-click this file to finish installing OpenMontage on this Mac.
# It only installs things inside this folder, plus (if needed, and only via Homebrew)
# Python, Node.js and FFmpeg. Safe to run again if something fails.

cd "$(dirname "$0")" || exit 1
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

say_step() { printf "\n==> %s\n" "$1"; }
finish()   { printf "\n%s\n\nPress Return to close this window." "$1"; read -r _; exit "${2:-0}"; }

find_python() {
  for p in python3.13 python3.12 python3.11 python3.10 python3; do
    if command -v "$p" >/dev/null 2>&1 && "$p" -c 'import sys; raise SystemExit(0 if sys.version_info[:2] >= (3,10) else 1)' 2>/dev/null; then
      command -v "$p"; return 0
    fi
  done
  return 1
}
node_ok() { command -v node >/dev/null 2>&1 && [ "$(node -p 'parseInt(process.versions.node)')" -ge 18 ] 2>/dev/null; }

say_step "Checking what this Mac already has"
MISSING=()
PY="$(find_python)" || MISSING+=("python@3.12")
node_ok                              || MISSING+=("node")
command -v ffmpeg >/dev/null 2>&1    || MISSING+=("ffmpeg")
echo "Python 3.10+: ${PY:-missing}"
echo "Node 18+:     $(node_ok && node -v || echo missing)"
echo "FFmpeg:       $(command -v ffmpeg || echo missing)"

if [ ${#MISSING[@]} -gt 0 ]; then
  if command -v brew >/dev/null 2>&1; then
    say_step "Installing with Homebrew: ${MISSING[*]}"
    brew install "${MISSING[@]}" || finish "Homebrew could not install: ${MISSING[*]}. Send Claude a screenshot of this window." 1
    PY="$(find_python)" || finish "Python 3.10+ still not found after install. Send Claude a screenshot of this window." 1
  else
    finish "Missing: ${MISSING[*]}
Homebrew isn't installed, so I can't add them automatically.
1. Install Homebrew from https://brew.sh (it will ask for your Mac password)
2. Double-click this file again." 1
  fi
fi

say_step "Creating a private Python environment (.venv)"
[ -x .venv/bin/python ] || "$PY" -m venv .venv || finish "Could not create .venv. Send Claude a screenshot of this window." 1

say_step "Installing Python packages (a few minutes)"
.venv/bin/python -m pip install --upgrade pip >/dev/null
.venv/bin/python -m pip install -r requirements.txt || finish "Python packages failed to install. Send Claude a screenshot of this window." 1

say_step "Installing the video renderer (Remotion)"
( cd remotion-composer && npm install ) || finish "Remotion install failed. Send Claude a screenshot of this window." 1

say_step "Installing the free offline voice (Piper)"
.venv/bin/python -m pip install piper-tts || echo "   Skipped: Piper didn't install. Narration will need a cloud voice key instead."

[ -f .env ] || { cp .env.example .env && echo "Created .env (add API keys there later; none are required)."; }

finish "Done. OpenMontage is installed in: $(pwd)
Next: open this folder in Claude Code and tell it what video to make." 0
