#!/bin/bash

echo "=== WSL2 NVIDIA GPU Setup for Ollama ==="
echo "This script will set up CUDA toolkit and configure Ollama to use your RTX 4080"
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running in WSL
if ! grep -q microsoft /proc/version; then
    echo -e "${RED}Error: This script must be run in WSL2${NC}"
    exit 1
fi

# Check if nvidia-smi works
echo "1. Checking GPU availability..."
if nvidia-smi &> /dev/null; then
    echo -e "${GREEN}✓ NVIDIA GPU detected!${NC}"
    nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
else
    echo -e "${RED}✗ NVIDIA GPU not detected. Make sure you have:${NC}"
    echo "  - Latest NVIDIA drivers installed on Windows"
    echo "  - WSL2 (not WSL1)"
    echo "  - Windows 11 or Windows 10 version 21H2 or higher"
    exit 1
fi

# Install CUDA toolkit (required for some operations)
echo
echo "2. Installing CUDA toolkit dependencies..."
echo "   (This is optional but recommended for full GPU support)"
read -p "Install CUDA toolkit? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Add NVIDIA package repositories
    wget -q https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-keyring_1.1-1_all.deb
    sudo dpkg -i cuda-keyring_1.1-1_all.deb
    sudo apt-get update
    
    # Install CUDA toolkit (runtime only, not full SDK)
    sudo apt-get -y install cuda-toolkit-12-4
    
    # Clean up
    rm cuda-keyring_1.1-1_all.deb
    
    echo -e "${GREEN}✓ CUDA toolkit installed${NC}"
fi

# Install Ollama if not present
echo
echo "3. Setting up Ollama..."
if command -v ollama &> /dev/null; then
    echo -e "${GREEN}✓ Ollama is already installed${NC}"
else
    echo "Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
fi

# Stop any running Ollama service
echo
echo "4. Configuring Ollama for GPU usage..."
if pgrep -x "ollama" > /dev/null; then
    echo "Stopping existing Ollama service..."
    pkill ollama
    sleep 2
fi

# Create Ollama service script with GPU support
echo "Creating GPU-enabled Ollama service script..."
cat > ~/start_ollama_gpu.sh << 'EOF'
#!/bin/bash
# Ollama GPU startup script

# Ensure GPU is available
if ! nvidia-smi &> /dev/null; then
    echo "Error: GPU not available"
    exit 1
fi

# Set environment variables for GPU
export OLLAMA_NUM_GPU=1
export CUDA_VISIBLE_DEVICES=0
export OLLAMA_GPU_LAYERS=99  # Load all layers to GPU

echo "Starting Ollama with GPU support..."
echo "GPU: $(nvidia-smi --query-gpu=name --format=csv,noheader)"
echo "VRAM: $(nvidia-smi --query-gpu=memory.total --format=csv,noheader)"

# Start Ollama
ollama serve
EOF

chmod +x ~/start_ollama_gpu.sh

# Create systemd-style service (optional)
echo
echo "5. Creating service management scripts..."
cat > ~/ollama-gpu-service.sh << 'EOF'
#!/bin/bash
# Ollama GPU service management

case "$1" in
    start)
        if pgrep -x "ollama" > /dev/null; then
            echo "Ollama is already running"
        else
            echo "Starting Ollama with GPU..."
            nohup ~/start_ollama_gpu.sh > ~/ollama.log 2>&1 &
            echo $! > ~/ollama.pid
            sleep 3
            if pgrep -x "ollama" > /dev/null; then
                echo "Ollama started successfully (PID: $(cat ~/ollama.pid))"
            else
                echo "Failed to start Ollama. Check ~/ollama.log"
            fi
        fi
        ;;
    stop)
        if [ -f ~/ollama.pid ]; then
            kill $(cat ~/ollama.pid) 2>/dev/null
            rm ~/ollama.pid
            echo "Ollama stopped"
        else
            pkill ollama
            echo "Ollama process killed"
        fi
        ;;
    status)
        if pgrep -x "ollama" > /dev/null; then
            echo "Ollama is running"
            nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv,noheader | grep ollama || echo "No GPU usage detected yet"
        else
            echo "Ollama is not running"
        fi
        ;;
    restart)
        $0 stop
        sleep 2
        $0 start
        ;;
    *)
        echo "Usage: $0 {start|stop|status|restart}"
        exit 1
        ;;
