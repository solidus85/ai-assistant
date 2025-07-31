#!/usr/bin/env python3
"""Show all IP addresses where WSL can be accessed from outside."""
import subprocess
import socket
import os

def run_command(cmd):
    """Run a shell command and return output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    except:
        return None

def get_windows_ips():
    """Get Windows host IPs using PowerShell."""
    try:
        # Run PowerShell command from WSL
        cmd = 'powershell.exe -Command "Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.InterfaceAlias -notlike \'*Loopback*\' -and $_.IPAddress -ne \'127.0.0.1\'} | Select-Object -ExpandProperty IPAddress"'
        result = run_command(cmd)
        if result:
            return [ip.strip() for ip in result.split('\n') if ip.strip()]
    except:
        pass
    return []

def main():
    port = int(os.environ.get('PORT', 5000))
    
    print("🌐 WSL2 Network Access Points")
    print("=" * 60)
    
    # WSL Internal IPs
    print("\n📍 WSL2 Internal IPs:")
    wsl_ips = run_command("hostname -I").split()
    for ip in wsl_ips:
        print(f"   - {ip}")
    
    # Network interfaces detail
    print("\n🔌 Network Interfaces:")
    interfaces = {
        'eth0': 'WSL2 internal network (link-local)',
        'eth1': 'Primary network interface',
        'eth4': 'VPN or special network',
        'br0': 'Bridge interface',
        'lo': 'Loopback (local only)'
    }
    
    for iface, desc in interfaces.items():
        cmd = f"ip addr show {iface} 2>/dev/null | grep 'inet ' | awk '{{print $2}}' | cut -d'/' -f1"
        ip = run_command(cmd)
        if ip and ip != '127.0.0.1':
            print(f"   - {iface}: {ip} ({desc})")
    
    # Windows host gateway
    print("\n🪟 Windows Host Gateway:")
    gateway = run_command("ip route | grep default | awk '{print $3}'")
    if gateway:
        print(f"   - {gateway}")
    
    # Windows host IPs
    print("\n💻 Windows Host Network IPs:")
    windows_ips = get_windows_ips()
    if windows_ips:
        for ip in windows_ips:
            if ip and not ip.startswith('169.254'):  # Skip link-local
                print(f"   - {ip}")
    
    # Access URLs
    print(f"\n🌐 Access URLs (Port {port}):")
    print("\n  From WSL/Linux:")
    print(f"   - http://localhost:{port}")
    print(f"   - http://127.0.0.1:{port}")
    
    print("\n  From Windows (same machine):")
    # The primary WSL IP that Windows can access
    primary_wsl_ip = None
    for ip in wsl_ips:
        if ip.startswith('10.') or ip.startswith('172.') or ip.startswith('192.'):
            primary_wsl_ip = ip
            break
    
    if primary_wsl_ip:
        print(f"   - http://{primary_wsl_ip}:{port}")
    
    print("\n  From other devices on network:")
    print("   (Requires port forwarding to be set up)")
    for ip in windows_ips:
        if ip and not ip.startswith('169.254'):
            print(f"   - http://{ip}:{port}")
    
    # Check current networking mode
    print("\n⚙️  WSL2 Networking Mode:")
    if len([ip for ip in wsl_ips if ip.startswith('10.') or ip.startswith('172.')]) > 1:
        print("   - Appears to be using mirrored/bridged networking")
        print("   - Multiple network interfaces detected")
    else:
        print("   - Using standard NAT mode")
        print("   - Port forwarding required for external access")
    
    print("\n📝 Notes:")
    print("   - 169.254.x.x = Link-local addresses (not routable)")
    print("   - 10.x.x.x = Private network addresses")
    print("   - Use ./utilities/enable_external_access.sh for port forwarding")

if __name__ == "__main__":
    main()