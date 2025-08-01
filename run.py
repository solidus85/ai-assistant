#!/usr/bin/env python3
"""Application entry point."""
import config
from app import create_app

# Create application
app = create_app()

if __name__ == '__main__':
    # Run the application
    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG
    )