#!/bin/bash
# Check WSL2 network configuration

echo "🔍 WSL2 Network Configuration Check"
echo "===================================="

# Check current IP configuration
echo -e "\n📡 Current Network Configuration:"
ip -4 addr show | grep -E "inet|^[0-9]+:"

# Check default route
echo -e "\n🌐 Default Gateway (Windows host):"
ip route | grep default

# Check if we have a LAN IP
LAN_IP=$(ip -4 addr show | grep -oP '(?<=inet\s)192\.168\.|10\.|172\.(?:1[6-9]|2[0-9]|3[01])\.' | head -1)
if [ -n "$LAN_IP" ]; then
    echo -e "\n✅ Possible LAN IP detected: ${LAN_IP}x.x"
else
    echo -e "\n❌ No LAN IP detected (using NAT mode)"
fi

# Check WSL version info
echo -e "\n💻 WSL Environment:"
echo "Kernel: $(uname -r)"
echo "Distro: $(lsb_release -d | cut -f2)"

# Test connectivity
echo -e "\n🧪 Connectivity Test:"
if ping -c 1 8.8.8.8 &> /dev/null; then
    echo "✅ Internet connectivity: OK"
else
    echo "❌ Internet connectivity: Failed"
fi

# Check if .wslconfig exists
echo -e "\n📄 WSL Configuration:"
if [ -f "/mnt/c/Users/$USER/.wslconfig" ]; then
    echo "✅ .wslconfig found at /mnt/c/Users/$USER/.wslconfig"
    echo "Contents:"
    cat "/mnt/c/Users/$USER/.wslconfig" | sed 's/^/  /'
else
    echo "❌ No .wslconfig found (using default NAT mode)"
fi

echo -e "\n💡 To apply network changes:"
echo "  1. Exit WSL"
echo "  2. Run in PowerShell: wsl --shutdown"
echo "  3. Start WSL again"