"""Unit tests for parse API endpoint."""
import pytest
import json
from unittest.mock import patch, MagicMock


class TestParseAPI:
    """Test cases for parse API endpoint."""
    
    def test_parse_stream_success(self, client):
        """Test successful streaming parse."""
        with patch('src.api.parse.get_ollama_service') as mock_get_service:
            mock_service = MagicMock()
            # Mock generate_stream to return proper chunks
            mock_service.generate_stream.return_value = [
                {'response': 'Parsed', 'done': False},
                {'response': ' content', 'done': True}
            ]
            mock_get_service.return_value = mock_service
            
            response = client.post('/api/parse/stream',
                                 json={'text': 'Parse this text'},
                                 headers={'Content-Type': 'application/json'})
            
            assert response.status_code == 200
            assert response.content_type == 'application/json'
    
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
    
    def test_parse_stream_error_handling(self, client):
        """Test error handling in parse stream."""
        with patch('src.api.parse.get_ollama_service') as mock_get_service:
            mock_service = MagicMock()
            # Simulate an error with generate_stream (not chat_stream)
            mock_service.generate_stream.side_effect = Exception("API Error")
            mock_get_service.return_value = mock_service
            
            response = client.post('/api/parse/stream',
                                 json={'text': 'Test'},
                                 headers={'Content-Type': 'application/json'})
            
            # Should still return 200 but with error in stream
            assert response.status_code == 200
            data = response.data.decode('utf-8')
            # The error will be caught and returned in the stream
            assert 'error' in data.lower() or 'done' in data