# Start Kali AI Terminal Backend
Write-Host "🔧 Starting Kali AI Terminal Backend..." -ForegroundColor Cyan
Set-Location "C:\Users\Bandula\Pictures\Screenshots\kali-ai-terminal"
& "backend\venv\Scripts\Activate.ps1"
Set-Location backend
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
