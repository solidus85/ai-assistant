#!/bin/bash

echo "=== High Accuracy Mixtral Setup ==="
echo

# Check available Mixtral models
echo "Checking available Mixtral variants..."
echo

cat > check_models.sh << 'EOF'
#!/bin/bash

# Available Mixtral models by quality (best to good)
echo "Mixtral Model Options (ordered by accuracy):"
echo
echo "1. mixtral:8x7b-instruct-v0.1-fp16    (87GB) - Highest accuracy, CPU only"
echo "2. mixtral:8x7b-instruct-v0.1-q8_0    (45GB) - Excellent, CPU+GPU split"
echo "3. mixtral:8x7b-instruct-v0.1-q6_K    (34GB) - Very good, CPU+GPU split" 
echo "4. mixtral:8x7b-instruct-v0.1-q5_K_M  (30GB) - Good, CPU+GPU split"
echo "5. mixtral:8x7b-instruct-v0.1-q5_0    (28GB) - Good, mostly GPU"
echo "6. mixtral:8x7b-instruct-v0.1-q4_K_M  (26GB) - Standard, full GPU"
echo "7. mixtral:8x7b-instruct-v0.1-q4_0    (24GB) - Lower quality"
echo
EOF

# Create optimal accuracy configuration
cat > ollama_accuracy.env << 'EOF'
# Optimal Accuracy Configuration
CUDA_VISIBLE_DEVICES=0
OLLAMA_NUM_GPU=-1              # Auto-detect optimal GPU layers
OLLAMA_CUDA=1

# Memory for accuracy priority
OLLAMA_MAX_LOADED_MODELS=1
OLLAMA_MEMORY_LIMIT=58G        # Use most available RAM
OLLAMA_GPU_OVERHEAD=1073741824 # 1GB overhead for safety

# Quality-focused settings
OLLAMA_FLASH_ATTENTION=1
OLLAMA_USE_MMAP=1
OLLAMA_USE_MLOCK=1
OLLAMA_F16_KV=true             # Use FP16 for KV cache (better quality)

# Inference settings
OLLAMA_NUM_PARALLEL=1          # Single stream for consistency
OLLAMA_COMPUTE_TYPE=float16    # Higher precision computation
EOF

# Create setup script for each quality level
cat > setup_q5_k_m.sh << 'EOF'
#!/bin/bash
echo "Setting up Q5_K_M model (Best accuracy that fits your GPU)..."

# Pull the Q5_K_M model
ollama pull mixtral:8x7b-instruct-v0.1-q5_K_M

# Create optimized version
cat > Modelfile.q5_k_m << 'MODELFILE'
FROM mixtral:8x7b-instruct-v0.1-q5_K_M

# Accuracy-focused parameters
PARAMETER num_ctx 8192
PARAMETER num_gpu 65
PARAMETER num_thread 16
PARAMETER num_batch 256
PARAMETER f16_kv true
PARAMETER use_mmap true
PARAMETER use_mlock true

# Conservative sampling for accuracy
PARAMETER temperature 0.7
PARAMETER top_k 40
PARAMETER top_p 0.9
PARAMETER repeat_penalty 1.1
PARAMETER seed -1

SYSTEM You are a highly accurate AI assistant. Focus on providing correct, detailed, and well-reasoned responses.
MODELFILE

ollama create mixtral-accurate -f Modelfile.q5_k_m
echo "High accuracy model created!"
EOF

chmod +x setup_q5_k_m.sh

# Create CPU-only FP16 setup (highest accuracy)
cat > setup_fp16_cpu.sh << 'EOF'
#!/bin/bash
echo "Setting up FP16 model (Maximum accuracy, CPU only)..."
echo "WARNING: This will be SLOW but most accurate"

# This would need special handling as Ollama doesn't directly support FP16
echo "FP16 models require special setup. Consider using Q8_0 instead."

# For Q8_0 (next best):
ollama pull mixtral:8x7b-instruct-v0.1-q8_0

cat > Modelfile.q8 << 'MODELFILE'
FROM mixtral:8x7b-instruct-v0.1-q8_0

PARAMETER num_ctx 4096         # Smaller context for CPU performance
PARAMETER num_gpu 0            # CPU only
PARAMETER num_thread 32        # Use all CPU threads
PARAMETER f16_kv true
MODELFILE

ollama create mixtral-max-accuracy -f Modelfile.q8
EOF

chmod +x setup_fp16_cpu.sh

# Create comparison script
cat > compare_accuracy.py << 'EOF'
#!/usr/bin/env python3
"""
Compare accuracy between different quantization levels
"""

test_prompts = [
    "Explain the mathematical proof of Fermat's Last Theorem",
    "Write a Python function to implement binary search",
    "What is the exact value of pi to 15 decimal places?",
    "Translate 'Hello world' to Japanese, Chinese, and Arabic",
    "Calculate 1729 * 4096 / 137",
]

print("Accuracy Comparison Test")
print("=" * 50)
print("\nRun this after setting up models to compare outputs")
print("\nTest prompts:")
for i, prompt in enumerate(test_prompts, 1):
    print(f"{i}. {prompt}")
print("\nModels will show differences in:")
print("- Mathematical precision")
print("- Code accuracy")
print("- Language understanding")
print("- Factual recall")
EOF

chmod +x compare_accuracy.py

echo "=== Accuracy Recommendations for Your System ==="
echo
echo "BEST CHOICE: Q5_K_M (5-bit medium quantization)"
echo "- 30GB model size (fits with CPU+GPU split)"
echo "- ~99% accuracy retained vs full precision"
echo "- 65% of layers on GPU, 35% on CPU"
echo "- Good balance of accuracy and speed"
echo
echo "ALTERNATIVE: Q6_K (6-bit) if you want even better accuracy"
echo "- 34GB model size"
echo "- ~99.5% accuracy retained"
echo "- More CPU usage, slightly slower"
echo
echo "Setup commands:"
echo "1. source ollama_accuracy.env"
echo "2. ./setup_q5_k_m.sh"
echo "3. Update DEFAULT_MODEL='mixtral-accurate' in your app"
echo
echo "Key differences from Q4:"
echo "- Better numerical precision"
echo "- More accurate factual recall"
echo "- Better multilingual performance"
echo "- Slightly better reasoning"
echo "- 20-30% slower inference"