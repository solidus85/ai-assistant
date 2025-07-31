#!/bin/bash
# Check memory usage and model requirements

echo "💾 Memory Status for LLM App"
echo "============================"

# Current memory usage
echo -e "\n📊 Current Memory Usage:"
free -h | grep -E "Mem:|Swap:" | sed 's/^/  /'

# WSL2 memory allocation
echo -e "\n🖥️ WSL2 Memory Allocation:"
if [ -f "/mnt/c/Users/$USER/.wslconfig" ]; then
    grep -i "memory" "/mnt/c/Users/$USER/.wslconfig" | sed 's/^/  /'
else
    echo "  No custom allocation (WSL2 default: 50% of Windows RAM)"
fi

# Check Ollama models
echo -e "\n🤖 Installed Models & Memory Requirements:"
if command -v ollama &> /dev/null; then
    ollama list | while read -r line; do
        if [[ ! "$line" =~ ^NAME ]]; then
            model=$(echo "$line" | awk '{print $1}')
            size=$(echo "$line" | awk '{print $3 " " $4}')
            echo "  $model: $size on disk"
            
            # Estimate VRAM usage
            case "$model" in
                *phi3*) echo "    → ~2-3 GB VRAM when loaded" ;;
                *mistral:7b*) echo "    → ~4-5 GB VRAM when loaded" ;;
                *llama3.1:8b*) echo "    → ~5-6 GB VRAM when loaded" ;;
                *mixtral*) echo "    → ~15-16 GB VRAM when loaded" ;;
                *) echo "    → VRAM usage varies" ;;
            esac
        fi
    done
else
    echo "  Ollama not found"
fi

# GPU memory
echo -e "\n🎮 GPU Memory:"
if command -v nvidia-smi &> /dev/null; then
    nvidia-smi --query-gpu=name,memory.total,memory.used,memory.free --format=csv,noheader,nounits | while read -r line; do
        gpu_name=$(echo "$line" | cut -d',' -f1)
        mem_total=$(echo "$line" | cut -d',' -f2)
        mem_used=$(echo "$line" | cut -d',' -f3)
        mem_free=$(echo "$line" | cut -d',' -f4)
        echo "  $gpu_name:"
        echo "    Total: $((mem_total / 1024)) GB"
        echo "    Used: $((mem_used / 1024)) GB"
        echo "    Free: $((mem_free / 1024)) GB"
    done
else
    echo "  NVIDIA GPU not detected"
fi

# Python/Flask memory
echo -e "\n🐍 Python Processes:"
ps aux | grep -E "python|flask" | grep -v grep | awk '{printf "  PID %s: %.1f MB (%s)\n", $2, $6/1024, $11}'

# Recommendations
echo -e "\n💡 Memory Optimization Tips:"
echo "  • Current WSL2 allocation: 8GB (from .wslconfig)"
echo "  • You have 62GB available - can increase if needed"
echo "  • Models are loaded to GPU VRAM, not system RAM"
echo "  • Flask app uses minimal RAM (~50-100MB)"

echo -e "\n📝 To change WSL2 memory allocation:"
echo "  Edit /mnt/c/Users/$USER/.wslconfig"
echo "  Change: memory=16GB (or desired amount)"
echo "  Then: wsl --shutdown && wsl"