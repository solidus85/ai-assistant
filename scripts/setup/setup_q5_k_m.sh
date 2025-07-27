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
