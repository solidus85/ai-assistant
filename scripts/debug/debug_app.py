#!/usr/bin/env python3
"""Debug app connectivity."""
import requests

print("Testing Ollama connectivity...\n")

# Test 1: Direct API call
try:
    response = requests.get('http://localhost:11434/api/tags', timeout=2)
    print(f"✓ Direct API call: {response.status_code}")
except Exception as e:
    print(f"✗ Direct API call failed: {e}")

# Test 2: App health endpoint
try:
    response = requests.get('http://localhost:5000/api/health', timeout=2)
    print(f"✓ App health endpoint: {response.status_code}")
    print(f"  Response: {response.json()}")
except Exception as e:
    print(f"✗ App health endpoint failed: {e}")

# Test 3: Chat endpoint
try:
    response = requests.post(
        'http://localhost:5000/api/chat/stream',
        json={'message': 'test', 'session_id': 'test'},
        timeout=2
    )
    print(f"✓ Chat endpoint: {response.status_code}")
except Exception as e:
    print(f"✗ Chat endpoint failed: {e}")

print("\nIf the app endpoints fail, make sure the app is running with:")
print("  source venv/bin/activate && python run.py")