"""ChromaDB-based memory system for the agent."""
import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import json
from tenacity import retry, stop_after_attempt, wait_exponential

from ..config import settings
from ..logger import get_logger

logger = get_logger(__name__)


class VectorMemory:
    """Vector-based memory system using ChromaDB."""
    
    def __init__(self):
        """Initialize ChromaDB client and collections."""
        try:
            self.client = chromadb.PersistentClient(
                path=settings.chroma_persist_directory,
                settings=ChromaSettings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            
            # Collection for conversation history
            self.conversation_collection = self.client.get_or_create_collection(
                name="conversations",
                metadata={"description": "Agent conversation history"}
            )
            
            # Collection for catalog structure
            self.catalog_collection = self.client.get_or_create_collection(
                name="catalog",
                metadata={"description": "Product catalog structure"}
            )
            
            # Collection for agent actions
            self.actions_collection = self.client.get_or_create_collection(
                name="agent_actions",
                metadata={"description": "Agent action history"}
            )
            
            logger.info("VectorMemory initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize VectorMemory: {e}")
            raise
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def add_conversation(self, session_id: str, role: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Add a conversation message to memory."""
        try:
            doc_id = f"{session_id}_{datetime.now(timezone.utc).isoformat()}"
            doc_metadata = {
                "session_id": session_id,
                "role": role,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                **(metadata or {})
            }
            
            self.conversation_collection.add(
                documents=[content],
                metadatas=[doc_metadata],
                ids=[doc_id]
            )
            
            logger.info(f"Added conversation to memory: {doc_id}")
            
        except Exception as e:
            logger.error(f"Failed to add conversation to memory: {e}")
            raise
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def get_conversation_history(self, session_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieve conversation history for a session."""
        try:
            results = self.conversation_collection.get(
                where={"session_id": session_id},
                limit=limit
            )
            
            if not results['documents']:
                return []
            
            history = []
            for doc, metadata in zip(results['documents'], results['metadatas']):
                history.append({
                    "role": metadata.get("role"),
                    "content": doc,
                    "timestamp": metadata.get("timestamp")
                })
            
            # Sort by timestamp
            history.sort(key=lambda x: x.get("timestamp", ""))
            
            return history
            
        except Exception as e:
            logger.error(f"Failed to retrieve conversation history: {e}")
            return []
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def add_catalog_item(self, item_id: str, name: str, description: str = "", metadata: Optional[Dict[str, Any]] = None) -> None:
        """Add or update a catalog item in memory."""
        try:
            doc_metadata = {
                "item_id": item_id,
                "name": name,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                **(metadata or {})
            }
            
            # Combine name and description for better semantic search
            document = f"{name}. {description}" if description else name
            
            self.catalog_collection.upsert(
                documents=[document],
                metadatas=[doc_metadata],
                ids=[item_id]
            )
            
            logger.info(f"Added catalog item to memory: {item_id}")
            
        except Exception as e:
            logger.error(f"Failed to add catalog item to memory: {e}")
            raise
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def search_catalog(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search catalog items by semantic similarity."""
        try:
            results = self.catalog_collection.query(
                query_texts=[query],
                n_results=limit
            )
            
            if not results['documents'] or not results['documents'][0]:
                return []
            
            items = []
            for doc, metadata in zip(results['documents'][0], results['metadatas'][0]):
                items.append({
                    "id": metadata.get("item_id"),
                    "name": metadata.get("name"),
                    "content": doc,
                    "metadata": metadata
                })
            
            return items
            
        except Exception as e:
            logger.error(f"Failed to search catalog: {e}")
            return []
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def add_action(self, session_id: str, action: str, parameters: Dict[str, Any], result: Any) -> None:
        """Record an agent action."""
        try:
            doc_id = f"{session_id}_{action}_{datetime.now(timezone.utc).isoformat()}"
            doc_content = f"Action: {action}, Parameters: {json.dumps(parameters)}"
            doc_metadata = {
                "session_id": session_id,
                "action": action,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "result": str(result)
            }
            
            self.actions_collection.add(
                documents=[doc_content],
                metadatas=[doc_metadata],
                ids=[doc_id]
            )
            
            logger.info(f"Recorded action: {action}")
            
        except Exception as e:
            logger.error(f"Failed to record action: {e}")
            # Don't raise - action recording failure shouldn't break the flow
            # TODO: Consider adding metrics/monitoring for action recording failures
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def get_action_history(self, session_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieve action history for a session."""
        try:
            results = self.actions_collection.get(
                where={"session_id": session_id},
                limit=limit
            )
            
            if not results['documents']:
                return []
            
            actions = []
            for doc, metadata in zip(results['documents'], results['metadatas']):
                actions.append({
                    "action": metadata.get("action"),
                    "timestamp": metadata.get("timestamp"),
                    "result": metadata.get("result"),
                    "details": doc
                })
            
            # Sort by timestamp
            actions.sort(key=lambda x: x.get("timestamp", ""))
            
            return actions
            
        except Exception as e:
            logger.error(f"Failed to retrieve action history: {e}")
            return []


# Singleton instance
_memory_instance = None


def get_memory() -> VectorMemory:
    """Get or create the singleton VectorMemory instance."""
    global _memory_instance
    if _memory_instance is None:
        _memory_instance = VectorMemory()
    return _memory_instance
