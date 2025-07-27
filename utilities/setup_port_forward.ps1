# PowerShell script to forward port from Windows to WSL2
# Run this in Windows PowerShell as Administrator

param(
    [int]$Port = 8080
)

# Get WSL2 IP address
$wslIp = (wsl hostname -I).Trim().Split()[0]
Write-Host "WSL2 IP Address: $wslIp" -ForegroundColor Green

# Remove any existing port proxy for this port
netsh interface portproxy delete v4tov4 listenport=$Port listenaddress=0.0.0.0 2>$null

# Add port forwarding rule
netsh interface portproxy add v4tov4 listenport=$Port listenaddress=0.0.0.0 connectport=$Port connectaddress=$wslIp

# Show the rule
Write-Host "`nPort forwarding rule added:" -ForegroundColor Yellow
netsh interface portproxy show v4tov4 | findstr $Port

# Add firewall rule if it doesn't exist
$ruleName = "WSL2 Flask App Port $Port"
Remove-NetFirewallRule -DisplayName $ruleName -ErrorAction SilentlyContinue
New-NetFirewallRule -DisplayName $ruleName -Direction Inbound -Protocol TCP -LocalPort $Port -Action Allow | Out-Null

Write-Host "`nFirewall rule added for port $Port" -ForegroundColor Green
Write-Host "`nYour app should now be accessible at:" -ForegroundColor Cyan
Write-Host "  http://localhost:$Port" -ForegroundColor White
Write-Host "  http://$((Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -like '192.168.*' -or $_.IPAddress -like '10.*' -or $_.IPAddress -like '172.*'} | Select-Object -First 1).IPAddress):$Port" -ForegroundColor White