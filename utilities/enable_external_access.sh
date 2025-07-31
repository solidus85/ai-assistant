#!/bin/bash
# Script to enable external access for WSL2 Flask app

PORT=${1:-5000}

echo "🔧 Setting up port forwarding for WSL2..."
echo "=================================="

# Get WSL2 IP
WSL_IP=$(hostname -I | awk '{print $1}')
echo "WSL2 IP: $WSL_IP"

# Get Windows host IP (the gateway)
WINDOWS_IP=$(ip route | grep default | awk '{print $3}')
echo "Windows Host IP: $WINDOWS_IP"

# Create PowerShell command
echo ""
echo "📋 Run this command in Windows PowerShell as Administrator:"
echo ""
echo "netsh interface portproxy add v4tov4 listenport=$PORT listenaddress=0.0.0.0 connectport=$PORT connectaddress=$WSL_IP"
echo ""
echo "Or run the PowerShell script:"
echo "powershell.exe -ExecutionPolicy Bypass -File \"C:\\Users\\Cody\\OneDrive\\Documents\\Cline\\Projects\\llm\\utilities\\setup_port_forward.ps1\" -Port $PORT"
echo ""

# Try to run it automatically (requires Windows Terminal or proper setup)
if command -v powershell.exe &> /dev/null; then
    echo "🚀 Attempting to set up port forwarding automatically..."
    powershell.exe -Command "Start-Process PowerShell -Verb RunAs -ArgumentList '-ExecutionPolicy Bypass -File \"C:\\Users\\Cody\\OneDrive\\Documents\\Cline\\Projects\\llm\\utilities\\setup_port_forward.ps1\" -Port $PORT'"
    echo ""
    echo "⚠️  If a UAC prompt appeared, please click 'Yes' to allow admin access."
else
    echo "⚠️  Cannot run PowerShell automatically. Please run the command above manually."
fi

echo ""
echo "📱 After port forwarding is set up, your app will be accessible at:"
echo "   http://<your-computer-ip>:$PORT"
echo ""
echo "💡 To find your computer's IP on the network, run:"
echo "   ipconfig (in Windows) and look for IPv4 Address"