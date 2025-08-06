"""Unit tests for health API endpoint."""
import pytest
from unittest.mock import patch, MagicMock


class TestHealthAPI:
    """Test cases for health API endpoint."""
    
    def test_health_check_connected(self, client):
        """Test health check when Ollama is connected."""
        with patch('src.api.health.ollama_service') as mock_service:
            mock_service.check_health.return_value = {
                'status': 'connected',
                'model_available': True,
                'models': ['gemma3:12b-it-qat']
            }
            
            response = client.get('/api/health')
            
            assert response.status_code == 200
            data = response.get_json()
            assert data['status'] == 'connected'
            assert data['model_available'] is True
            assert 'gemma3:12b-it-qat' in data['models']
    
    def test_health_check_disconnected(self, client):
        """Test health check when Ollama is disconnected."""
        with patch('src.api.health.ollama_service') as mock_service:
            mock_service.check_health.return_value = {
                'status': 'disconnected',
                'message': 'Connection failed'
            }
            
            response = client.get('/api/health')
            
            assert response.status_code == 200
            data = response.get_json()
            assert data['status'] == 'disconnected'
            assert 'message' in data
    
    def test_health_check_model_unavailable(self, client):
        """Test health check when model is not available."""
        with patch('src.api.health.ollama_service') as mock_service:
            mock_service.check_health.return_value = {
                'status': 'connected',
                'model_available': False,
                'models': ['llama2']
            }
            
            response = client.get('/api/health')
            
            assert response.status_code == 200
            data = response.get_json()
            assert data['status'] == 'connected'
            assert data['model_available'] is False
            assert 'gemma3:12b-it-qat' not in data['models']