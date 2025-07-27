#!/bin/bash
echo "=== Setting up Fast Model for Testing ==="
echo ""
echo "This will configure Phi-3 Mini for maximum responsiveness."
echo "It's a 3.8B parameter model that runs entirely on GPU."
echo ""

# Check if Ollama is running
if ! pgrep -x "ollama" > /dev/null; then
    echo "Starting Ollama service..."
    ollama serve &
    sleep 3
fi

# Pull the model if not already present
if ! ollama list | grep -q "phi3:mini"; then
    echo "Pulling Phi-3 Mini model..."
    ollama pull phi3:mini
else
    echo "Phi-3 Mini already installed!"
fi

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Model: Phi-3 Mini (3.8B parameters)"
echo "Expected response time: 1-2 seconds"
echo "VRAM usage: ~2-3GB"
echo ""
echo "To switch back to high-accuracy Mixtral:"
echo "  Edit app.py and change MODEL_NAME = 'mixtral-accurate'"
echo ""
echo "Start the app with:"
echo "  source venv/bin/activate && python app.py"