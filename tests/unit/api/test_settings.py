"""Unit tests for settings API endpoint."""
import pytest
from unittest.mock import patch
import config


class TestSettingsAPI:
    """Test cases for settings API endpoint."""
    
    def test_get_settings(self, client):
        """Test getting application settings."""
        response = client.get('/api/settings')
        
        assert response.status_code == 200
        data = response.get_json()
        
        # Check that expected settings are returned
        assert 'model' in data
        assert 'temperature' in data
        assert 'max_tokens' in data
        assert 'system_prompt' in data
        
        # Check values match config
        assert data['model'] == config.MODEL_NAME
        assert data['temperature'] == config.TEMPERATURE
        assert data['max_tokens'] == config.MAX_TOKENS
    
    def test_update_settings_temperature(self, client):
        """Test updating temperature setting."""
        response = client.post('/api/settings',
                              json={'temperature': 0.5},
                              headers={'Content-Type': 'application/json'})
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'updated'
        assert 'settings' in data
        assert data['settings']['temperature'] == 0.5
    
    def test_update_settings_max_tokens(self, client):
        """Test updating max_tokens setting."""
        response = client.post('/api/settings',
                              json={'max_tokens': 1000},
                              headers={'Content-Type': 'application/json'})
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['settings']['max_tokens'] == 1000
    
    def test_update_settings_invalid_temperature(self, client):
        """Test updating with invalid temperature value."""
        response = client.post('/api/settings',
                              json={'temperature': 2.0},  # Invalid: > 1.0
                              headers={'Content-Type': 'application/json'})
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_update_settings_invalid_max_tokens(self, client):
        """Test updating with invalid max_tokens value."""
        response = client.post('/api/settings',
                              json={'max_tokens': -100},  # Invalid: negative
                              headers={'Content-Type': 'application/json'})
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_update_settings_empty_body(self, client):
        """Test updating with empty request body."""
        response = client.post('/api/settings',
                              json={},
                              headers={'Content-Type': 'application/json'})
        
        # Should still return success but no changes
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'updated'
    
    def test_update_settings_unknown_field(self, client):
        """Test updating with unknown field."""
        response = client.post('/api/settings',
                              json={'unknown_field': 'value'},
                              headers={'Content-Type': 'application/json'})
        
        # Should ignore unknown fields
        assert response.status_code == 200
        data = response.get_json()
        assert 'unknown_field' not in data['settings']