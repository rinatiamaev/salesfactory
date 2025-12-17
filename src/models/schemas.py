"""Pydantic models for the API."""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class ChatMessage(BaseModel):
    """A chat message."""
    role: str = Field(..., description="Role of the message sender (user/assistant)")
    content: str = Field(..., description="Content of the message")


class ChatRequest(BaseModel):
    """Request for chat endpoint."""
    message: str = Field(..., description="User message")
    session_id: Optional[str] = Field(None, description="Session ID for conversation continuity")


class ChatResponse(BaseModel):
    """Response from chat endpoint."""
    response: str = Field(..., description="Agent response")
    session_id: str = Field(..., description="Session ID")
    request_id: str = Field(..., description="Request ID for tracking")
    actions: Optional[List[Dict[str, Any]]] = Field(None, description="Actions performed by the agent")


class CatalogRow(BaseModel):
    """A catalog row/item."""
    id: str = Field(..., description="Unique identifier")
    name: str = Field(..., description="Item name")
    description: Optional[str] = Field(None, description="Item description")
    price: Optional[float] = Field(None, description="Item price")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class CatalogRowCreate(BaseModel):
    """Request to create a catalog row."""
    name: str = Field(..., description="Item name")
    description: Optional[str] = Field(None, description="Item description")
    price: Optional[float] = Field(None, description="Item price")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class CatalogRowUpdate(BaseModel):
    """Request to update a catalog row."""
    name: Optional[str] = Field(None, description="Item name")
    description: Optional[str] = Field(None, description="Item description")
    price: Optional[float] = Field(None, description="Item price")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
