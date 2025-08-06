# Database Management Guide

## Automatic Table Creation

### Where Tables Are Created
1. **Models defined in**: `src/models/database.py`
2. **Creation triggered in**: `src/__init__.py` line 52: `db.create_all()`
3. **Database location**: Configured via `DATABASE_PATH` in `.env`

### First Run Behavior
When you run the app for the first time:
```
1. App starts
2. Checks if ./data/ directory exists → Creates it
3. Checks if work_assistant.db exists → Creates it
4. Runs db.create_all() → Creates all tables
5. Creates indexes automatically
6. Applies SQLite optimizations
```

## Manual Database Management

### View Database Schema
```bash
# Using SQLite CLI
sqlite3 data/work_assistant.db

# Show all tables
.tables

# Show schema for a specific table
.schema projects

# Show all indexes
.indexes

# Exit
.quit
```

### Using Python to Inspect
```python
# Run in Python shell with app context
from run import app
from src.models.database import db

with app.app_context():
    # Get all table names
    tables = db.metadata.tables.keys()
    print("Tables:", list(tables))
    
    # Inspect a specific table
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    columns = inspector.get_columns('projects')
    for col in columns:
        print(f"{col['name']}: {col['type']}")
```

## Schema Migrations (For Future Changes)

### Initial Setup (one time)
```bash
# Initialize migrations
flask db init

# Create first migration
flask db migrate -m "Initial migration"

# Apply migration
flask db upgrade
```

### Making Schema Changes
```bash
# 1. Modify models in database.py

# 2. Generate migration
flask db migrate -m "Add new field to projects"

# 3. Review migration file in migrations/versions/

# 4. Apply migration
flask db upgrade

# Rollback if needed
flask db downgrade
```

## Direct SQL Execution

### Add Custom Indexes
```python
from src.models.database import db
from sqlalchemy import text

with app.app_context():
    # Create composite index
    db.session.execute(text("""
        CREATE INDEX IF NOT EXISTS idx_email_project_date 
        ON emails(project_id, received_date DESC)
    """))
    db.session.commit()
```

### Run Raw Queries
```python
with app.app_context():
    result = db.session.execute(text("""
        SELECT p.name, COUNT(e.id) as email_count
        FROM projects p
        LEFT JOIN emails e ON p.id = e.project_id
        GROUP BY p.id
    """))
    for row in result:
        print(f"{row.name}: {row.email_count} emails")
```

## Database Maintenance

### Backup Database
```bash
# Simple file copy (safe while app running due to WAL mode)
cp data/work_assistant.db data/backup_$(date +%Y%m%d).db

# Using SQLite backup
sqlite3 data/work_assistant.db ".backup data/backup.db"
```

### Optimize Database
```python
from src.utils.db_optimizer import vacuum_database, analyze_database

with app.app_context():
    # Update statistics for query planner
    analyze_database(db)
    
    # Reclaim space and defragment
    vacuum_database(db)
```

### Check Database Integrity
```bash
sqlite3 data/work_assistant.db "PRAGMA integrity_check"
```

## Troubleshooting

### Database Locked Error
```python
# Increase timeout in config.py
SQLALCHEMY_ENGINE_OPTIONS = {
    'connect_args': {
        'timeout': 15  # seconds
    }
}
```

### Reset Database (Warning: Deletes All Data!)
```bash
# Delete database file
rm data/work_assistant.db

# Run app - will recreate everything
python run.py
```

### Export/Import Data
```bash
# Export to SQL
sqlite3 data/work_assistant.db .dump > export.sql

# Import from SQL
sqlite3 new_database.db < export.sql

# Export to CSV
sqlite3 -header -csv data/work_assistant.db "SELECT * FROM projects" > projects.csv
```

## Performance Monitoring

### Check Database Size
```python
from src.utils.db_optimizer import get_database_stats

with app.app_context():
    stats = get_database_stats(db)
    print(f"Database size: {stats['size_mb']:.2f} MB")
    print(f"Projects: {stats['projects_count']}")
    print(f"Emails: {stats['emails_count']}")
```

### Query Performance
```bash
# Enable query timing in SQLite
sqlite3 data/work_assistant.db
.timer on

# Run query
SELECT * FROM emails WHERE project_id = 1;

# Shows execution time
```

## Schema Documentation

### Current Tables
1. **projects** - Work projects
2. **emails** - Processed emails  
3. **status_updates** - Project status updates
4. **deliverables** - Tasks with due dates
5. **people** - People mentioned in emails

### Relationships
```
projects (1) → (N) emails
projects (1) → (N) status_updates  
projects (1) → (N) deliverables
```

### Indexes (Automatic)
- Primary keys: All `id` columns
- Foreign keys: All `project_id` columns
- Unique constraints: `projects.name`, `people.email`
- Date indexes: `received_date`, `due_date`, `created_at`
- Status indexes: `deliverables.status`, `projects.status`