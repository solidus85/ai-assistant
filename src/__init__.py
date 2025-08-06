from flask import Flask
from flask_migrate import Migrate
import config
import logging
import os


def ensure_data_directories(app):
    """Ensure all required data directories exist."""
    # Extract directory paths from configuration
    
    # SQLite database directory
    db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
    if db_uri.startswith('sqlite:///'):
        db_path = db_uri.replace('sqlite:///', '')
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
            logging.info(f"Created database directory: {db_dir}")
    
    # ChromaDB directory
    chroma_dir = app.config.get('CHROMA_PERSIST_DIRECTORY')
    if chroma_dir and not os.path.exists(chroma_dir):
        os.makedirs(chroma_dir, exist_ok=True)
        logging.info(f"Created ChromaDB directory: {chroma_dir}")


def create_app():
    """Application factory pattern."""
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    
    # Load configuration
    app.config.from_object(config)
    
    # Configure logging
    logging.basicConfig(level=getattr(logging, config.LOG_LEVEL))
    
    # Ensure data directories exist
    ensure_data_directories(app)
    
    # Initialize database
    from src.models.database import db
    db.init_app(app)
    
    # Initialize Flask-Migrate
    migrate = Migrate(app, db)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Apply SQLite optimizations if using SQLite
        if 'sqlite' in app.config.get('SQLALCHEMY_DATABASE_URI', ''):
            from src.utils.db_optimizer import optimize_sqlite, create_fts_tables
            optimize_sqlite(app)
            # Optionally enable Full-Text Search
            # create_fts_tables(db)
    
    # Initialize vector store (optional - only if chromadb is available)
    try:
        # Try the optimized Ollama-based vector store first
        from src.services.vector_store_ollama import VectorStoreOllama
        app.vector_store = VectorStoreOllama(
            config.CHROMA_PERSIST_DIRECTORY,
            config.OLLAMA_BASE_URL,
            "nomic-embed-text"  # Ollama's embedding model
        )
        app.vector_store_available = True
        logging.info("Using Ollama-based vector store (fast)")
    except (ImportError, ValueError, Exception) as e:
        logging.warning(f"Ollama vector store failed: {e}")
        try:
            # Fall back to sentence-transformers version
            from src.services.vector_store import VectorStore
            app.vector_store = VectorStore(config.CHROMA_PERSIST_DIRECTORY)
            app.vector_store_available = True
            logging.info("Using sentence-transformers vector store (slower)")
        except (ImportError, Exception) as e:
            logging.warning(f"Vector store not available: {e}")
            app.vector_store = None
            app.vector_store_available = False
    
    # Register blueprints
    from src.api import health, chat, conversation, settings, parse
    app.register_blueprint(health.bp)
    app.register_blueprint(chat.bp)
    app.register_blueprint(conversation.bp)
    app.register_blueprint(settings.bp)
    app.register_blueprint(parse.bp)
    
    # Register work assistant blueprints
    from src.api import work_assistant
    app.register_blueprint(work_assistant.bp)
    
    # Register main routes
    from src import routes
    routes.init_app(app)
    
    return app