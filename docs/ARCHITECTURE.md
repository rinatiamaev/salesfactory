# Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Applications                      │
│  (Web Browser, Mobile App, External Systems, WordPress)          │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                       FastAPI Application                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Request ID Middleware                       │  │
│  │         (Tracking, Logging, CORS)                        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                   │
│  ┌────────────────────┐         ┌────────────────────┐          │
│  │  Chat API          │         │  REST API          │          │
│  │  /api/chat         │         │  /api/catalog/*    │          │
│  │                    │         │                    │          │
│  │  - Conversational  │         │  - CRUD ops        │          │
│  │  - Natural lang.   │         │  - Search          │          │
│  │  - Session mgmt    │         │  - Stats           │          │
│  └─────────┬──────────┘         └─────────┬──────────┘          │
│            │                               │                     │
└────────────┼───────────────────────────────┼─────────────────────┘
             │                               │
             ▼                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Business Logic Layer                        │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              LangChain Agent (OpenAI)                    │  │
│  │                                                            │  │
│  │  ├─ Agent Executor                                        │  │
│  │  ├─ Conversational Memory                                 │  │
│  │  ├─ Tool Selection & Execution                           │  │
│  │  └─ Response Generation                                   │  │
│  └────────────────────┬─────────────────────────────────────┘  │
│                       │                                          │
│  ┌────────────────────▼─────────────────────────────────────┐  │
│  │                   Catalog Tools                          │  │
│  │                                                            │  │
│  │  ├─ create_catalog_item    ├─ search_catalog            │  │
│  │  ├─ list_catalog_items     ├─ get_catalog_statistics    │  │
│  │  ├─ get_catalog_item       └─ ...                        │  │
│  │  ├─ update_catalog_item                                   │  │
│  │  └─ delete_catalog_item                                   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                   │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Data Layer                                 │
│                                                                   │
│  ┌────────────────────┐         ┌────────────────────┐          │
│  │  In-Memory Store   │         │  ChromaDB          │          │
│  │                    │         │  (Vector DB)       │          │
│  │  ├─ Catalog Items  │         │                    │          │
│  │  ├─ Metadata       │         │  ├─ Conversations  │          │
│  │  └─ Quick Access   │         │  ├─ Catalog Index  │          │
│  │                    │         │  ├─ Agent Actions  │          │
│  │                    │         │  └─ Embeddings     │          │
│  └────────────────────┘         └────────────────────┘          │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                   External Services                              │
│                                                                   │
│  ┌────────────────────┐         ┌────────────────────┐          │
│  │  OpenAI API        │         │  WordPress (future)│          │
│  │                    │         │                    │          │
│  │  ├─ GPT-4          │         │  ├─ Webhooks       │          │
│  │  ├─ Embeddings     │         │  ├─ Integration    │          │
│  │  └─ Completions    │         │  └─ Sync           │          │
│  └────────────────────┘         └────────────────────┘          │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. API Layer

**Chat API** (`/api/chat`)
- Natural language interface
- Session management
- Agent orchestration
- Action tracking

**REST API** (`/api/catalog/*`)
- WordPress-compatible endpoints
- Standard CRUD operations
- Semantic search
- Statistics

### 2. Agent Layer

**LangChain Agent**
- OpenAI Function Calling
- Tool selection and execution
- Context-aware responses
- Error handling

**Tools**
- Catalog management functions
- Integrated with vector memory
- Action logging
- Result validation

### 3. Memory Layer

**Vector Memory (ChromaDB)**
- Conversation history
- Agent action log
- Catalog semantic index
- Context retrieval

**In-Memory Storage**
- Fast catalog access
- Runtime state
- Temporary data

### 4. Observability

**Structured Logging**
- JSON format
- Request tracking
- Performance metrics
- Error reporting

**Request ID Tracking**
- End-to-end tracing
- Distributed logging
- Debug support

**Retry Logic**
- Exponential backoff
- Graceful degradation
- Resilience

## Data Flow

### Conversational Flow

```
1. User sends message → Chat API
2. Chat API → LangChain Agent
3. Agent analyzes intent → Selects tools
4. Tools execute operations → Update storage
5. Results stored in vector memory
6. Agent generates response → User
```

### REST API Flow

```
1. Client makes HTTP request → REST API
2. Request validated → Business logic
3. Catalog tools execute → Update storage
4. Results returned → Client
```

## Security Considerations

1. **API Key Management**
   - Environment variables
   - Never commit secrets
   - Rotate keys regularly

2. **Input Validation**
   - Pydantic models
   - Type checking
   - Sanitization

3. **Rate Limiting** (Future)
   - Per-IP limits
   - Per-API-key limits
   - Burst protection

4. **Authentication** (Future)
   - OAuth 2.0
   - JWT tokens
   - API keys

## Scalability

**Current Architecture**
- Single instance
- In-memory storage
- Local ChromaDB

**Future Enhancements**
- PostgreSQL for catalog
- Redis for sessions
- Distributed ChromaDB
- Load balancing
- Caching layer

## Deployment

**Development**
```bash
./run.sh
```

**Production** (Future)
- Docker container
- Kubernetes deployment
- Cloud hosting (AWS, GCP, Azure)
- CI/CD pipeline
