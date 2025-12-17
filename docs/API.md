# API Documentation

## Overview

The SalesFactory AI Catalog Service provides two main interfaces:
1. **Conversational AI Interface** - Natural language interaction with the catalog
2. **REST API** - Traditional RESTful API for programmatic access

## Base URL

```
http://localhost:8000
```

## Endpoints

### Health Check

#### `GET /health`

Check service health status.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-01-15T10:30:45.123Z"
}
```

---

### Conversational Interface

#### `POST /api/chat`

Interact with the AI agent using natural language.

**Request:**
```json
{
  "message": "Add new row Books with price 25.99",
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "response": "Successfully created item 'Books' with price $25.99",
  "session_id": "abc-123-def",
  "request_id": "req-456-ghi",
  "actions": [
    {
      "tool": "create_catalog_item",
      "input": "{\"name\": \"Books\", \"price\": 25.99}",
      "output": "Successfully created item 'Books'"
    }
  ]
}
```

---

### Catalog REST API

#### `POST /api/catalog/items` - Create item
#### `GET /api/catalog/items` - List items  
#### `GET /api/catalog/items/{item_id}` - Get item
#### `PUT /api/catalog/items/{item_id}` - Update item
#### `DELETE /api/catalog/items/{item_id}` - Delete item
#### `GET /api/catalog/search?q=query` - Search items
#### `GET /api/catalog/stats` - Get statistics

See full API documentation at http://localhost:8000/docs when running the service.
