#!/usr/bin/env python3
"""Test response speed of different models."""
import time
import requests
import sys

def test_model_speed(model_name, prompt="Explain in one sentence what Python is."):
    """Test a model's response speed."""
    print(f"\nTesting {model_name}...")
    print("-" * 50)
    
    start_time = time.time()
    first_token_time = None
    
    try:
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': model_name,
                'prompt': prompt,
                'stream': True,
                'options': {
                    'num_predict': 100,  # Limit tokens for fair comparison
                    'temperature': 0.7
                }
            },
            stream=True,
            timeout=120
        )
        
        tokens = 0
        response_text = ""
        
        for line in response.iter_lines():
            if line:
                try:
                    import json
                    data = json.loads(line)
                    
                    if 'response' in data:
                        if first_token_time is None:
                            first_token_time = time.time()
                        response_text += data['response']
                        tokens += 1
                    
                    if data.get('done', False):
                        break
                except:
                    pass
        
        end_time = time.time()
        total_time = end_time - start_time
        time_to_first_token = first_token_time - start_time if first_token_time else 0
        
        print(f"Response: {response_text[:100]}...")
        print(f"\nMetrics:")
        print(f"  Time to first token: {time_to_first_token:.2f}s")
        print(f"  Total time: {total_time:.2f}s")
        print(f"  Tokens generated: {tokens}")
        if tokens > 0:
            print(f"  Tokens/second: {tokens / (total_time - time_to_first_token):.2f}")
        
        return {
            'model': model_name,
            'first_token': time_to_first_token,
            'total_time': total_time,
            'tokens': tokens
        }
        
    except Exception as e:
        print(f"Error testing {model_name}: {e}")
        return None

def main():
    models_to_test = [
        'phi3:mini',
        'mixtral:latest',
        # Add more models as needed
    ]
    
    if len(sys.argv) > 1:
        # Test specific model
        models_to_test = [sys.argv[1]]
    
    print("Model Speed Test")
    print("=" * 50)
    print("Testing with prompt: 'Explain in one sentence what Python is.'")
    
    results = []
    for model in models_to_test:
        result = test_model_speed(model)
        if result:
            results.append(result)
    
    if results:
        print("\n\nSummary:")
        print("=" * 50)
        print(f"{'Model':<25} {'First Token':<12} {'Total Time':<12}")
        print("-" * 50)
        
        for result in sorted(results, key=lambda x: x['total_time']):
            print(f"{result['model']:<25} {result['first_token']:<12.2f}s {result['total_time']:<12.2f}s")

if __name__ == "__main__":
    main()