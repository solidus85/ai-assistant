#!/usr/bin/env python3
"""Compare different models for accuracy and speed."""
import time
import requests
import json

def test_model(model_name, prompt):
    """Test a model with a given prompt."""
    print(f"\n{'='*60}")
    print(f"Testing: {model_name}")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    response = requests.post(
        'http://localhost:11434/api/generate',
        json={
            'model': model_name,
            'prompt': prompt,
            'stream': False,
            'options': {
                'temperature': 0.7,
                'num_predict': 500
            }
        }
    )
    
    end_time = time.time()
    
    if response.status_code == 200:
        data = response.json()
        print(f"Response: {data['response'][:500]}...")
        print(f"\nTime taken: {end_time - start_time:.2f} seconds")
        print(f"Tokens/sec: {data.get('eval_count', 0) / (data.get('eval_duration', 1) / 1e9):.2f}")
    else:
        print(f"Error: {response.status_code}")

def main():
    # Test prompt that requires reasoning
    prompt = """Explain the difference between machine learning and deep learning in simple terms. 
    Then provide a real-world example of each."""
    
    models = [
        'phi3:mini',
        'mixtral-accurate:latest'
    ]
    
    print("Model Comparison Test")
    print("=" * 60)
    print(f"Prompt: {prompt}")
    
    for model in models:
        try:
            test_model(model, prompt)
        except Exception as e:
            print(f"Error testing {model}: {e}")

if __name__ == "__main__":
    main()