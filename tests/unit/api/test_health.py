"""Unit tests for health API endpoint."""
import pytest
from unittest.mock import patch, MagicMock


class TestHealthAPI:
    """Test cases for health API endpoint."""
    
    def test_health_check_connected(self, client):
        """Test health check when Ollama is connected."""
        with patch('src.api.health.get_ollama_service') as mock_get_service, \
             patch('src.api.health.current_app') as mock_app:
            
            mock_service = MagicMock()
            mock_service.check_health.return_value = {
                'status': 'connected',
                'model_available': True,
                'models': ['gemma3:12b-it-qat']
            }
            mock_get_service.return_value = mock_service
            
            mock_app.config.get.side_effect = lambda key, default: {
                'NUM_CTX': 4096,
                'MODEL_NAME': 'gemma3:12b-it-qat'
            }.get(key, default)
            
            response = client.get('/api/health')
            
            assert response.status_code == 200
            data = response.get_json()
            assert data['status'] == 'connected'
            assert data['model_available'] is True
            assert 'gemma3:12b-it-qat' in data['models']
            assert data['context_limit'] == 4096
            assert data['context_limit_k'] == '4K'
            assert data['current_model'] == 'gemma3:12b-it-qat'
    
    def test_health_check_disconnected(self, client):
        """Test health check when Ollama is disconnected."""
        with patch('src.api.health.get_ollama_service') as mock_get_service, \
             patch('src.api.health.current_app') as mock_app:
            
            mock_service = MagicMock()
            mock_service.check_health.return_value = {
                'status': 'disconnected',
                'message': 'Connection failed'
            }
            mock_get_service.return_value = mock_service
            
            mock_app.config.get.side_effect = lambda key, default: {
                'NUM_CTX': 32768,
                'MODEL_NAME': 'phi3:mini'
            }.get(key, default)
            
            response = client.get('/api/health')
            
            assert response.status_code == 200
            data = response.get_json()
            assert data['status'] == 'disconnected'
            assert 'message' in data
            assert data['context_limit'] == 32768
            assert data['context_limit_k'] == '32K'
    
    def test_health_check_model_unavailable(self, client):
        """Test health check when model is not available."""
        with patch('src.api.health.get_ollama_service') as mock_get_service, \
             patch('src.api.health.current_app') as mock_app:
            
            mock_service = MagicMock()
            mock_service.check_health.return_value = {
                'status': 'connected',
                'model_available': False,
                'models': ['llama2']
            }
            mock_get_service.return_value = mock_service
            
            mock_app.config.get.side_effect = lambda key, default: {
                'NUM_CTX': 8192,
                'MODEL_NAME': 'gemma3:12b-it-qat'
            }.get(key, default)
            
            response = client.get('/api/health')
            
            assert response.status_code == 200
            data = response.get_json()
            assert data['status'] == 'connected'
            assert data['model_available'] is False
            assert 'gemma3:12b-it-qat' not in data['models']
            assert data['context_limit'] == 8192
            assert data['context_limit_k'] == '8K'
            assert data['current_model'] == 'gemma3:12b-it-qat'