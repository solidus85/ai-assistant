# AI Assistant

A high-performance, GPU-accelerated conversational AI assistant built with Flask and Ollama. This application provides an intelligent chat interface with real-time streaming responses, text parsing capabilities, work assistant features, and comprehensive conversation management.

## Features

### Core Capabilities
- **Real-time Chat Interface**: Interactive conversations with streaming responses
- **Text Parsing & Summarization**: Extract structured information and generate summaries from text
- **Work Assistant**: Track projects, deliverables, and team interactions with vector-based search
- **Conversation Management**: Save, load, and manage chat history with SQLite backend
- **Token Tracking**: Real-time token usage monitoring with visual indicators
- **GPU Acceleration**: Optimized for NVIDIA RTX GPUs (tested on RTX 4080)
- **Vector Search**: ChromaDB integration for semantic search capabilities
- **Keyword Extraction**: Automatic entity and keyword extraction using NLP

### Technical Features
- **Modular Architecture**: Clean separation of concerns with services, models, and API layers
- **Docker Support**: Full containerization with Docker Compose
- **CI/CD Pipeline**: Jenkins integration for automated testing and deployment
- **Comprehensive Testing**: Unit and integration tests with 80%+ coverage
- **SQLite Optimization**: FTS (Full-Text Search) support and performance tuning
- **Responsive Web UI**: Modern, mobile-friendly interface with tabbed navigation

## Tech Stack

- **Backend**: Python 3.11, Flask 3.0
- **AI/ML**: 
  - Ollama (LLM inference)
  - ChromaDB (vector database)
  - Sentence Transformers (embeddings)
  - NLTK (text processing)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: Vanilla JavaScript (ES6 modules), CSS3
- **Deployment**: Docker, Docker Compose
- **Testing**: pytest, pytest-cov, pytest-flask
- **CI/CD**: Jenkins

## Requirements

### System Requirements
- Python 3.10+ (tested with 3.11)
- 16GB+ RAM recommended
- NVIDIA GPU with CUDA support (optional but recommended)
- 10GB+ free disk space for models

