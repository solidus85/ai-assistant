# WSL2 Bridge Mode Configuration

## Overview
By default, WSL2 uses NAT networking. Bridge mode gives WSL2 its own IP address on your LAN, eliminating the need for port forwarding.

## Method 1: Using Hyper-V Virtual Switch (Recommended)

### Step 1: Create .wslconfig
Create or edit `C:\Users\Cody\.wslconfig`:

```ini
[wsl2]
networkingMode=bridged
vmSwitch=WSLBridge
dhcp=true
```

### Step 2: Create Virtual Switch in Hyper-V Manager
1. Open Hyper-V Manager (requires Windows Pro/Enterprise)
2. Click "Virtual Switch Manager" on the right
3. Create a new External virtual switch named "WSLBridge"
4. Select your physical network adapter
5. Apply changes

### Step 3: Restart WSL
```powershell
wsl --shutdown
wsl
```

## Method 2: Using .wslconfig with mirrored mode (Windows 11 Build 22H2+)

### Step 1: Create .wslconfig
Create or edit `C:\Users\Cody\.wslconfig`:

```ini
[wsl2]
networkingMode=mirrored
dnsTunneling=true
firewall=true
autoProxy=true

[experimental]
autoMemoryReclaim=gradual
sparseVhd=true
hostAddressLoopback=true
```

### Step 2: Restart WSL
```powershell
wsl --shutdown
wsl
```

## Method 3: Manual Bridge (More Complex)

### Step 1: Install bridge-utils in WSL
```bash
sudo apt update
sudo apt install bridge-utils
```

### Step 2: Create bridge script
Create `/etc/wsl-bridge.sh`:

```bash
#!/bin/bash
# Get the Windows host IP
WIN_HOST=$(ip route | grep default | awk '{print $3}')

# Create bridge
sudo ip link add name br0 type bridge
sudo ip link set dev eth0 master br0
sudo ip link set dev br0 up
sudo dhclient br0
```

### Step 3: Run on startup
Add to `/etc/wsl.conf`:

```ini
[boot]
command=/etc/wsl-bridge.sh
```

## Pros and Cons

### Bridge Mode Pros:
- ✅ WSL2 gets its own LAN IP
- ✅ No port forwarding needed
- ✅ Works like a real Linux machine on network
- ✅ Can run multiple services easily

### Bridge Mode Cons:
- ❌ Requires Windows Pro for Hyper-V (Method 1)
- ❌ May not work with all network adapters
- ❌ Can cause issues with VPNs
- ❌ More complex setup

## Current Workaround vs Bridge Mode

### Current (NAT + Port Forwarding):
- Simple and reliable
- Works on all Windows versions
- Just needs PowerShell command

### Bridge Mode:
- More "proper" networking
- Better for running multiple services
- Acts like a real machine on network

## Quick Decision Guide

**Use Bridge Mode if:**
- You have Windows Pro/Enterprise
- You need multiple services accessible
- You want WSL2 to act like a separate machine
- You don't use VPNs frequently

**Stick with Port Forwarding if:**
- You have Windows Home
- You only need one or two ports
- You use VPNs
- You want simple, reliable setup

## Testing Bridge Mode

After configuration, check if it worked:

```bash
# In WSL2
ip addr show
# Should show an IP in your LAN range (e.g., 192.168.1.x)

# Test from another device
ping <wsl2-lan-ip>
```

## Rollback

To go back to NAT mode:
1. Delete or rename `.wslconfig`
2. Run `wsl --shutdown`
3. Start WSL again