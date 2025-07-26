#!/bin/bash

echo "=== Mistral 7B Setup (Fast Alternative) ==="
echo

# Create Mistral configuration
cat > setup_mistral_models.sh << 'EOF'
#!/bin/bash

echo "Available Mistral 7B models:"
echo
echo "1. mistral:7b-instruct-v0.2-q8_0    (7.7GB)  - Best quality"
echo "2. mistral:7b-instruct-v0.2-q6_K    (5.9GB)  - Excellent quality"
echo "3. mistral:7b-instruct-v0.2-q5_K_M  (5.1GB)  - Very good quality"
echo "4. mistral:7b-instruct-v0.2-q4_K_M  (4.4GB)  - Good quality"
echo

# Pull high-quality Mistral
echo "Pulling Mistral Q6_K (best quality that fits easily)..."
ollama pull mistral:7b-instruct-v0.2-q6_K

# Create optimized Mistral model
cat > Modelfile.mistral_fast << 'MODELFILE'
FROM mistral:7b-instruct-v0.2-q6_K

# Fast inference parameters
PARAMETER num_ctx 8192
PARAMETER num_gpu 99         # All on GPU (only 6GB)
PARAMETER num_thread 16
PARAMETER num_batch 512
PARAMETER f16_kv true

# Quality settings
PARAMETER temperature 0.7
PARAMETER top_k 40
PARAMETER top_p 0.9
PARAMETER repeat_penalty 1.1

SYSTEM You are a helpful, fast, and accurate AI assistant.
MODELFILE

ollama create mistral-fast -f Modelfile.mistral_fast
echo "Fast Mistral model created!"
EOF

chmod +x setup_mistral_models.sh

echo "=== When to Use Each Model ==="
echo
echo "Use MISTRAL when you need:"
echo "✓ Very fast responses (2-3x faster)"
echo "✓ Simple queries and conversations"
echo "✓ Basic coding assistance"
echo "✓ Low VRAM usage (under 8GB)"
echo "✓ Running multiple models"
echo
echo "Use MIXTRAL when you need:"
echo "✓ Maximum accuracy"
echo "✓ Complex reasoning"
echo "✓ Advanced coding/debugging"
echo "✓ Mathematical computations"
echo "✓ Multi-language support"
echo "✓ Professional/technical work"
echo
echo "Setup: ./setup_mistral_models.sh"