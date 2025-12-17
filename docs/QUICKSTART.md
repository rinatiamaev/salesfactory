# Quick Start Guide

## Prerequisites

- Python 3.9 or higher
- OpenAI API key
- Git

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/rinatiamaev/salesfactory.git
cd salesfactory
```

### 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```env
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4-turbo-preview
```

## Running the Service

### Option 1: Using the run script

```bash
./run.sh
```

### Option 2: Manual start

```bash
cd src
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The service will start on `http://localhost:8000`

## Quick Demo

Run the demo script to see the catalog functionality:

```bash
python3 demo.py
```

## Using the Service

### 1. Interactive API Documentation

Visit `http://localhost:8000/docs` for Swagger UI

### 2. Conversational Interface

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Add new row Books with price 25.99"
  }'
```

Response:
```json
{
  "response": "Successfully created item 'Books' with price $25.99",
  "session_id": "abc-123",
  "request_id": "req-456",
  "actions": [...]
}
```

### 3. REST API

**Create an item:**
```bash
curl -X POST http://localhost:8000/api/catalog/items \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "description": "Gaming laptop",
    "price": 1299.99
  }'
```

**List items:**
```bash
curl http://localhost:8000/api/catalog/items?limit=10
```

**Search items:**
```bash
curl http://localhost:8000/api/catalog/search?q=laptop&limit=5
```

## Example Conversations

### Creating Items

```
User: "Add new row Books"
Agent: "Successfully created item 'Books'"

User: "Create a laptop item with price 1299.99"
Agent: "Successfully created item 'laptop' with price $1299.99"
```

### Querying Items

```
User: "Show me all items"
Agent: "Here are the items in the catalog: Books, Laptop, ..."

User: "Search for books"
Agent: "Found 1 item: Books - Educational books, $25.99"
```

### Managing Items

```
User: "Update laptop price to 1199.99"
Agent: "Successfully updated laptop with new price $1199.99"

User: "Delete the books item"
Agent: "Successfully deleted item 'Books'"
```

## Testing

Run the test suite:

```bash
pytest tests/ -v
```

Run with coverage:

```bash
pytest tests/ --cov=src --cov-report=html
```

## Troubleshooting

### ChromaDB Initialization Issues

If ChromaDB fails to initialize, ensure you have write permissions in the project directory.

### OpenAI API Errors

- Verify your API key is correct in `.env`
- Check your OpenAI account has available credits
- Ensure you have access to the specified model

### Port Already in Use

If port 8000 is already in use, change it in `.env`:

```env
PORT=8001
```

## Next Steps

1. Explore the API documentation at `/docs`
2. Read the [Architecture Guide](docs/ARCHITECTURE.md)
3. Review the [API Documentation](docs/API.md)
4. Customize the agent prompts in `src/agents/catalog_agent.py`
5. Add more tools for your specific use case

## Production Deployment

For production deployment:

1. Set proper environment variables
2. Use a production WSGI server (gunicorn)
3. Configure authentication
4. Set up rate limiting
5. Use a production database (PostgreSQL)
6. Deploy behind a reverse proxy (nginx)
7. Enable HTTPS

Example with gunicorn:

```bash
gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Support

For issues and questions:
- Open an issue on GitHub
- Check the documentation in `/docs`
- Review example code in `/tests`
