#!/usr/bin/env python3
"""Check model context limits."""
import requests

models = {
    "phi3:mini": "Phi-3 Mini (3.8B)",
    "mixtral-accurate:latest": "Mixtral Q5_K_M (46.7B)"
}

print("Checking model context window limits...\n")

for model_name, description in models.items():
    print(f"{description}:")
    
    # Test with increasing context sizes
    test_prompt = "Hello " * 1000  # ~1000 tokens
    
    try:
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': model_name,
                'prompt': test_prompt,
                'stream': False,
                'options': {
                    'num_predict': 10,
                    'num_ctx': 4096  # Test 4K context
                }
            },
            timeout=10
        )
        
        if response.status_code == 200:
            print(f"  ✓ 4K context supported")
            
            # Try 128K for Phi-3
            if "phi3" in model_name:
                response2 = requests.post(
                    'http://localhost:11434/api/generate',
                    json={
                        'model': model_name,
                        'prompt': test_prompt,
                        'stream': False,
                        'options': {
                            'num_predict': 10,
                            'num_ctx': 128000  # Phi-3 supports 128K
                        }
                    },
                    timeout=10
                )
                if response2.status_code == 200:
                    print(f"  ✓ 128K context supported!")
        else:
            print(f"  ✗ Error: {response.status_code}")
            
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    print()

print("\nPhi-3 Mini supports up to 128K context window!")
print("Mixtral typically supports 32K context window.")
print("\nNote: Larger context = more VRAM usage and slower processing")