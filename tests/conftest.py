"""Pytest configuration and fixtures."""
import pytest
import sys
import os
from unittest.mock import MagicMock

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src import create_app


@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['DEBUG'] = False
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create test CLI runner."""
    return app.test_cli_runner()


@pytest.fixture
def mock_ollama_service():
    """Mock OllamaService for testing."""
    mock = MagicMock()
    mock.check_health.return_value = {
        'status': 'connected',
        'model_available': True,
        'models': ['gemma3:12b-it-qat']
    }
    mock.generate_stream.return_value = [
        {'response': 'Hello', 'done': False},
        {'response': ' world', 'done': False},
        {'response': '!', 'done': True}
    ]
    mock.generate.return_value = {
        'response': 'Test response',
        'done': True
    }
    return mock


@pytest.fixture
def mock_conversation_service():
    """Mock ConversationService for testing."""
    mock = MagicMock()
    mock.add_message.return_value = None
    mock.get_history.return_value = [
        {'role': 'user', 'content': 'Hello'},
        {'role': 'assistant', 'content': 'Hi there!'}
    ]
    mock.clear.return_value = None
    mock.get_context.return_value = "User: Hello\nAssistant: Hi there!"
    return mock