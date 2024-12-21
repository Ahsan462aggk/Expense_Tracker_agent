# app/routers/agent_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.agent import AgentQueryRequest, AgentQueryResponse
from app.agents.agent import compiled_graph, current_user_id  # Import current_user_id
import logging
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from app.auth.auth import get_current_user
from app.models.user import User
import contextvars

router = APIRouter(prefix="/agents", tags=["Agents"])

logger = logging.getLogger(__name__)

@router.post("/query", response_model=AgentQueryResponse)
async def query_agent(
    request: AgentQueryRequest,
    current_user: User = Depends(get_current_user),
):
    """
    Endpoint to handle user queries and return agent responses, now with user authentication and automatic inclusion of user ID.

    **Authorization:** Bearer token (JWT) included in the request headers.

    **Endpoint:** POST /agents/query

    **Request Body:**
    {
        "messages": "Your user query here"
    }

    **Response:**
    {
        "response": "Agent's response message"
    }
    """

    # Authenticate the user
    logger.info(f"Authenticated user: {current_user.username}")  # Log username for debugging

    try:
        # Create a thread
        config = {"configurable": {"thread_id": "1"}}

        # Automatically include user ID in HumanMessage
        user_message = request.messages
        human_message = HumanMessage(content=user_message)
        messages = [human_message]

        logger.info(f"Received user message from {current_user.username}: {user_message}")
        logger.info(f"Message structure before invoking the graph: {messages}")

        # Set the user_id in the ContextVar
        token = current_user_id.set(current_user.id)

        try:
            # Invoke the graph and get the response
            response_state = compiled_graph.invoke({"messages": messages}, config)
        finally:
            # Reset the ContextVar to its previous state
            current_user_id.reset(token)

        logger.info(f"Agent response state: {response_state}")

        # Extract messages from the response
        messages = response_state.get("messages", [])

        if not messages:
            logger.warning("No messages returned from the agent.")
            raise ValueError("No messages returned from the agent.")

        # Log all messages for debugging
        logger.debug(f"All messages: {messages}")

        # Find the last AI message
        if isinstance(messages, dict):
            # If messages is a dictionary with a 'content' key
            assistant_message = messages.get("content")
        else:
            # If messages is a list
            assistant_message = next(
                (msg for msg in reversed(messages) if isinstance(msg, AIMessage)),
                None
            )

        if not assistant_message:
            logger.error("No AI message found in the response.")
            raise ValueError("No AI message found in the response.")

        logger.info(f"Assistant message: {assistant_message}")

        # Extract the content of the assistant's message
        response_content = assistant_message.content if hasattr(assistant_message, "content") else assistant_message

        logger.info(f"Response content: {response_content}")

        return {"response": response_content}

    except Exception as e:
        logger.error(f"Error processing agent query: {e}")
        raise HTTPException(status_code=500, detail=str(e))
