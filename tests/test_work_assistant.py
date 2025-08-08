#!/usr/bin/env python3
"""Test script for work assistant functionality."""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5000/api/work"

def test_create_project():
    """Test creating a new project."""
    print("Testing: Create Project")
    data = {
        "name": "Q4 Product Launch",
        "company": "TechCorp",
        "description": "Launch of new AI-powered analytics platform"
    }
    response = requests.post(f"{BASE_URL}/projects", json=data)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        project = response.json()
        print(f"Created project: {project['name']} (ID: {project['id']})")
        return project['id']
    else:
        print(f"Error: {response.text}")
        return None

def test_process_email(project_id=None):
    """Test email processing."""
    print("\nTesting: Process Email")
    email_data = {
        "subject": "Q4 Product Launch - Status Update",
        "sender": "john.smith@techcorp.com",
        "recipients": ["team@techcorp.com"],
        "content": """Hi Team,

I wanted to provide an update on our Q4 product launch. We're making good progress 
on the AI analytics platform. Sarah Johnson has completed the backend integration, 
and Mike Chen is finalizing the UI components.

Key deliverables for next week:
- Complete API documentation by Friday
- Finish performance testing by end of week
- Prepare demo for stakeholders meeting on Monday

We have a blocker with the authentication module that needs immediate attention.
The integration with the SSO provider is causing issues.

Please review the attached specifications and provide feedback by Thursday.

Best regards,
John Smith
Product Manager""",
        "received_date": datetime.now().isoformat()
    }
    
    response = requests.post(f"{BASE_URL}/emails/process", json=email_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        result = response.json()
        print(f"Email processed successfully")
        print(f"Extracted Info:")
        print(f"  - Project: {result['extracted_info'].get('project_name')}")
        print(f"  - Company: {result['extracted_info'].get('company')}")
        print(f"  - People: {result['extracted_info'].get('people')}")
        print(f"  - Keywords: {result['extracted_info'].get('keywords')}")
        print(f"  - Importance: {result['extracted_info'].get('importance')}")
        return result.get('project', {}).get('id')
    else:
        print(f"Error: {response.text}")
        return project_id

def test_add_status_update(project_id):
    """Test adding a status update."""
    print("\nTesting: Add Status Update")
    data = {
        "project_id": project_id,
        "content": "Completed 75% of the backend API development. The authentication module is now working after fixing the SSO integration issue. Next steps include finalizing the API documentation and preparing for load testing.",
        "created_by": "Developer"
    }
    
    response = requests.post(f"{BASE_URL}/status-updates", json=data)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        result = response.json()
        print(f"Status update added successfully")
        print(f"  - Type: {result['extracted_info'].get('update_type')}")
        print(f"  - Keywords: {result['extracted_info'].get('keywords')}")
    else:
        print(f"Error: {response.text}")

def test_add_deliverable(project_id):
    """Test adding a deliverable."""
    print("\nTesting: Add Deliverable")
    due_date = (datetime.now() + timedelta(days=5)).isoformat()
    data = {
        "project_id": project_id,
        "title": "Complete API Documentation",
        "description": "Finalize and review all API endpoint documentation",
        "due_date": due_date,
        "priority": "high",
        "assigned_to": "Sarah Johnson"
    }
    
    response = requests.post(f"{BASE_URL}/deliverables", json=data)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        deliverable = response.json()
        print(f"Deliverable added: {deliverable['title']}")
        print(f"  - Due: {deliverable['due_date']}")
        print(f"  - Priority: {deliverable['priority']}")
    else:
        print(f"Error: {response.text}")

def test_query_system():
    """Test the intelligent query system."""
    print("\nTesting: Intelligent Query System")
    
    queries = [
        "What deliverables are due soon?",
        "Show me recent emails about the product launch",
        "What's the latest status on the Q4 project?"
    ]
    
    for query in queries:
        print(f"\nQuery: {query}")
        response = requests.post(f"{BASE_URL}/query", json={"query": query})
        
        if response.status_code == 200:
            result = response.json()
            print(f"Answer: {result['answer']}")
            
            # Show some results if available
            if result.get('results', {}).get('deliverables'):
                print(f"Found {len(result['results']['deliverables'])} deliverables")
            if result.get('results', {}).get('emails'):
                print(f"Found {len(result['results']['emails'])} related emails")
            if result.get('results', {}).get('status_updates'):
                print(f"Found {len(result['results']['status_updates'])} status updates")
        else:
            print(f"Error: {response.text}")

def test_get_upcoming_deliverables():
    """Test fetching upcoming deliverables."""
    print("\nTesting: Get Upcoming Deliverables")
    response = requests.get(f"{BASE_URL}/deliverables?upcoming_days=7")
    
    if response.status_code == 200:
        deliverables = response.json()
        print(f"Found {len(deliverables)} upcoming deliverables:")
        for d in deliverables:
            print(f"  - {d['title']} (Due: {d['due_date']}, Project: {d['project_name']})")
    else:
        print(f"Error: {response.text}")

def main():
    """Run all tests."""
    print("=" * 60)
    print("Work Assistant API Tests")
    print("=" * 60)
    
    # Create or use existing project
    project_id = test_create_project()
    
    if project_id:
        # Process an email (might create new project)
        new_project_id = test_process_email(project_id)
        if new_project_id:
            project_id = new_project_id
        
        # Add status update
        test_add_status_update(project_id)
        
        # Add deliverable
        test_add_deliverable(project_id)
    
    # Test query system
    test_query_system()
    
    # Get upcoming deliverables
    test_get_upcoming_deliverables()
    
    print("\n" + "=" * 60)
    print("Tests completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()