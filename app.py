from flask import Flask, render_template, request, jsonify, Response, stream_with_context, session
import requests
import json
import logging
import os
import time
import uuid
import tiktoken
from config import config

# Get configuration
config_name = os.environ.get('FLASK_ENV', 'default')
app_config = config[config_name]

app = Flask(__name__)
app.config.from_object(app_config)

# Configure logging
logging.basicConfig(level=getattr(logging, app_config.LOG_LEVEL))
logger = logging.getLogger(__name__)

# Ollama configuration
OLLAMA_BASE_URL = app_config.OLLAMA_BASE_URL
MODEL_NAME = "phi3:mini"  # Using smaller, faster model for responsiveness

# Store conversations in memory (use Redis or database for production)
conversations = {}

# Initialize tokenizer (using GPT-2 tokenizer as approximation for Mixtral)
try:
    encoding = tiktoken.get_encoding("gpt2")
except Exception as e:
    logger.warning(f"Could not load tiktoken: {e}")
    encoding = None

def count_tokens(text):
    """Count approximate tokens in text."""
    try:
        if encoding:
            return len(encoding.encode(text))
        else:
            # Fallback: rough estimation of 1 token per 4 characters
            return len(text) // 4
    except:
        # Fallback: rough estimation of 1 token per 4 characters
        return len(text) // 4

def query_ollama(prompt):
    """Send a query to Ollama and get the response."""
    try:
        url = f"{OLLAMA_BASE_URL}/api/generate"
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
        
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        result = response.json()
        return result.get('response', 'No response received')
    
    except requests.exceptions.ConnectionError:
        logger.error("Failed to connect to Ollama. Make sure Ollama is running.")
        return "Error: Could not connect to Ollama. Please ensure Ollama is running on your system."
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {str(e)}")
        return f"Error: {str(e)}"
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return f"Unexpected error: {str(e)}"

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat requests with streaming support."""
    try:
        data = request.get_json()
        user_input = data.get('message', '')
        
        if not user_input:
            return jsonify({'error': 'No message provided'}), 400
        
        # Query Ollama
        response = query_ollama(user_input)
        
        return jsonify({
            'response': response,
            'status': 'success'
        })
    
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/chat/stream', methods=['POST'])
def chat_stream():
    """Handle streaming chat requests with conversation history."""
    def generate():
        try:
            data = request.get_json()
            user_input = data.get('message', '')
            session_id = data.get('session_id', None)
            
            if not user_input:
                yield json.dumps({'error': 'No message provided'}) + '\n'
                return
            
            # Generate session ID if not provided
            if not session_id:
                session_id = str(uuid.uuid4())
                yield json.dumps({'session_id': session_id}) + '\n'
            
            # Get conversation history
            if session_id not in conversations:
                conversations[session_id] = []
            
            # Build conversation context
            context = ""
            for msg in conversations[session_id]:
                context += f"User: {msg['user']}\nAssistant: {msg['assistant']}\n\n"
            context += f"User: {user_input}\nAssistant:"
            
            # Start timing
            start_time = time.time()
            
            url = f"{OLLAMA_BASE_URL}/api/generate"
            payload = {
                "model": MODEL_NAME,
                "prompt": context,
                "stream": True,
                "options": {
                    "num_predict": app_config.MAX_TOKENS,
                    "temperature": app_config.TEMPERATURE,
                    "top_k": app_config.TOP_K,
                    "top_p": app_config.TOP_P,
                    "num_ctx": app_config.NUM_CTX,
                    "num_batch": app_config.NUM_BATCH,
                    "num_thread": app_config.NUM_THREAD,
                    "repeat_penalty": app_config.REPEAT_PENALTY,
                    "num_gpu": app_config.NUM_GPU,
                    "gpu_layers": app_config.GPU_LAYERS
                }
            }
            
            with requests.post(url, json=payload, stream=True) as response:
                response.raise_for_status()
                
                full_response = ""
                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line)
                        if 'response' in chunk:
                            full_response += chunk['response']
                            yield json.dumps({
                                'token': chunk['response'],
                                'done': chunk.get('done', False)
                            }) + '\n'
                        
                        if chunk.get('done', False):
                            # Store conversation in history
                            conversations[session_id].append({
                                'user': user_input,
                                'assistant': full_response
                            })
                            
                            # Limit conversation history to last 10 exchanges
                            if len(conversations[session_id]) > 10:
                                conversations[session_id] = conversations[session_id][-10:]
                            
                            total_time = time.time() - start_time
                            yield json.dumps({
                                'done': True,
                                'total_time': total_time,
                                'session_id': session_id
                            }) + '\n'
                            break
                            
        except requests.exceptions.ConnectionError:
            yield json.dumps({'error': 'Could not connect to Ollama'}) + '\n'
        except Exception as e:
            yield json.dumps({'error': str(e)}) + '\n'
    
    return Response(stream_with_context(generate()), mimetype='application/x-ndjson')

@app.route('/api/tokens/count', methods=['POST'])
def count_prompt_tokens():
    """Count tokens in the current conversation context."""
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        current_message = data.get('message', '')
        
        # Build the same context that would be sent to Ollama
        context = ""
        if session_id and session_id in conversations:
            for msg in conversations[session_id]:
                context += f"User: {msg['user']}\nAssistant: {msg['assistant']}\n\n"
        
        # Add current message
        if current_message:
            context += f"User: {current_message}\nAssistant:"
        
        # Count tokens
        token_count = count_tokens(context)
        
        return jsonify({
            'status': 'success',
            'token_count': token_count,
            'context_limit': app_config.NUM_CTX,
            'percentage': round((token_count / app_config.NUM_CTX) * 100, 1)
        })
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)}), 500

@app.route('/api/conversation/clear', methods=['POST'])
def clear_conversation():
    """Clear conversation history for a session."""
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        
        if session_id and session_id in conversations:
            conversations[session_id] = []
            return jsonify({'status': 'success', 'message': 'Conversation cleared'})
        
        return jsonify({'status': 'success', 'message': 'No conversation to clear'})
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Check if Ollama is accessible."""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags")
        response.raise_for_status()
        models = response.json().get('models', [])
        
        # Check if mixtral is available
        mixtral_available = any(model.get('name', '').startswith('mixtral') for model in models)
        
        return jsonify({
            'status': 'healthy',
            'ollama_connected': True,
            'mixtral_available': mixtral_available,
            'available_models': [model.get('name') for model in models],
            'context_limit': app_config.NUM_CTX
        })
    except:
        return jsonify({
            'status': 'unhealthy',
            'ollama_connected': False,
            'mixtral_available': False
        }), 503

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)