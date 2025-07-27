# Allowing External Access to Your LLM Web App

## Current Configuration
✅ Your app is already configured to accept external connections (`host='0.0.0.0'`)

## Steps to Enable External Access

### 1. Check Your Firewall
Since you're on WSL, you need to allow traffic through Windows Firewall:

```powershell
# Run in Windows PowerShell as Administrator
New-NetFirewallRule -DisplayName "Flask LLM App" -Direction Inbound -Protocol TCP -LocalPort 8080 -Action Allow
```

### 2. Find Your IP Address
```bash
# In WSL
ip addr show eth0 | grep inet | awk '{print $2}' | cut -d/ -f1

# Or in Windows
ipconfig
# Look for your IPv4 address (usually 192.168.x.x)
```

### 3. Access from Other Devices
- Same network: `http://YOUR-IP:8080`
- Example: `http://192.168.1.100:8080`

## Security Considerations ⚠️

### For Home/Private Network Use:
Current setup is fine for trusted networks.

### For Public/Untrusted Networks:
Add these security measures:

1. **Add Authentication** (create `app/auth.py`):
```python
from functools import wraps
from flask import request, Response

def check_auth(username, password):
    """Check if username/password is valid."""
    return username == 'admin' and password == 'your-secure-password'

def authenticate():
    """Send 401 response that enables basic auth."""
    return Response(
        'Could not verify your access level.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
```

2. **Use HTTPS** (for production):
```bash
# Generate self-signed cert for testing
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

# Update run.py
app.run(host='0.0.0.0', port=8080, ssl_context=('cert.pem', 'key.pem'))
```

3. **Rate Limiting** (add to requirements.txt):
```
flask-limiter==3.5.0
```

Then in `app/__init__.py`:
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# In create_app():
limiter.init_app(app)
```

## Quick Start Commands

```bash
# Start with external access (already configured)
python run.py

# Start with specific port
PORT=8080 python run.py

# Start with debug mode (development only)
FLASK_ENV=development python run.py
```

## Troubleshooting

### Can't connect from other devices?
1. Check Windows Firewall (most common issue)
2. Verify IP address is correct
3. Ensure both devices are on same network
4. Try disabling VPN if active

### WSL2 Specific Issues:
WSL2 uses a virtual network adapter. You might need to:
1. Use the Windows host IP instead of WSL IP
2. Enable port forwarding:
```powershell
netsh interface portproxy add v4tov4 listenport=5000 listenaddress=0.0.0.0 connectport=5000 connectaddress=(WSL IP)
```

## Current Status
- ✅ App listens on all interfaces (0.0.0.0)
- ✅ Port 8080 (configurable via PORT env var)
- ⚠️ No authentication (add if needed)
- ⚠️ HTTP only (use HTTPS for sensitive data)