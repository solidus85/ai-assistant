#!/bin/bash

# Script to download wheels using Docker with Python 3.11

echo "📦 Downloading Python wheels using Docker (Python 3.11)..."

# Create wheels directory if it doesn't exist
WHEELS_DIR="./wheels"
mkdir -p "$WHEELS_DIR"

# Clear old wheels
echo "🧹 Clearing old wheels..."
rm -f "$WHEELS_DIR"/*.whl

# Use Docker to download wheels with Python 3.11
echo "🐳 Using Docker to download wheels with Python 3.11..."
docker run --rm \
    -v "$(pwd)/requirements.txt:/requirements.txt:ro" \
    -v "$(pwd)/wheels:/wheels" \
    python:3.11-slim \
    bash -c "
        pip download --dest /wheels -r /requirements.txt &&
        pip download --dest /wheels 'numpy<2.0'
    "

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