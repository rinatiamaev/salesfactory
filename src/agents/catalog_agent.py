"""LangChain agent for catalog management."""
from typing import List, Dict, Any, Optional
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from ..config import settings
from ..tools.catalog_tools import (
    create_row, list_rows, get_row, update_row, delete_row, search_rows, get_catalog_stats
)
from ..memory.vector_memory import get_memory
from ..logger import get_logger

logger = get_logger(__name__)


class CatalogAgent:
    """Agent for managing e-commerce catalog with conversational AI."""
    
    def __init__(self):
        """Initialize the catalog agent."""
        self.llm = ChatOpenAI(
            model=settings.openai_model,
            temperature=0.7,
            openai_api_key=settings.openai_api_key
        )
        
        self.tools = self._create_tools()
        self.agent = self._create_agent()
        self.memory = get_memory()
        
        logger.info("CatalogAgent initialized successfully")
    
    def _create_tools(self) -> List[Tool]:
        """Create LangChain tools from catalog functions."""
        return [
            Tool(
                name="create_catalog_item",
                func=lambda x: create_row(**self._parse_tool_input(x)),
                description=(
                    "Create a new catalog item/row. "
                    "Input should be a JSON-like string with 'name' (required), "
                    "'description' (optional), 'price' (optional), and any additional metadata. "
                    "Example: {\"name\": \"Books\", \"description\": \"Collection of books\", \"price\": 15.99}"
                )
            ),
            Tool(
                name="list_catalog_items",
                func=lambda x: list_rows(limit=int(x) if x.isdigit() else 10),
                description=(
                    "List all catalog items. "
                    "Input should be the maximum number of items to return (default: 10). "
                    "Example: 20"
                )
            ),
            Tool(
                name="get_catalog_item",
                func=get_row,
                description=(
                    "Get a specific catalog item by ID. "
                    "Input should be the item ID. "
                    "Example: abc123-def456"
                )
            ),
            Tool(
                name="update_catalog_item",
                func=lambda x: update_row(**self._parse_tool_input(x)),
                description=(
                    "Update an existing catalog item. "
                    "Input should be a JSON-like string with 'item_id' (required) and fields to update. "
                    "Example: {\"item_id\": \"abc123\", \"name\": \"Updated Books\", \"price\": 19.99}"
                )
            ),
            Tool(
                name="delete_catalog_item",
                func=delete_row,
                description=(
                    "Delete a catalog item by ID. "
                    "Input should be the item ID. "
                    "Example: abc123-def456"
                )
            ),
            Tool(
                name="search_catalog",
                func=lambda x: search_rows(query=x, limit=5),
                description=(
                    "Search catalog items using semantic search. "
                    "Input should be the search query. "
                    "Example: books about science"
                )
            ),
            Tool(
                name="get_catalog_statistics",
                func=lambda x: get_catalog_stats(),
                description=(
                    "Get catalog statistics including total items, items with/without prices. "
                    "No input required."
                )
            ),
        ]
    
    def _parse_tool_input(self, input_str: str) -> Dict[str, Any]:
        """Parse tool input string to dictionary."""
        import json
        try:
            # Try to parse as JSON
            return json.loads(input_str)
        except json.JSONDecodeError:
            # If not valid JSON, try to parse key=value format
            params = {}
            for part in input_str.split(','):
                if '=' in part:
                    key, value = part.split('=', 1)
                    params[key.strip()] = value.strip()
            return params
    
    def _create_agent(self) -> AgentExecutor:
        """Create the LangChain agent."""
        
        system_message = """You are an intelligent assistant for managing an e-commerce catalog.
        
Your capabilities:
- Create new catalog items with name, description, price, and metadata
- List and search existing catalog items
- Update and delete catalog items
- Provide catalog statistics

When a user asks to add, create, or insert an item:
1. Think about what information is needed
2. Use the appropriate tool to create the item
3. Confirm the result to the user in a friendly way

Always be helpful, concise, and confirm actions you take.
When creating items, if the user doesn't provide a price or description, you can create the item without them.
"""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_message),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        agent = create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
        
        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            return_intermediate_steps=True,
            max_iterations=5,
            handle_parsing_errors=True
        )
    
    def _get_chat_history(self, session_id: str) -> List:
        """Get chat history for a session."""
        history = self.memory.get_conversation_history(session_id, limit=10)
        
        messages = []
        for msg in history:
            if msg['role'] == 'user':
                messages.append(HumanMessage(content=msg['content']))
            elif msg['role'] == 'assistant':
                messages.append(AIMessage(content=msg['content']))
        
        return messages
    
    async def process_message(self, message: str, session_id: str) -> Dict[str, Any]:
        """
        Process a user message and return agent response.
        
        Args:
            message: User message
            session_id: Session ID for conversation continuity
        
        Returns:
            Dict with response and actions
        """
        try:
            logger.info(f"Processing message for session {session_id}")
            
            # Store user message in memory
            self.memory.add_conversation(session_id, "user", message)
            
            # Get chat history
            chat_history = self._get_chat_history(session_id)
            
            # Run the agent
            result = await self.agent.ainvoke({
                "input": message,
                "chat_history": chat_history
            })
            
            response = result.get("output", "I'm sorry, I couldn't process that request.")
            intermediate_steps = result.get("intermediate_steps", [])
            
            # Store assistant response in memory
            self.memory.add_conversation(session_id, "assistant", response)
            
            # Extract actions from intermediate steps
            actions = []
            for step in intermediate_steps:
                if len(step) >= 2:
                    action, observation = step[0], step[1]
                    actions.append({
                        "tool": action.tool,
                        "input": str(action.tool_input),
                        "output": str(observation)
                    })
                    
                    # Record action in memory
                    self.memory.add_action(
                        session_id=session_id,
                        action=action.tool,
                        parameters={"input": str(action.tool_input)},
                        result=str(observation)
                    )
            
            logger.info(f"Successfully processed message, performed {len(actions)} actions")
            
            return {
                "response": response,
                "actions": actions,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Failed to process message: {e}", exc_info=True)
            return {
                "response": "I encountered an error processing your request. Please try again.",
                "actions": [],
                "success": False,
                "error": str(e)
            }


# Singleton instance
_agent_instance = None


def get_agent() -> CatalogAgent:
    """Get or create the singleton CatalogAgent instance."""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = CatalogAgent()
    return _agent_instance
