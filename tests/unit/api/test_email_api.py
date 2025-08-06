"""Unit tests for email processing API with standard email fields."""
import pytest
from datetime import datetime
from unittest.mock import Mock, patch


class TestEmailAPI:
    """Test email processing API with standard fields."""
    
    def test_process_email_with_standard_fields(self, client):
        """Test processing email with from, to, cc, subject, body."""
        with patch('src.api.work_assistant.KeywordExtractor') as mock_extractor_class:
            with patch('src.api.work_assistant.get_ollama_service'):
                with patch('src.api.work_assistant.current_app') as mock_app:
                    # Setup mocks
                    mock_extractor = Mock()
                    mock_extractor_class.return_value = mock_extractor
                    mock_app.vector_store = None
                    mock_app.config.get.return_value = 'phi3'
                    
                    mock_extractor.extract_email_info.return_value = {
                        'project_name': 'Test Project',
                        'company': 'Test Corp',
                        'people': [],
                        'keywords': ['test'],
                        'action_items': [],
                        'deliverables': [],
                        'importance': 'medium',
                        'summary': 'Test email'
                    }
                    
                    # Test with all fields
                    response = client.post('/api/work/emails/process', json={
                        'from': 'sender@example.com',
                        'to': 'recipient@example.com',  # Single string
                        'cc': 'cc@example.com',  # Single string
                        'subject': 'Test Subject',
                        'body': 'This is the email body content.',
                        'received_date': datetime.now().isoformat()
                    })
                    
                    assert response.status_code == 201
                    data = response.json
                    assert 'email_id' in data
                    assert data['extracted_info']['project_name'] == 'Test Project'
    
    def test_process_email_with_list_recipients(self, client):
        """Test processing email with to and cc as lists."""
        with patch('src.api.work_assistant.KeywordExtractor') as mock_extractor_class:
            with patch('src.api.work_assistant.get_ollama_service'):
                with patch('src.api.work_assistant.current_app') as mock_app:
                    mock_extractor = Mock()
                    mock_extractor_class.return_value = mock_extractor
                    mock_app.vector_store = None
                    mock_app.config.get.return_value = 'phi3'
                    
                    mock_extractor.extract_email_info.return_value = {
                        'project_name': None,
                        'company': None,
                        'people': [],
                        'keywords': [],
                        'action_items': [],
                        'deliverables': [],
                        'importance': 'low',
                        'summary': 'Email'
                    }
                    
                    # Test with lists
                    response = client.post('/api/work/emails/process', json={
                        'from': 'sender@example.com',
                        'to': ['recipient1@example.com', 'recipient2@example.com'],
                        'cc': ['cc1@example.com', 'cc2@example.com'],
                        'subject': 'Multiple Recipients',
                        'body': 'Email to multiple people'
                    })
                    
                    assert response.status_code == 201
    
    def test_process_email_without_cc(self, client):
        """Test processing email without CC field."""
        with patch('src.api.work_assistant.KeywordExtractor') as mock_extractor_class:
            with patch('src.api.work_assistant.get_ollama_service'):
                with patch('src.api.work_assistant.current_app') as mock_app:
                    mock_extractor = Mock()
                    mock_extractor_class.return_value = mock_extractor
                    mock_app.vector_store = None
                    mock_app.config.get.return_value = 'phi3'
                    
                    mock_extractor.extract_email_info.return_value = {
                        'project_name': None,
                        'company': None,
                        'people': [],
                        'keywords': [],
                        'action_items': [],
                        'deliverables': [],
                        'importance': 'low',
                        'summary': 'Email'
                    }
                    
                    # Test without CC
                    response = client.post('/api/work/emails/process', json={
                        'from': 'sender@example.com',
                        'to': 'recipient@example.com',
                        'subject': 'No CC',
                        'body': 'Email without CC'
                    })
                    
                    assert response.status_code == 201
    
    def test_process_email_missing_from(self, client):
        """Test that missing 'from' field returns 400."""
        response = client.post('/api/work/emails/process', json={
            'to': 'recipient@example.com',
            'subject': 'Missing From',
            'body': 'Email without sender'
        })
        
        assert response.status_code == 400
        assert 'from' in response.json['error'].lower()
    
    def test_process_email_missing_to(self, client):
        """Test that missing 'to' field returns 400."""
        response = client.post('/api/work/emails/process', json={
            'from': 'sender@example.com',
            'subject': 'Missing To',
            'body': 'Email without recipient'
        })
        
        assert response.status_code == 400
        assert 'to' in response.json['error'].lower()
    
    def test_process_email_missing_content(self, client):
        """Test that missing both subject and body returns 400."""
        response = client.post('/api/work/emails/process', json={
            'from': 'sender@example.com',
            'to': 'recipient@example.com'
        })
        
        assert response.status_code == 400
        assert 'subject and body' in response.json['error'].lower()
    
    def test_process_email_with_only_subject(self, client):
        """Test that email with only subject (no body) is accepted."""
        with patch('src.api.work_assistant.KeywordExtractor') as mock_extractor_class:
            with patch('src.api.work_assistant.get_ollama_service'):
                with patch('src.api.work_assistant.current_app') as mock_app:
                    mock_extractor = Mock()
                    mock_extractor_class.return_value = mock_extractor
                    mock_app.vector_store = None
                    mock_app.config.get.return_value = 'phi3'
                    
                    mock_extractor.extract_email_info.return_value = {
                        'project_name': None,
                        'company': None,
                        'people': [],
                        'keywords': [],
                        'action_items': [],
                        'deliverables': [],
                        'importance': 'low',
                        'summary': 'Subject only'
                    }
                    
                    response = client.post('/api/work/emails/process', json={
                        'from': 'sender@example.com',
                        'to': 'recipient@example.com',
                        'subject': 'Subject Only Email'
                        # No body field
                    })
                    
                    assert response.status_code == 201
    
    def test_process_email_with_only_body(self, client):
        """Test that email with only body (no subject) is accepted."""
        with patch('src.api.work_assistant.KeywordExtractor') as mock_extractor_class:
            with patch('src.api.work_assistant.get_ollama_service'):
                with patch('src.api.work_assistant.current_app') as mock_app:
                    mock_extractor = Mock()
                    mock_extractor_class.return_value = mock_extractor
                    mock_app.vector_store = None
                    mock_app.config.get.return_value = 'phi3'
                    
                    mock_extractor.extract_email_info.return_value = {
                        'project_name': None,
                        'company': None,
                        'people': [],
                        'keywords': [],
                        'action_items': [],
                        'deliverables': [],
                        'importance': 'low',
                        'summary': 'Body only'
                    }
                    
                    response = client.post('/api/work/emails/process', json={
                        'from': 'sender@example.com',
                        'to': 'recipient@example.com',
                        'body': 'This email has no subject line'
                    })
                    
                    assert response.status_code == 201
    
    def test_process_email_empty_strings(self, client):
        """Test handling of empty string values."""
        with patch('src.api.work_assistant.KeywordExtractor') as mock_extractor_class:
            with patch('src.api.work_assistant.get_ollama_service'):
                with patch('src.api.work_assistant.current_app') as mock_app:
                    mock_extractor = Mock()
                    mock_extractor_class.return_value = mock_extractor
                    mock_app.vector_store = None
                    mock_app.config.get.return_value = 'phi3'
                    
                    mock_extractor.extract_email_info.return_value = {
                        'project_name': None,
                        'company': None,
                        'people': [],
                        'keywords': [],
                        'action_items': [],
                        'deliverables': [],
                        'importance': 'low',
                        'summary': 'Empty CC'
                    }
                    
                    # Empty CC string should be handled gracefully
                    response = client.post('/api/work/emails/process', json={
                        'from': 'sender@example.com',
                        'to': 'recipient@example.com',
                        'cc': '',  # Empty string
                        'subject': 'Test',
                        'body': 'Test body'
                    })
                    
                    assert response.status_code == 201