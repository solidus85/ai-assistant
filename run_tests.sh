#!/bin/bash

# Ensure we're in the project directory
cd /mnt/c/Users/Cody/OneDrive/Documents/Projects/ai-assistant

# Activate virtual environment
source .venv/bin/activate

# Check Python path
echo "Python path: $(which python)"
echo "Python version: $(python --version)"

# Check if Flask is available
python -c "import flask; print('Flask version:', flask.__version__)" 2>/dev/null || echo "Flask not found!"

# Run tests
echo "Running tests..."
python -m pytest tests/ --cov=src --cov-report=term-missing --tb=short -q