from flask import Flask
from config import config
import os
import logging


def create_app(config_name=None):
    """Application factory pattern."""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Configure logging
    logging.basicConfig(level=getattr(logging, config[config_name].LOG_LEVEL))
    
    # Register blueprints
    from app.api import health, chat, conversation, settings, summarize
    app.register_blueprint(health.bp)
    app.register_blueprint(chat.bp)
    app.register_blueprint(conversation.bp)
    app.register_blueprint(settings.bp)
    app.register_blueprint(summarize.bp)
    
    # Register main routes
    from app import routes
    routes.init_app(app)
    
    return app