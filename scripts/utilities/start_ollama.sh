#!/bin/bash
echo "=== Starting Ollama Service ==="

# Check if Ollama is already running
if pgrep -x "ollama" > /dev/null; then
    echo "✓ Ollama is already running (PID: $(pgrep ollama))"
else
    echo "Starting Ollama service..."
    ollama serve &
    sleep 3
    echo "✓ Ollama started (PID: $(pgrep ollama))"
fi

# List available models
echo ""
echo "Available models:"
ollama list | grep -E "^(phi3:mini|mixtral)" || echo "No models found"

echo ""
echo "To start the Flask app, run:"
echo "  source venv/bin/activate && python run.py"