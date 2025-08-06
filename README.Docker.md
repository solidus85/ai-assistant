# Docker Setup for AI Assistant

## Prerequisites
- Docker Desktop installed on Windows
- NVIDIA GPU drivers (if using GPU acceleration)

## Quick Start

### Development Mode (using existing Ollama)
If you already have Ollama running locally:
```bash
docker-compose -f docker-compose.dev.yml up --build
```

### Full Stack (includes Ollama)
To run both the app and Ollama in Docker:
```bash
docker-compose up --build
```

## Configuration

### Environment Variables
Copy `.env.example` to `.env` and modify as needed:
```bash
cp .env.example .env
```

### Secret Key
The Docker container will automatically generate a secret key on first run if `.secret_key` doesn't exist.

## Docker Commands

### Build the image
```bash
docker-compose build
```

### Start services
```bash
docker-compose up -d
```

### View logs
```bash
docker-compose logs -f
```

### Stop services
```bash
docker-compose down
```

### Remove volumes (careful - removes Ollama models)
```bash
docker-compose down -v
```

## Accessing the Application
- Web UI: http://localhost:5000
- Ollama API: http://localhost:11434 (if using full stack)

## GPU Support
The docker-compose.yml includes GPU support for Ollama. Make sure:
1. NVIDIA Container Toolkit is installed
2. Docker Desktop has WSL2 backend enabled
3. GPU is available in WSL2

## Development Tips
- Use `docker-compose.dev.yml` for development with hot-reload
- Volumes are mounted for live code updates in dev mode
- Check container health: `docker-compose ps`

## Troubleshooting
- If Ollama connection fails, ensure the `OLLAMA_BASE_URL` is correct
- For Windows: use `http://host.docker.internal:11434` to connect to local Ollama
- Check logs: `docker-compose logs web` or `docker-compose logs ollama`