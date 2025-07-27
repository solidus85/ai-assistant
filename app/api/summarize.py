"""Summarization API endpoints."""
from flask import Blueprint, request, Response, stream_with_context, current_app, jsonify
import json
import time
import logging
from app.utils.extensions import get_ollama_service
from app.utils.token_counter import TokenCounter

bp = Blueprint('summarize', __name__, url_prefix='/api')
logger = logging.getLogger(__name__)

# Fixed system prompt for summarization
SUMMARIZATION_PROMPT = """Task: Read the paragraph and rewrite it to preserve only the essential meaning.
Remove filler, repetition, and minor details. Keep it concise but clear.
Limit the output to 2–3 sentences if needed, but prioritize clarity and brevity."""


@bp.route('/summarize/stream', methods=['POST'])
def summarize_stream():
    """Handle streaming summarization requests using Phi3:mini."""
    data = request.json
    user_input = data.get('text', '')
    
    if not user_input:
        return Response(
            json.dumps({'error': 'No text provided'}) + '\n',
            mimetype='application/json'
        )
    
    return Response(
        stream_with_context(generate_summarization_stream(user_input)),
        mimetype='application/json'
    )


def generate_summarization_stream(user_input: str):
    """Generate streaming summarization response using Phi3:mini."""
    # Create a temporary Ollama service instance for Phi3:mini
    ollama = get_ollama_service()
    original_model = ollama.model_name
    ollama.model_name = 'phi3:mini'  # Force Phi3:mini for summarization
    
    try:
        # Start timing
        start_time = time.time()
        
        # Prepare options from config (but use Phi3:mini)
        options = {
            "num_predict": current_app.config.get('MAX_TOKENS', 8192),
            "temperature": 0.3,  # Lower temperature for more focused summaries
            "top_k": current_app.config.get('TOP_K', 40),
            "top_p": 0.9,
            "num_ctx": current_app.config.get('NUM_CTX', 8192),
            "num_batch": current_app.config.get('NUM_BATCH', 512),
            "num_thread": current_app.config.get('NUM_THREAD', 8),
            "repeat_penalty": current_app.config.get('REPEAT_PENALTY', 1.1),
            "num_gpu": current_app.config.get('NUM_GPU', -1),
            "gpu_layers": current_app.config.get('GPU_LAYERS', 99)
        }
        
        # Stream response from Ollama with fixed system prompt
        full_response = ""
        for chunk in ollama.generate_stream(user_input, options, SUMMARIZATION_PROMPT):
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
                total_time = time.time() - start_time
                yield json.dumps({
                    'done': True,
                    'total_time': total_time,
                    'model': 'phi3:mini',
                    'eval_count': chunk.get('eval_count', 0),
                    'eval_duration': chunk.get('eval_duration', 0)
                }) + '\n'
                
                logger.info(f"Summarization completed in {total_time:.2f}s")
                
    except Exception as e:
        logger.error(f"Summarization stream error: {e}")
        yield json.dumps({
            'error': f'An error occurred: {str(e)}',
            'done': True
        }) + '\n'
    finally:
        # Restore original model
        ollama.model_name = original_model


@bp.route('/summarize/tokens', methods=['POST'])
def count_summarize_tokens():
    """Count tokens in the text to be summarized."""
    data = request.json
    text = data.get('text', '')
    
    token_counter = TokenCounter()
    
    # Include system prompt in token count
    full_context = f"System: {SUMMARIZATION_PROMPT}\n\nUser: {text}"
    token_count = token_counter.count(full_context)
    
    return jsonify({
        'count': token_count,
        'limit': current_app.config.get('NUM_CTX', 8192)
    })