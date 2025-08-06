#!/bin/bash
set -e

# Generate secret key if it doesn't exist
if [ ! -f ".secret_key" ]; then
    echo "Generating new secret key..."
    python -c "import secrets; print(secrets.token_hex(32))" > .secret_key
    echo "Secret key generated successfully"
fi

# Wait for Ollama to be ready (if using docker-compose with ollama service)
if [ ! -z "$WAIT_FOR_OLLAMA" ]; then
    echo "Waiting for Ollama service to be ready..."
    while ! curl -s ${OLLAMA_BASE_URL}/api/tags > /dev/null 2>&1; do
        echo "Ollama not ready yet, waiting..."
        sleep 2
    done
    echo "Ollama service is ready!"
fi

# Run the application
exec python run.py