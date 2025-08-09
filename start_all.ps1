# KALI AI TERMINAL - Complete Startup Script
Write-Host "🚀 Starting Kali AI Terminal..." -ForegroundColor Cyan

# Check if Node.js and Python are available
try {
    $nodeVersion = node --version
    $pythonVersion = python --version
    Write-Host "✓ Node.js: $nodeVersion" -ForegroundColor Green
    Write-Host "✓ Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Missing dependencies. Please install Node.js and Python." -ForegroundColor Red
    exit 1
}

# Start Backend (FastAPI)
Write-Host "🔧 Starting Backend Server..." -ForegroundColor Yellow
$backendJob = Start-Job -ScriptBlock {
    Set-Location "C:\Users\Bandula\Pictures\Screenshots\kali-ai-terminal"
    & "backend\venv\Scripts\Activate.ps1"
    Set-Location backend
    python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
}

# Wait a moment for backend to start
Start-Sleep -Seconds 3

# Start Frontend (React + Electron)
Write-Host "⚡ Starting Frontend Application..." -ForegroundColor Yellow
$frontendJob = Start-Job -ScriptBlock {
    Set-Location "C:\Users\Bandula\Pictures\Screenshots\kali-ai-terminal"
    npm run electron-dev
}

Write-Host "🌟 Kali AI Terminal is starting up!" -ForegroundColor Green
Write-Host "📡 Backend API: http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host "🖥️  Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop all services" -ForegroundColor Magenta

# Keep the script running and monitor jobs
try {
    while ($true) {
        Start-Sleep -Seconds 1
        
        # Check if jobs are still running
        $backendStatus = Get-Job -Id $backendJob.Id
        $frontendStatus = Get-Job -Id $frontendJob.Id
        
        if ($backendStatus.State -eq "Failed") {
            Write-Host "❌ Backend failed! Check logs." -ForegroundColor Red
            Receive-Job -Id $backendJob.Id
        }
        
        if ($frontendStatus.State -eq "Failed") {
            Write-Host "❌ Frontend failed! Check logs." -ForegroundColor Red
            Receive-Job -Id $frontendJob.Id
        }
    }
} finally {
    Write-Host "🛑 Stopping all services..." -ForegroundColor Red
    Stop-Job -Id $backendJob.Id -ErrorAction SilentlyContinue
    Stop-Job -Id $frontendJob.Id -ErrorAction SilentlyContinue
    Remove-Job -Id $backendJob.Id -ErrorAction SilentlyContinue
    Remove-Job -Id $frontendJob.Id -ErrorAction SilentlyContinue
    Write-Host "✅ All services stopped." -ForegroundColor Green
}
