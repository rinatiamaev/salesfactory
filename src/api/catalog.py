"""API routes for catalog management."""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import uuid

from ..models.schemas import CatalogRow, CatalogRowCreate, CatalogRowUpdate
from ..tools.catalog_tools import (
    create_row, list_rows, get_row, update_row, delete_row, search_rows, get_catalog_stats
)
from ..logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/catalog", tags=["catalog"])


@router.post("/items", response_model=Dict[str, Any])
async def create_catalog_item(item: CatalogRowCreate) -> Dict[str, Any]:
    """Create a new catalog item (WordPress-like REST API)."""
    try:
        result = create_row(
            name=item.name,
            description=item.description or "",
            price=item.price,
            **(item.metadata or {})
        )
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("message"))
        
        return result
        
    except Exception as e:
        logger.error(f"Failed to create catalog item: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/items", response_model=Dict[str, Any])
async def list_catalog_items(limit: int = 10) -> Dict[str, Any]:
    """List all catalog items."""
    try:
        result = list_rows(limit=limit)
        return result
        
    except Exception as e:
        logger.error(f"Failed to list catalog items: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/items/{item_id}", response_model=Dict[str, Any])
async def get_catalog_item(item_id: str) -> Dict[str, Any]:
    """Get a specific catalog item by ID."""
    try:
        result = get_row(item_id)
        
        if not result.get("success"):
            raise HTTPException(status_code=404, detail=result.get("message"))
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get catalog item: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/items/{item_id}", response_model=Dict[str, Any])
async def update_catalog_item(item_id: str, item: CatalogRowUpdate) -> Dict[str, Any]:
    """Update a catalog item."""
    try:
        result = update_row(
            item_id=item_id,
            name=item.name,
            description=item.description,
            price=item.price,
            **(item.metadata or {})
        )
        
        if not result.get("success"):
            raise HTTPException(status_code=404, detail=result.get("message"))
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update catalog item: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/items/{item_id}", response_model=Dict[str, Any])
async def delete_catalog_item(item_id: str) -> Dict[str, Any]:
    """Delete a catalog item."""
    try:
        result = delete_row(item_id)
        
        if not result.get("success"):
            raise HTTPException(status_code=404, detail=result.get("message"))
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete catalog item: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search", response_model=Dict[str, Any])
async def search_catalog_items(q: str, limit: int = 5) -> Dict[str, Any]:
    """Search catalog items using semantic search."""
    try:
        result = search_rows(query=q, limit=limit)
        return result
        
    except Exception as e:
        logger.error(f"Failed to search catalog: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats", response_model=Dict[str, Any])
async def get_stats() -> Dict[str, Any]:
    """Get catalog statistics."""
    try:
        result = get_catalog_stats()
        return result
        
    except Exception as e:
        logger.error(f"Failed to get catalog stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))
