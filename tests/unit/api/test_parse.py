"""Unit tests for parse API endpoint."""
import pytest
import json
from unittest.mock import patch, MagicMock


class TestParseAPI:
    """Test cases for parse API endpoint."""
    
    def test_parse_stream_success(self, client):
        """Test successful streaming parse."""
        with patch('src.api.parse.get_ollama_service') as mock_get_service, \
             patch('src.api.parse.current_app') as mock_app:
            
            mock_service = MagicMock()
            mock_service.chat_stream.return_value = [
                {'message': {'content': 'Parsing'}, 'done': False},
                {'message': {'content': ' complete'}, 'done': True}
            ]
            mock_get_service.return_value = mock_service
            
            mock_app.config.get.side_effect = lambda key, default: {
                'PARSE_SYSTEM_PROMPT': 'You are a parsing assistant',
                'MAX_TOKENS': 8192,
                'TOP_K': 40,
                'NUM_CTX': 8192,
                'NUM_BATCH': 512,
                'NUM_THREAD': 8,
                'REPEAT_PENALTY': 1.1,
                'NUM_GPU': -1,
                'GPU_LAYERS': 99
            }.get(key, default)
            
            response = client.post('/api/parse/stream',
                                 json={'text': 'Parse this text'},
                                 headers={'Content-Type': 'application/json'})
            
            assert response.status_code == 200
            assert response.content_type == 'application/json'
            
            # Parse streaming JSON data
            data = response.data.decode('utf-8')
            lines = data.strip().split('\n')
            
            assert len(lines) >= 1
            # Check that we got some content
            for line in lines:
                if line:
                    parsed = json.loads(line)
                    assert 'content' in parsed or 'error' in parsed
                    assert 'done' in parsed
    
    def test_parse_stream_missing_text(self, client):
        """Test parse stream with missing text."""
        response = client.post('/api/parse/stream',
                              json={},
                              headers={'Content-Type': 'application/json'})
        
        assert response.status_code == 200  # Returns 200 with error in response
        data = response.data.decode('utf-8')
        parsed = json.loads(data.strip())
        assert 'error' in parsed
        assert 'No text provided' in parsed['error']
    
    def test_parse_stream_empty_text(self, client):
        """Test parse stream with empty text."""
        response = client.post('/api/parse/stream',
                              json={'text': ''},
                              headers={'Content-Type': 'application/json'})
        
        assert response.status_code == 200
        data = response.data.decode('utf-8')
        parsed = json.loads(data.strip())
        assert 'error' in parsed
        assert 'No text provided' in parsed['error']
    
    def test_parse_stream_with_custom_system_prompt(self, client):
        """Test parse stream with custom system prompt from config."""
        with patch('src.api.parse.get_ollama_service') as mock_get_service, \
             patch('src.api.parse.current_app') as mock_app:
            
            mock_service = MagicMock()
            mock_service.chat_stream.return_value = [
                {'message': {'content': 'Result'}, 'done': True}
            ]
            mock_get_service.return_value = mock_service
            
            mock_app.config.get.return_value = 'Custom parsing instructions'
            
            response = client.post('/api/parse/stream',
                                 json={'text': 'Test text'},
                                 headers={'Content-Type': 'application/json'})
            
            assert response.status_code == 200
            
            # Verify that chat_stream was called with messages including system prompt
            call_args = mock_service.chat_stream.call_args
            messages = call_args[0][0]
            assert len(messages) == 2
            assert messages[0]['role'] == 'system'
            assert 'Custom parsing instructions' in messages[0]['content']
    
    def test_parse_stream_error_handling(self, client):
        """Test error handling in parse stream."""
        with patch('src.api.parse.get_ollama_service') as mock_get_service:
            mock_service = MagicMock()
            mock_service.chat_stream.side_effect = Exception("API Error")
            mock_get_service.return_value = mock_service
            
            response = client.post('/api/parse/stream',
                                 json={'text': 'Test'},
                                 headers={'Content-Type': 'application/json'})
            
            # Should still return 200 but with error in stream
            assert response.status_code == 200
            data = response.data.decode('utf-8')
            assert 'error' in data.lower() or 'API Error' in data