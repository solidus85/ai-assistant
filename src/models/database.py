"""Database models for work assistant."""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Index
from sqlalchemy.dialects.sqlite import JSON

db = SQLAlchemy()


class Project(db.Model):
    """Project model for tracking work projects."""
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    company = db.Column(db.String(200))
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    emails = db.relationship('Email', backref='project', lazy='dynamic')
    status_updates = db.relationship('StatusUpdate', backref='project', lazy='dynamic')
    deliverables = db.relationship('Deliverable', backref='project', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'company': self.company,
            'description': self.description,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Email(db.Model):
    """Email model for storing processed emails."""
    __tablename__ = 'emails'
    
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(500))
    sender = db.Column(db.String(200), nullable=False)
    recipients = db.Column(JSON)
    cc = db.Column(JSON)
    content = db.Column(db.Text, nullable=False)
    processed_content = db.Column(db.Text)
    keywords = db.Column(JSON)
    people_mentioned = db.Column(JSON)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    importance = db.Column(db.String(20), default='normal')
    received_date = db.Column(db.DateTime)
    processed_at = db.Column(db.DateTime, default=datetime.utcnow)
    vector_id = db.Column(db.String(100))
    
    __table_args__ = (
        Index('idx_email_project', 'project_id'),
        Index('idx_email_date', 'received_date'),
        Index('idx_email_importance', 'importance'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'subject': self.subject,
            'sender': self.sender,
            'recipients': self.recipients,
            'cc': self.cc,
            'content': self.content[:500] + '...' if len(self.content) > 500 else self.content,
            'keywords': self.keywords,
            'people_mentioned': self.people_mentioned,
            'project_id': self.project_id,
            'project_name': self.project.name if self.project else None,
            'importance': self.importance,
            'received_date': self.received_date.isoformat() if self.received_date else None,
            'processed_at': self.processed_at.isoformat() if self.processed_at else None
        }


class StatusUpdate(db.Model):
    """Status update model for tracking project progress."""
    __tablename__ = 'status_updates'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    update_type = db.Column(db.String(50))
    keywords = db.Column(JSON)
    created_by = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    vector_id = db.Column(db.String(100))
    
    __table_args__ = (
        Index('idx_status_project', 'project_id'),
        Index('idx_status_date', 'created_at'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'project_name': self.project.name if self.project else None,
            'content': self.content,
            'update_type': self.update_type,
            'keywords': self.keywords,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Deliverable(db.Model):
    """Deliverable model for tracking project deliverables and deadlines."""
    __tablename__ = 'deliverables'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    title = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.DateTime)
    status = db.Column(db.String(50), default='pending')
    priority = db.Column(db.String(20), default='medium')
    assigned_to = db.Column(db.String(200))
    completed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_deliverable_project', 'project_id'),
        Index('idx_deliverable_due', 'due_date'),
        Index('idx_deliverable_status', 'status'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'project_name': self.project.name if self.project else None,
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'status': self.status,
            'priority': self.priority,
            'assigned_to': self.assigned_to,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Person(db.Model):
    """Person model for tracking people mentioned in emails and projects."""
    __tablename__ = 'people'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True)
    company = db.Column(db.String(200))
    role = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'company': self.company,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }