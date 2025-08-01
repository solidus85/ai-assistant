# Flask settings
SECRET_KEY = 'dev-secret-key-change-in-production'
HOST = '0.0.0.0'
PORT = 5000
DEBUG = False
TESTING = False

# Ollama settings
OLLAMA_BASE_URL = 'http://localhost:11434'
MODEL_NAME = 'gemma3:12b-it-qat'
SUMMARIZE_MODEL_NAME = 'phi3:3.8b'
MAX_CONVERSATION_HISTORY = 10

# Model performance settings (optimized for RTX 4080)
MAX_TOKENS = 2048  # Optimized for 4K context window
TEMPERATURE = 0.7
NUM_CTX = 4096  # 4K context - maximum speed

# System prompts
SYSTEM_PROMPT = 'You are a helpful AI assistant. Provide clear, accurate, and well-structured responses.'
SUMMARIZE_SYSTEM_PROMPT = """ 
    Task: Read the paragraph and rewrite it to preserve only the essential meaning. 
    Remove filler, repetition, and minor details. Keep it concise but clear. 
    Limit the output to 2–3 sentences if needed, but prioritize clarity and brevity.
"""
PARSE_SYSTEM_PROMPT = 'You are a text parsing assistant. Extract and structure information from the provided text, identifying key entities, relationships, and important data points.'

# Advanced model settings
NUM_BATCH = 512  # Optimal batch size for RTX 4080
NUM_THREAD = 16  # More threads with available CPU
TOP_K = 40
TOP_P = 0.9
REPEAT_PENALTY = 1.1

# GPU settings
NUM_GPU = 99  # Use all GPU layers
GPU_LAYERS = 99  # Load all layers to GPU

# Logging
LOG_LEVEL = 'INFO'
LOG_FILE = None