#!/bin/bash

echo "=== WSL2 Resource Allocation Check ==="
echo

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Memory Information
echo -e "${YELLOW}Memory Information:${NC}"
echo "-------------------"
free -h
echo

# Detailed memory
echo -e "${YELLOW}Detailed Memory Stats:${NC}"
echo "---------------------"
cat /proc/meminfo | grep -E "MemTotal|MemFree|MemAvailable|SwapTotal|SwapFree" | awk '{print $1 " " $2/1024/1024 " GB"}'
echo

# CPU Information
echo -e "${YELLOW}CPU Information:${NC}"
echo "----------------"
echo "CPU Cores: $(nproc)"
echo "CPU Model: $(cat /proc/cpuinfo | grep "model name" | head -1 | cut -d: -f2)"
echo

# GPU Information
echo -e "${YELLOW}GPU Information:${NC}"
echo "----------------"
if command -v nvidia-smi &> /dev/null; then
    nvidia-smi --query-gpu=name,memory.total,memory.free,utilization.gpu --format=csv,noheader
else
    echo "NVIDIA GPU not available or drivers not installed"
fi
echo

# Disk Space
echo -e "${YELLOW}Disk Space:${NC}"
echo "-----------"
df -h | grep -E "^/dev/|^Filesystem"
echo

# WSL Specific Info
echo -e "${YELLOW}WSL Configuration:${NC}"
echo "------------------"
echo "WSL Version: $(uname -r | grep -oP 'WSL\K[0-9]' || echo "2")"
echo "Kernel: $(uname -r)"
echo "Distribution: $(lsb_release -d | cut -f2)"
echo

# System Limits
echo -e "${YELLOW}System Limits:${NC}"
echo "--------------"
echo "Max open files: $(ulimit -n)"
echo "Max processes: $(ulimit -u)"
echo "Max memory lock: $(ulimit -l)"
echo

# Performance Tips
echo -e "${GREEN}Performance Tips for 64GB Setup:${NC}"
echo "--------------------------------"
echo "1. Your system now has 64GB RAM + 16GB swap available"
echo "2. This allows running multiple large language models simultaneously"
echo "3. Recommended model allocations for your RTX 4080 (16GB VRAM):"
echo "   - Mixtral: ~8-10GB VRAM + 20-30GB system RAM"
echo "   - LLaMA 70B quantized: ~35-40GB total memory"
echo "   - Multiple 13B models: ~10-15GB each"
echo
echo "4. Monitor memory usage during model loading:"
echo "   watch -n 1 'free -h; nvidia-smi'"
echo

# Check if Ollama is installed
if command -v ollama &> /dev/null; then
    echo -e "${BLUE}Ollama Status:${NC}"
    echo "--------------"
    if pgrep -x "ollama" > /dev/null; then
        echo "Ollama is running"
        echo "Models available:"
        ollama list 2>/dev/null || echo "Unable to list models"
    else
        echo "Ollama is installed but not running"
        echo "Start with: ~/ollama-gpu-service.sh start"
    fi
fi