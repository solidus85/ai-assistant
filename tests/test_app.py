"""Integration tests for the Flask application."""
import pytest
from unittest.mock import patch, MagicMock


class TestApp:
    """Test cases for Flask application."""
    
    def test_app_creation(self, app):
        """Test that app is created properly."""
        assert app is not None
        assert app.config['TESTING'] is True
    
    def test_index_route(self, client):
        """Test the index route."""
        response = client.get('/')
        assert response.status_code == 200
        # Check that it returns HTML
        assert b'<!DOCTYPE html>' in response.data or b'<html' in response.data
    
    def test_404_error(self, client):
        """Test 404 error handling."""
        response = client.get('/nonexistent')
        assert response.status_code == 404
    
    def test_api_prefix(self, client):
        """Test that API routes use /api prefix."""
        with patch('src.api.health.get_ollama_service') as mock_get_service:
            mock_service = MagicMock()
            mock_service.check_health.return_value = {'status': 'connected'}
            mock_get_service.return_value = mock_service
            
            # API routes should work with /api prefix
            response = client.get('/api/health')
            assert response.status_code == 200
            
            # Without prefix should not work for API
            response = client.get('/health')
            assert response.status_code == 404
    
    def test_cors_headers(self, client):
        """Test CORS headers if configured."""
        response = client.get('/api/health')
        # If CORS is enabled, check headers
        # This is optional based on your configuration
    
    def test_json_content_type(self, client):
        """Test that API returns JSON content type."""
        with patch('src.api.health.get_ollama_service') as mock_get_service:
            mock_service = MagicMock()
            mock_service.check_health.return_value = {'status': 'connected'}
            mock_get_service.return_value = mock_service
            
            response = client.get('/api/health')
            assert response.content_type == 'application/json'