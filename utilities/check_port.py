#!/usr/bin/env python3
"""Check if a port is available."""
import socket
import sys

def check_port(port):
    """Check if a port is available."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('', port))
            return True
        except OSError:
            return False

def find_available_port(start=8000, end=9000):
    """Find an available port in the given range."""
    for port in range(start, end):
        if check_port(port):
            return port
    return None

if __name__ == "__main__":
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
        if check_port(port):
            print(f"Port {port} is available")
        else:
            print(f"Port {port} is in use")
    else:
        port = find_available_port()
        if port:
            print(f"Available port: {port}")
        else:
            print("No available ports found in range 8000-9000")