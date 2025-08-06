"""Token counting utilities."""
import logging

logger = logging.getLogger(__name__)


class TokenCounter:
    """Handles token counting for conversation context."""
    
    def __init__(self, model: str = "gemma"):
        """Initialize token counter for Ollama models."""
        self.model = model
        # Approximate tokens per character for estimation
        # Most models average around 3-4 characters per token
        self.chars_per_token = 4
    
    def count(self, text: str) -> int:
        """
        Estimate token count for text.
        
        For Ollama models, we use character-based estimation
        since tiktoken is specific to OpenAI models.
        """
        if not text:
            return 0
        
        # Basic estimation: ~4 characters per token on average
        # This is a reasonable approximation for most LLMs
        estimated_tokens = len(text) // self.chars_per_token
        
        # Account for whitespace and punctuation which often become separate tokens
        whitespace_count = text.count(' ') + text.count('\n') + text.count('\t')
        punctuation_count = sum(1 for char in text if char in '.,!?;:()[]{}"\'-')
        
        # Adjust estimate based on whitespace and punctuation
        estimated_tokens += (whitespace_count + punctuation_count) // 4
        
        return max(1, estimated_tokens)  # Ensure at least 1 token for non-empty text