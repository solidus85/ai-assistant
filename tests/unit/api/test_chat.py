"""Unit tests for chat API endpoint."""
import pytest
import json
from unittest.mock import patch, MagicMock


class TestChatAPI:
    """Test cases for chat API endpoint."""
    
    def test_chat_stream_success(self, client):
        """Test successful streaming chat."""
        with patch('src.api.chat.ollama_service') as mock_service, \
             patch('src.api.chat.conversation_service') as mock_conv:
            
            mock_service.generate_stream.return_value = [
                {'response': 'Hello', 'done': False},
                {'response': ' world', 'done': False},
                {'response': '!', 'done': True}
            ]
            
            response = client.post('/api/chat/stream',
                                 json={'prompt': 'Say hello'},
                                 headers={'Content-Type': 'application/json'})
            
            assert response.status_code == 200
            assert response.content_type == 'text/event-stream'
            
            # Parse SSE data
            data = response.data.decode('utf-8')
            events = data.strip().split('\n\n')
            
            assert len(events) >= 3
            mock_service.generate_stream.assert_called_once()
            mock_conv.add_message.assert_called()
    
    def test_chat_stream_missing_prompt(self, client):
        """Test chat stream with missing prompt."""
        response = client.post('/api/chat/stream',
                              json={},
                              headers={'Content-Type': 'application/json'})
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_chat_stream_with_options(self, client):
        """Test chat stream with custom options."""
        with patch('src.api.chat.ollama_service') as mock_service, \
             patch('src.api.chat.conversation_service'):
            
            mock_service.generate_stream.return_value = [
                {'response': 'Test', 'done': True}
            ]
            
            response = client.post('/api/chat/stream',
                                 json={
                                     'prompt': 'Test',
                                     'temperature': 0.5,
                                     'max_tokens': 100
                                 },
                                 headers={'Content-Type': 'application/json'})
            
            assert response.status_code == 200
            
            # Check that options were passed
            call_args = mock_service.generate_stream.call_args
            options = call_args[1]['options']
            assert options['temperature'] == 0.5
            assert options['num_predict'] == 100
    
    def test_chat_stream_with_system_prompt(self, client):
        """Test chat stream with system prompt."""
        with patch('src.api.chat.ollama_service') as mock_service, \
             patch('src.api.chat.conversation_service'):
            
            mock_service.generate_stream.return_value = [
                {'response': 'Response', 'done': True}
            ]
            
            response = client.post('/api/chat/stream',
                                 json={
                                     'prompt': 'Test',
                                     'system_prompt': 'Be concise'
                                 },
                                 headers={'Content-Type': 'application/json'})
            
            assert response.status_code == 200
            
            call_args = mock_service.generate_stream.call_args
            assert call_args[1]['system_prompt'] == 'Be concise'
    
    def test_chat_stream_error_handling(self, client):
        """Test error handling in chat stream."""
        with patch('src.api.chat.ollama_service') as mock_service, \
             patch('src.api.chat.conversation_service'):
            
            mock_service.generate_stream.side_effect = Exception("API Error")
            
            response = client.post('/api/chat/stream',
                                 json={'prompt': 'Test'},
                                 headers={'Content-Type': 'application/json'})
            
            # Should still return 200 but with error in stream
            assert response.status_code == 200
            data = response.data.decode('utf-8')
            assert 'error' in data.lower()