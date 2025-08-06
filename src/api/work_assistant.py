"""Work assistant API endpoints for email processing, status updates, and intelligent queries."""
from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta
from dateutil import parser as date_parser
import logging

from src.models.database import db, Project, Email, StatusUpdate, Deliverable, Person
from src.services.keyword_extractor import KeywordExtractor
from src.utils.extensions import get_ollama_service

bp = Blueprint('work_assistant', __name__, url_prefix='/api/work')
logger = logging.getLogger(__name__)


@bp.route('/projects', methods=['GET', 'POST'])
def projects():
    """Manage projects."""
    if request.method == 'GET':
        try:
            all_projects = Project.query.all()
            return jsonify([p.to_dict() for p in all_projects])
        except Exception as e:
            logger.error(f"Failed to fetch projects: {e}")
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'POST':
        try:
            data = request.json
            project = Project(
                name=data['name'],
                company=data.get('company'),
                description=data.get('description'),
                status=data.get('status', 'active')
            )
            db.session.add(project)
            db.session.commit()
            
            return jsonify(project.to_dict()), 201
        except Exception as e:
            logger.error(f"Failed to create project: {e}")
            db.session.rollback()
            return jsonify({'error': str(e)}), 500


@bp.route('/projects/<int:project_id>', methods=['GET', 'PUT', 'DELETE'])
def project_detail(project_id):
    """Get, update, or delete a specific project."""
    project = Project.query.get_or_404(project_id)
    
    if request.method == 'GET':
        return jsonify(project.to_dict())
    
    elif request.method == 'PUT':
        try:
            data = request.json
            project.name = data.get('name', project.name)
            project.company = data.get('company', project.company)
            project.description = data.get('description', project.description)
            project.status = data.get('status', project.status)
            project.updated_at = datetime.utcnow()
            
            db.session.commit()
            return jsonify(project.to_dict())
        except Exception as e:
            logger.error(f"Failed to update project: {e}")
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'DELETE':
        try:
            db.session.delete(project)
            db.session.commit()
            return '', 204
        except Exception as e:
            logger.error(f"Failed to delete project: {e}")
            db.session.rollback()
            return jsonify({'error': str(e)}), 500


