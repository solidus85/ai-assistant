"""Token counting utilities."""
import tiktoken
import logging

logger = logging.getLogger(__name__)


class TokenCounter:
    """Handles token counting for conversation context."""
    
    def __init__(self, model: str = "gpt-3.5-turbo"):
        """Initialize with tiktoken encoder."""
        try:
            self.encoder = tiktoken.encoding_for_model(model)
        except KeyError:
            # Fallback to cl100k_base encoding
            self.encoder = tiktoken.get_encoding("cl100k_base")
    
    def count(self, text: str) -> int:
        """Count tokens in text."""
        try:
            return len(self.encoder.encode(text))
        except Exception as e:
            logger.error(f"Token counting error: {e}")
            # Fallback to character-based estimation
            return len(text) // 4