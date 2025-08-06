# AI Assistant Project Documentation

## Project Overview

**AI Assistant** is a Flask-based web application that provides an intelligent conversational interface powered by Ollama LLM (Large Language Model). The application offers real-time chat capabilities with streaming responses, text parsing functionality, and is optimized for GPU acceleration (specifically RTX 4080).

### Key Features
- **Real-time Chat Interface**: Interactive chat with streaming responses
- **Text Parsing**: Dedicated parsing mode for extracting structured information from text
- **Token Counting**: Real-time token usage tracking with visual indicators
- **GPU Optimization**: Configured for optimal performance on NVIDIA RTX 4080
- **Docker Support**: Containerized deployment with health checks
- **CI/CD Pipeline**: Comprehensive Jenkins pipeline for testing and deployment
- **Modern Web UI**: Responsive design with tabbed interface

### Technology Stack
- **Backend**: Python 3.11, Flask 3.0.0
- **LLM Integration**: Ollama API (using gemma3:12b-it-qat model)
- **Frontend**: Vanilla JavaScript (ES6 modules), CSS3
- **Deployment**: Docker, Docker Compose
- **CI/CD**: Jenkins (Windows and cross-platform pipelines)
- **Testing**: pytest, pytest-cov, pytest-flask

## Project Structure

```
ai-assistant/
├── src/                    # Main application source code
├── tests/                  # Test suite
├── docs/                   # Documentation
├── htmlcov/               # Test coverage reports
├── jenkins_console.txt    # Jenkins build logs
└── Configuration files    # Various config and setup files
```

## File Index and Descriptions

### Root Configuration Files

| File | Purpose |
|------|---------|
| `config.py` | Central configuration file with Flask settings, Ollama configuration, GPU settings, and environment variables |
| `requirements.txt` | Python dependencies (Flask, requests, Werkzeug, python-dotenv) |
| `requirements-dev.txt` | Development dependencies for testing and linting |
| `run.py` | Application entry point that creates and runs the Flask app |
| `run.sh` | Unix/Linux startup script |
| `run.bat` | Windows startup script |
| `stop.bat` | Windows script to stop the application |
| `stop-all.bat` | Windows script to stop all related processes |
| `pytest.ini` | pytest configuration |
| `CLAUDE.md` | Project-specific instructions for Claude AI assistant |

### Docker & CI/CD Files

| File | Purpose |
|------|---------|
| `Dockerfile` | Docker container definition with Python 3.11 slim image |
| `docker-compose.yml` | Docker Compose configuration for multi-container setup |
| `docker-entrypoint.sh` | Docker container entry point script |
| `Jenkinsfile` | Windows-specific Jenkins CI/CD pipeline |
| `Jenkinsfile.crossplatform` | Cross-platform Jenkins pipeline |
| `README.Docker.md` | Docker-specific documentation |

### Source Code Structure (`src/`)

#### Core Application Files
| File | Purpose |
|------|---------|
| `src/__init__.py` | Flask application factory with blueprint registration |
| `src/routes.py` | Main route handlers for the web interface |

#### API Endpoints (`src/api/`)
| File | Purpose |
|------|---------|
| `chat.py` | Streaming chat endpoint with token counting (`/api/chat/stream`, `/api/chat/tokens`) |
| `conversation.py` | Conversation management endpoints (history, clearing) |
| `health.py` | Health check endpoint for monitoring Ollama connection |
| `parse.py` | Text parsing endpoint with custom system prompt |
| `settings.py` | Settings management endpoints |
| `summarize.py` | Text summarization endpoints |

#### Services (`src/services/`)
| File | Purpose |
|------|---------|
| `ollama_service.py` | Core service for Ollama API interaction, handles streaming and non-streaming responses |
| `conversation_service.py` | Manages conversation history and context |

#### Utilities (`src/utils/`)
| File | Purpose |
|------|---------|
| `extensions.py` | Flask extensions and service initialization |
| `token_counter.py` | Token counting implementation for context management |

#### Frontend Assets

##### Templates (`src/templates/`)
| File | Purpose |
|------|---------|
| `index.html` | Main HTML template with tabbed interface for Chat and Parse modes |

