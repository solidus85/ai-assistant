#!/usr/bin/env python3
"""Test the prompt display feature."""
import requests
import json

print("Testing prompt display feature...\n")

# Test chat endpoint to see if it returns full_prompt
response = requests.post(
    'http://localhost:5000/api/chat/stream',
    json={
        'message': 'Hello, how are you?',
        'session_id': 'test-prompt-display'
    },
    stream=True
)

print("Response from chat endpoint:")
print("-" * 50)

prompt_found = False
for line in response.iter_lines():
    if line:
        try:
            data = json.loads(line)
            if 'full_prompt' in data:
                print("✓ Full prompt received:")
                print(f"  {data['full_prompt'][:100]}...")
                prompt_found = True
            elif 'token' in data:
                # Just show we're getting tokens
                pass
            elif 'error' in data:
                print(f"✗ Error: {data['error']}")
        except json.JSONDecodeError:
            pass

if prompt_found:
    print("\n✅ Prompt display feature is working!")
    print("\nTo use in the UI:")
    print("1. Click 'Show Prompt' button")
    print("2. Send a message")
    print("3. The full prompt will appear above the response")
else:
    print("\n❌ No prompt found in response")