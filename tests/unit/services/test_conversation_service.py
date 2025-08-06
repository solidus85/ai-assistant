"""Unit tests for ConversationService."""
import pytest
from src.services.conversation_service import ConversationService


class TestConversationService:
    """Test cases for ConversationService."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.service = ConversationService(max_history=5)
    
    def test_get_or_create_session_new(self):
        """Test creating a new session."""
        session_id = self.service.get_or_create_session()
        
        assert session_id is not None
        assert session_id in self.service.conversations
        assert self.service.conversations[session_id] == []
    
    def test_get_or_create_session_existing(self):
        """Test getting an existing session."""
        session_id = "test-session-123"
        self.service.conversations[session_id] = [{'user': 'Hi', 'assistant': 'Hello'}]
        
        returned_id = self.service.get_or_create_session(session_id)
        
        assert returned_id == session_id
        assert len(self.service.conversations[session_id]) == 1
    
    def test_add_exchange(self):
        """Test adding conversation exchange."""
        session_id = "test-session"
        self.service.add_exchange(session_id, "Hello", "Hi there!")
        
        history = self.service.get_history(session_id)
        assert len(history) == 1
        assert history[0]['user'] == "Hello"
        assert history[0]['assistant'] == "Hi there!"
    
    def test_max_history_limit(self):
        """Test that history respects max limit."""
        session_id = "test-session"
        
        for i in range(10):
            self.service.add_exchange(session_id, f"Message {i}", f"Response {i}")
        
        history = self.service.get_history(session_id)
        assert len(history) == 5  # max_history is 5
        assert history[0]['user'] == "Message 5"
        assert history[-1]['user'] == "Message 9"
    
    def test_build_context(self):
        """Test building conversation context."""
        session_id = "test-session"
        self.service.add_exchange(session_id, "What's the weather?", "I don't have weather data.")
        self.service.add_exchange(session_id, "Tell me a joke", "Why did the chicken cross the road?")
        
        context = self.service.build_context(session_id, "What time is it?")
        
        assert "Human: What's the weather?" in context
        assert "I don't have weather data." in context
        assert "Human: Tell me a joke" in context
        assert "Why did the chicken cross the road?" in context
        assert "Human: What time is it?" in context
    
    def test_build_context_no_history(self):
        """Test building context with no history."""
        session_id = "new-session"
        context = self.service.build_context(session_id, "Hello")
        
        assert context == "Human: Hello\n\n"
    
    def test_clear_session_success(self):
        """Test clearing session history."""
        session_id = "test-session"
        self.service.add_exchange(session_id, "Hello", "Hi")
        
        assert len(self.service.get_history(session_id)) == 1
        
        result = self.service.clear_session(session_id)
        
        assert result is True
        assert len(self.service.get_history(session_id)) == 0
    
    def test_clear_session_not_found(self):
        """Test clearing non-existent session."""
        result = self.service.clear_session("nonexistent")
        assert result is False
    
    def test_get_token_estimate(self):
        """Test token estimation for conversation."""
        session_id = "test-session"
        self.service.add_exchange(session_id, "Hello", "Hi there!")
        self.service.add_exchange(session_id, "How are you?", "I'm doing well, thank you!")
        
        estimate = self.service.get_token_estimate(session_id)
        
        # Rough estimate should be total chars / 4
        total_chars = len("Hello") + len("Hi there!") + len("How are you?") + len("I'm doing well, thank you!")
        expected = total_chars // 4
        
        assert estimate == expected
    
    def test_get_token_estimate_no_session(self):
        """Test token estimation for non-existent session."""
        estimate = self.service.get_token_estimate("nonexistent")
        assert estimate == 0