##### JavaScript (`src/static/js/`)
| File | Purpose |
|------|---------|
| `app.js` | Main application entry point, initializes all modules |
| **modules/** | |
| `api.js` | API client for backend communication |
| `chat.js` | Chat functionality with streaming support |
| `parse.js` | Text parsing interface |
| `prompt.js` | Prompt management and display |
| `status.js` | Connection status monitoring |
| `summarize.js` | Summarization features |
| `summarize-system-prompt.js` | System prompt for summarization |
| `system-prompt.js` | System prompt management |
| `tabs.js` | Tab navigation controller |
| `timer.js` | Response time tracking |
| `tokens.js` | Token usage display and tracking |
| **utils/** | |
| `dom.js` | DOM manipulation utilities |
| `error-handler.js` | Global error handling |
| `storage.js` | Local storage management |

##### CSS (`src/static/css/`)
| File | Purpose |
|------|---------|
| `main.css` | Main stylesheet importing all components |
| **base/** | |
| `animations.css` | CSS animations and transitions |
| `reset.css` | CSS reset for consistent styling |
| **components/** | |
| `buttons.css` | Button styles |
| `chat.css` | Chat interface styles |
| `console-entry.css` | Console-like entry styling |
| `input.css` | Input field styles |
| `messages.css` | Message bubble styles |
| `progress-indicator.css` | Loading and progress animations |
| `prompt-display.css` | Prompt display styling |
| `status.css` | Status indicator styles |
| `summarize.css` | Summarization interface styles |
| `system-prompt.css` | System prompt UI styles |
| `tabs.css` | Tab navigation styles |
| `token-counter.css` | Token counter visualization |
| **layout/** | |
| `container.css` | Container layouts |
| `header.css` | Header styling |
| `main-layout.css` | Main layout structure |
| **utilities/** | |
| `responsive.css` | Responsive design breakpoints |

### Test Suite (`tests/`)

| File/Directory | Purpose |
|------|---------|
| `conftest.py` | pytest fixtures and test configuration |
| `test_app.py` | Main application integration tests |
| **unit/api/** | Unit tests for API endpoints |
| `test_chat.py` | Chat endpoint tests |
| `test_conversation.py` | Conversation management tests |
| `test_health.py` | Health check tests |
| `test_parse.py` | Parse endpoint tests |
| `test_settings.py` | Settings endpoint tests |
| **unit/services/** | Unit tests for services |
| `test_conversation_service.py` | Conversation service tests |
| `test_ollama_service.py` | Ollama service tests |
| **unit/utils/** | Unit tests for utilities |
| `test_token_counter.py` | Token counter tests |
| **integration/** | Integration test directory (placeholder) |

### Documentation (`docs/`)

| File | Purpose |
|------|---------|
| `setup_notes.md` | Setup and installation notes |

### Test Coverage Reports (`htmlcov/`)

Contains HTML coverage reports generated by pytest-cov, including:
- `index.html` - Main coverage report
- Individual file coverage reports
- JavaScript and CSS assets for the coverage viewer

## Key Configuration Settings

### Flask Configuration
- **Host**: 0.0.0.0 (accessible from all interfaces)
- **Port**: 5000
- **Debug Mode**: Configurable via environment variable

### Ollama Configuration
- **Base URL**: http://localhost:11434
- **Model**: gemma3:12b-it-qat (optimized for RTX 4080)
- **Context Window**: 4096 tokens
- **Max Tokens**: 2048
- **Temperature**: 0.7

### GPU Optimization
- **GPU Layers**: 99 (all layers on GPU)
- **Batch Size**: 512 (optimized for RTX 4080)
- **Thread Count**: 16

## CI/CD Pipeline Stages

1. **Checkout**: Retrieve code from SCM
2. **Setup Environment**: Create Python virtual environment
3. **Lint and Format Check**: Run flake8 and black
4. **Run Tests**: Execute pytest with coverage
5. **Docker Build**: Build Docker image (main branch only)
6. **Security Scan**: Run safety and bandit security checks
7. **Deploy to Test**: Deploy to test environment (develop branch)
8. **Archive Artifacts**: Store test results and coverage reports

## API Endpoints

### Chat
- `POST /api/chat/stream` - Streaming chat responses
- `POST /api/chat/tokens` - Count tokens in message

### Health
- `GET /api/health` - Check Ollama connection status

### Parse
- `POST /api/parse` - Parse text with custom prompt

### Settings
- `GET /api/settings` - Get current settings
- `POST /api/settings` - Update settings

### Conversation
- `GET /api/conversation/history` - Get conversation history
- `DELETE /api/conversation/clear` - Clear conversation

## Development Workflow

1. **Local Development**: Use `run.py` or `run.sh`/`run.bat` scripts
2. **Testing**: Run `pytest` with coverage reporting
3. **Docker Build**: Use `docker-compose up` for containerized deployment
4. **CI/CD**: Jenkins pipeline handles automated testing and deployment

## Security Features

- Non-root Docker user
- Secret key management via environment variables
- Security scanning in CI/CD pipeline (safety, bandit)
- Health checks for monitoring
- Input validation and sanitization

## Performance Optimizations

- GPU acceleration for LLM inference
- Streaming responses for better UX
- Token counting for context management
- Optimized batch sizes for RTX 4080
- Efficient memory management

## Future Enhancements

Based on the current structure, potential areas for enhancement include:
- Additional LLM model support
- Enhanced conversation persistence
- User authentication and sessions
- API rate limiting
- WebSocket support for real-time communication
- Advanced prompt engineering features