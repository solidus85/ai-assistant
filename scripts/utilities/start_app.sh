#!/bin/bash

# Check if Ollama is running
if ! pgrep -x "ollama" > /dev/null; then
    echo "Starting Ollama service..."
    ollama serve &
    sleep 5
fi

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Set environment variables for performance
export FLASK_ENV=development
export NUM_THREAD=8
export MAX_TOKENS=300
export NUM_CTX=2048

echo "Starting Mixtral Chat application..."
echo "Access the app at: http://localhost:5000"
python app.py
