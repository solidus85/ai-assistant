# WSL2 External Access Fix

## The Problem
WSL2 runs in a lightweight VM with its own virtual network adapter. This means:
- Apps in WSL2 are NOT directly accessible from your network
- The WSL2 IP changes on every reboot
- Windows Firewall alone won't help

## Solution: Port Forwarding

### Method 1: Quick Setup (Recommended)
Run this from WSL:
```bash
./utilities/enable_external_access.sh
```
Then follow the instructions to run the PowerShell command as admin.

### Method 2: Manual PowerShell Commands
1. Open PowerShell as Administrator
2. Get your WSL2 IP:
   ```powershell
   wsl hostname -I
   ```
3. Set up port forwarding:
   ```powershell
   netsh interface portproxy add v4tov4 listenport=8080 listenaddress=0.0.0.0 connectport=8080 connectaddress=<WSL2-IP>
   ```

### Method 3: Automatic Script
Run in PowerShell as Administrator:
```powershell
cd C:\Users\Cody\OneDrive\Documents\Cline\Projects\llm\utilities
.\setup_port_forward.ps1 -Port 8080
```

## Verify It's Working

1. Check port forwarding rules:
   ```powershell
   netsh interface portproxy show v4tov4
   ```

2. Test from another device:
   - Find your Windows IP: `ipconfig` (look for IPv4)
   - Access: `http://<windows-ip>:8080`

3. Test with nmap:
   ```bash
   nmap -p 8080 <windows-ip>
   ```

## Important Notes

### The forwarding needs to be reset when:
- Windows restarts
- WSL2 restarts
- WSL2 IP changes

### Permanent Solution Options:

1. **Task Scheduler** (Recommended)
   - Create a task that runs the PowerShell script at startup
   - Run with highest privileges

2. **WSL1 Instead**
   - WSL1 shares network with Windows (no forwarding needed)
   - But loses some Linux compatibility

3. **Use localhost + SSH Tunnel**
   - For remote access, use SSH tunnel instead
   - More secure than exposing ports

## Troubleshooting

### Port still shows as closed?
1. Verify Flask is running: `curl localhost:8080` in WSL
2. Check Windows is listening: `netstat -an | findstr 8080` in Windows
3. Temporarily disable Windows Defender Firewall completely
4. Check if another app is using port 8080

### "Access Denied" errors?
- Must run PowerShell as Administrator
- Windows Defender might block the script - add exception

### Can't access from phone/tablet?
1. Ensure devices are on same network
2. Check router doesn't have client isolation enabled
3. Try using computer hostname instead of IP

## Quick Test Commands

```bash
# In WSL - check if app is running
curl -I localhost:8080

# In Windows - check if port forwarding is active
netstat -an | findstr :8080

# From another device - test connection
curl http://<windows-ip>:8080
```