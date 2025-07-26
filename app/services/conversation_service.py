"""Service for managing conversation history."""
import uuid
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class ConversationService:
    """Manages conversation history and context."""
    
    def __init__(self, max_history: int = 10):
        self.conversations: Dict[str, List[Dict[str, str]]] = {}
        self.max_history = max_history
    
    def get_or_create_session(self, session_id: Optional[str] = None) -> str:
        """Get existing session or create new one."""
        if not session_id:
            session_id = str(uuid.uuid4())
        
        if session_id not in self.conversations:
            self.conversations[session_id] = []
            
        return session_id
    
    def add_exchange(self, session_id: str, user_input: str, assistant_response: str) -> None:
        """Add a conversation exchange to history."""
        if session_id not in self.conversations:
            self.conversations[session_id] = []
        
        self.conversations[session_id].append({
            'user': user_input,
            'assistant': assistant_response
        })
        
        # Limit conversation history
        if len(self.conversations[session_id]) > self.max_history:
            self.conversations[session_id] = self.conversations[session_id][-self.max_history:]
    
    def build_context(self, session_id: str, user_input: str) -> str:
        """Build conversation context for the model."""
        context = ""
        
        if session_id in self.conversations:
            for msg in self.conversations[session_id]:
                context += f"Human: {msg['user']}\n\n{msg['assistant']}\n\n"
        
        context += f"Human: {user_input}\n\n"
        return context
    
    def get_history(self, session_id: str) -> List[Dict[str, str]]:
        """Get conversation history for a session."""
        return self.conversations.get(session_id, [])
    
    def clear_session(self, session_id: str) -> bool:
        """Clear conversation history for a session."""
        if session_id in self.conversations:
            self.conversations[session_id] = []
            logger.info(f"Cleared conversation for session: {session_id}")
            return True
        return False
    
    def get_token_estimate(self, session_id: str) -> int:
        """Estimate token count for conversation (rough estimate)."""
        if session_id not in self.conversations:
            return 0
        
        # Rough estimate: ~4 characters per token
        char_count = 0
        for msg in self.conversations[session_id]:
            char_count += len(msg['user']) + len(msg['assistant'])
        
        return char_count // 4