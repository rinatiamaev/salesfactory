#!/usr/bin/env python3
"""Demo script to showcase the AI Catalog Service functionality."""

import asyncio
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import after path is set
from unittest.mock import MagicMock, patch

# Mock the memory module to avoid ChromaDB initialization
sys.modules['src.memory.vector_memory'] = MagicMock()

from src.tools.catalog_tools import create_row, list_rows, get_catalog_stats, _catalog_storage


async def demo():
    """Run a demo of the catalog functionality."""
    
    # Clear storage first
    _catalog_storage.clear()
    
    print("=" * 60)
    print("AI Catalog Service Demo")
    print("=" * 60)
    print()
    
    # 1. Create some items
    print("1. Creating catalog items...")
    print("-" * 60)
    
    items = [
        {"name": "Books", "description": "Educational books", "price": 25.99},
        {"name": "Laptop", "description": "Gaming laptop", "price": 1299.99},
        {"name": "Coffee Maker", "description": "Automatic coffee maker", "price": 89.99},
        {"name": "Headphones", "description": "Noise-cancelling headphones", "price": 199.99},
        {"name": "Desk Chair", "description": "Ergonomic office chair", "price": 349.99},
    ]
    
    for item_data in items:
        result = create_row(**item_data)
        if result["success"]:
            print(f"✓ Created: {item_data['name']} - ${item_data['price']}")
        else:
            print(f"✗ Failed: {item_data['name']}")
    
    print()
    
    # 2. List all items
    print("2. Listing all catalog items...")
    print("-" * 60)
    
    result = list_rows(limit=10)
    if result["success"]:
        print(f"Total items: {result['total']}")
        for item in result["items"]:
            price = f"${item['price']:.2f}" if item['price'] else "No price"
            print(f"  - {item['name']}: {price}")
    
    print()
    
    # 3. Get statistics
    print("3. Catalog Statistics...")
    print("-" * 60)
    
    result = get_catalog_stats()
    if result["success"]:
        stats = result["stats"]
        print(f"Total items: {stats['total_items']}")
        print(f"Items with price: {stats['items_with_price']}")
        print(f"Items without price: {stats['items_without_price']}")
    
    print()
    
    print("=" * 60)
    print("Demo completed successfully!")
    print("=" * 60)
    print()
    print("To run the full service with AI agent:")
    print("  1. Set OPENAI_API_KEY in .env file")
    print("  2. Run: ./run.sh")
    print("  3. Visit: http://localhost:8000/docs")
    print()


if __name__ == "__main__":
    asyncio.run(demo())
