"""Unit tests for conversation API endpoints."""
import pytest
from unittest.mock import patch, MagicMock


class TestConversationAPI:
    """Test cases for conversation API endpoints."""
    
    def test_get_conversation_history_with_session(self, client):
        """Test getting conversation history with session ID."""
        with patch('src.api.conversation.get_conversation_service') as mock_get_service:
            mock_service = MagicMock()
            mock_service.get_history.return_value = [
                {'user': 'Hello', 'assistant': 'Hi there!'},
                {'user': 'How are you?', 'assistant': 'I am doing well, thank you!'}
            ]
            mock_get_service.return_value = mock_service
            
            response = client.get('/api/conversation/history?session_id=test-123')
            
            assert response.status_code == 200
            data = response.get_json()
            assert 'history' in data
            assert len(data['history']) == 2
            assert data['history'][0]['user'] == 'Hello'
            assert data['history'][0]['assistant'] == 'Hi there!'
            mock_service.get_history.assert_called_once_with('test-123')
    
    def test_get_conversation_history_without_session(self, client):
        """Test getting conversation history without session ID."""
        response = client.get('/api/conversation/history')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'history' in data
        assert data['history'] == []
    
    def test_clear_conversation_success(self, client):
        """Test successfully clearing conversation history."""
        with patch('src.api.conversation.get_conversation_service') as mock_get_service:
            mock_service = MagicMock()
            mock_service.clear_session.return_value = True
            mock_get_service.return_value = mock_service
            
            response = client.post('/api/conversation/clear',
                                  json={'session_id': 'test-123'},
                                  headers={'Content-Type': 'application/json'})
            
            assert response.status_code == 200
            data = response.get_json()
            assert data['success'] is True
            assert data['message'] == 'Conversation cleared'
            mock_service.clear_session.assert_called_once_with('test-123')
    
    def test_clear_conversation_no_session_id(self, client):
        """Test clearing conversation without session ID."""
        response = client.post('/api/conversation/clear',
                              json={},
                              headers={'Content-Type': 'application/json'})
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
        assert 'No session ID provided' in data['message']
    
    def test_clear_conversation_session_not_found(self, client):
        """Test clearing non-existent conversation session."""
        with patch('src.api.conversation.get_conversation_service') as mock_get_service:
            mock_service = MagicMock()
            mock_service.clear_session.return_value = False
            mock_get_service.return_value = mock_service
            
            response = client.post('/api/conversation/clear',
                                  json={'session_id': 'nonexistent'},
                                  headers={'Content-Type': 'application/json'})
            
            assert response.status_code == 404
            data = response.get_json()
            assert data['success'] is False
            assert 'Session not found' in data['message']