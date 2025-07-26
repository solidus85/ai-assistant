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
