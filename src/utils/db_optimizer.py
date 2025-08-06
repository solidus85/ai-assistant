"""SQLite optimization utilities for better performance."""
import logging
from sqlalchemy import event, text
from sqlalchemy.engine import Engine

logger = logging.getLogger(__name__)


def optimize_sqlite(app):
    """Apply SQLite optimizations for better performance."""
    
    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_conn, connection_record):
        """Set SQLite pragmas for optimal performance."""
        cursor = dbapi_conn.cursor()
        
        # Performance optimizations
        cursor.execute("PRAGMA journal_mode = WAL")  # Write-Ahead Logging - faster writes
        cursor.execute("PRAGMA synchronous = NORMAL")  # Faster writes, still safe
        cursor.execute("PRAGMA cache_size = -64000")  # 64MB cache (negative = KB)
        cursor.execute("PRAGMA temp_store = MEMORY")  # Use memory for temp tables
        cursor.execute("PRAGMA mmap_size = 268435456")  # 256MB memory-mapped I/O
        
        # Enable query optimizer
        cursor.execute("PRAGMA optimize")
        
        cursor.close()
        logger.info("SQLite optimizations applied")


def analyze_database(db):
    """Run ANALYZE to update SQLite statistics for better query planning."""
    try:
        db.session.execute(text("ANALYZE"))
        db.session.commit()
        logger.info("Database statistics updated")
    except Exception as e:
        logger.error(f"Failed to analyze database: {e}")


def create_fts_tables(db):
    """Create Full-Text Search tables for super fast text searching."""
    try:
        # Create FTS5 virtual table for emails
        db.session.execute(text("""
            CREATE VIRTUAL TABLE IF NOT EXISTS email_fts USING fts5(
                email_id UNINDEXED,
                subject,
                content,
                sender,
                keywords,
                content=emails,
                content_rowid=id
            )
        """))
        
        # Create triggers to keep FTS in sync
        db.session.execute(text("""
            CREATE TRIGGER IF NOT EXISTS email_fts_insert 
            AFTER INSERT ON emails BEGIN
                INSERT INTO email_fts(email_id, subject, content, sender, keywords)
                VALUES (new.id, new.subject, new.content, new.sender, new.keywords);
            END
        """))
        
        db.session.execute(text("""
            CREATE TRIGGER IF NOT EXISTS email_fts_update
            AFTER UPDATE ON emails BEGIN
                UPDATE email_fts 
                SET subject = new.subject, 
                    content = new.content,
                    sender = new.sender,
                    keywords = new.keywords
                WHERE email_id = new.id;
            END
        """))
        
        db.session.execute(text("""
            CREATE TRIGGER IF NOT EXISTS email_fts_delete
            AFTER DELETE ON emails BEGIN
                DELETE FROM email_fts WHERE email_id = old.id;
            END
        """))
        
        db.session.commit()
        logger.info("Full-Text Search tables created")
        
    except Exception as e:
        logger.error(f"Failed to create FTS tables: {e}")
        db.session.rollback()


def vacuum_database(db):
    """Vacuum database to reclaim space and optimize."""
    try:
        # Note: VACUUM cannot be run in a transaction
        db.session.close()
        db.engine.execute("VACUUM")
        logger.info("Database vacuumed and optimized")
    except Exception as e:
        logger.error(f"Failed to vacuum database: {e}")


def get_database_stats(db):
    """Get database statistics and performance metrics."""
    try:
        stats = {}
        
        # Get database size
        result = db.session.execute(text("SELECT page_count * page_size FROM pragma_page_count(), pragma_page_size()"))
        stats['size_bytes'] = result.scalar()
        stats['size_mb'] = stats['size_bytes'] / (1024 * 1024)
        
        # Get table counts
        for table in ['projects', 'emails', 'status_updates', 'deliverables', 'people']:
            result = db.session.execute(text(f"SELECT COUNT(*) FROM {table}"))
            stats[f'{table}_count'] = result.scalar()
        
        # Get cache statistics
        result = db.session.execute(text("PRAGMA cache_size"))
        stats['cache_size'] = result.scalar()
        
        result = db.session.execute(text("PRAGMA page_size"))
        stats['page_size'] = result.scalar()
        
        return stats
        
    except Exception as e:
        logger.error(f"Failed to get database stats: {e}")
        return {}