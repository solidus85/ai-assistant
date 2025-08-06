"""Vector store service for semantic search using ChromaDB."""
import chromadb
from chromadb.config import Settings
import logging
from typing import List, Dict, Any, Optional
import hashlib
import json

logger = logging.getLogger(__name__)


class VectorStore:
    """Manage vector embeddings for semantic search."""
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        """Initialize ChromaDB client."""
        try:
            self.client = chromadb.PersistentClient(
                path=persist_directory,
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            
            self.email_collection = self.client.get_or_create_collection(
                name="emails",
                metadata={"description": "Email embeddings for semantic search"}
            )
            
            self.status_collection = self.client.get_or_create_collection(
                name="status_updates",
                metadata={"description": "Status update embeddings"}
            )
            
            self.deliverable_collection = self.client.get_or_create_collection(
                name="deliverables",
                metadata={"description": "Deliverable embeddings"}
            )
            
            logger.info("VectorStore initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize VectorStore: {e}")
            raise
    
    def add_email(self, email_id: int, content: str, metadata: Dict[str, Any]) -> str:
        """Add email to vector store."""
        try:
            vector_id = self._generate_id(f"email_{email_id}")
            
            self.email_collection.upsert(
                ids=[vector_id],
                documents=[content],
                metadatas=[{
                    "email_id": email_id,
                    "subject": metadata.get("subject", ""),
                    "sender": metadata.get("sender", ""),
                    "project_id": metadata.get("project_id"),
                    "project_name": metadata.get("project_name", ""),
                    "company": metadata.get("company", ""),
                    "keywords": json.dumps(metadata.get("keywords", [])),
                    "people": json.dumps(metadata.get("people", [])),
                    "importance": metadata.get("importance", "normal"),
                    "received_date": metadata.get("received_date", "")
                }]
            )
            
            logger.info(f"Added email {email_id} to vector store with ID {vector_id}")
            return vector_id
            
        except Exception as e:
            logger.error(f"Failed to add email to vector store: {e}")
            return None
    
    def add_status_update(self, update_id: int, content: str, metadata: Dict[str, Any]) -> str:
        """Add status update to vector store."""
        try:
            vector_id = self._generate_id(f"status_{update_id}")
            
            self.status_collection.upsert(
                ids=[vector_id],
                documents=[content],
                metadatas=[{
                    "update_id": update_id,
                    "project_id": metadata.get("project_id"),
                    "project_name": metadata.get("project_name", ""),
                    "update_type": metadata.get("update_type", "general"),
                    "keywords": json.dumps(metadata.get("keywords", [])),
                    "created_at": metadata.get("created_at", "")
                }]
            )
            
            logger.info(f"Added status update {update_id} to vector store")
            return vector_id
            
        except Exception as e:
            logger.error(f"Failed to add status update to vector store: {e}")
            return None
    
    def add_deliverable(self, deliverable_id: int, content: str, metadata: Dict[str, Any]) -> str:
        """Add deliverable to vector store."""
        try:
            vector_id = self._generate_id(f"deliverable_{deliverable_id}")
            
            self.deliverable_collection.upsert(
                ids=[vector_id],
                documents=[content],
                metadatas=[{
                    "deliverable_id": deliverable_id,
                    "project_id": metadata.get("project_id"),
                    "project_name": metadata.get("project_name", ""),
                    "title": metadata.get("title", ""),
                    "status": metadata.get("status", "pending"),
                    "priority": metadata.get("priority", "medium"),
                    "due_date": metadata.get("due_date", ""),
                    "assigned_to": metadata.get("assigned_to", "")
                }]
            )
            
            logger.info(f"Added deliverable {deliverable_id} to vector store")
            return vector_id
            
        except Exception as e:
            logger.error(f"Failed to add deliverable to vector store: {e}")
            return None
    
    def search_emails(self, query: str, n_results: int = 5, 
                      filter_dict: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search emails using semantic similarity."""
        try:
            where_clause = self._build_where_clause(filter_dict)
            
            results = self.email_collection.query(
                query_texts=[query],
                n_results=n_results,
                where=where_clause if where_clause else None
            )
            
            return self._format_results(results, "email")
            
        except Exception as e:
            logger.error(f"Email search failed: {e}")
            return []
    
    def search_status_updates(self, query: str, n_results: int = 5,
                            filter_dict: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search status updates using semantic similarity."""
        try:
            where_clause = self._build_where_clause(filter_dict)
            
            results = self.status_collection.query(
                query_texts=[query],
                n_results=n_results,
                where=where_clause if where_clause else None
            )
            
            return self._format_results(results, "status")
            
        except Exception as e:
            logger.error(f"Status update search failed: {e}")
            return []
    
    def search_deliverables(self, query: str, n_results: int = 5,
                          filter_dict: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search deliverables using semantic similarity."""
        try:
            where_clause = self._build_where_clause(filter_dict)
            
            results = self.deliverable_collection.query(
                query_texts=[query],
                n_results=n_results,
                where=where_clause if where_clause else None
            )
            
            return self._format_results(results, "deliverable")
            
        except Exception as e:
            logger.error(f"Deliverable search failed: {e}")
            return []
    
    def search_all(self, query: str, n_results: int = 5,
                  filter_dict: Optional[Dict[str, Any]] = None) -> Dict[str, List[Dict[str, Any]]]:
        """Search across all collections."""
        return {
            "emails": self.search_emails(query, n_results, filter_dict),
            "status_updates": self.search_status_updates(query, n_results, filter_dict),
            "deliverables": self.search_deliverables(query, n_results, filter_dict)
        }
    
    def delete_email(self, email_id: int):
        """Delete email from vector store."""
        try:
            vector_id = self._generate_id(f"email_{email_id}")
            self.email_collection.delete(ids=[vector_id])
            logger.info(f"Deleted email {email_id} from vector store")
        except Exception as e:
            logger.error(f"Failed to delete email from vector store: {e}")
    
    def delete_status_update(self, update_id: int):
        """Delete status update from vector store."""
        try:
            vector_id = self._generate_id(f"status_{update_id}")
            self.status_collection.delete(ids=[vector_id])
            logger.info(f"Deleted status update {update_id} from vector store")
        except Exception as e:
            logger.error(f"Failed to delete status update from vector store: {e}")
    
    def delete_deliverable(self, deliverable_id: int):
        """Delete deliverable from vector store."""
        try:
            vector_id = self._generate_id(f"deliverable_{deliverable_id}")
            self.deliverable_collection.delete(ids=[vector_id])
            logger.info(f"Deleted deliverable {deliverable_id} from vector store")
        except Exception as e:
            logger.error(f"Failed to delete deliverable from vector store: {e}")
    
    def _generate_id(self, base_string: str) -> str:
        """Generate a unique ID for vector storage."""
        return hashlib.md5(base_string.encode()).hexdigest()
    
    def _build_where_clause(self, filter_dict: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Build ChromaDB where clause from filter dictionary."""
        if not filter_dict:
            return None
        
        where_clause = {}
        
        for key, value in filter_dict.items():
            if value is not None:
                if isinstance(value, list):
                    where_clause[key] = {"$in": value}
                else:
                    where_clause[key] = value
        
        return where_clause if where_clause else None
    
    def _format_results(self, results: Dict[str, Any], result_type: str) -> List[Dict[str, Any]]:
        """Format ChromaDB results into consistent structure."""
        formatted = []
        
        if not results or not results.get('ids'):
            return formatted
        
        ids = results['ids'][0] if results['ids'] else []
        documents = results['documents'][0] if results['documents'] else []
        metadatas = results['metadatas'][0] if results['metadatas'] else []
        distances = results['distances'][0] if results.get('distances') else []
        
        for i in range(len(ids)):
            item = {
                'id': ids[i] if i < len(ids) else None,
                'content': documents[i] if i < len(documents) else None,
                'metadata': metadatas[i] if i < len(metadatas) else {},
                'similarity_score': 1 - distances[i] if i < len(distances) else 0,
                'type': result_type
            }
            
            if item['metadata'].get('keywords'):
                try:
                    item['metadata']['keywords'] = json.loads(item['metadata']['keywords'])
                except:
                    pass
            
            if item['metadata'].get('people'):
                try:
                    item['metadata']['people'] = json.loads(item['metadata']['people'])
                except:
                    pass
            
            formatted.append(item)
        
        return formatted