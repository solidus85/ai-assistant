#!/usr/bin/env python3
"""Application entry point."""
import config
from src import create_app
import logging
import sys

# Suppress the development server warning
cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None

# Create application
app = create_app()

if __name__ == '__main__':
    # Suppress werkzeug logging info
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    
    # Run the application
    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG
    )