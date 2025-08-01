# Restart WSL with new 64GB memory configuration
Write-Host "=== Restarting WSL with 64GB RAM Configuration ===" -ForegroundColor Green
Write-Host ""

# Show current memory allocation
Write-Host "Current WSL Status:" -ForegroundColor Yellow
wsl --status

Write-Host "`nShutting down WSL..." -ForegroundColor Yellow
wsl --shutdown

Write-Host "Waiting for WSL to fully shut down..."
Start-Sleep -Seconds 5

Write-Host "`nStarting WSL with new configuration..." -ForegroundColor Yellow
Write-Host "Configuration file: C:\Users\Cody\.wslconfig" -ForegroundColor Cyan
Write-Host "New settings:" -ForegroundColor Cyan
Write-Host "  - Memory: 64GB"
Write-Host "  - Processors: 16"
Write-Host "  - Swap: 16GB"
Write-Host "  - GPU Support: Enabled"
Write-Host ""

# Start default WSL distro
wsl -d Ubuntu-22.04 -- echo "WSL Started Successfully"

Write-Host "`nVerifying new memory allocation..." -ForegroundColor Green
wsl -d Ubuntu-22.04 -- bash -c "free -h | grep Mem"

Write-Host "`nTo verify full configuration from within WSL, run:" -ForegroundColor Cyan
Write-Host "  free -h" -ForegroundColor White
Write-Host "  nproc" -ForegroundColor White
Write-Host "  nvidia-smi" -ForegroundColor White

Write-Host "`n=== WSL Restart Complete ===" -ForegroundColor Green