@bp.route('/emails/process', methods=['POST'])
def process_email():
    """Process an email and extract information."""
    try:
        data = request.json
        email_content = data.get('content', '')
        subject = data.get('subject', '')
        sender = data.get('sender', '')
        recipients = data.get('recipients', [])
        cc = data.get('cc', [])
        received_date = data.get('received_date')
        
        if received_date:
            received_date = date_parser.parse(received_date)
        else:
            received_date = datetime.utcnow()
        
        # Initialize keyword extractor
        ollama = get_ollama_service()
        extractor = KeywordExtractor(ollama, current_app.config.get('EXTRACTION_MODEL', 'phi3'))
        
        # Extract information from email
        extracted_info = extractor.extract_email_info(email_content, subject)
        
        # Find or create project
        project = None
        if extracted_info.get('project_name'):
            project = Project.query.filter_by(name=extracted_info['project_name']).first()
            if not project:
                project = Project(
                    name=extracted_info['project_name'],
                    company=extracted_info.get('company')
                )
                db.session.add(project)
                db.session.flush()
        
        # Store email in database
        email = Email(
            subject=subject,
            sender=sender,
            recipients=recipients,
            cc=cc,
            content=email_content,
            processed_content=extracted_info.get('summary', ''),
            keywords=extracted_info.get('keywords', []),
            people_mentioned=extracted_info.get('people', []),
            project_id=project.id if project else None,
            importance=extracted_info.get('importance', 'normal'),
            received_date=received_date
        )
        db.session.add(email)
        db.session.flush()
        
        # Add to vector store for semantic search
        vector_store = current_app.vector_store
        vector_id = vector_store.add_email(
            email.id,
            f"{subject}\n{email_content}",
            {
                'subject': subject,
                'sender': sender,
                'project_id': project.id if project else None,
                'project_name': project.name if project else '',
                'company': extracted_info.get('company', ''),
                'keywords': extracted_info.get('keywords', []),
                'people': extracted_info.get('people', []),
                'importance': extracted_info.get('importance', 'normal'),
                'received_date': received_date.isoformat()
            }
        )
        
        email.vector_id = vector_id
        
        # Process deliverables if any
        for deliverable_info in extracted_info.get('deliverables', []):
            if project and deliverable_info.get('title'):
                deliverable = Deliverable(
                    project_id=project.id,
                    title=deliverable_info['title'],
                    due_date=date_parser.parse(deliverable_info['due_date']) if deliverable_info.get('due_date') else None,
                    status='pending'
                )
                db.session.add(deliverable)
        
        # Store people mentioned
        for person_name in extracted_info.get('people', []):
            person = Person.query.filter_by(name=person_name).first()
            if not person:
                person = Person(
                    name=person_name,
                    company=extracted_info.get('company')
                )
                db.session.add(person)
        
        db.session.commit()
        
        return jsonify({
            'email_id': email.id,
            'extracted_info': extracted_info,
            'project': project.to_dict() if project else None,
            'message': 'Email processed successfully'
        }), 201
        
    except Exception as e:
        logger.error(f"Failed to process email: {e}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/status-updates', methods=['POST'])
def create_status_update():
    """Create a status update for a project."""
    try:
        data = request.json
        project_id = data.get('project_id')
        content = data.get('content', '')
        update_type = data.get('update_type', 'general')
        created_by = data.get('created_by', 'User')
        
        if not project_id or not content:
            return jsonify({'error': 'project_id and content are required'}), 400
        
        project = Project.query.get_or_404(project_id)
        
        # Extract keywords and information
        ollama = get_ollama_service()
        extractor = KeywordExtractor(ollama, current_app.config.get('EXTRACTION_MODEL', 'phi3'))
        extracted_info = extractor.extract_status_update_info(content, project.name)
        
        # Create status update
        status_update = StatusUpdate(
            project_id=project_id,
            content=content,
            update_type=extracted_info.get('update_type', update_type),
            keywords=extracted_info.get('keywords', []),
            created_by=created_by
        )
        db.session.add(status_update)
        db.session.flush()
        
        # Add to vector store
        vector_store = current_app.vector_store
        vector_id = vector_store.add_status_update(
            status_update.id,
            content,
            {
                'project_id': project_id,
                'project_name': project.name,
                'update_type': status_update.update_type,
                'keywords': extracted_info.get('keywords', []),
                'created_at': status_update.created_at.isoformat()
            }
        )
        
        status_update.vector_id = vector_id
        
        # Process any deliverables mentioned
        for deliverable_title in extracted_info.get('deliverables_mentioned', []):
            # Check if deliverable exists for this project
            existing = Deliverable.query.filter_by(
                project_id=project_id,
                title=deliverable_title
            ).first()
            
            if not existing:
                deliverable = Deliverable(
                    project_id=project_id,
                    title=deliverable_title,
                    status='in_progress'
                )
                db.session.add(deliverable)
        
        db.session.commit()
        
        return jsonify({
            'status_update': status_update.to_dict(),
            'extracted_info': extracted_info,
            'message': 'Status update created successfully'
        }), 201
        
    except Exception as e:
        logger.error(f"Failed to create status update: {e}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/deliverables', methods=['GET', 'POST'])
def deliverables():
    """Manage deliverables."""
    if request.method == 'GET':
        try:
            # Query parameters
            project_id = request.args.get('project_id', type=int)
            status = request.args.get('status')
            upcoming_days = request.args.get('upcoming_days', type=int)
            
            query = Deliverable.query
            
            if project_id:
                query = query.filter_by(project_id=project_id)
            
            if status:
                query = query.filter_by(status=status)
            
            if upcoming_days:
                deadline = datetime.utcnow() + timedelta(days=upcoming_days)
                query = query.filter(Deliverable.due_date <= deadline)
                query = query.filter(Deliverable.due_date >= datetime.utcnow())
            
            deliverables = query.order_by(Deliverable.due_date.asc()).all()
            
            return jsonify([d.to_dict() for d in deliverables])
            
        except Exception as e:
            logger.error(f"Failed to fetch deliverables: {e}")
            return jsonify({'error': str(e)}), 500
    
    elif request.method == 'POST':
        try:
            data = request.json
            
            deliverable = Deliverable(
                project_id=data['project_id'],
                title=data['title'],
                description=data.get('description'),
                due_date=date_parser.parse(data['due_date']) if data.get('due_date') else None,
                status=data.get('status', 'pending'),
                priority=data.get('priority', 'medium'),
                assigned_to=data.get('assigned_to')
            )
            db.session.add(deliverable)
            db.session.flush()
            
            # Add to vector store
            project = Project.query.get(deliverable.project_id)
            vector_store = current_app.vector_store
            
            content = f"{deliverable.title}\n{deliverable.description or ''}"
            vector_id = vector_store.add_deliverable(
                deliverable.id,
                content,
                {
                    'project_id': deliverable.project_id,
                    'project_name': project.name if project else '',
                    'title': deliverable.title,
                    'status': deliverable.status,
                    'priority': deliverable.priority,
                    'due_date': deliverable.due_date.isoformat() if deliverable.due_date else '',
                    'assigned_to': deliverable.assigned_to or ''
                }
            )
            
            db.session.commit()
            
            return jsonify(deliverable.to_dict()), 201
            
        except Exception as e:
            logger.error(f"Failed to create deliverable: {e}")
            db.session.rollback()
            return jsonify({'error': str(e)}), 500


@bp.route('/query', methods=['POST'])
def intelligent_query():
    """Process intelligent queries about work information."""
    try:
        data = request.json
        query = data.get('query', '')
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        # Parse the query to understand intent
        ollama = get_ollama_service()
        
        parse_prompt = f"""Analyze this work-related query and extract:
1. query_type: 'deliverables', 'emails', 'status', 'people', or 'general'
2. project_name: If a specific project is mentioned
3. time_frame: 'upcoming', 'past', 'today', 'this_week', etc.
4. specific_person: If asking about a specific person
5. urgency: If asking about urgent/important items

Query: {query}

Return ONLY JSON."""
        
        response = ollama.generate(parse_prompt, options={"temperature": 0.3, "num_predict": 200})
        
        import json
        import re
        response_text = response.get('response', '{}')
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            response_text = json_match.group()
        
        query_intent = json.loads(response_text)
        
        results = {}
        vector_store = current_app.vector_store
        
        # Handle different query types
        if 'deliverable' in query.lower() or query_intent.get('query_type') == 'deliverables':
            # Check for upcoming deliverables
            upcoming_days = current_app.config.get('DELIVERABLE_WARNING_DAYS', 7)
            
            if 'soon' in query.lower() or 'upcoming' in query.lower():
                deliverables = Deliverable.query.filter(
                    Deliverable.due_date <= datetime.utcnow() + timedelta(days=upcoming_days),
                    Deliverable.due_date >= datetime.utcnow(),
                    Deliverable.status != 'completed'
                )
                
                if query_intent.get('project_name'):
                    project = Project.query.filter_by(name=query_intent['project_name']).first()
                    if project:
                        deliverables = deliverables.filter_by(project_id=project.id)
                
                deliverables = deliverables.order_by(Deliverable.due_date.asc()).all()
                results['deliverables'] = [d.to_dict() for d in deliverables]
            
            # Also do semantic search
            search_results = vector_store.search_deliverables(query, n_results=5)
            results['related_deliverables'] = search_results
        
        # Search emails if relevant
        if 'email' in query.lower() or query_intent.get('query_type') == 'emails':
            search_results = vector_store.search_emails(query, n_results=5)
            results['emails'] = search_results
        
        # Search status updates
        if 'status' in query.lower() or 'update' in query.lower() or query_intent.get('query_type') == 'status':
            search_results = vector_store.search_status_updates(query, n_results=5)
            results['status_updates'] = search_results
        
        # If no specific type, search everything
        if not results:
            all_results = vector_store.search_all(query, n_results=5)
            results = all_results
        
        # Generate a natural language response
        context = json.dumps(results, indent=2)[:3000]
        
        answer_prompt = f"""Based on this work data, answer the user's query in a helpful way:

Query: {query}

Data:
{context}

Provide a concise, helpful answer that directly addresses the query."""
        
        answer_response = ollama.generate(answer_prompt, options={"temperature": 0.5, "num_predict": 300})
        
        return jsonify({
            'query': query,
            'answer': answer_response.get('response', 'I found the relevant information above.'),
            'results': results,
            'query_intent': query_intent
        })
        
    except Exception as e:
        logger.error(f"Failed to process query: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/people', methods=['GET'])
def get_people():
    """Get all people in the system."""
    try:
        people = Person.query.all()
        return jsonify([p.to_dict() for p in people])
    except Exception as e:
        logger.error(f"Failed to fetch people: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/emails', methods=['GET'])
def get_emails():
    """Get emails with optional filtering."""
    try:
        project_id = request.args.get('project_id', type=int)
        importance = request.args.get('importance')
        limit = request.args.get('limit', 20, type=int)
        
        query = Email.query
        
        if project_id:
            query = query.filter_by(project_id=project_id)
        
        if importance:
            query = query.filter_by(importance=importance)
        
        emails = query.order_by(Email.received_date.desc()).limit(limit).all()
        
        return jsonify([e.to_dict() for e in emails])
        
    except Exception as e:
        logger.error(f"Failed to fetch emails: {e}")
        return jsonify({'error': str(e)}), 500


@bp.route('/status-updates/<int:project_id>', methods=['GET'])
def get_status_updates(project_id):
    """Get status updates for a project."""
    try:
        updates = StatusUpdate.query.filter_by(project_id=project_id)\
                                   .order_by(StatusUpdate.created_at.desc())\
                                   .all()
        
        return jsonify([u.to_dict() for u in updates])
        
    except Exception as e:
        logger.error(f"Failed to fetch status updates: {e}")
        return jsonify({'error': str(e)}), 500