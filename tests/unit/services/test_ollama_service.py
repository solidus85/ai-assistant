"""Unit tests for OllamaService."""
import pytest
from unittest.mock import patch, MagicMock
import json
import requests

from src.services.ollama_service import OllamaService


class TestOllamaService:
    """Test cases for OllamaService."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.base_url = "http://localhost:11434"
        self.model_name = "gemma3:12b-it-qat"
        self.service = OllamaService(self.base_url, self.model_name)
    
    @patch('src.services.ollama_service.requests.get')
    def test_check_health_success(self, mock_get):
        """Test successful health check."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'models': [
                {'name': 'gemma3:12b-it-qat'},
                {'name': 'llama2'}
            ]
        }
        mock_get.return_value = mock_response
        
        result = self.service.check_health()
        
        assert result['status'] == 'connected'
        assert result['model_available'] is True
        assert 'gemma3:12b-it-qat' in result['models']
        mock_get.assert_called_once_with(f"{self.base_url}/api/tags", timeout=2)
    
    @patch('src.services.ollama_service.requests.get')
    def test_check_health_model_not_available(self, mock_get):
        """Test health check when model is not available."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'models': [{'name': 'llama2'}]
        }
        mock_get.return_value = mock_response
        
        result = self.service.check_health()
        
        assert result['status'] == 'connected'
        assert result['model_available'] is False
    
    @patch('src.services.ollama_service.requests.get')
    def test_check_health_connection_error(self, mock_get):
        """Test health check with connection error."""
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed")
        
        result = self.service.check_health()
        
        assert result['status'] == 'disconnected'
        assert 'message' in result
    
    @patch('src.services.ollama_service.requests.post')
    def test_generate_stream_success(self, mock_post):
        """Test successful streaming generation."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.iter_lines.return_value = [
            json.dumps({'message': {'content': 'Hello'}, 'done': False}).encode(),
            json.dumps({'message': {'content': ' world'}, 'done': False}).encode(),
            json.dumps({'message': {'content': '!'}, 'done': True}).encode()
        ]
        mock_response.__enter__ = MagicMock(return_value=mock_response)
        mock_response.__exit__ = MagicMock(return_value=None)
        mock_post.return_value = mock_response
        
        responses = list(self.service.generate_stream("Test prompt"))
        
        assert len(responses) == 3
        assert responses[0]['response'] == 'Hello'
        assert responses[1]['response'] == ' world'
        assert responses[2]['response'] == '!'
        assert responses[2]['done'] is True
    
    @patch('src.services.ollama_service.requests.post')
    def test_generate_stream_with_system_prompt(self, mock_post):
        """Test streaming generation with system prompt."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.iter_lines.return_value = [
            json.dumps({'message': {'content': 'Response'}, 'done': True}).encode()
        ]
        mock_response.__enter__ = MagicMock(return_value=mock_response)
        mock_response.__exit__ = MagicMock(return_value=None)
        mock_post.return_value = mock_response
        
        list(self.service.generate_stream("Test", system_prompt="Be helpful"))
        
        call_args = mock_post.call_args
        payload = call_args[1]['json']
        
        assert len(payload['messages']) == 2
        assert payload['messages'][0]['role'] == 'system'
        assert payload['messages'][0]['content'] == 'Be helpful'
        assert payload['messages'][1]['role'] == 'user'
        assert payload['messages'][1]['content'] == 'Test'
    
    @patch('src.services.ollama_service.requests.post')
    def test_generate_stream_error_handling(self, mock_post):
        """Test error handling in streaming generation."""
        mock_post.side_effect = requests.exceptions.RequestException("API Error")
        
        responses = list(self.service.generate_stream("Test prompt"))
        
        assert len(responses) == 1
        assert 'error' in responses[0]
        assert responses[0]['done'] is True
    
    @patch('src.services.ollama_service.requests.post')
    def test_generate_non_streaming(self, mock_post):
        """Test non-streaming generation."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            'response': 'Test response',
            'done': True
        }
        mock_post.return_value = mock_response
        
        result = self.service.generate("Test prompt", {'temperature': 0.7})
        
        assert result['response'] == 'Test response'
        assert result['done'] is True
        
        call_args = mock_post.call_args
        payload = call_args[1]['json']
        assert payload['model'] == self.model_name
        assert payload['prompt'] == 'Test prompt'
        assert payload['stream'] is False
        assert payload['options']['temperature'] == 0.7