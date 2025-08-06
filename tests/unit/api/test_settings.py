"""Unit tests for settings API endpoint."""
import pytest
from unittest.mock import patch
import os


class TestSettingsAPI:
    """Test cases for settings API endpoint."""
    
    def test_get_system_prompt(self, client):
        """Test getting system prompt setting."""
        with patch('src.api.settings.current_app') as mock_app:
            mock_app.config.get.return_value = 'You are a helpful assistant'
            
            response = client.get('/api/settings/system-prompt')
            
            assert response.status_code == 200
            data = response.get_json()
            assert 'system_prompt' in data
            assert data['system_prompt'] == 'You are a helpful assistant'
    
    def test_get_system_prompt_empty(self, client):
        """Test getting system prompt when not set."""
        with patch('src.api.settings.current_app') as mock_app:
            mock_app.config.get.return_value = ''
            
            response = client.get('/api/settings/system-prompt')
            
            assert response.status_code == 200
            data = response.get_json()
            assert 'system_prompt' in data
            assert data['system_prompt'] == ''
    
    def test_update_system_prompt(self, client):
        """Test updating system prompt setting."""
        with patch('src.api.settings.current_app') as mock_app, \
             patch('src.api.settings.os.environ', {}) as mock_environ:
            
            mock_app.config = {}
            
            response = client.post('/api/settings/system-prompt',
                                  json={'system_prompt': 'Be concise and helpful'},
                                  headers={'Content-Type': 'application/json'})
            
            assert response.status_code == 200
            data = response.get_json()
            assert data['success'] is True
            assert data['system_prompt'] == 'Be concise and helpful'
            assert 'message' in data
            
            # Check that config was updated
            assert mock_app.config['SYSTEM_PROMPT'] == 'Be concise and helpful'
    
    def test_update_system_prompt_empty(self, client):
        """Test updating system prompt with empty value."""
        with patch('src.api.settings.current_app') as mock_app, \
             patch('src.api.settings.os.environ', {}) as mock_environ:
            
            mock_app.config = {}
            
            response = client.post('/api/settings/system-prompt',
                                  json={'system_prompt': ''},
                                  headers={'Content-Type': 'application/json'})
            
            assert response.status_code == 200
            data = response.get_json()
            assert data['success'] is True
            assert data['system_prompt'] == ''
    
    def test_update_system_prompt_missing_field(self, client):
        """Test updating system prompt with missing field."""
        with patch('src.api.settings.current_app') as mock_app, \
             patch('src.api.settings.os.environ', {}) as mock_environ:
            
            mock_app.config = {}
            
            response = client.post('/api/settings/system-prompt',
                                  json={},
                                  headers={'Content-Type': 'application/json'})
            
            assert response.status_code == 200
            data = response.get_json()
            assert data['success'] is True
            # Should set to empty string when field is missing
            assert data['system_prompt'] == ''
    
    def test_update_system_prompt_with_special_characters(self, client):
        """Test updating system prompt with special characters."""
        with patch('src.api.settings.current_app') as mock_app, \
             patch('src.api.settings.os.environ', {}) as mock_environ:
            
            mock_app.config = {}
            prompt_with_special = "You're an AI assistant! Use \"quotes\" & symbols: @#$%"
            
            response = client.post('/api/settings/system-prompt',
                                  json={'system_prompt': prompt_with_special},
                                  headers={'Content-Type': 'application/json'})
            
            assert response.status_code == 200
            data = response.get_json()
            assert data['success'] is True
            assert data['system_prompt'] == prompt_with_special