"""Health check API endpoints."""
from flask import Blueprint, jsonify, current_app
from app.utils.extensions import get_ollama_service

bp = Blueprint('health', __name__, url_prefix='/api')


@bp.route('/health')
def health_check():
    """Check if Ollama is connected and model is available."""
    ollama = get_ollama_service()
    result = ollama.check_health()
    
    # Add context limit from config
    result['context_limit'] = current_app.config.get('NUM_CTX', 8192)
    
    return jsonify(result)