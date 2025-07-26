#!/bin/bash

echo "=== Ollama GPU & Memory Optimization Script ==="
echo

# Create Ollama environment configuration
cat > ollama.env << 'EOF'
# GPU Configuration
CUDA_VISIBLE_DEVICES=0
OLLAMA_NUM_GPU=1

# Memory Configuration
# Allow Ollama to use up to 48GB of system RAM (leaving ~14GB for system)
OLLAMA_MAX_LOADED_MODELS=1
OLLAMA_MEMORY_LIMIT=48G

# Performance Settings
OLLAMA_NUM_PARALLEL=4          # Number of parallel requests
OLLAMA_MAX_QUEUE=10            # Maximum queue size
OLLAMA_FLASH_ATTENTION=1       # Enable Flash Attention for better performance
OLLAMA_KEEP_ALIVE=30m          # Keep models loaded for 30 minutes

# Model Loading Settings
OLLAMA_MODELS=/home/$USER/.ollama/models
OLLAMA_RUNNERS_DIR=/home/$USER/.ollama/runners

# Enable GPU acceleration
OLLAMA_CUDA=1
OLLAMA_GPU_OVERHEAD=0          # No overhead, use all available VRAM

# Logging
OLLAMA_DEBUG=0
OLLAMA_LOG_LEVEL=info
EOF

# Create optimized start script
cat > start_ollama_gpu.sh << 'EOF'
#!/bin/bash

# Source the environment configuration
source ollama.env

# Export all variables
export CUDA_VISIBLE_DEVICES OLLAMA_NUM_GPU OLLAMA_MAX_LOADED_MODELS
export OLLAMA_MEMORY_LIMIT OLLAMA_NUM_PARALLEL OLLAMA_MAX_QUEUE
export OLLAMA_FLASH_ATTENTION OLLAMA_KEEP_ALIVE OLLAMA_MODELS
export OLLAMA_RUNNERS_DIR OLLAMA_CUDA OLLAMA_GPU_OVERHEAD
export OLLAMA_DEBUG OLLAMA_LOG_LEVEL

echo "Starting Ollama with GPU acceleration..."
echo "GPU: NVIDIA RTX 4080 (16GB VRAM)"
echo "RAM Limit: 48GB"
echo "Flash Attention: Enabled"
echo

# Kill any existing Ollama processes
pkill ollama 2>/dev/null

# Start Ollama with optimized settings
ollama serve &
OLLAMA_PID=$!

echo "Ollama started with PID: $OLLAMA_PID"
echo

# Wait for Ollama to be ready
sleep 5

# Show GPU usage
echo "Current GPU usage:"
nvidia-smi --query-gpu=name,memory.used,memory.total,utilization.gpu --format=csv,noheader,nounits

echo
echo "Ollama is ready for high-performance inference!"
echo "To stop: kill $OLLAMA_PID"
EOF

chmod +x start_ollama_gpu.sh

# Create model optimization script
cat > optimize_mixtral.sh << 'EOF'
#!/bin/bash

echo "=== Mixtral Model Optimization ==="
echo

# Pull the quantized version for better performance
echo "Pulling optimized Mixtral model..."
ollama pull mixtral:8x7b-instruct-v0.1-q4_K_M

# Create a custom modelfile for maximum performance
cat > Modelfile.mixtral << 'MODELFILE'
FROM mixtral:8x7b-instruct-v0.1-q4_K_M

# Optimal parameters for RTX 4080
PARAMETER num_gpu 99
PARAMETER num_thread 16
PARAMETER num_ctx 8192
PARAMETER num_batch 512
PARAMETER repeat_penalty 1.1
PARAMETER temperature 0.7
PARAMETER top_k 40
PARAMETER top_p 0.9

# System prompt for better responses
SYSTEM You are a helpful AI assistant. Provide clear, concise, and accurate responses.
MODELFILE

# Create the optimized model
echo "Creating optimized Mixtral model..."
ollama create mixtral-fast -f Modelfile.mixtral

echo "Optimization complete! Use 'mixtral-fast' for best performance."
EOF

chmod +x optimize_mixtral.sh

echo "=== Configuration Complete ==="
echo
echo "1. To start Ollama with GPU:"
echo "   ./start_ollama_gpu.sh"
echo
echo "2. To optimize Mixtral model:"
echo "   ./optimize_mixtral.sh"
echo
echo "GPU Capabilities:"
echo "- RTX 4080: 16GB VRAM"
echo "- CUDA 12.9 support"
echo "- Flash Attention enabled"
echo "- Can handle 8K+ context windows"
echo
echo "Memory Configuration:"
echo "- 48GB RAM allocated to Ollama"
echo "- 14GB reserved for system"
echo "- Supports large context windows"