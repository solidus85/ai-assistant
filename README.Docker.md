# Docker Setup for AI Assistant

## Prerequisites
- Docker Desktop installed on Windows
- Ollama running on your Windows host machine (with GPU access)

## Quick Start

### 1. Ensure Ollama is running on Windows
Make sure Ollama is running and accessible at `http://localhost:11434`

### 2. Build and run the Docker container
```bash
docker-compose up --build
```

## Configuration

### Environment Variables
Copy `.env.example` to `.env` and modify as needed:
```bash
cp .env.example .env
```

The Docker container is configured to connect to Ollama running on your Windows host using `http://host.docker.internal:11434`.

### Secret Key
The Docker container will automatically generate a secret key on first run if `.secret_key` doesn't exist.

## Docker Commands

### Build the image
```bash
docker-compose build
```

### Start the service
```bash
docker-compose up -d
```

### View logs
```bash
docker-compose logs -f
```

### Stop the service
```bash
docker-compose down
```

### Rebuild after code changes
```bash
docker-compose up --build
```

## Accessing the Application
- Web UI: http://localhost:5000
- Ollama API (on host): http://localhost:11434

## Development Mode
To enable hot-reload during development, uncomment the volume mounts in `docker-compose.yml`:
```yaml
volumes:
  - ./.secret_key:/app/.secret_key:ro
  - ./src:/app/src              # Uncomment these lines
  - ./config.py:/app/config.py  # for development
  - ./run.py:/app/run.py        # hot-reload
```

Then restart the container:
```bash
docker-compose restart
```

## Troubleshooting

### Connection to Ollama fails
- Ensure Ollama is running on Windows: `ollama list`
- Check if Ollama is accessible: `curl http://localhost:11434/api/tags`
- The container uses `host.docker.internal:11434` to reach Ollama on the Windows host

### Port already in use
If port 5000 is already in use, change it in `docker-compose.yml`:
```yaml
ports:
  - "5001:5000"  # Change 5001 to any available port
```

### View container health
```bash
docker-compose ps
```

### Check logs
```bash
docker-compose logs web
```