#!/usr/bin/env python3
"""Quick model switcher for testing different models."""
import os
import sys
import subprocess

MODELS = {
    'phi3': {
        'name': 'phi3:mini',
        'installed': True,
        'speed': '1-2 seconds',
        'quality': 'Good for simple tasks',
        'size': '2.2 GB'
    },
    'mixtral': {
        'name': 'mixtral:latest',
        'installed': True,
        'speed': '10-20 seconds',
        'quality': 'Excellent (Q4 quantization)',
        'size': '26 GB'
    },
    'mixtral-accurate': {
        'name': 'mixtral-accurate:latest',
        'installed': True,
        'speed': '20-40 seconds',
        'quality': 'Best quality (Q5_K_M)',
        'size': '33 GB'
    },
    'llama3': {
        'name': 'llama3.1:8b',
        'installed': True,
        'speed': '2-3 seconds',
        'quality': 'Very good, latest Llama',
        'size': '4.7 GB'
    },
    'qwen': {
        'name': 'qwen2.5:7b',
        'installed': False,
        'speed': '2-4 seconds',
        'quality': 'Excellent for 7B',
        'size': '4.5 GB'
    },
    'gemma': {
        'name': 'gemma2:9b',
        'installed': False,
        'speed': '3-5 seconds',
        'quality': 'Google\'s latest, very good',
        'size': '5.5 GB'
    },
    'mistral': {
        'name': 'mistral:7b',
        'installed': True,
        'speed': '1-2 seconds',
        'quality': 'Good, very fast',
        'size': '4.1 GB'
    }
}

def show_models():
    """Display available models."""
    print("\nAvailable Models:")
    print("=" * 70)
    print(f"{'Key':<15} {'Model Name':<25} {'Speed':<15} {'Status':<10}")
    print("-" * 70)
    
    for key, info in MODELS.items():
        status = "✓ Installed" if info['installed'] else "Download"
        print(f"{key:<15} {info['name']:<25} {info['speed']:<15} {status:<10}")
    
    print("\nModel Details:")
    print("-" * 70)
    for key, info in MODELS.items():
        print(f"\n{key}: {info['name']}")
        print(f"  Speed: {info['speed']}")
        print(f"  Quality: {info['quality']}")
        print(f"  Size: {info['size']}")

def switch_model(model_key):
    """Switch to a different model."""
    if model_key not in MODELS:
        print(f"Error: Unknown model '{model_key}'")
        print(f"Available models: {', '.join(MODELS.keys())}")
        return False
    
    model_info = MODELS[model_key]
    model_name = model_info['name']
    
    # Check if model needs to be downloaded
    if not model_info['installed']:
        print(f"\nModel {model_name} is not installed.")
        response = input("Do you want to download it? (y/n): ")
        if response.lower() == 'y':
            print(f"Downloading {model_name}...")
            result = subprocess.run(['ollama', 'pull', model_name], capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Error downloading model: {result.stderr}")
                return False
            print(f"Successfully downloaded {model_name}")
        else:
            return False
    
    # Update .env file
    env_content = []
    model_line_found = False
    
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                if line.startswith('MODEL_NAME='):
                    env_content.append(f'MODEL_NAME={model_name}\n')
                    model_line_found = True
                else:
                    env_content.append(line)
    
    if not model_line_found:
        env_content.append(f'MODEL_NAME={model_name}\n')
    
    with open('.env', 'w') as f:
        f.writelines(env_content)
    
    print(f"\n✓ Switched to {model_name}")
    print(f"  Expected speed: {model_info['speed']}")
    print(f"  Quality: {model_info['quality']}")
    print("\nRestart your Flask app to use the new model.")
    return True

def main():
    if len(sys.argv) < 2:
        show_models()
        print("\nUsage: python switch_model.py <model_key>")
        print("Example: python switch_model.py llama3")
        return
    
    model_key = sys.argv[1].lower()
    switch_model(model_key)

if __name__ == "__main__":
    main()