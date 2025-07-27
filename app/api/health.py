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
    context_limit = current_app.config.get('NUM_CTX', 32768)
    result['context_limit'] = context_limit
    result['context_limit_k'] = f"{context_limit // 1024}K"
    
    # Add current model info
    result['current_model'] = current_app.config.get('MODEL_NAME', 'phi3:mini')
    
    return jsonify(result)