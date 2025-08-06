from flask import Flask
import config
import logging


def create_app():
    """Application factory pattern."""
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    
    # Load configuration
    app.config.from_object(config)
    
    # Configure logging
    logging.basicConfig(level=getattr(logging, config.LOG_LEVEL))
    
    # Register blueprints
    from src.api import health, chat, conversation, settings, parse
    app.register_blueprint(health.bp)
    app.register_blueprint(chat.bp)
    app.register_blueprint(conversation.bp)
    app.register_blueprint(settings.bp)
    app.register_blueprint(parse.bp)
    
    # Register main routes
    from src import routes
    routes.init_app(app)
    
    return app