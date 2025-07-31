#!/bin/bash
# Diagnose and fix firewall issues for Flask app

PORT=5000

echo "🔍 Diagnosing network connectivity for port $PORT..."
echo "=================================================="

# Check if app is running
echo -e "\n1️⃣ Checking if app is listening on port $PORT:"
if netstat -tln | grep -q ":$PORT"; then
    echo "   ✅ App is listening on port $PORT"
    netstat -tln | grep $PORT
else
    echo "   ❌ App is NOT listening on port $PORT"
    echo "   Please start the Flask app first!"
    exit 1
fi

# Check local connectivity
echo -e "\n2️⃣ Testing local connectivity:"
if timeout 2 bash -c "echo > /dev/tcp/localhost/$PORT" 2>/dev/null; then
    echo "   ✅ Local connection works (localhost:$PORT)"
else
    echo "   ❌ Local connection failed"
fi

# Check WSL IP connectivity
WSL_IP=$(hostname -I | awk '{print $1}')
echo -e "\n3️⃣ Testing WSL IP connectivity ($WSL_IP):"
if timeout 2 bash -c "echo > /dev/tcp/$WSL_IP/$PORT" 2>/dev/null; then
    echo "   ✅ WSL IP connection works"
else
    echo "   ❌ WSL IP connection failed"
fi

# Check firewall commands
echo -e "\n4️⃣ Firewall Fix Commands:"
echo "   Run these commands to open port $PORT:"
echo ""
echo "   Option A - Using UFW (if installed):"
echo "   sudo ufw allow $PORT/tcp"
echo "   sudo ufw reload"
echo ""
echo "   Option B - Using iptables directly:"
echo "   sudo iptables -A INPUT -p tcp --dport $PORT -j ACCEPT"
echo "   sudo iptables -A OUTPUT -p tcp --sport $PORT -j ACCEPT"
echo ""
echo "   Option C - Disable UFW completely (not recommended):"
echo "   sudo ufw disable"
echo ""

# Windows Firewall check
echo -e "\n5️⃣ Windows Firewall Commands:"
echo "   Run this in PowerShell as Administrator:"
echo "   New-NetFirewallRule -DisplayName 'Flask Port $PORT' -Direction Inbound -Protocol TCP -LocalPort $PORT -Action Allow"
echo ""

# Test from Windows
echo -e "\n6️⃣ Test from Windows PowerShell:"
echo "   Test-NetConnection -ComputerName $WSL_IP -Port $PORT"
echo ""

# Check if iptables has any rules
echo -e "\n7️⃣ Current iptables status (requires sudo):"
echo "   sudo iptables -L -n | grep $PORT"
echo "   sudo iptables -L INPUT -n --line-numbers"
echo ""

# Permanent fix suggestion
echo -e "\n💡 For a permanent fix, add this to your ~/.bashrc:"
echo "   # Open port $PORT for Flask app"
echo "   sudo iptables -A INPUT -p tcp --dport $PORT -j ACCEPT 2>/dev/null"
echo ""
echo "Or create a systemd service to apply firewall rules on boot."