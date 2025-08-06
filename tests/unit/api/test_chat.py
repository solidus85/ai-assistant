"""Unit tests for chat API endpoint."""
import pytest
import json
from unittest.mock import patch, MagicMock


class TestChatAPI:
    """Test cases for chat API endpoint."""
    
    def test_chat_stream_success(self, client):
        """Test successful streaming chat."""
        with patch('src.api.chat.get_ollama_service') as mock_get_service:
            mock_service = MagicMock()
            mock_service.model_name = 'gemma3:12b-it-qat'
            mock_service.generate_stream.return_value = [
                {'response': 'Hello', 'done': False},
                {'response': ' world', 'done': False},
                {'response': '!', 'done': True}
            ]
            mock_get_service.return_value = mock_service
            
            response = client.post('/api/chat/stream',
                                 json={'message': 'Say hello'},
                                 headers={'Content-Type': 'application/json'})
            
            assert response.status_code == 200
            assert response.content_type == 'application/json'
            
            # Parse streaming JSON data
            data = response.data.decode('utf-8')
            lines = data.strip().split('\n')
            
            assert len(lines) >= 1
            mock_service.generate_stream.assert_called_once()
    
    def test_chat_stream_missing_message(self, client):
        """Test chat stream with missing message."""
        response = client.post('/api/chat/stream',
                              json={},
                              headers={'Content-Type': 'application/json'})
        
        assert response.status_code == 200  # Returns 200 with error in response
        data = response.data.decode('utf-8')
        assert 'error' in data
        assert 'No message provided' in data
    
    def test_chat_stream_with_session_id(self, client):
        """Test chat stream with session ID."""
        with patch('src.api.chat.get_ollama_service') as mock_get_service:
            mock_service = MagicMock()
            mock_service.model_name = 'gemma3:12b-it-qat'
            mock_service.generate_stream.return_value = [
                {'response': 'Test', 'done': True}
            ]
            mock_get_service.return_value = mock_service
            
            response = client.post('/api/chat/stream',
                                 json={
                                     'message': 'Test',
                                     'session_id': 'test-session-123'
                                 },
                                 headers={'Content-Type': 'application/json'})
            
            assert response.status_code == 200
    
    def test_chat_stream_with_system_prompt(self, client):
        """Test chat stream with system prompt from config."""
        with patch('src.api.chat.get_ollama_service') as mock_get_service, \
             patch('src.api.chat.current_app') as mock_app:
            
            mock_app.config.get.return_value = 'Be concise'
            mock_service = MagicMock()
            mock_service.model_name = 'gemma3:12b-it-qat'
            mock_service.generate_stream.return_value = [
                {'response': 'Response', 'done': True}
            ]
            mock_get_service.return_value = mock_service
            
            response = client.post('/api/chat/stream',
                                 json={'message': 'Test'},
                                 headers={'Content-Type': 'application/json'})
            
            assert response.status_code == 200
            data = response.data.decode('utf-8')
            # First line should contain full_prompt with system prompt
            first_line = data.split('\n')[0]
            assert 'full_prompt' in first_line
    
    def test_chat_stream_error_handling(self, client):
        """Test error handling in chat stream."""
        with patch('src.api.chat.get_ollama_service') as mock_get_service:
            mock_service = MagicMock()
            mock_service.model_name = 'gemma3:12b-it-qat'
            mock_service.generate_stream.side_effect = Exception("API Error")
            mock_get_service.return_value = mock_service
            
            response = client.post('/api/chat/stream',
                                 json={'message': 'Test'},
                                 headers={'Content-Type': 'application/json'})
            
            # Should still return 200 but with error in stream
            assert response.status_code == 200
            data = response.data.decode('utf-8')
            assert 'error' in data.lower() or 'API Error' in data