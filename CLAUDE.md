# Project Status and Context for Claude

## Project Overview
Building a Flask web app that interfaces with Ollama to run LLMs locally with GPU acceleration. Currently using Phi-3 Mini for fast responses, with option to switch to Mixtral for higher accuracy.

## Current Status
- ✅ Flask app refactored into modular structure
- ✅ Streaming responses ~~with conversation history~~ (simplified to single request/response)
- ✅ Token counter with 32K context window (increased from 8K)
- ✅ GPU acceleration working (RTX 4080, 16GB VRAM)
- ✅ Prompt display feature in separate console panel
- ✅ Dark mode theme implemented
- ✅ System prompt configuration with UI
- ✅ Text summarization feature with dedicated tab
- ✅ Wider layout for better screen utilization
- ✅ User message formatting preservation

## Hardware Capabilities
- **GPU**: RTX 4080 with 16GB VRAM
- **RAM**: 62GB available (110GB possible)
- **CUDA**: 12.9 support with Flash Attention
- **Current Model**: Phi-3 Mini (3.8B, ~1s response time)
- **Alternative**: Mixtral Q5_K_M (46.7B, ~57s response time, 99% accuracy)

## Project Structure
```
llm/
├── app/                    # Main application package
│   ├── __init__.py        # App factory
│   ├── routes.py          # Main routes (index page)
│   ├── api/               # API blueprints
│   │   ├── health.py      # Health check endpoints
│   │   ├── chat.py        # Chat streaming endpoints
│   │   ├── conversation.py # Conversation management
│   │   ├── settings.py    # System prompt settings
│   │   └── summarize.py   # Text summarization endpoint
│   ├── services/          # Business logic
│   │   ├── ollama_service.py      # Ollama API client (uses chat endpoint)
│   │   └── conversation_service.py # Conversation history
│   ├── models/            # Data models (future use)
│   └── utils/             # Utilities
│       ├── extensions.py  # Service singletons
│       └── token_counter.py # Token counting
├── static/                
│   ├── css/              # Modularized CSS
│   │   ├── base/         # Reset, animations
│   │   ├── components/   # UI components
│   │   ├── layout/       # Page structure
│   │   └── utilities/    # Responsive design
│   └── js/               # Modularized JavaScript
│       ├── modules/      # Feature modules
│       └── utils/        # Helper functions
├── templates/             # HTML templates
├── scripts/              # Organized scripts
│   ├── setup/           # Setup scripts
│   ├── debug/           # Testing/debug scripts
│   └── utilities/       # Utility scripts
├── docs/                 # Documentation
├── config.py            # Configuration classes
├── run.py               # Application entry point
└── requirements.txt     # Dependencies
```

## Key Features
1. **Modular Architecture**: Clean separation of concerns with services, blueprints, and utilities
2. **Streaming Chat**: Real-time token streaming with conversation history
3. **Token Management**: Visual token counter with color-coded usage (32K context)
4. **GPU Optimization**: Configured for RTX 4080 with Flash Attention
5. **Prompt Display**: Toggle to show full prompts sent to model
6. **Model Flexibility**: Easy switching between speed (Phi-3) and accuracy (Mixtral)

## Configuration
- **Current Model**: `MODEL_NAME = "phi3:mini"` (in config.py)
- **Context Window**: `NUM_CTX = 32768` (32K tokens, can go up to 128K)
- **Conversation History**: Limited to 10 exchanges
- **Token Counter**: Updates in real-time with color coding

## Available Models
1. **phi3:mini** (Current)
   - Size: 3.8B parameters
   - Speed: ~1 second responses
   - VRAM: 2-3GB
   - Context: Up to 128K tokens

2. **mixtral-accurate:latest**
   - Size: 46.7B parameters (Q5_K_M)
   - Speed: ~57 seconds responses
   - VRAM: 15-16GB
   - Context: Up to 32K tokens
   - Accuracy: 99% retention

3. **mixtral:latest**
   - Size: 46.7B parameters (Q4_0)
   - Speed: ~20-30 seconds
   - VRAM: 13-15GB
   - Context: Up to 32K tokens

## Running the Application

1. **Ensure Ollama is running**:
   ```bash
   ./start_ollama.sh
   ```

2. **Start the Flask app**:
   ```bash
   source venv/bin/activate
   python run.py
   ```

3. **Access the app**:
   - Open http://localhost:5000
   - Green status = Connected
   - Token counter shows usage/limit
   - "Show Prompt" button reveals full context

## API Endpoints
- `GET /api/health` - Check Ollama connection and model status
- `POST /api/chat/stream` - Stream chat responses
- `POST /api/chat/tokens` - Get token count for session
- `POST /api/conversation/clear` - Clear conversation history
- `GET /api/conversation/history` - Get conversation history

## Recent Updates
1. **Modular Refactoring**: App split into services, blueprints, and utilities
2. **Token Limit Increase**: From 8K to 32K (configurable up to 128K)
3. **Prompt Display Feature**: Shows full context sent to model
4. **Bug Fixes**: 
   - Token counter now updates properly
   - Show Prompt button works correctly
   - Fixed API endpoint paths

## Debugging Tools
- `./debug_app.py` - Test Ollama connectivity
- `./test_speed.py` - Compare model response times
- `./test_structure.py` - Verify modular structure
- `./test_bug_fixes.py` - Test token counter and prompt display
- `./check_model_limits.py` - Test context window limits

## Environment Variables
- `NUM_CTX` - Set context window size (default: 32768)
- `MODEL_NAME` - Override default model
- `FLASK_ENV` - Set to 'development' for debug mode
- `OLLAMA_BASE_URL` - Ollama API URL (default: http://localhost:11434)

## Common Commands
```bash
# Check Ollama status
ollama list

# Test model directly
ollama run phi3:mini "Hello"

# Monitor GPU usage
nvidia-smi

# Run speed comparison
python3 test_speed.py

# Change context limit
export NUM_CTX=65536  # For 64K context
```

## Troubleshooting
- **Red status indicator**: Check if Ollama is running (`./start_ollama.sh`)
- **Token counter shows 0/0**: Refresh page, check browser console
- **Slow responses**: Switch to phi3:mini for speed
- **Out of memory**: Reduce NUM_CTX or switch to smaller model
- **Model not found**: Run `ollama pull phi3:mini`

## Next Steps
- Add database for persistent conversation storage
- Implement user authentication
- Add more model options (gemma, tinyllama)
- Create model switching UI
- Add conversation export feature
- Implement rate limiting
- Add OpenAI-compatible API endpoint