### Required Services
- Ollama running locally or remotely (default: http://localhost:11434)
- Models:
  - Main chat: `gemma3:12b-it-qat` (or configure your preferred model)
  - Embeddings: `nomic-embed-text` (for vector search)
  - Extraction: `phi3` (for keyword extraction)

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/ai-assistant.git
cd ai-assistant
```

### 2. Install Ollama
Follow instructions at [ollama.ai](https://ollama.ai) to install Ollama, then pull required models:
```bash
ollama pull gemma3:12b-it-qat
ollama pull nomic-embed-text
ollama pull phi3
```

### 3. Setup Python Environment

#### Using venv (Recommended)
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

#### Using Poetry (Alternative)
```bash
poetry install
poetry shell
```

### 4. Configuration
Create a `.env` file in the project root:
```env
# Flask Settings
HOST=0.0.0.0
PORT=5000
DEBUG=False
SECRET_KEY_PATH=.secret_key

# Ollama Settings
OLLAMA_BASE_URL=http://localhost:11434
MODEL_NAME=gemma3:12b-it-qat
EXTRACTION_MODEL=phi3

# Performance Settings (adjust for your GPU)
MAX_TOKENS=2048
TEMPERATURE=0.7
NUM_CTX=4096
NUM_GPU=99  # Use all GPU layers
NUM_BATCH=512

# Database Settings
DATABASE_PATH=./data/work_assistant.db
CHROMA_PERSIST_DIRECTORY=./data/chroma_db

# Work Assistant Settings
MAX_SEARCH_RESULTS=10
DELIVERABLE_WARNING_DAYS=7
```

### 5. Run the Application

#### Development Mode
```bash
python run.py
```

#### Production Mode with Docker
```bash
docker-compose up -d
```

Access the application at `http://localhost:5000`

## Docker Deployment

### Build and Run with Docker Compose
```bash
# Build the image
docker-compose build

# Run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

### Docker Configuration
The application includes:
- Multi-stage build for optimized image size
- Non-root user for security
- Health checks for monitoring
- Volume mounts for persistent data
- Environment variable configuration

## API Endpoints

### Chat API
- `POST /api/chat` - Send a chat message (supports streaming)
- `GET /api/conversations` - List all conversations
- `POST /api/conversations` - Create new conversation
- `DELETE /api/conversations/<id>` - Delete conversation

### Text Processing
- `POST /api/parse` - Parse and extract information from text
- `POST /api/summarize` - Generate text summaries

### Work Assistant
- `GET /api/work-assistant/search` - Search work-related content
- `POST /api/work-assistant/store` - Store work information
- `GET /api/work-assistant/deliverables` - Get deliverable status
- `GET /api/work-assistant/stats` - Get work statistics

### System
- `GET /api/health` - Health check endpoint
- `GET /api/settings` - Get current settings
- `POST /api/settings` - Update settings

## Project Structure

```
ai-assistant/
├── src/
│   ├── __init__.py           # Flask app factory
│   ├── routes.py             # Main route handlers
│   ├── api/                  # API endpoints
│   │   ├── chat.py          # Chat functionality
│   │   ├── conversation.py  # Conversation management
│   │   ├── parse.py         # Text parsing
│   │   ├── summarize.py     # Summarization
│   │   └── work_assistant.py # Work tracking
│   ├── models/              # Database models
│   │   └── database.py      # SQLAlchemy models
│   ├── services/            # Business logic
│   │   ├── conversation_service.py
│   │   ├── ollama_service.py
│   │   ├── keyword_extractor.py
│   │   └── vector_store.py
│   ├── utils/               # Utility functions
│   │   ├── db_optimizer.py
│   │   ├── extensions.py
│   │   └── token_counter.py
│   ├── static/              # Frontend assets
│   │   ├── css/            # Stylesheets
│   │   └── js/             # JavaScript modules
│   └── templates/           # HTML templates
├── tests/                   # Test suite
│   ├── unit/               # Unit tests
│   └── integration/        # Integration tests
├── docs/                    # Documentation
├── config.py               # Configuration file
├── run.py                  # Application entry point
├── Dockerfile              # Container definition
├── docker-compose.yml      # Compose configuration
├── requirements.txt        # Python dependencies
└── pyproject.toml         # Poetry configuration
```

## Testing

### Run Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/api/test_chat.py

# Run integration tests only
pytest tests/integration/
```

### View Coverage Report
```bash
# Generate HTML coverage report
pytest --cov=src --cov-report=html

# Open coverage report
open htmlcov/index.html  # macOS/Linux
start htmlcov/index.html  # Windows
```

## Development

### Setting Up Development Environment
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests before committing
pytest

# Check code style (if using linters)
flake8 src/
black src/ --check
```

### Environment Variables

Key configuration options:

| Variable | Description | Default |
|----------|-------------|---------|
| `OLLAMA_BASE_URL` | Ollama API endpoint | `http://localhost:11434` |
| `MODEL_NAME` | Primary LLM model | `gemma3:12b-it-qat` |
| `MAX_TOKENS` | Maximum response tokens | `2048` |
| `NUM_CTX` | Context window size | `4096` |
| `NUM_GPU` | GPU layers to use | `99` (all) |
| `DATABASE_PATH` | SQLite database location | `./data/work_assistant.db` |
| `CHROMA_PERSIST_DIRECTORY` | Vector DB storage | `./data/chroma_db` |

## Performance Optimization

### GPU Configuration
For NVIDIA RTX 4080 or similar:
```env
NUM_GPU=99        # Use all GPU layers
NUM_BATCH=512     # Optimal batch size
NUM_THREAD=16     # CPU threads
NUM_CTX=4096      # 4K context for speed
```

### Database Optimization
The application automatically applies SQLite optimizations:
- WAL mode for concurrent access
- Memory-mapped I/O
- Optimized cache size
- Optional FTS (Full-Text Search) support

## Troubleshooting

### Common Issues

1. **Ollama Connection Error**
   - Ensure Ollama is running: `ollama serve`
   - Check OLLAMA_BASE_URL in .env file
   - Verify firewall settings

2. **GPU Not Detected**
   - Install CUDA drivers
   - Check nvidia-smi output
   - Verify NUM_GPU setting

3. **Database Locked Error**
   - Application uses WAL mode to prevent this
   - If persists, restart the application

4. **Docker Network Issues**
   - Use `host.docker.internal` for Ollama on host
   - Check docker-compose.yml extra_hosts configuration

## CI/CD with Jenkins

The project includes Jenkins pipeline configurations:
- `Jenkinsfile` - Main pipeline for testing and deployment
- Automated testing on push
- Docker image building and tagging
- Coverage reporting

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Ollama](https://ollama.ai) for local LLM inference
- [ChromaDB](https://www.trychroma.com/) for vector storage
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [Sentence Transformers](https://www.sbert.net/) for embeddings

## Support

For issues, questions, or suggestions, please open an issue on GitHub.