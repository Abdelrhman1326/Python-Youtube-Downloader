Write-Host "Updating yt-dlp..." -ForegroundColor Cyan
python -m pip install --upgrade yt-dlp

Write-Host "`nLaunching Downloader..." -ForegroundColor Green
python .\Downloader.py
