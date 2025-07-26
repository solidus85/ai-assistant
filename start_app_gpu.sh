#!/bin/bash

echo "=== Starting Mixtral Chat with GPU Acceleration ==="
echo

# Source Ollama environment if it exists
if [ -f "ollama.env" ]; then
    source ollama.env
fi

# Check if Ollama is running
if ! pgrep -x "ollama" > /dev/null; then
    echo "Ollama not running. Starting with GPU support..."
    if [ -f "start_ollama_gpu.sh" ]; then
        ./start_ollama_gpu.sh
    else
        # Fallback to standard start with GPU env vars
        export CUDA_VISIBLE_DEVICES=0
        export OLLAMA_NUM_GPU=1
        export OLLAMA_CUDA=1
        ollama serve &
    fi
    sleep 5
fi

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Set environment variables for maximum performance
export FLASK_ENV=production
export NUM_THREAD=16
export MAX_TOKENS=1000
export NUM_CTX=8192
export NUM_GPU=99
export GPU_LAYERS=99
export OLLAMA_FLASH_ATTENTION=1

echo
echo "Configuration:"
echo "- GPU: RTX 4080 (16GB VRAM)"
echo "- Context Window: 8192 tokens"
echo "- Max Response: 1000 tokens"
echo "- Flash Attention: Enabled"
echo "- Memory: 48GB allocated to Ollama"
echo

# Show current GPU usage
echo "Current GPU Status:"
nvidia-smi --query-gpu=name,memory.used,memory.total,utilization.gpu --format=csv,noheader

echo
echo "Starting Flask application..."
echo "Access the app at: http://localhost:5000"
echo

python app.py