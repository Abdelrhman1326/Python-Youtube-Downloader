Write-Host "=== System setup for Youtube Downloader ==="

# Check winget
if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
    Write-Error "winget is required but not found. Install App Installer from Microsoft Store."
    exit 1
}

# Install Deno if missing
if (-not (Get-Command deno -ErrorAction SilentlyContinue)) {
    Write-Host "Installing Deno..."
    winget install -e --id DenoLand.Deno
} else {
    Write-Host "Deno already installed."
}

# Install FFmpeg if missing
if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) {
    Write-Host "Installing FFmpeg..."
    winget install -e --id Gyan.FFmpeg
} else {
    Write-Host "FFmpeg already installed."
}

# Ensure venv exists
$venvPython = ".\.venv\Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    Write-Host "Creating virtual environment..."
    python -m venv .venv
}

# Install Python requirements using venv python
Write-Host "Installing Python requirements into venv..."
& $venvPython -m pip install --upgrade pip
& $venvPython -m pip install -r requirements.txt

Write-Host "=== Setup complete ==="