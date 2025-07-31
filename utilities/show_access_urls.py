#!/usr/bin/env python3
"""Show URLs to access the app from different devices."""
import socket
import subprocess
import sys
import os

def get_wsl_ip():
    """Get WSL2 IP address."""
    try:
        result = subprocess.run(['ip', 'addr', 'show', 'eth0'], 
                              capture_output=True, text=True)
        for line in result.stdout.split('\n'):
            if 'inet ' in line:
                return line.split()[1].split('/')[0]
    except:
        return None

def get_windows_ip():
    """Get Windows host IP."""
    try:
        # Get the default gateway (usually the Windows host in WSL2)
        result = subprocess.run(['ip', 'route', 'show', 'default'], 
                              capture_output=True, text=True)
        if result.stdout:
            return result.stdout.split()[2]
    except:
        return None

def get_lan_ip():
    """Get LAN IP address."""
    try:
        # Connect to a public DNS to find our LAN IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return None

def main():
    port = int(os.environ.get('PORT', 5000))
    
    print("🌐 LLM Web App Access URLs")
    print("=" * 60)
    
    print("\n📍 Local Access:")
    print(f"   http://localhost:{port}")
    print(f"   http://127.0.0.1:{port}")
    
    wsl_ip = get_wsl_ip()
    if wsl_ip:
        print(f"\n🐧 WSL2 IP:")
        print(f"   http://{wsl_ip}:{port}")
    
    windows_ip = get_windows_ip()
    if windows_ip:
        print(f"\n🪟 Windows Host IP:")
        print(f"   http://{windows_ip}:{port}")
    
    lan_ip = get_lan_ip()
    if lan_ip:
        print(f"\n🏠 LAN Access (for other devices on your network):")
        print(f"   http://{lan_ip}:{port}")
        print(f"\n📱 QR Code for mobile access:")
        print(f"   https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=http://{lan_ip}:{port}")
    
    print("\n⚠️  Security Notes:")
    print("   - Only share with trusted devices on your network")
    print("   - Consider adding authentication for external access")
    print("   - Check Windows Firewall if connection fails")
    
    print("\n🔥 Firewall Command (run in Windows PowerShell as Admin):")
    print(f"   New-NetFirewallRule -DisplayName 'Flask LLM App' -Direction Inbound -Protocol TCP -LocalPort {port} -Action Allow")

if __name__ == "__main__":
    main()