"""Model-specific configuration profiles for optimal performance."""

MODEL_PROFILES = {
    'phi3:mini': {
        'description': 'Fast, lightweight model for quick responses',
        'settings': {
            'NUM_CTX': 32768,  # Phi-3 can handle up to 128K
            'MAX_TOKENS': 8192,
            'TEMPERATURE': 0.7,
            'NUM_BATCH': 512,
            'NUM_THREAD': 16,
            'TOP_K': 40,
            'TOP_P': 0.9,
            'REPEAT_PENALTY': 1.1,
            'NUM_GPU': 99,
            'GPU_LAYERS': 99
        },
        'expected_speed': '1-2 seconds',
        'vram_usage': '2-3 GB'
    },
    
    'mixtral-accurate:latest': {
        'description': 'High accuracy model, optimized for speed',
        'settings': {
            'NUM_CTX': 8192,  # Reduced from 32K for 2x speed improvement
            'MAX_TOKENS': 4096,  # Reduced for faster responses
            'TEMPERATURE': 0.7,
            'NUM_BATCH': 512,
            'NUM_THREAD': 8,  # Reduced threads for better GPU utilization
            'TOP_K': 40,
            'TOP_P': 0.9,
            'REPEAT_PENALTY': 1.1,
            'NUM_GPU': 99,
            'GPU_LAYERS': 99
        },
        'expected_speed': '15-25 seconds (vs 30-60s with 32K context)',
        'vram_usage': '15-16 GB'
    },
    
    'mixtral:latest': {
        'description': 'Balanced Mixtral with Q4 quantization',
        'settings': {
            'NUM_CTX': 4096,  # Smaller context for speed
            'MAX_TOKENS': 2048,
            'TEMPERATURE': 0.7,
            'NUM_BATCH': 256,
            'NUM_THREAD': 8,
            'TOP_K': 40,
            'TOP_P': 0.9,
            'REPEAT_PENALTY': 1.1,
            'NUM_GPU': 99,
            'GPU_LAYERS': 99
        },
        'expected_speed': '10-20 seconds',
        'vram_usage': '13-15 GB'
    },
    
    'llama3.1:8b': {
        'description': 'Balanced model with good speed and accuracy',
        'settings': {
            'NUM_CTX': 8192,
            'MAX_TOKENS': 4096,
            'TEMPERATURE': 0.7,
            'NUM_BATCH': 512,
            'NUM_THREAD': 16,
            'TOP_K': 40,
            'TOP_P': 0.9,
            'REPEAT_PENALTY': 1.1,
            'NUM_GPU': 99,
            'GPU_LAYERS': 99
        },
        'expected_speed': '2-3 seconds',
        'vram_usage': '5-6 GB'
    },
    
    'qwen2.5:14b': {
        'description': 'Modern model with excellent multilingual support',
        'settings': {
            'NUM_CTX': 16384,
            'MAX_TOKENS': 4096,
            'TEMPERATURE': 0.7,
            'NUM_BATCH': 512,
            'NUM_THREAD': 16,
            'TOP_K': 40,
            'TOP_P': 0.9,
            'REPEAT_PENALTY': 1.1,
            'NUM_GPU': 99,
            'GPU_LAYERS': 99
        },
        'expected_speed': '5-10 seconds',
        'vram_usage': '8-10 GB'
    }
}

# Speed optimization tips
OPTIMIZATION_TIPS = {
    'context_window': {
        'title': 'Context Window Size',
        'impact': 'High',
        'tips': [
            '32K → 8K context: ~50% speed improvement',
            '8K → 4K context: ~25% additional speed improvement',
            '2K context: Maximum speed but limited conversation history'
        ]
    },
    'max_tokens': {
        'title': 'Maximum Response Length',
        'impact': 'Medium',
        'tips': [
            'Reducing from 8K to 2K tokens can save 5-10 seconds',
            'Most responses use <1000 tokens',
            'Set based on your typical use case'
        ]
    },
    'batch_size': {
        'title': 'Batch Size',
        'impact': 'Low',
        'tips': [
            '512 is optimal for most models',
            'Larger batch sizes may slow down Mixtral',
            'Smaller batch sizes (256) can help with memory constraints'
        ]
    },
    'temperature': {
        'title': 'Temperature',
        'impact': 'Low',
        'tips': [
            'Lower temperature (0.3-0.5) for faster, more deterministic responses',
            'Higher temperature (0.7-0.9) for more creative outputs',
            'Minimal impact on speed'
        ]
    }
}

def get_model_config(model_name):
    """Get optimized configuration for a specific model."""
    return MODEL_PROFILES.get(model_name, MODEL_PROFILES['phi3:mini'])

def apply_model_profile(app, model_name):
    """Apply model-specific settings to Flask app config."""
    profile = get_model_config(model_name)
    for key, value in profile['settings'].items():
        app.config[key] = value
    return profile