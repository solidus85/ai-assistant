"""Pytest configuration and fixtures."""
import pytest
import sys
import os
import tempfile
import shutil

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture(scope='function')
def app():
    """Create application for testing."""
    # Create a temporary database file
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    chroma_dir = tempfile.mkdtemp()
    
    # Set test configuration
    test_config = {
        'TESTING': True,
        'DEBUG': False,
        'SECRET_KEY': 'test-secret-key-for-testing',
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'CHROMA_PERSIST_DIRECTORY': chroma_dir,
        'WTF_CSRF_ENABLED': False,
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    }
    
    # Create a new app instance for each test
    from flask import Flask
    from src.models.database import db
    
    app = Flask(__name__, 
                template_folder='../src/templates',
                static_folder='../src/static')
    
    # Apply test configuration
    app.config.update(test_config)
    
    # Add required config for Ollama
    app.config['OLLAMA_BASE_URL'] = 'http://localhost:11434'
    app.config['DEFAULT_LLM_MODEL'] = 'gemma3'
    app.config['EXTRACTION_MODEL'] = 'phi3'
    app.config['MODEL_NAME'] = 'gemma3'
    
    # Initialize database
    db.init_app(app)
    
    # Register blueprints
    from src.api import health, chat, conversation, settings, parse, work_assistant
    app.register_blueprint(health.bp)
    app.register_blueprint(chat.bp)
    app.register_blueprint(conversation.bp)
    app.register_blueprint(settings.bp)
    app.register_blueprint(parse.bp)
    app.register_blueprint(work_assistant.bp)
    
    # Register main routes for index
    from src import routes
    routes.init_app(app)
    
    # Disable vector store for tests
    app.vector_store = None
    app.vector_store_available = False
    
    # Create tables
    with app.app_context():
        db.create_all()
        yield app
        # Clean up database after each test
        db.session.remove()
        db.drop_all()
        db.engine.dispose()
    
    # Cleanup files
    try:
        os.close(db_fd)
        os.unlink(db_path)
    except:
        pass
    
    # Clean up chroma directory
    try:
        shutil.rmtree(chroma_dir)
    except:
        pass


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create test CLI runner."""
    return app.test_cli_runner()