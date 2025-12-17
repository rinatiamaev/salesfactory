"""Tests for API endpoints."""
import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data


def test_health_endpoint():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "timestamp" in data


def test_create_catalog_item():
    """Test creating a catalog item via API."""
    response = client.post(
        "/api/catalog/items",
        json={
            "name": "Test Product",
            "description": "A test product",
            "price": 29.99
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["item"]["name"] == "Test Product"


def test_list_catalog_items():
    """Test listing catalog items via API."""
    # Create some items first
    client.post("/api/catalog/items", json={"name": "Item 1"})
    client.post("/api/catalog/items", json={"name": "Item 2"})
    
    response = client.get("/api/catalog/items?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["count"] >= 2


def test_request_id_header():
    """Test that request ID is added to response headers."""
    response = client.get("/health")
    assert "X-Request-ID" in response.headers
    assert len(response.headers["X-Request-ID"]) > 0
