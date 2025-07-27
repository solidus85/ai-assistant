#!/usr/bin/env python3
"""Test the bug fixes for token counter and prompt display."""
import requests
import json
import time

print("Testing bug fixes...\n")

# Test 1: Token counter endpoint
print("1. Testing token counter endpoint:")
try:
    response = requests.post(
        'http://localhost:5000/api/chat/tokens',
        json={
            'session_id': 'test-session',
            'message': 'Hello world'
        }
    )
    if response.status_code == 200:
        data = response.json()
        print(f"   ✓ Token count: {data.get('count', 'N/A')}")
        print(f"   ✓ Limit: {data.get('limit', 'N/A')}")
        print(f"   Response: {data}")
    else:
        print(f"   ✗ Error: {response.status_code}")
except Exception as e:
    print(f"   ✗ Connection error: {e}")

# Test 2: Chat stream with prompt
print("\n2. Testing chat stream for prompt display:")
try:
    response = requests.post(
        'http://localhost:5000/api/chat/stream',
        json={
            'message': 'Test message',
            'session_id': 'test-session'
        },
        stream=True
    )
    
    found_prompt = False
    for line in response.iter_lines():
        if line:
            try:
                data = json.loads(line)
                if 'full_prompt' in data:
                    print(f"   ✓ Full prompt received: {data['full_prompt'][:50]}...")
                    found_prompt = True
                    break
            except:
                pass
    
    if not found_prompt:
        print("   ✗ No prompt found in stream")
        
except Exception as e:
    print(f"   ✗ Connection error: {e}")

print("\n3. Manual testing required:")
print("   - Open http://localhost:5000")
print("   - Check if token counter shows numbers (not 0/0)")
print("   - Click 'Show Prompt' button")
print("   - Send a message")
print("   - Verify prompt appears between user message and response")
print("\nMake sure the app is running: python run.py")