#!/usr/bin/env bash

set -e

echo "=== System setup for Youtube Downloader ==="

install_deno() {
  if command -v deno >/dev/null 2>&1; then
    echo "Deno already installed."
  else
    echo "Installing Deno..."
    curl -fsSL https://deno.land/install.sh | sh
    export DENO_INSTALL="$HOME/.deno"
    export PATH="$DENO_INSTALL/bin:$PATH"
  fi
}

install_ffmpeg() {
  if command -v ffmpeg >/dev/null 2>&1; then
    echo "FFmpeg already installed."
  else
    echo "Installing FFmpeg..."
    if command -v apt >/dev/null 2>&1; then
      sudo apt update && sudo apt install -y ffmpeg
    elif command -v dnf >/dev/null 2>&1; then
      sudo dnf install -y ffmpeg
    elif command -v brew >/dev/null 2>&1; then
      brew install ffmpeg
    else
      echo "Please install FFmpeg manually for your system."
      exit 1
    fi
  fi
}

install_deno
install_ffmpeg

# Ensure venv exists
VENV_PYTHON="./.venv/bin/python"

if [ ! -f "$VENV_PYTHON" ]; then
  echo "Creating virtual environment..."
  python3 -m venv .venv
fi

echo "Installing Python requirements into venv..."
"$VENV_PYTHON" -m pip install --upgrade pip
"$VENV_PYTHON" -m pip install -r requirements.txt

echo "=== Setup complete ==="