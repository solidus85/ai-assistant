"""Chat API endpoints."""
from flask import Blueprint, request, Response, stream_with_context, current_app
import json
import time
import logging
from app.utils.extensions import get_ollama_service, get_conversation_service
from app.utils.token_counter import TokenCounter

bp = Blueprint('chat', __name__, url_prefix='/api')
logger = logging.getLogger(__name__)


@bp.route('/chat/stream', methods=['POST'])
def chat_stream():
    """Handle streaming chat requests."""
    data = request.json
    user_input = data.get('message', '')
    session_id = data.get('session_id')
    
    if not user_input:
        return Response(
            json.dumps({'error': 'No message provided'}) + '\n',
            mimetype='application/json'
        )
    
    return Response(
        stream_with_context(generate_chat_stream(user_input, session_id)),
        mimetype='application/json'
    )


def generate_chat_stream(user_input: str, session_id: str = None):
    """Generate streaming chat response."""
    ollama = get_ollama_service()
    conversation = get_conversation_service()
    
    try:
        # Get or create session
        session_id = conversation.get_or_create_session(session_id)
        if not session_id:
            session_id = conversation.get_or_create_session()
            yield json.dumps({'session_id': session_id}) + '\n'
        
        # Build conversation context
        context = conversation.build_context(session_id, user_input)
        
        # Send the full prompt immediately if requested
        yield json.dumps({'full_prompt': context}) + '\n'
        
        # Start timing
        start_time = time.time()
        
        # Prepare options from config
        options = {
            "num_predict": current_app.config.get('MAX_TOKENS', 1000),
            "temperature": current_app.config.get('TEMPERATURE', 0.7),
            "top_k": current_app.config.get('TOP_K', 40),
            "top_p": current_app.config.get('TOP_P', 0.9),
            "num_ctx": current_app.config.get('NUM_CTX', 8192),
            "num_batch": current_app.config.get('NUM_BATCH', 512),
            "num_thread": current_app.config.get('NUM_THREAD', 8),
            "repeat_penalty": current_app.config.get('REPEAT_PENALTY', 1.1),
            "num_gpu": current_app.config.get('NUM_GPU', -1),
            "gpu_layers": current_app.config.get('GPU_LAYERS', 99)
        }
        
        # Stream response from Ollama
        full_response = ""
        for chunk in ollama.generate_stream(context, options):
            if 'error' in chunk:
                yield json.dumps({
                    'error': chunk['error'],
                    'done': True
                }) + '\n'
                return
            
            if 'response' in chunk:
                full_response += chunk['response']
                yield json.dumps({
                    'token': chunk['response'],
                    'done': chunk.get('done', False)
                }) + '\n'
            
            if chunk.get('done', False):
                # Store conversation in history
                conversation.add_exchange(session_id, user_input, full_response)
                
                total_time = time.time() - start_time
                yield json.dumps({
                    'done': True,
                    'total_time': total_time,
                    'model': chunk.get('model', ''),
                    'eval_count': chunk.get('eval_count', 0),
                    'eval_duration': chunk.get('eval_duration', 0)
                }) + '\n'
                
                logger.info(f"Chat completed in {total_time:.2f}s")
                
    except Exception as e:
        logger.error(f"Chat stream error: {e}")
        yield json.dumps({
            'error': f'An error occurred: {str(e)}',
            'done': True
        }) + '\n'


@bp.route('/chat/tokens', methods=['POST'])
def count_tokens():
    """Count tokens in the current conversation."""
    data = request.json
    session_id = data.get('session_id')
    
    if not session_id:
        return jsonify({'count': 0})
    
    conversation = get_conversation_service()
    token_counter = TokenCounter()
    
    # Build full context to count tokens
    context = conversation.build_context(session_id, "")
    token_count = token_counter.count(context)
    
    return jsonify({
        'count': token_count,
        'limit': current_app.config.get('NUM_CTX', 8192)
    })