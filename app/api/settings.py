"""Settings API endpoints."""
from flask import Blueprint, request, jsonify, current_app
import os

bp = Blueprint('settings', __name__, url_prefix='/api')


@bp.route('/settings/system-prompt', methods=['GET'])
def get_system_prompt():
    """Get the current system prompt."""
    system_prompt = current_app.config.get('SYSTEM_PROMPT', '')
    return jsonify({'system_prompt': system_prompt})


@bp.route('/settings/system-prompt', methods=['POST'])
def update_system_prompt():
    """Update the system prompt."""
    data = request.json
    new_prompt = data.get('system_prompt', '')
    
    # Update the running config
    current_app.config['SYSTEM_PROMPT'] = new_prompt
    
    # Optionally save to environment variable for persistence
    # Note: This won't persist across restarts unless saved to a file
    os.environ['SYSTEM_PROMPT'] = new_prompt
    
    return jsonify({
        'success': True,
        'system_prompt': new_prompt,
        'message': 'System prompt updated successfully'
    })


