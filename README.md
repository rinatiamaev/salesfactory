# SalesFactory - AI-Powered E-Commerce Catalog

An intelligent e-commerce catalog management system powered by AI agents, built with FastAPI, LangChain, and ChromaDB.

## 🚀 Features

### 1. **AI Service (Python)**
- **FastAPI**: Modern, fast web framework for building APIs
- **LangChain**: Advanced AI agent framework with tool calling capabilities

### 2. **Agent with Tools**
Intelligent catalog agent with the following capabilities:
- `create_catalog_item`: Add new products to catalog
- `list_catalog_items`: View all catalog items
- `get_catalog_item`: Retrieve specific items by ID
- `update_catalog_item`: Modify existing items
- `delete_catalog_item`: Remove items from catalog
- `search_catalog`: Semantic search across catalog
- `get_catalog_statistics`: View catalog metrics

### 3. **Vector DB + Memory**
- **ChromaDB**: Vector database for semantic search and memory
- **OpenAI Embeddings**: High-quality embeddings for similarity search
- **Stored Data**:
  - Agent action history
  - User conversation context
  - Catalog structure and metadata

### 4. **Conversational Flow (Agentic AI)**
Natural language interaction:
```
User: Add new row "Books"
Agent: 
  - Analyzes request
  - Calls create_catalog_item tool
  - Confirms: "Successfully created item 'Books'"
```

### 5. **WordPress-like Integration**
RESTful API endpoints compatible with WordPress patterns:
- `POST /api/catalog/items` - Create item
- `GET /api/catalog/items` - List items
- `GET /api/catalog/items/{id}` - Get item
- `PUT /api/catalog/items/{id}` - Update item
- `DELETE /api/catalog/items/{id}` - Delete item
- `GET /api/catalog/search?q=query` - Search items

### 6. **Observability**
- **Structured Logging**: JSON-formatted logs with contextual information
- **Request ID**: Unique identifier for tracking requests across the system
- **Retry Logic**: Automatic retry with exponential backoff using Tenacity
- **Error Handling**: Comprehensive error tracking and logging

## 📋 Requirements

- Python 3.9+
- OpenAI API key

## 🛠️ Installation

1. **Clone the repository**
```bash
git clone https://github.com/rinatiamaev/salesfactory.git
cd salesfactory
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## 🚀 Usage

### Quick Start

Run the service using the provided script:
```bash
./run.sh
```

Or manually:
```bash
cd src
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### API Documentation

Once running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### Conversational Interface

**Example: Create a catalog item**
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Add new row Books with price 15.99"
  }'
```

Response:
```json
{
  "response": "Successfully created item 'Books' with price $15.99",
  "session_id": "abc-123-def",
  "request_id": "req-456-ghi",
  "actions": [
    {
      "tool": "create_catalog_item",
      "input": "{\"name\": \"Books\", \"price\": 15.99}",
      "output": "Successfully created item 'Books'"
    }
  ]
}
```

### REST API (WordPress-like)

**Create Item**
```bash
curl -X POST http://localhost:8000/api/catalog/items \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Books",
    "description": "Collection of books",
    "price": 15.99
  }'
```

**List Items**
```bash
curl http://localhost:8000/api/catalog/items?limit=10
```

**Search Items**
```bash
curl http://localhost:8000/api/catalog/search?q=books&limit=5
```

## 🏗️ Architecture

```
salesfactory/
├── src/
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration management
│   ├── logger.py               # Structured logging setup
│   ├── api/
│   │   ├── catalog.py          # REST API endpoints
│   │   └── chat.py             # Conversational interface
│   ├── agents/
│   │   └── catalog_agent.py    # LangChain agent
│   ├── tools/
│   │   └── catalog_tools.py    # Agent tools for catalog management
│   ├── memory/
│   │   └── vector_memory.py    # ChromaDB vector memory
│   ├── middleware/
│   │   └── request_id.py       # Request tracking middleware
│   └── models/
│       └── schemas.py          # Pydantic models
├── tests/                      # Test files
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
└── run.sh                     # Run script

```

## 🔧 Configuration

Edit `.env` file:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4-turbo-preview

# Server Configuration
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO

# ChromaDB Configuration
CHROMA_PERSIST_DIRECTORY=./chroma_db
```

## 🧪 Testing

```bash
pytest tests/ -v
```

## 📊 Logging

The service uses structured JSON logging. Example log entry:

```json
{
  "timestamp": "2024-01-15T10:30:45.123Z",
  "level": "INFO",
  "logger": "src.agents.catalog_agent",
  "request_id": "req-abc-123",
  "message": "Successfully processed message",
  "method": "POST",
  "path": "/api/chat",
  "duration_ms": 245.67
}
```

## 🔄 Retry Logic

All vector DB operations include automatic retry logic:
- Maximum 3 attempts
- Exponential backoff (2s, 4s, 8s)
- Graceful degradation on failure

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

See LICENSE file for details.

## 🙋 Support

For issues and questions, please open an issue on GitHub.
