"""API routes for chat/conversational interface."""
from fastapi import APIRouter, HTTPException
import uuid

from ..models.schemas import ChatRequest, ChatResponse
from ..agents.catalog_agent import get_agent
from ..logger import get_logger, get_request_id

logger = get_logger(__name__)

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Chat endpoint for conversational interaction with the catalog agent.
    
    Example:
        User: "Add new row 'Books'"
        Agent: Thinks, calls create_row, confirms result
    """
    try:
        # Generate session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())
        
        # Get the agent
        agent = get_agent()
        
        # Process the message
        result = await agent.process_message(request.message, session_id)
        
        if not result.get("success"):
            logger.warning(f"Agent processing failed: {result.get('error')}")
        
        # Get current request ID
        request_id = get_request_id()
        
        return ChatResponse(
            response=result.get("response"),
            session_id=session_id,
            request_id=request_id,
            actions=result.get("actions")
        )
        
    except Exception as e:
        logger.error(f"Chat endpoint error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
