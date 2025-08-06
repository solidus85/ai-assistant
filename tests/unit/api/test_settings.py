"""Unit tests for settings API endpoint."""
import pytest
from unittest.mock import patch, MagicMock
import os


class TestSettingsAPI:
    """Test cases for settings API endpoint."""
    
    def test_get_system_prompt(self, client):
        """Test getting system prompt setting."""
        response = client.get('/api/settings/system-prompt')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'system_prompt' in data
        # System prompt will be whatever is in config
    
    def test_get_system_prompt_with_value(self, app, client):
        """Test getting system prompt when set."""
        app.config['SYSTEM_PROMPT'] = 'You are a helpful assistant'
        
        response = client.get('/api/settings/system-prompt')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'system_prompt' in data
        assert data['system_prompt'] == 'You are a helpful assistant'
    
    def test_update_system_prompt(self, client):
        """Test updating system prompt setting."""
        response = client.post('/api/settings/system-prompt',
                              json={'system_prompt': 'Be concise and helpful'},
                              headers={'Content-Type': 'application/json'})
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['system_prompt'] == 'Be concise and helpful'
        assert 'message' in data
    
    def test_update_system_prompt_empty(self, client):
        """Test updating system prompt with empty value."""
        response = client.post('/api/settings/system-prompt',
                              json={'system_prompt': ''},
                              headers={'Content-Type': 'application/json'})
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['system_prompt'] == ''
    
    def test_update_system_prompt_missing_field(self, client):
        """Test updating system prompt with missing field."""
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
        prompt_with_special = "You're an AI assistant! Use \"quotes\" & symbols: @#$%"
        
        response = client.post('/api/settings/system-prompt',
                              json={'system_prompt': prompt_with_special},
                              headers={'Content-Type': 'application/json'})
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['system_prompt'] == prompt_with_special