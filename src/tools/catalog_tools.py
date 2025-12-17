"""Catalog management tools for the LangChain agent."""
from typing import Dict, Any, List, Optional
import uuid
from datetime import datetime

from ..memory.vector_memory import get_memory
from ..logger import get_logger

logger = get_logger(__name__)

# In-memory catalog storage (can be replaced with a real database)
_catalog_storage: Dict[str, Dict[str, Any]] = {}


def create_row(name: str, description: str = "", price: Optional[float] = None, **kwargs) -> Dict[str, Any]:
    """
    Create a new catalog row/item.
    
    Args:
        name: Name of the item
        description: Description of the item
        price: Price of the item
        **kwargs: Additional metadata
    
    Returns:
        Dict with the created item details
    """
    try:
        item_id = str(uuid.uuid4())
        timestamp = datetime.utcnow()
        
        item = {
            "id": item_id,
            "name": name,
            "description": description,
            "price": price,
            "metadata": kwargs,
            "created_at": timestamp.isoformat(),
            "updated_at": timestamp.isoformat()
        }
        
        _catalog_storage[item_id] = item
        
        # Add to vector memory for semantic search
        memory = get_memory()
        memory.add_catalog_item(
            item_id=item_id,
            name=name,
            description=description,
            metadata={"price": price, **kwargs}
        )
        
        logger.info(f"Created catalog row: {name} (ID: {item_id})")
        
        return {
            "success": True,
            "item": item,
            "message": f"Successfully created item '{name}'"
        }
        
    except Exception as e:
        logger.error(f"Failed to create catalog row: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to create item '{name}'"
        }


def list_rows(limit: int = 10) -> Dict[str, Any]:
    """
    List all catalog rows.
    
    Args:
        limit: Maximum number of items to return
    
    Returns:
        Dict with list of items
    """
    try:
        items = list(_catalog_storage.values())[:limit]
        
        logger.info(f"Listed {len(items)} catalog rows")
        
        return {
            "success": True,
            "items": items,
            "count": len(items),
            "total": len(_catalog_storage),
            "message": f"Found {len(items)} items"
        }
        
    except Exception as e:
        logger.error(f"Failed to list catalog rows: {e}")
        return {
            "success": False,
            "error": str(e),
            "items": [],
            "count": 0
        }


def get_row(item_id: str) -> Dict[str, Any]:
    """
    Get a specific catalog row by ID.
    
    Args:
        item_id: ID of the item to retrieve
    
    Returns:
        Dict with item details
    """
    try:
        if item_id not in _catalog_storage:
            return {
                "success": False,
                "message": f"Item with ID '{item_id}' not found"
            }
        
        item = _catalog_storage[item_id]
        
        logger.info(f"Retrieved catalog row: {item_id}")
        
        return {
            "success": True,
            "item": item,
            "message": f"Found item '{item['name']}'"
        }
        
    except Exception as e:
        logger.error(f"Failed to get catalog row: {e}")
        return {
            "success": False,
            "error": str(e)
        }


def update_row(item_id: str, name: Optional[str] = None, description: Optional[str] = None, 
               price: Optional[float] = None, **kwargs) -> Dict[str, Any]:
    """
    Update a catalog row.
    
    Args:
        item_id: ID of the item to update
        name: New name (optional)
        description: New description (optional)
        price: New price (optional)
        **kwargs: Additional metadata to update
    
    Returns:
        Dict with update status
    """
    try:
        if item_id not in _catalog_storage:
            return {
                "success": False,
                "message": f"Item with ID '{item_id}' not found"
            }
        
        item = _catalog_storage[item_id]
        
        if name is not None:
            item["name"] = name
        if description is not None:
            item["description"] = description
        if price is not None:
            item["price"] = price
        if kwargs:
            item["metadata"].update(kwargs)
        
        item["updated_at"] = datetime.utcnow().isoformat()
        
        # Update in vector memory
        memory = get_memory()
        memory.add_catalog_item(
            item_id=item_id,
            name=item["name"],
            description=item["description"],
            metadata={"price": item["price"], **item["metadata"]}
        )
        
        logger.info(f"Updated catalog row: {item_id}")
        
        return {
            "success": True,
            "item": item,
            "message": f"Successfully updated item '{item['name']}'"
        }
        
    except Exception as e:
        logger.error(f"Failed to update catalog row: {e}")
        return {
            "success": False,
            "error": str(e)
        }


def delete_row(item_id: str) -> Dict[str, Any]:
    """
    Delete a catalog row.
    
    Args:
        item_id: ID of the item to delete
    
    Returns:
        Dict with deletion status
    """
    try:
        if item_id not in _catalog_storage:
            return {
                "success": False,
                "message": f"Item with ID '{item_id}' not found"
            }
        
        item = _catalog_storage.pop(item_id)
        
        logger.info(f"Deleted catalog row: {item_id}")
        
        return {
            "success": True,
            "message": f"Successfully deleted item '{item['name']}'"
        }
        
    except Exception as e:
        logger.error(f"Failed to delete catalog row: {e}")
        return {
            "success": False,
            "error": str(e)
        }


def search_rows(query: str, limit: int = 5) -> Dict[str, Any]:
    """
    Search catalog rows using semantic search.
    
    Args:
        query: Search query
        limit: Maximum number of results
    
    Returns:
        Dict with search results
    """
    try:
        memory = get_memory()
        results = memory.search_catalog(query, limit=limit)
        
        # Get full item details
        items = []
        for result in results:
            item_id = result.get("id")
            if item_id and item_id in _catalog_storage:
                items.append(_catalog_storage[item_id])
        
        logger.info(f"Search for '{query}' returned {len(items)} results")
        
        return {
            "success": True,
            "items": items,
            "count": len(items),
            "query": query,
            "message": f"Found {len(items)} items matching '{query}'"
        }
        
    except Exception as e:
        logger.error(f"Failed to search catalog: {e}")
        return {
            "success": False,
            "error": str(e),
            "items": [],
            "count": 0
        }


def get_catalog_stats() -> Dict[str, Any]:
    """
    Get catalog statistics.
    
    Returns:
        Dict with catalog stats
    """
    try:
        total_items = len(_catalog_storage)
        items_with_price = sum(1 for item in _catalog_storage.values() if item.get("price") is not None)
        
        return {
            "success": True,
            "stats": {
                "total_items": total_items,
                "items_with_price": items_with_price,
                "items_without_price": total_items - items_with_price
            },
            "message": f"Catalog has {total_items} items"
        }
        
    except Exception as e:
        logger.error(f"Failed to get catalog stats: {e}")
        return {
            "success": False,
            "error": str(e)
        }
