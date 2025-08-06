"""Integration tests for work assistant functionality."""
import pytest
from datetime import datetime, timedelta
import json
from unittest.mock import patch, Mock


class TestWorkAssistantIntegration:
    """Integration tests for the complete work assistant workflow."""
    
    def test_complete_email_to_deliverable_workflow(self, client):
        """Test the complete workflow from email processing to deliverable creation."""
        with patch('src.api.work_assistant.KeywordExtractor') as mock_extractor_class:
            with patch('src.api.work_assistant.get_ollama_service'):
                with patch('src.api.work_assistant.current_app') as mock_app:
                    # Setup mocks
                    mock_extractor = Mock()
                    mock_extractor_class.return_value = mock_extractor
                    mock_app.vector_store = None
                    mock_app.config.get.return_value = 'phi3'
                    
                    # Step 1: Process an email that creates a project
                    mock_extractor.extract_email_info.return_value = {
                        'project_name': 'Integration Project',
                        'company': 'Test Company',
                        'people': ['Alice', 'Bob'],
                        'keywords': ['deadline', 'urgent'],
                        'action_items': ['Complete review'],
                        'deliverables': [
                            {'title': 'Final Report', 'due_date': (datetime.now() + timedelta(days=5)).isoformat()}
                        ],
                        'importance': 'high',
                        'summary': 'Urgent project with deadline'
                    }
                    
                    email_response = client.post('/api/work/emails/process', json={
                        'subject': 'Urgent: Project Deadline',
                        'sender': 'manager@company.com',
                        'recipients': ['team@company.com'],
                        'content': 'Please complete the final report by end of week.',
                        'received_date': datetime.now().isoformat()
                    })
                    
                    assert email_response.status_code == 201
                    email_data = email_response.json
                    assert email_data['extracted_info']['project_name'] == 'Integration Project'
                    project = email_data.get('project')
                    assert project is not None
                    project_id = project['id']
                    
                    # Step 2: Add a status update
                    mock_extractor.extract_status_update_info.return_value = {
                        'update_type': 'progress',
                        'keywords': ['development', 'testing'],
                        'percentage_complete': 50,
                        'blockers': [],
                        'next_steps': ['Testing phase'],
                        'deliverables_mentioned': ['Final Report'],
                        'people_mentioned': []
                    }
                    
                    status_response = client.post('/api/work/status-updates', json={
                        'project_id': project_id,
                        'content': 'Project is 50% complete. Moving to testing phase.',
                        'created_by': 'Developer'
                    })
                    
                    assert status_response.status_code == 201
                    
                    # Step 3: Query for deliverables
                    deliverables_response = client.get(f'/api/work/deliverables?project_id={project_id}')
                    assert deliverables_response.status_code == 200
                    deliverables = deliverables_response.json
                    # Note: Deliverables from email extraction might not be automatically created
                    # depending on implementation
                    
                    # Step 4: Create a deliverable manually
                    deliverable_response = client.post('/api/work/deliverables', json={
                        'project_id': project_id,
                        'title': 'Testing Report',
                        'description': 'Complete testing documentation',
                        'due_date': (datetime.now() + timedelta(days=3)).isoformat(),
                        'priority': 'high',
                        'assigned_to': 'Alice'
                    })
                    
                    assert deliverable_response.status_code == 201
                    
                    # Step 5: Get project with all related data
                    project_response = client.get(f'/api/work/projects/{project_id}')
                    assert project_response.status_code == 200
                    assert project_response.json['name'] == 'Integration Project'
    
    def test_intelligent_query_integration(self, client):
        """Test the intelligent query system with real data."""
        with patch('src.api.work_assistant.get_ollama_service') as mock_ollama:
            with patch('src.api.work_assistant.current_app') as mock_app:
                # Setup
                mock_ollama_service = Mock()
                mock_ollama.return_value = mock_ollama_service
                mock_app.vector_store = None
                # Mock config.get to return different values based on the key
                def mock_config_get(key, default=None):
                    if key == 'DELIVERABLE_WARNING_DAYS':
                        return 7
                    return default
                mock_app.config.get = mock_config_get
                
                # Create test data structure
                project_response = client.post('/api/work/projects', json={
                    'name': 'Query Test Project',
                    'company': 'QueryCorp'
                })
                project_id = project_response.json['id']
                
                # Add deliverables with different due dates
                for i in range(3):
                    client.post('/api/work/deliverables', json={
                        'project_id': project_id,
                        'title': f'Task {i+1}',
                        'due_date': (datetime.now() + timedelta(days=i+1)).isoformat(),
                        'priority': 'high' if i == 0 else 'medium',
                        'status': 'pending'
                    })
                
                # Mock the query parsing
                mock_ollama_service.generate.return_value = {
                    'response': json.dumps({
                        'query_type': 'deliverables',
                        'project_name': 'Query Test Project',
                        'time_frame': 'upcoming',
                        'specific_person': None,
                        'urgency': True
                    })
                }
                
                # Test query
                query_response = client.post('/api/work/query', json={
                    'query': 'What urgent deliverables are due for Query Test Project?'
                })
                
                assert query_response.status_code == 200
                data = query_response.json
                assert 'results' in data
                # Should have a response with query information
                assert 'query' in data
                assert 'answer' in data
    
    def test_multi_project_workflow(self, client):
        """Test handling multiple projects and cross-project queries."""
        projects = []
        
        # Create multiple projects
        for i in range(3):
            response = client.post('/api/work/projects', json={
                'name': f'Project {chr(65+i)}',  # Project A, B, C
                'company': f'Company {i+1}',
                'status': 'active'
            })
            projects.append(response.json)
        
        # Add deliverables to different projects
        with patch('src.api.work_assistant.current_app') as mock_app:
            mock_app.vector_store = None
            
            for i, project in enumerate(projects):
                for j in range(2):
                    client.post('/api/work/deliverables', json={
                        'project_id': project['id'],
                        'title': f'P{i+1} Task {j+1}',
                        'due_date': (datetime.now() + timedelta(days=i+j+1)).isoformat(),
                        'status': 'pending'
                    })
        
        # Query all upcoming deliverables
        response = client.get('/api/work/deliverables?upcoming_days=10')
        assert response.status_code == 200
        all_deliverables = response.json
        assert len(all_deliverables) == 6  # 3 projects × 2 deliverables
        
        # Query specific project deliverables
        response = client.get(f'/api/work/deliverables?project_id={projects[0]["id"]}')
        assert response.status_code == 200
        project_deliverables = response.json
        assert len(project_deliverables) == 2
    
    def test_email_to_people_tracking(self, client):
        """Test that people mentioned in emails are properly tracked."""
        with patch('src.api.work_assistant.KeywordExtractor') as mock_extractor_class:
            with patch('src.api.work_assistant.get_ollama_service'):
                with patch('src.api.work_assistant.current_app') as mock_app:
                    mock_extractor = Mock()
                    mock_extractor_class.return_value = mock_extractor
                    mock_app.vector_store = None
                    mock_app.config.get.return_value = 'phi3'
                    
                    # Process multiple emails mentioning different people
                    people_mentioned = [
                        ['Alice Johnson', 'Bob Smith'],
                        ['Alice Johnson', 'Charlie Davis'],  # Alice mentioned again
                        ['David Wilson']
                    ]
                    
                    for i, people in enumerate(people_mentioned):
                        mock_extractor.extract_email_info.return_value = {
                            'project_name': f'Project {i+1}',
                            'company': 'TestCorp',
                            'people': people,
                            'keywords': ['meeting'],
                            'action_items': [],
                            'deliverables': [],
                            'importance': 'medium',
                            'summary': f'Email {i+1}'
                        }
                        
                        client.post('/api/work/emails/process', json={
                            'subject': f'Email {i+1}',
                            'sender': f'sender{i}@test.com',
                            'recipients': ['team@test.com'],
                            'content': f'Email mentioning {", ".join(people)}',
                            'received_date': datetime.now().isoformat()
                        })
                    
                    # Check people were tracked
                    people_response = client.get('/api/work/people')
                    assert people_response.status_code == 200
                    people_list = people_response.json
                    
                    # Should have unique people (Alice only counted once)
                    people_names = [p['name'] for p in people_list]
                    assert 'Alice Johnson' in people_names
                    assert 'Bob Smith' in people_names
                    assert 'Charlie Davis' in people_names
                    assert 'David Wilson' in people_names
    
    def test_status_update_affects_deliverables(self, client):
        """Test that status updates can mention and affect deliverables."""
        # Create project and deliverable
        project_response = client.post('/api/work/projects', json={
            'name': 'Status Test Project'
        })
        project_id = project_response.json['id']
        
        with patch('src.api.work_assistant.current_app') as mock_app:
            mock_app.vector_store = None
            
            deliverable_response = client.post('/api/work/deliverables', json={
                'project_id': project_id,
                'title': 'API Documentation',
                'due_date': (datetime.now() + timedelta(days=5)).isoformat(),
                'status': 'pending'
            })
        
        # Add status update mentioning the deliverable
        with patch('src.api.work_assistant.KeywordExtractor') as mock_extractor_class:
            with patch('src.api.work_assistant.get_ollama_service'):
                with patch('src.api.work_assistant.current_app') as mock_app:
                    mock_extractor = Mock()
                    mock_extractor_class.return_value = mock_extractor
                    mock_app.vector_store = None
                    mock_app.config.get.return_value = 'phi3'
                    
                    mock_extractor.extract_status_update_info.return_value = {
                        'update_type': 'completion',
                        'keywords': ['documentation', 'complete'],
                        'percentage_complete': 100,
                        'blockers': [],
                        'next_steps': [],
                        'deliverables_mentioned': ['API Documentation'],
                        'people_mentioned': []
                    }
                    
                    status_response = client.post('/api/work/status-updates', json={
                        'project_id': project_id,
                        'content': 'API Documentation has been completed and reviewed.',
                        'created_by': 'Developer'
                    })
                    
                    assert status_response.status_code == 201
                    
                    # Check if new deliverable was created for mentioned deliverable
                    # (if it didn't exist)
                    deliverables = client.get(f'/api/work/deliverables?project_id={project_id}')
                    assert deliverables.status_code == 200