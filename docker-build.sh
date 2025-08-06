#!/bin/bash

# Enable Docker BuildKit for better caching
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1

echo "🔨 Building AI Assistant with Docker BuildKit caching..."

# Build with docker-compose using BuildKit
docker-compose build --progress=plain

# Optional: Create a cache image for even faster subsequent builds
docker build --target builder -t ai-assistant:cache .

echo "✅ Build complete!"
echo ""
echo "📦 Cache volumes created:"
docker volume ls | grep -E "pip-cache|apt-cache"
echo ""
echo "🚀 To run the application:"
echo "   docker-compose up"
echo ""
echo "🧹 To clean cache (if needed):"
echo "   docker volume rm ai-assistant_pip-cache ai-assistant_apt-cache"