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


@bp.route('/settings/summarize-system-prompt', methods=['GET'])
def get_summarize_system_prompt():
    """Get the current summarization system prompt."""
    summarize_prompt = current_app.config.get('SUMMARIZE_SYSTEM_PROMPT', 
        'Task: Read the paragraph and rewrite it to preserve only the essential meaning. '
        'Remove filler, repetition, and minor details. Keep it concise but clear. '
        'Limit the output to 2–3 sentences if needed, but prioritize clarity and brevity.')
    return jsonify({'system_prompt': summarize_prompt})


@bp.route('/settings/summarize-system-prompt', methods=['POST'])
def update_summarize_system_prompt():
    """Update the summarization system prompt."""
    data = request.json
    new_prompt = data.get('system_prompt', '')
    
    # Update the running config
    current_app.config['SUMMARIZE_SYSTEM_PROMPT'] = new_prompt
    
    # Optionally save to environment variable for persistence
    os.environ['SUMMARIZE_SYSTEM_PROMPT'] = new_prompt
    
    return jsonify({
        'success': True,
        'system_prompt': new_prompt,
        'message': 'Summarization system prompt updated successfully'
    })