# Project Status and Context for Claude

## Project Overview
Building a Flask web app that interfaces with Ollama to run Mixtral locally with GPU acceleration. User prioritizes **accuracy over speed**.

## Current Status
- ✅ Flask app built with streaming responses and conversation history
- ✅ Token counter implemented showing context usage
- ✅ GPU detected: NVIDIA RTX 4080 (16GB VRAM)
- ✅ System has 62GB RAM (can expand to 110GB)
- ⏸️ **PAUSED**: User is moving WSL from C: to D: drive for space

## Hardware Capabilities
- **GPU**: RTX 4080 with 16GB VRAM
- **RAM**: 62GB available (110GB possible)
- **CUDA**: 12.9 support with Flash Attention
- **Optimal Model**: Mixtral Q5_K_M (30GB, 99% accuracy)

## Next Steps After WSL Move

1. **Install Ollama on Linux** (if not already done):
   ```bash
   ./setup_linux.sh
   ```

2. **Set up high-accuracy Mixtral Q5_K_M**:
   ```bash
   ./setup_high_accuracy.sh
   source ollama_accuracy.env
   ./setup_q5_k_m.sh
   ```

3. **Start app with GPU optimization**:
   ```bash
   ./start_app_gpu.sh
   ```

## Key Files Created
- `app.py` - Flask backend with Ollama integration
- `templates/index.html` - Frontend with token counter
- `config.py` - Configuration with GPU settings
- `setup_high_accuracy.sh` - Sets up Q5_K_M model
- `start_app_gpu.sh` - Starts app with GPU settings
- `ollama_accuracy.env` - Environment for high accuracy

## Model Configuration
- **Current**: MODEL_NAME = "mixtral-accurate" (in app.py)
- **Type**: Mixtral Q5_K_M (5-bit quantization)
- **Context**: 8192 tokens (can do 32K but slower)
- **GPU Split**: 65% GPU, 35% CPU

## Important Notes
- User wants **accuracy over speed**
- Q5_K_M chosen as best accuracy that fits GPU
- Ollama will use 48GB RAM + 14-15GB VRAM
- Token counter uses tiktoken (approximation)
- Conversation history limited to 10 exchanges

## Commands to Test After Setup
```bash
# Check if Ollama is running
ollama list

# Test the model
ollama run mixtral-accurate "Hello, test"

# Monitor GPU usage
nvidia-smi

# Start the web app
./start_app_gpu.sh
```

## Troubleshooting
- If "mixtral-accurate" not found, run `./setup_q5_k_m.sh` again
- If GPU not detected, check `nvidia-smi` and WSL GPU support
- If out of memory, reduce NUM_CTX in config.py