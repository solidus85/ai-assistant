"""Unit tests for work assistant API endpoints."""
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
import json


class TestWorkAssistantAPI:
    """Test work assistant API endpoints."""
    
    def test_get_projects_empty(self, client):
        """Test getting projects when none exist."""
        response = client.get('/api/work/projects')
        assert response.status_code == 200
        assert response.json == []
    
    def test_create_project_success(self, client):
        """Test creating a new project."""
        project_data = {
            'name': 'Test Project',
            'company': 'Test Corp',
            'description': 'A test project'
        }
        
        response = client.post('/api/work/projects', 
                              json=project_data)
        
        assert response.status_code == 201
        data = response.json
        assert data['name'] == 'Test Project'
        assert data['company'] == 'Test Corp'
        assert data['description'] == 'A test project'
        assert 'id' in data
        assert 'created_at' in data
    
    def test_create_project_minimal(self, client):
        """Test creating project with minimal data."""
        response = client.post('/api/work/projects', 
                              json={'name': 'Minimal Project'})
        
        assert response.status_code == 201
        data = response.json
        assert data['name'] == 'Minimal Project'
        assert data['status'] == 'active'
    
    def test_get_projects_with_data(self, client):
        """Test getting projects after creating some."""
        # Create projects
        client.post('/api/work/projects', json={'name': 'Project 1'})
        client.post('/api/work/projects', json={'name': 'Project 2'})
        
        response = client.get('/api/work/projects')
        assert response.status_code == 200
        data = response.json
        assert len(data) == 2
        assert data[0]['name'] == 'Project 1'
        assert data[1]['name'] == 'Project 2'
    
    def test_get_project_by_id(self, client):
        """Test getting a specific project."""
        # Create a project
        create_response = client.post('/api/work/projects', 
                                     json={'name': 'Test Project'})
        project_id = create_response.json['id']
        
        # Get the project
        response = client.get(f'/api/work/projects/{project_id}')
        assert response.status_code == 200
        assert response.json['name'] == 'Test Project'
    
    def test_update_project(self, client):
        """Test updating a project."""
        # Create a project
        create_response = client.post('/api/work/projects', 
                                     json={'name': 'Original Name'})
        project_id = create_response.json['id']
        
        # Update the project
        update_data = {
            'name': 'Updated Name',
            'company': 'New Company',
            'status': 'completed'
        }
        response = client.put(f'/api/work/projects/{project_id}', 
                            json=update_data)
        
        assert response.status_code == 200
        data = response.json
        assert data['name'] == 'Updated Name'
        assert data['company'] == 'New Company'
        assert data['status'] == 'completed'
    
    def test_delete_project(self, client):
        """Test deleting a project."""
        # Create a project
        create_response = client.post('/api/work/projects', 
                                     json={'name': 'To Delete'})
        project_id = create_response.json['id']
        
        # Delete the project
        response = client.delete(f'/api/work/projects/{project_id}')
        assert response.status_code == 204
        
        # Verify it's deleted
        get_response = client.get(f'/api/work/projects/{project_id}')
        assert get_response.status_code == 404
    
    @patch('src.api.work_assistant.get_ollama_service')
    @patch('src.api.work_assistant.current_app')
    def test_process_email_success(self, mock_app, mock_ollama, client):
        """Test processing an email."""
        # Mock Ollama service
        mock_ollama_service = Mock()
        mock_ollama.return_value = mock_ollama_service
        
        # Mock vector store
        mock_vector_store = Mock()
        mock_vector_store.add_email.return_value = 'vector_123'
        mock_app.vector_store = mock_vector_store
        mock_app.config.get.return_value = 'phi3'
        
        # Mock keyword extractor
        with patch('src.api.work_assistant.KeywordExtractor') as mock_extractor_class:
            mock_extractor = Mock()
            mock_extractor_class.return_value = mock_extractor
            mock_extractor.extract_email_info.return_value = {
                'project_name': 'Email Project',
                'company': 'Email Corp',
                'people': ['John Doe', 'Jane Smith'],
                'keywords': ['meeting', 'deadline'],
                'action_items': [],
                'deliverables': [],
                'importance': 'high',
                'summary': 'Test email summary'
            }
            
            email_data = {
                'from': 'sender@test.com',
                'to': ['recipient@test.com'],
                'cc': ['cc@test.com'],
                'subject': 'Test Email',
                'body': 'This is a test email about the project.',
                'received_date': datetime.now().isoformat()
            }
            
            response = client.post('/api/work/emails/process', json=email_data)
            
            assert response.status_code == 201
            data = response.json
            assert 'email_id' in data
            assert data['extracted_info']['project_name'] == 'Email Project'
            assert data['extracted_info']['importance'] == 'high'
            assert len(data['extracted_info']['people']) == 2
    
    def test_create_status_update(self, client):
        """Test creating a status update."""
        # First create a project
        project_response = client.post('/api/work/projects', 
                                      json={'name': 'Status Project'})
        project_id = project_response.json['id']
        
        # Mock the keyword extractor
        with patch('src.api.work_assistant.KeywordExtractor') as mock_extractor_class:
            mock_extractor = Mock()
            mock_extractor_class.return_value = mock_extractor
            mock_extractor.extract_status_update_info.return_value = {
                'update_type': 'progress',
                'keywords': ['development', 'testing'],
                'percentage_complete': 75,
                'blockers': [],
                'next_steps': ['Code review'],
                'deliverables_mentioned': [],
                'people_mentioned': []
            }
            
            with patch('src.api.work_assistant.get_ollama_service'):
                with patch('src.api.work_assistant.current_app') as mock_app:
                    mock_app.vector_store = None  # No vector store
                    mock_app.config.get.return_value = 'phi3'
                    
                    status_data = {
                        'project_id': project_id,
                        'content': 'Project is 75% complete. Ready for code review.',
                        'created_by': 'Test User'
                    }
                    
                    response = client.post('/api/work/status-updates', json=status_data)
                    
                    assert response.status_code == 201
                    data = response.json
                    assert data['status_update']['project_id'] == project_id
                    assert data['extracted_info']['update_type'] == 'progress'
    
    def test_create_status_update_missing_project(self, client):
        """Test creating status update without project_id."""
        response = client.post('/api/work/status-updates', 
                              json={'content': 'Some update'})
        assert response.status_code == 400
    
    def test_get_deliverables_empty(self, client):
        """Test getting deliverables when none exist."""
        response = client.get('/api/work/deliverables')
        assert response.status_code == 200
        assert response.json == []
    
    def test_create_deliverable(self, client):
        """Test creating a deliverable."""
        # Create a project first
        project_response = client.post('/api/work/projects', 
                                      json={'name': 'Deliverable Project'})
        project_id = project_response.json['id']
        
        with patch('src.api.work_assistant.current_app') as mock_app:
            mock_app.vector_store = None
            
            deliverable_data = {
                'project_id': project_id,
                'title': 'Complete Documentation',
                'description': 'Write comprehensive docs',
                'due_date': (datetime.now() + timedelta(days=7)).isoformat(),
                'priority': 'high',
                'assigned_to': 'John Doe'
            }
            
            response = client.post('/api/work/deliverables', json=deliverable_data)
            
            assert response.status_code == 201
            data = response.json
            assert data['title'] == 'Complete Documentation'
            assert data['priority'] == 'high'
            assert data['status'] == 'pending'
    
    def test_get_deliverables_with_filters(self, client):
        """Test getting deliverables with filters."""
        # Create project and deliverables
        project_response = client.post('/api/work/projects', 
                                      json={'name': 'Filter Project'})
        project_id = project_response.json['id']
        
        with patch('src.api.work_assistant.current_app') as mock_app:
            mock_app.vector_store = None
            
            # Create multiple deliverables
            for i in range(3):
                client.post('/api/work/deliverables', json={
                    'project_id': project_id,
                    'title': f'Deliverable {i}',
                    'due_date': (datetime.now() + timedelta(days=i+1)).isoformat(),
                    'status': 'pending' if i < 2 else 'completed'
                })
            
            # Test filter by project
            response = client.get(f'/api/work/deliverables?project_id={project_id}')
            assert response.status_code == 200
            assert len(response.json) == 3
            
            # Test filter by status
            response = client.get('/api/work/deliverables?status=pending')
            assert response.status_code == 200
            assert len(response.json) == 2
    
    @patch('src.api.work_assistant.get_ollama_service')
    @patch('src.api.work_assistant.current_app')
    def test_intelligent_query(self, mock_app, mock_ollama, client):
        """Test the intelligent query endpoint."""
        # Setup mocks
        mock_ollama_service = Mock()
        mock_ollama.return_value = mock_ollama_service
        mock_ollama_service.generate.return_value = {
            'response': json.dumps({
                'query_type': 'deliverables',
                'project_name': None,
                'time_frame': 'upcoming',
                'specific_person': None,
                'urgency': True
            })
        }
        
        mock_app.vector_store = None
        # Mock config.get to return different values based on the key
        def mock_config_get(key, default=None):
            if key == 'DELIVERABLE_WARNING_DAYS':
                return 7
            return default
        mock_app.config.get = mock_config_get
        
        # Create test data
        project_response = client.post('/api/work/projects', 
                                      json={'name': 'Query Project'})
        project_id = project_response.json['id']
        
        with patch('src.api.work_assistant.current_app') as mock_app2:
            mock_app2.vector_store = None
            
            # Create a deliverable due soon
            client.post('/api/work/deliverables', json={
                'project_id': project_id,
                'title': 'Urgent Task',
                'due_date': (datetime.now() + timedelta(days=2)).isoformat(),
                'status': 'pending'
            })
        
        # Test query
        response = client.post('/api/work/query', 
                              json={'query': 'What deliverables are due soon?'})
        
        assert response.status_code == 200
        data = response.json
        assert 'query' in data
        assert 'answer' in data
        assert 'results' in data
    
    def test_intelligent_query_no_query(self, client):
        """Test query endpoint without query."""
        response = client.post('/api/work/query', json={})
        assert response.status_code == 400
    
    def test_get_people(self, client):
        """Test getting people list."""
        response = client.get('/api/work/people')
        assert response.status_code == 200
        assert isinstance(response.json, list)
    
    def test_get_emails(self, client):
        """Test getting emails."""
        response = client.get('/api/work/emails')
        assert response.status_code == 200
        assert isinstance(response.json, list)
    
    def test_get_emails_with_filters(self, client):
        """Test getting emails with filters."""
        # Test with project filter
        response = client.get('/api/work/emails?project_id=1')
        assert response.status_code == 200
        
        # Test with importance filter
        response = client.get('/api/work/emails?importance=high')
        assert response.status_code == 200
        
        # Test with limit
        response = client.get('/api/work/emails?limit=5')
        assert response.status_code == 200
    
    def test_get_status_updates(self, client):
        """Test getting status updates for a project."""
        # Create a project
        project_response = client.post('/api/work/projects', 
                                      json={'name': 'Status Project'})
        project_id = project_response.json['id']
        
        response = client.get(f'/api/work/status-updates/{project_id}')
        assert response.status_code == 200
        assert response.json == []  # Empty initially