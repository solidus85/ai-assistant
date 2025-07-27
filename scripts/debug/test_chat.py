#!/usr/bin/env python3
import requests
import json

# Test the chat endpoint
response = requests.post(
    'http://localhost:11434/api/generate',
    json={
        'model': 'phi3:mini',
        'prompt': 'Human: What is 2+2?\n\n',
        'stream': False,
        'options': {
            'num_predict': 50,
            'temperature': 0.1
        }
    }
)

if response.status_code == 200:
    result = response.json()
    print("Raw response:")
    print(result['response'])
    print("\n---")
    print("Looking for any 'User:' or 'Human:' labels in response...")
    if "User:" in result['response'] or "Human:" in result['response']:
        print("⚠️  Found unwanted labels in response!")
    else:
        print("✓ Response looks clean")
else:
    print(f"Error: {response.status_code}")