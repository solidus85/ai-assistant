#!/bin/bash

echo "=== Ollama & Mixtral Chat Setup Script for Linux/WSL ==="
echo

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Install Ollama
echo "1. Installing Ollama..."
if command_exists ollama; then
    echo "   Ollama is already installed!"
else
    echo "   Downloading and installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
fi

# Start Ollama service
echo
echo "2. Starting Ollama service..."
ollama serve &
OLLAMA_PID=$!
echo "   Ollama service started (PID: $OLLAMA_PID)"
sleep 5  # Give Ollama time to start

# Pull Mixtral model
echo
echo "3. Pulling Mixtral model (this may take a while)..."
ollama pull mixtral

# Install Python dependencies
echo
echo "4. Setting up Python environment..."
if command_exists python3; then
    echo "   Python3 found. Installing dependencies..."
    
    # Create virtual environment (optional but recommended)
    if [ ! -d "venv" ]; then
        echo "   Creating virtual environment..."
        python3 -m venv venv
    fi
    
    echo "   Activating virtual environment..."
    source venv/bin/activate
    
    echo "   Installing Python packages..."
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "   Error: Python3 not found. Please install Python3 first."
    kill $OLLAMA_PID
    exit 1
fi

# Create a start script
echo
echo "5. Creating start script..."
cat > start_app.sh << 'EOF'
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
EOF

chmod +x start_app.sh

echo
echo "=== Setup Complete! ==="
echo
echo "To start the application:"
echo "  ./start_app.sh"
echo
echo "To stop Ollama service now:"
echo "  kill $OLLAMA_PID"
echo
echo "Note: Ollama will continue running in the background."
echo "      Use 'pkill ollama' to stop it completely."