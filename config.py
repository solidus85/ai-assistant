import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def read_secret_key():
    """Read secret key from file or return default."""
    secret_key_path = os.getenv('SECRET_KEY_PATH', '.secret_key')
    
    if os.path.exists(secret_key_path):
        try:
            with open(secret_key_path, 'r') as f:
                key = f.read().strip()
                if key:
                    return key
        except Exception as e:
            print(f"Warning: Could not read secret key from {secret_key_path}: {e}")
    
    return 'dev-secret-key-change-in-production'

# Flask settings
SECRET_KEY = read_secret_key()
SECRET_KEY_PATH = os.getenv('SECRET_KEY_PATH', '.secret_key')
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 5000))
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
TESTING = os.getenv('TESTING', 'False').lower() == 'true'

# Ollama settings
OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
MODEL_NAME = os.getenv('MODEL_NAME', 'gemma3:12b-it-qat')
MAX_CONVERSATION_HISTORY = int(os.getenv('MAX_CONVERSATION_HISTORY', 10))

# Model performance settings (optimized for RTX 4080)
MAX_TOKENS = int(os.getenv('MAX_TOKENS', 2048))  # Optimized for 4K context window
TEMPERATURE = float(os.getenv('TEMPERATURE', 0.7))
NUM_CTX = int(os.getenv('NUM_CTX', 4096))  # 4K context - maximum speed

# System prompts
SYSTEM_PROMPT = os.getenv('SYSTEM_PROMPT', 
    'You are a helpful AI assistant. Provide clear, accurate, and well-structured responses.')
PARSE_SYSTEM_PROMPT = os.getenv('PARSE_SYSTEM_PROMPT',
    'You are a text parsing assistant. Extract and structure information from the provided text, identifying key entities, relationships, and important data points.')

# Advanced model settings
NUM_BATCH = int(os.getenv('NUM_BATCH', 512))  # Optimal batch size for RTX 4080
NUM_THREAD = int(os.getenv('NUM_THREAD', 16))  # More threads with available CPU
TOP_K = int(os.getenv('TOP_K', 40))
TOP_P = float(os.getenv('TOP_P', 0.9))
REPEAT_PENALTY = float(os.getenv('REPEAT_PENALTY', 1.1))

# GPU settings
NUM_GPU = int(os.getenv('NUM_GPU', 99))  # Use all GPU layers
GPU_LAYERS = int(os.getenv('GPU_LAYERS', 99))  # Load all layers to GPU

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', None)