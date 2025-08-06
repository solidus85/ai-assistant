from flask import Flask
from flask_migrate import Migrate
import config
import logging
import os


def create_app():
    """Application factory pattern."""
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    
    # Load configuration
    app.config.from_object(config)
    
    # Configure logging
    logging.basicConfig(level=getattr(logging, config.LOG_LEVEL))
    
    # Initialize database
    from src.models.database import db
    db.init_app(app)
    
    # Initialize Flask-Migrate
    migrate = Migrate(app, db)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Initialize vector store
    from src.services.vector_store import VectorStore
    app.vector_store = VectorStore(config.CHROMA_PERSIST_DIRECTORY)
    
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