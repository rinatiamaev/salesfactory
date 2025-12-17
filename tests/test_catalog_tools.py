"""Tests for catalog tools."""
import pytest
from unittest.mock import MagicMock, patch
from src.tools.catalog_tools import (
    create_row, list_rows, get_row, update_row, delete_row, get_catalog_stats,
    _catalog_storage
)


@pytest.fixture(autouse=True)
def clear_catalog():
    """Clear catalog before each test."""
    _catalog_storage.clear()
    yield
    _catalog_storage.clear()


@pytest.fixture(autouse=True)
def mock_memory():
    """Mock the vector memory to avoid ChromaDB initialization."""
    with patch('src.tools.catalog_tools.get_memory') as mock:
        mock_instance = MagicMock()
        mock_instance.add_catalog_item.return_value = None
        mock.return_value = mock_instance
        yield mock_instance


def test_create_row(mock_memory):
    """Test creating a catalog row."""
    result = create_row(name="Test Item", description="Test description", price=10.99)
    
    assert result["success"] is True
    assert "item" in result
    assert result["item"]["name"] == "Test Item"
    assert result["item"]["description"] == "Test description"
    assert result["item"]["price"] == 10.99
    
    # Verify memory was called
    mock_memory.add_catalog_item.assert_called_once()


def test_create_row_minimal(mock_memory):
    """Test creating a catalog row with minimal data."""
    result = create_row(name="Minimal Item")
    
    assert result["success"] is True
    assert result["item"]["name"] == "Minimal Item"
    assert result["item"]["description"] == ""
    assert result["item"]["price"] is None


def test_list_rows():
    """Test listing catalog rows."""
    # Create some items
    create_row(name="Item 1")
    create_row(name="Item 2")
    create_row(name="Item 3")
    
    result = list_rows(limit=10)
    
    assert result["success"] is True
    assert result["count"] == 3
    assert result["total"] == 3
    assert len(result["items"]) == 3


def test_list_rows_with_limit():
    """Test listing catalog rows with limit."""
    # Create some items
    for i in range(5):
        create_row(name=f"Item {i}")
    
    result = list_rows(limit=3)
    
    assert result["success"] is True
    assert result["count"] == 3
    assert len(result["items"]) == 3


def test_get_row():
    """Test getting a specific catalog row."""
    # Create an item
    create_result = create_row(name="Test Item")
    item_id = create_result["item"]["id"]
    
    # Get the item
    result = get_row(item_id)
    
    assert result["success"] is True
    assert result["item"]["id"] == item_id
    assert result["item"]["name"] == "Test Item"


def test_get_row_not_found():
    """Test getting a non-existent catalog row."""
    result = get_row("non-existent-id")
    
    assert result["success"] is False
    assert "not found" in result["message"].lower()


def test_update_row(mock_memory):
    """Test updating a catalog row."""
    # Create an item
    create_result = create_row(name="Original Name", price=10.99)
    item_id = create_result["item"]["id"]
    
    # Update the item
    result = update_row(item_id, name="Updated Name", price=15.99)
    
    assert result["success"] is True
    assert result["item"]["name"] == "Updated Name"
    assert result["item"]["price"] == 15.99


def test_update_row_partial(mock_memory):
    """Test partial update of a catalog row."""
    # Create an item
    create_result = create_row(name="Original Name", description="Original Desc", price=10.99)
    item_id = create_result["item"]["id"]
    
    # Update only the price
    result = update_row(item_id, price=20.00)
    
    assert result["success"] is True
    assert result["item"]["name"] == "Original Name"  # Unchanged
    assert result["item"]["description"] == "Original Desc"  # Unchanged
    assert result["item"]["price"] == 20.00  # Updated


def test_update_row_not_found():
    """Test updating a non-existent catalog row."""
    result = update_row("non-existent-id", name="New Name")
    
    assert result["success"] is False
    assert "not found" in result["message"].lower()


def test_delete_row():
    """Test deleting a catalog row."""
    # Create an item
    create_result = create_row(name="To Delete")
    item_id = create_result["item"]["id"]
    
    # Delete the item
    result = delete_row(item_id)
    
    assert result["success"] is True
    assert "deleted" in result["message"].lower()
    
    # Verify it's gone
    get_result = get_row(item_id)
    assert get_result["success"] is False


def test_delete_row_not_found():
    """Test deleting a non-existent catalog row."""
    result = delete_row("non-existent-id")
    
    assert result["success"] is False
    assert "not found" in result["message"].lower()


def test_get_catalog_stats():
    """Test getting catalog statistics."""
    # Create items
    create_row(name="Item 1", price=10.99)
    create_row(name="Item 2", price=15.99)
    create_row(name="Item 3")  # No price
    
    result = get_catalog_stats()
    
    assert result["success"] is True
    assert result["stats"]["total_items"] == 3
    assert result["stats"]["items_with_price"] == 2
    assert result["stats"]["items_without_price"] == 1
