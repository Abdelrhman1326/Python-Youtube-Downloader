Write-Host "Setting up Python Youtube Downloader..."

if (Test-Path ".venv\bin\Activate") {
    Write-Host "Cleaning up accidental 'Activate' folder..."
    Remove-Item -Recurse -Force ".venv\bin\Activate"
}

if (-not (Test-Path ".venv")) {
    Write-Host "Creating fresh virtual environment..."
    python -m venv .venv
}

Write-Host "Activating virtual environment..."
. .\.venv\Scripts\Activate.ps1

Write-Host "Installing/verifying requirements..."
pip install -r requirements.txt

Write-Host "Starting Downloader.py..."
Write-Host "-----------------------------------"
python Downloader.py
Write-Host "-----------------------------------"

deactivate
Write-Host "Downloader closed and environment deactivated."
