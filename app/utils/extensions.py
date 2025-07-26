"""Application extensions and service instances."""
from flask import current_app
from app.services import OllamaService, ConversationService

# Service instances
_ollama_service = None
_conversation_service = None


def get_ollama_service() -> OllamaService:
    """Get or create Ollama service instance."""
    global _ollama_service
    if _ollama_service is None:
        _ollama_service = OllamaService(
            base_url=current_app.config['OLLAMA_BASE_URL'],
            model_name=current_app.config['MODEL_NAME']
        )
    return _ollama_service


def get_conversation_service() -> ConversationService:
    """Get or create conversation service instance."""
    global _conversation_service
    if _conversation_service is None:
        _conversation_service = ConversationService(
            max_history=current_app.config.get('MAX_CONVERSATION_HISTORY', 10)
        )
    return _conversation_service