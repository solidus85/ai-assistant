"""Parse API endpoints."""
from flask import Blueprint, request, Response, stream_with_context, current_app, jsonify
import json
import time
import logging
from app.utils.extensions import get_ollama_service

bp = Blueprint('parse', __name__, url_prefix='/api')
logger = logging.getLogger(__name__)


@bp.route('/parse/stream', methods=['POST'])
def parse_stream():
    """Handle streaming parse requests."""
    data = request.json
    text_input = data.get('text', '')
    
    if not text_input:
        return Response(
            json.dumps({'error': 'No text provided'}) + '\n',
            mimetype='application/json'
        )
    
    return Response(
        stream_with_context(generate_parse_stream(text_input)),
        mimetype='application/json'
    )


def generate_parse_stream(text_input: str):
    """Generate streaming parse response."""
    ollama = get_ollama_service()
    
    try:
        # Create a parsing prompt
        parse_prompt = f"""Parse the following text and extract structured information from it. 
Identify key entities, relationships, and important data points. 
Present the results in a clear, organized format.

Text to parse:
{text_input}"""
        
        # Get parsing system prompt from config or use default
        system_prompt = current_app.config.get('PARSE_SYSTEM_PROMPT', 
            'You are a text parsing assistant. Extract and structure information from the provided text.')
        
        # Prepare options
        options = {
            "num_predict": current_app.config.get('MAX_TOKENS', 8192),
            "temperature": 0.3,  # Lower temperature for more consistent parsing
            "top_k": current_app.config.get('TOP_K', 40),
            "top_p": 0.9,
            "num_ctx": current_app.config.get('NUM_CTX', 8192),
            "num_batch": current_app.config.get('NUM_BATCH', 512),
            "num_thread": current_app.config.get('NUM_THREAD', 8),
            "repeat_penalty": current_app.config.get('REPEAT_PENALTY', 1.1),
            "num_gpu": current_app.config.get('NUM_GPU', -1),
            "gpu_layers": current_app.config.get('GPU_LAYERS', 99)
        }
        
        # Use the chat endpoint with system prompt
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": parse_prompt})
        
        # Stream the response
        for chunk in ollama.chat_stream(messages, options):
            if 'message' in chunk and 'content' in chunk['message']:
                yield json.dumps({
                    'content': chunk['message']['content'],
                    'done': False
                }) + '\n'
        
        # Send done signal
        yield json.dumps({
            'content': '',
            'done': True
        }) + '\n'
        
    except Exception as e:
        logger.error(f"Parse error: {str(e)}")
        yield json.dumps({
            'error': str(e),
            'done': True
        }) + '\n'