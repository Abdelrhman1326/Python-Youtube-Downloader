#!/bin/bash

# Get the directory where the script is located to handle spaces in paths
PARENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PARENT_DIR"

echo "Setting up Python Youtube Downloader..."

# Use lowercase 'activate' (standard for venv)
if [ -d ".venv/bin/activate" ]; then
    echo "Environment exists."
else
    echo "Creating fresh virtual environment..."
    python3 -m venv .venv
fi

echo "Activating virtual environment..."
# Quote the path to handle spaces
source "./.venv/bin/activate"

echo "Installing/verifying requirements..."
# Always use 'python -m pip' inside scripts for better reliability
python3 -m pip install -r requirements.txt

echo "Starting Downloader.py..."
echo "-----------------------------------"
python3 Downloader.py
echo "-----------------------------------"

deactivate
echo "Downloader closed and environment deactivated."
