"""Conversation management API endpoints."""
from flask import Blueprint, request, jsonify
from app.utils.extensions import get_conversation_service
import logging

bp = Blueprint('conversation', __name__, url_prefix='/api')
logger = logging.getLogger(__name__)


@bp.route('/conversation/clear', methods=['POST'])
def clear_conversation():
    """Clear conversation history for a session."""
    data = request.json
    session_id = data.get('session_id')
    
    if not session_id:
        return jsonify({'success': False, 'message': 'No session ID provided'}), 400
    
    conversation = get_conversation_service()
    success = conversation.clear_session(session_id)
    
    if success:
        return jsonify({'success': True, 'message': 'Conversation cleared'})
    else:
        return jsonify({'success': False, 'message': 'Session not found'}), 404


@bp.route('/conversation/history', methods=['GET'])
def get_history():
    """Get conversation history for a session."""
    session_id = request.args.get('session_id')
    
    if not session_id:
        return jsonify({'history': []})
    
    conversation = get_conversation_service()
    history = conversation.get_history(session_id)
    
    return jsonify({'history': history})