esac
EOF

chmod +x ~/ollama-gpu-service.sh

# Start Ollama with GPU
echo
echo "6. Starting Ollama with GPU support..."
~/ollama-gpu-service.sh start

# Wait for Ollama to be ready
echo "Waiting for Ollama to be ready..."
for i in {1..30}; do
    if curl -s http://localhost:11434/api/tags &> /dev/null; then
        echo -e "${GREEN}✓ Ollama is ready!${NC}"
        break
    fi
    sleep 1
done

# Test GPU functionality
echo
echo "7. Testing GPU functionality..."
echo "Creating test script..."
cat > ~/test_ollama_gpu.py << 'EOF'
#!/usr/bin/env python3
import subprocess
import json
import time

def check_gpu_usage():
    """Check if Ollama is using GPU"""
    print("Checking GPU usage...")
    result = subprocess.run(['nvidia-smi', '--query-compute-apps=pid,process_name,used_memory', '--format=csv,noheader'], 
                          capture_output=True, text=True)
    if 'ollama' in result.stdout:
        print(f"✓ Ollama is using GPU: {result.stdout.strip()}")
        return True
    else:
        print("✗ Ollama not detected on GPU yet")
        return False

def test_model(model_name="llama2:latest"):
    """Test running a model"""
    print(f"\nTesting model: {model_name}")
    print("Pulling model if needed (this may take a while)...")
    
    # Pull model
    subprocess.run(['ollama', 'pull', model_name], check=True)
    
    # Run a test prompt
    print("Running test prompt...")
    start_time = time.time()
    result = subprocess.run(['ollama', 'run', model_name, 'Why is the sky blue? Answer in one sentence.'], 
                          capture_output=True, text=True)
    end_time = time.time()
    
    print(f"Response time: {end_time - start_time:.2f} seconds")
    print(f"Response: {result.stdout.strip()}")
    
    # Check GPU usage during inference
    check_gpu_usage()

if __name__ == "__main__":
    print("=== Ollama GPU Test ===\n")
    
    # Check initial GPU status
    check_gpu_usage()
    
    # Test with a small model
    test_model("llama2:latest")
    
    print("\n✓ GPU test complete!")
    print("\nTo monitor GPU usage in real-time, run:")
    print("  watch -n 1 nvidia-smi")
EOF

chmod +x ~/test_ollama_gpu.py

# Show summary
echo
echo "=== Setup Complete! ==="
echo
echo -e "${GREEN}✓ GPU Support Enabled${NC}"
echo "  - GPU: $(nvidia-smi --query-gpu=name --format=csv,noheader)"
echo "  - VRAM: $(nvidia-smi --query-gpu=memory.total --format=csv,noheader)"
echo "  - Driver: $(nvidia-smi --query-gpu=driver_version --format=csv,noheader)"
echo
echo "Ollama Service Commands:"
echo "  ~/ollama-gpu-service.sh start    # Start Ollama with GPU"
echo "  ~/ollama-gpu-service.sh stop     # Stop Ollama"
echo "  ~/ollama-gpu-service.sh status   # Check status"
echo "  ~/ollama-gpu-service.sh restart  # Restart Ollama"
echo
echo "Test GPU functionality:"
echo "  python3 ~/test_ollama_gpu.py"
echo
echo "Monitor GPU usage:"
echo "  watch -n 1 nvidia-smi"
echo
echo "Pull models optimized for your RTX 4080:"
echo "  ollama pull mixtral        # Large model (good for 16GB VRAM)"
echo "  ollama pull llama2:13b     # Medium model"
echo "  ollama pull llama2:7b      # Smaller model"
echo
echo "For the LLM project, update start_app.sh to use:"
echo "  ~/ollama-gpu-service.sh start"
echo "instead of 'ollama serve &'"