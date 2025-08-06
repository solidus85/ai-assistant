"""Unit tests for conversation API endpoints."""
import pytest
from unittest.mock import patch


class TestConversationAPI:
    """Test cases for conversation API endpoints."""
    
    def test_get_conversation_history(self, client):
        """Test getting conversation history."""
        with patch('src.api.conversation.conversation_service') as mock_service:
            mock_service.get_history.return_value = [
                {'role': 'user', 'content': 'Hello'},
                {'role': 'assistant', 'content': 'Hi there!'}
            ]
            
            response = client.get('/api/conversation/history')
            
            assert response.status_code == 200
            data = response.get_json()
            assert 'history' in data
            assert len(data['history']) == 2
            assert data['history'][0]['role'] == 'user'
            assert data['history'][0]['content'] == 'Hello'
    
    def test_clear_conversation(self, client):
        """Test clearing conversation history."""
        with patch('src.api.conversation.conversation_service') as mock_service:
            response = client.post('/api/conversation/clear')
            
            assert response.status_code == 200
            data = response.get_json()
            assert data['status'] == 'cleared'
            mock_service.clear.assert_called_once()
    
    def test_get_conversation_context(self, client):
        """Test getting conversation context."""
        with patch('src.api.conversation.conversation_service') as mock_service:
            mock_service.get_context.return_value = "User: Hello\nAssistant: Hi!"
            
            response = client.get('/api/conversation/context')
            
            assert response.status_code == 200
            data = response.get_json()
            assert 'context' in data
            assert data['context'] == "User: Hello\nAssistant: Hi!"
    
    def test_get_context_with_limit(self, client):
        """Test getting context with message limit."""
        with patch('src.api.conversation.conversation_service') as mock_service:
            mock_service.get_context.return_value = "Limited context"
            
            response = client.get('/api/conversation/context?last_n=5')
            
            assert response.status_code == 200
            data = response.get_json()
            assert data['context'] == "Limited context"
            mock_service.get_context.assert_called_with(last_n=5)