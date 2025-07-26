# Application Structure

The application has been refactored into a modular structure for better organization and maintainability.

## Directory Structure

```
llm/
├── app/                    # Main application package
│   ├── __init__.py        # App factory
│   ├── routes.py          # Main routes (index page)
│   ├── api/               # API blueprints
│   │   ├── health.py      # Health check endpoints
│   │   ├── chat.py        # Chat streaming endpoints
│   │   └── conversation.py # Conversation management
│   ├── services/          # Business logic
│   │   ├── ollama_service.py      # Ollama API client
│   │   └── conversation_service.py # Conversation history
│   ├── models/            # Data models (future use)
│   └── utils/             # Utilities
│       ├── extensions.py  # Service singletons
│       └── token_counter.py # Token counting
├── static/                # CSS, JS files
├── templates/             # HTML templates
├── config.py             # Configuration classes
├── run.py                # Application entry point
└── requirements.txt      # Dependencies
```

## Key Components

### Services
- **OllamaService**: Handles all communication with Ollama API
- **ConversationService**: Manages conversation history and context building

### API Blueprints
- **/api/health**: Health check endpoint
- **/api/chat/stream**: Streaming chat endpoint
- **/api/chat/tokens**: Token counting endpoint
- **/api/conversation/clear**: Clear conversation history
- **/api/conversation/history**: Get conversation history

### Configuration
- Model settings in `config.py`
- Environment variables supported
- Easy to switch between models

## Running the Application

```bash
# Activate virtual environment
source venv/bin/activate

# Run the application
python run.py

# Or use the old command (will be deprecated)
python app.py
```

## Benefits of New Structure

1. **Separation of Concerns**: Business logic separated from routes
2. **Testability**: Each component can be tested independently
3. **Scalability**: Easy to add new features without cluttering
4. **Maintainability**: Clear organization makes code easier to navigate
5. **Reusability**: Services can be used in multiple endpoints