"""Unit tests for ConversationService."""
import pytest
from src.services.conversation_service import ConversationService


class TestConversationService:
    """Test cases for ConversationService."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.service = ConversationService(max_history=5)
    
    def test_add_message(self):
        """Test adding messages to conversation."""
        self.service.add_message("user", "Hello")
        self.service.add_message("assistant", "Hi there!")
        
        history = self.service.get_history()
        assert len(history) == 2
        assert history[0]['role'] == 'user'
        assert history[0]['content'] == 'Hello'
        assert history[1]['role'] == 'assistant'
        assert history[1]['content'] == 'Hi there!'
    
    def test_max_history_limit(self):
        """Test that history respects max limit."""
        for i in range(10):
            self.service.add_message("user", f"Message {i}")
        
        history = self.service.get_history()
        assert len(history) == 5
        assert history[0]['content'] == 'Message 5'
        assert history[-1]['content'] == 'Message 9'
    
    def test_clear_history(self):
        """Test clearing conversation history."""
        self.service.add_message("user", "Hello")
        self.service.add_message("assistant", "Hi")
        
        assert len(self.service.get_history()) == 2
        
        self.service.clear()
        assert len(self.service.get_history()) == 0
    
    def test_get_context(self):
        """Test getting formatted context."""
        self.service.add_message("user", "What's the weather?")
        self.service.add_message("assistant", "I don't have weather data.")
        self.service.add_message("user", "Tell me a joke")
        
        context = self.service.get_context()
        
        assert "User: What's the weather?" in context
        assert "Assistant: I don't have weather data." in context
        assert "User: Tell me a joke" in context
    
    def test_get_context_with_limit(self):
        """Test getting context with message limit."""
        for i in range(5):
            self.service.add_message("user", f"Message {i}")
            self.service.add_message("assistant", f"Response {i}")
        
        context = self.service.get_context(last_n=4)
        
        assert "Message 3" in context
        assert "Response 3" in context
        assert "Message 4" in context
        assert "Response 4" in context
        assert "Message 2" not in context
    
    def test_empty_context(self):
        """Test getting context when history is empty."""
        context = self.service.get_context()
        assert context == ""
    
    def test_invalid_role(self):
        """Test that invalid roles are still stored."""
        self.service.add_message("invalid_role", "Test message")
        history = self.service.get_history()
        
        assert len(history) == 1
        assert history[0]['role'] == 'invalid_role'
        assert history[0]['content'] == 'Test message'