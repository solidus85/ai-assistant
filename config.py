import os

class Config:
    """Base configuration class."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Ollama settings
    OLLAMA_BASE_URL = os.environ.get('OLLAMA_BASE_URL', 'http://localhost:11434')
    DEFAULT_MODEL = os.environ.get('DEFAULT_MODEL', 'mixtral')
    MODEL_NAME = os.environ.get('MODEL_NAME', 'phi3:mini')
    MAX_CONVERSATION_HISTORY = 10
    
    # Flask settings
    DEBUG = False
    TESTING = False
    
    # Model performance settings (optimized for RTX 4080)
    MAX_TOKENS = int(os.environ.get('MAX_TOKENS', 8192))  # Increased to allow longer responses
    TEMPERATURE = float(os.environ.get('TEMPERATURE', 0.7))
    NUM_CTX = int(os.environ.get('NUM_CTX', 32768))  # 32K context for Phi-3 (can go up to 128K)
    
    # System prompt
    SYSTEM_PROMPT = os.environ.get('SYSTEM_PROMPT', 'You are a helpful AI assistant. Provide clear, accurate, and well-structured responses.')
    NUM_BATCH = int(os.environ.get('NUM_BATCH', 512))  # Optimal batch size for RTX 4080
    NUM_THREAD = int(os.environ.get('NUM_THREAD', 16))  # More threads with available CPU
    TOP_K = int(os.environ.get('TOP_K', 40))
    TOP_P = float(os.environ.get('TOP_P', 0.9))
    REPEAT_PENALTY = float(os.environ.get('REPEAT_PENALTY', 1.1))
    
    # GPU settings
    NUM_GPU = int(os.environ.get('NUM_GPU', 99))  # Use all GPU layers
    GPU_LAYERS = int(os.environ.get('GPU_LAYERS', 99))  # Load all layers to GPU
    
    # API settings (for future API key support)
    API_KEY_REQUIRED = os.environ.get('API_KEY_REQUIRED', 'false').lower() == 'true'
    API_KEYS = os.environ.get('API_KEYS', '').split(',') if os.environ.get('API_KEYS') else []
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', None)
    
    # Rate limiting (for future implementation)
    RATE_LIMIT_ENABLED = os.environ.get('RATE_LIMIT_ENABLED', 'false').lower() == 'true'
    RATE_LIMIT_PER_MINUTE = int(os.environ.get('RATE_LIMIT_PER_MINUTE', 60))

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    
class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    
class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}