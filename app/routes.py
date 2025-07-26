"""Main application routes."""
from flask import render_template, session
import uuid


def init_app(app):
    """Initialize main routes."""
    
    @app.route('/')
    def index():
        """Render the main chat interface."""
        # Generate session ID if not exists
        if 'session_id' not in session:
            session['session_id'] = str(uuid.uuid4())
        return render_template('index.html')
    
    @app.before_request
    def before_request():
        """Set up session before each request."""
        session.permanent = True