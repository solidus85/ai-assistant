#!/bin/bash

# Script to download all Python wheels locally for offline Docker builds

echo "📦 Downloading Python wheels for offline installation..."

# Create wheels directory if it doesn't exist
WHEELS_DIR="./wheels"
mkdir -p "$WHEELS_DIR"

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Download all wheels from requirements.txt
echo "⬇️ Downloading wheels from requirements.txt..."
pip download --dest "$WHEELS_DIR" -r requirements.txt

# Also download numpy<2.0 specifically
echo "⬇️ Downloading numpy<2.0..."
pip download --dest "$WHEELS_DIR" "numpy<2.0"

# Download any additional commonly used packages
echo "⬇️ Downloading additional common packages..."
pip download --dest "$WHEELS_DIR" \
    pytest \
    pytest-cov \
    pytest-flask \
    2>/dev/null || true

echo ""
echo "✅ Wheels downloaded to $WHEELS_DIR"
echo ""

# Show statistics
WHEEL_COUNT=$(ls -1 "$WHEELS_DIR"/*.whl 2>/dev/null | wc -l)
TOTAL_SIZE=$(du -sh "$WHEELS_DIR" 2>/dev/null | cut -f1)

echo "📊 Statistics:"
echo "   Total wheels: $WHEEL_COUNT"
echo "   Total size: $TOTAL_SIZE"
echo ""
echo "These wheels will be used for offline Docker builds."
echo "Run this script again when you add new packages to requirements.txt"