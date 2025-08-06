#!/bin/bash
set -e

# Generate secret key if it doesn't exist
SECRET_KEY_FILE="${SECRET_KEY_PATH:-.secret_key}"

# If SECRET_KEY_PATH is a directory, append filename
if [ -d "$SECRET_KEY_FILE" ]; then
    SECRET_KEY_FILE="$SECRET_KEY_FILE/secret_key.txt"
fi

if [ ! -f "$SECRET_KEY_FILE" ]; then
    echo "Generating new secret key at $SECRET_KEY_FILE..."
    mkdir -p "$(dirname "$SECRET_KEY_FILE")"
    python -c "import secrets; print(secrets.token_hex(32))" > "$SECRET_KEY_FILE"
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