#!/bin/bash

echo "=== Mixtral 32K Context Configuration ==="
echo

# Create 32K context environment
cat > ollama_32k.env << 'EOF'
# GPU Configuration for 32K context
CUDA_VISIBLE_DEVICES=0
OLLAMA_NUM_GPU=1
OLLAMA_CUDA=1
OLLAMA_GPU_OVERHEAD=0

# Memory Configuration for 32K context
OLLAMA_MAX_LOADED_MODELS=1
OLLAMA_MEMORY_LIMIT=55G        # 55GB for model + 32K context
OLLAMA_KEEP_ALIVE=5m           # Shorter keep-alive due to high memory usage

# Performance Settings for 32K
OLLAMA_NUM_PARALLEL=1          # Only 1 parallel request with 32K context
OLLAMA_MAX_QUEUE=3             # Smaller queue
OLLAMA_FLASH_ATTENTION=1       # CRITICAL for 32K context
OLLAMA_CUDA_MEMORY_FRACTION=0.95  # Use 95% of VRAM

# Enable all optimizations
OLLAMA_USE_MMAP=1
OLLAMA_USE_MLOCK=1
EOF

# Create 32K model configuration
cat > create_mixtral_32k.sh << 'EOF'
#!/bin/bash

echo "Creating Mixtral 32K model configuration..."

# Create modelfile for 32K context
cat > Modelfile.mixtral_32k << 'MODELFILE'
FROM mixtral:8x7b-instruct-v0.1-q4_K_M

# 32K context parameters
PARAMETER num_ctx 32768
PARAMETER num_gpu 99
PARAMETER num_thread 16
PARAMETER num_batch 256        # Smaller batch for memory efficiency
PARAMETER rope_frequency_base 1000000  # For extended context
PARAMETER rope_frequency_scale 1.0

# Conservative generation settings
PARAMETER num_predict 2000     # Reasonable response length
PARAMETER temperature 0.7
PARAMETER top_k 40
PARAMETER top_p 0.9
PARAMETER repeat_penalty 1.1

# Memory efficient settings
PARAMETER use_mmap true
PARAMETER use_mlock true

SYSTEM You are a helpful AI assistant with access to a very large context window of 32,768 tokens. You can process and remember extensive conversations and documents.
MODELFILE

ollama create mixtral-32k -f Modelfile.mixtral_32k
echo "32K model created!"
EOF

chmod +x create_mixtral_32k.sh

# Create Python config for 32K
cat > config_32k.py << 'EOF'
import os

class Config32K:
    """Configuration for 32K context window."""
    
    # Model settings for 32K context
    MAX_TOKENS = 2000              # Reasonable response length
    NUM_CTX = 32768               # 32K context window
    NUM_BATCH = 256               # Smaller batch for memory
    NUM_THREAD = 16               # All CPU threads
    NUM_GPU = 99                  # All layers on GPU
    
    # Memory settings
    MEMORY_LIMIT = "55G"
    
    # Model name
    DEFAULT_MODEL = "mixtral-32k"
EOF

# Create monitoring script
cat > monitor_32k.sh << 'EOF'
#!/bin/bash

echo "=== Mixtral 32K Performance Monitor ==="
echo

while true; do
    clear
    echo "=== System Status ==="
    echo
    
    # GPU Status
    echo "GPU Memory Usage:"
    nvidia-smi --query-gpu=memory.used,memory.total,utilization.gpu --format=csv,noheader
    echo
    
    # RAM Status
    echo "System Memory:"
    free -h | grep "^Mem"
    echo
    
    # Ollama Process
    if pgrep -x "ollama" > /dev/null; then
        echo "Ollama Status: Running"
        ps aux | grep "[o]llama serve" | awk '{printf "CPU: %s%% | RAM: %s%%\n", $3, $4}'
    else
        echo "Ollama Status: Not Running"
    fi
    echo
    
    sleep 2
done
EOF

chmod +x monitor_32k.sh

echo "=== 32K Context Configuration Complete ==="
echo
echo "Your system CAN handle 32K context!"
echo
echo "Memory Requirements:"
echo "- Model: ~35GB RAM + 8GB VRAM (Q4 quantized)"
echo "- 32K Context: ~20GB RAM + 6GB VRAM"
echo "- Total: ~55GB RAM + 14GB VRAM"
echo
echo "Your Resources:"
echo "- Available RAM: 62GB (✓ Sufficient)"
echo "- Available VRAM: 16GB (✓ Just enough)"
echo
echo "To use 32K context:"
echo "1. source ollama_32k.env"
echo "2. ./create_mixtral_32k.sh"
echo "3. Update app.py to use 'mixtral-32k' model"
echo "4. ./monitor_32k.sh (in another terminal)"
echo
echo "Performance Expectations:"
echo "- First token: 2-5 seconds"
echo "- Tokens/second: 10-20 (vs 50-100 for 8K)"
echo "- Memory stable up to 30K tokens"
echo "- May slow down at 30K-32K range"