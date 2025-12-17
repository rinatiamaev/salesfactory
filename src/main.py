"""Main FastAPI application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from datetime import datetime

from .config import settings
from .logger import setup_logging, get_logger
from .middleware.request_id import RequestIdMiddleware
from .api import catalog, chat
from .models.schemas import HealthResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    logger = get_logger(__name__)
    logger.info("Starting AI Catalog Service")
    
    # Initialize components on startup
    try:
        from .memory.vector_memory import get_memory
        from .agents.catalog_agent import get_agent
        
        # Initialize memory
        memory = get_memory()
        logger.info("Vector memory initialized")
        
        # Initialize agent
        agent = get_agent()
        logger.info("Catalog agent initialized")
        
    except Exception as e:
        logger.error(f"Failed to initialize components: {e}", exc_info=True)
        raise
    
    yield
    
    logger.info("Shutting down AI Catalog Service")


# Setup logging
setup_logging(settings.log_level)

# Create FastAPI app
app = FastAPI(
    title="AI Catalog Service",
    description="AI-powered e-commerce catalog management with conversational interface",
    version="1.0.0",
    lifespan=lifespan
)

# Add middleware
app.add_middleware(RequestIdMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(catalog.router)
app.include_router(chat.router)


@app.get("/", response_model=dict)
async def root():
    """Root endpoint."""
    return {
        "name": "AI Catalog Service",
        "version": "1.0.0",
        "description": "AI-powered e-commerce catalog management",
        "endpoints": {
            "health": "/health",
            "chat": "/api/chat",
            "catalog": "/api/catalog",
            "docs": "/docs"
        }
    }


@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=datetime.utcnow()
    )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
        log_level=settings.log_level.lower()
    )
