"""Model-specific configurations."""

MODEL_CONFIGS = {
    "phi3:mini": {
        "name": "Phi-3 Mini",
        "size": "3.8B",
        "context_window": 128000,  # 128K max
        "recommended_context": 32768,  # 32K recommended for speed
        "vram_usage": "2-3GB",
        "speed": "Fast",
        "description": "Small, fast model with large context window"
    },
    "mixtral:latest": {
        "name": "Mixtral Q4",
        "size": "46.7B", 
        "context_window": 32768,  # 32K max
        "recommended_context": 8192,  # 8K recommended
        "vram_usage": "13-15GB",
        "speed": "Medium",
        "description": "Balanced accuracy and speed"
    },
    "mixtral-accurate:latest": {
        "name": "Mixtral Q5_K_M",
        "size": "46.7B",
        "context_window": 32768,  # 32K max
        "recommended_context": 8192,  # 8K recommended
        "vram_usage": "15-16GB",
        "speed": "Slow",
        "description": "High accuracy, 99% quality retention"
    },
    "tinyllama": {
        "name": "TinyLlama",
        "size": "1.1B",
        "context_window": 2048,
        "recommended_context": 2048,
        "vram_usage": "1GB",
        "speed": "Very Fast",
        "description": "Tiny model for basic tasks"
    }
}

def get_model_config(model_name):
    """Get configuration for a specific model."""
    return MODEL_CONFIGS.get(model_name, {
        "name": model_name,
        "context_window": 8192,
        "recommended_context": 8192,
        "description": "Unknown model"
    })