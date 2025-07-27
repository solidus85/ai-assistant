#!/usr/bin/env python3
import time
import requests
import json

models = [
    ("phi3:mini", "Small & Fast"),
    ("mixtral-accurate", "High Accuracy Q5_K_M")
]

test_prompt = "What is 2+2?"

print("Testing model response speeds...\n")

for model_name, description in models:
    print(f"Testing {model_name} ({description})...")
    
    start_time = time.time()
    
    try:
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': model_name,
                'prompt': test_prompt,
                'stream': False,
                'options': {
                    'num_predict': 50,  # Limit response length for speed test
                    'temperature': 0.1
                }
            }
        )
        
        end_time = time.time()
        elapsed = end_time - start_time
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Response time: {elapsed:.2f}s")
            print(f"  Response: {result['response'][:100]}...")
            print()
        else:
            print(f"✗ Error: {response.status_code}")
            print()
            
    except Exception as e:
        print(f"✗ Error: {e}")
        print()

print("\nFor the most responsive experience, use phi3:mini")
print("To switch models, update MODEL_NAME in app.py")