# KALI AI TERMINAL - Simple Launcher
param(
    [switch]$Backend,
    [switch]$Frontend,
    [switch]$All
)

$projectPath = "C:\Users\Bandula\Pictures\Screenshots\kali-ai-terminal"

function Start-Backend {
    Write-Host "Starting Kali AI Terminal Backend..." -ForegroundColor Yellow
    
    $backendScript = @"
Set-Location '$projectPath'
& 'backend\venv\Scripts\Activate.ps1'
Set-Location backend
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
"@
    
    Start-Process powershell -ArgumentList @("-NoExit", "-Command", $backendScript) -WindowStyle Normal
    Write-Host "Backend started in new window" -ForegroundColor Green
    Write-Host "API available at: http://127.0.0.1:8000" -ForegroundColor Cyan
}

function Start-Frontend {
    Write-Host "Starting Kali AI Terminal Frontend..." -ForegroundColor Yellow
    
    $frontendScript = @"
Set-Location '$projectPath'
npm install --legacy-peer-deps
npm start
"@
    
    Start-Process powershell -ArgumentList @("-NoExit", "-Command", $frontendScript) -WindowStyle Normal
    Write-Host "Frontend started in new window" -ForegroundColor Green  
    Write-Host "App available at: http://localhost:3000" -ForegroundColor Cyan
}

function Show-Status {
    Write-Host ""
    Write-Host "KALI AI TERMINAL - STATUS" -ForegroundColor Magenta
    Write-Host "=========================" -ForegroundColor Magenta
    
    # Check backend
    try {
        $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/health" -TimeoutSec 5
        Write-Host "Backend: RUNNING" -ForegroundColor Green
        Write-Host "   API: http://127.0.0.1:8000" -ForegroundColor Cyan
    } catch {
        Write-Host "Backend: NOT RUNNING" -ForegroundColor Red
    }
    
    # Check frontend (port 3000)
    try {
        $response = Test-NetConnection -ComputerName "localhost" -Port 3000 -InformationLevel Quiet
        if ($response) {
            Write-Host "Frontend: RUNNING" -ForegroundColor Green
            Write-Host "   App: http://localhost:3000" -ForegroundColor Cyan
        } else {
            Write-Host "Frontend: STARTING..." -ForegroundColor Yellow
        }
    } catch {
        Write-Host "Frontend: NOT RUNNING" -ForegroundColor Red
    }
    Write-Host ""
}

# Main execution
if ($All -or (-not $Backend -and -not $Frontend)) {
    Write-Host "LAUNCHING KALI AI TERMINAL" -ForegroundColor Cyan
    Write-Host "===========================" -ForegroundColor Cyan
    Write-Host ""
    
    Start-Backend
    Start-Sleep -Seconds 3
    Start-Frontend
    Start-Sleep -Seconds 5
    Show-Status
    
    Write-Host "Both services are starting up!" -ForegroundColor Green
    Write-Host "Wait a few moments for full initialization..." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Usage:" -ForegroundColor White
    Write-Host "   Backend API: http://127.0.0.1:8000" -ForegroundColor Gray
    Write-Host "   Frontend App: http://localhost:3000" -ForegroundColor Gray
    Write-Host "   API Docs: http://127.0.0.1:8000/docs" -ForegroundColor Gray
    Write-Host ""

} elseif ($Backend) {
    Start-Backend
} elseif ($Frontend) {
    Start-Frontend
}

Write-Host "To check status: .\start_kali_terminal.ps1 -Status" -ForegroundColor Magenta
