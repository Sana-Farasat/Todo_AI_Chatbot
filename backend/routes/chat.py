# """
# Chat endpoint for AI-powered task management.
# Handles natural language conversations with Gemini AI agent.
# """
# from fastapi import APIRouter, Depends, HTTPException, Body
# from pydantic import BaseModel, Field, validator
# from sqlmodel import SQLModel, select
# from sqlmodel.ext.asyncio.session import AsyncSession
# from db import get_session
# from middleware.jwt import get_current_user
# from models import Conversation, Message
# from services.mcp_tools import (
#     add_task,
#     list_tasks,
#     complete_task,
#     delete_task,
#     update_task
# )
# from services.gemini_agent import get_gemini_agent
# from datetime import datetime
# from sqlalchemy import update as sql_update
# from typing import Optional, List, Dict, Any

# #router = APIRouter(prefix="/api/{user_id}/chat", tags=["chat"])
# router = APIRouter(prefix="/api/chat", tags=["chat"])

# # Request/Response Models
# class ChatRequest(BaseModel):
#     conversation_id: Optional[int] = None
#     message: str = Field(..., min_length=1, max_length=500)

#     @validator('message')
#     def message_not_empty(cls, v):
#         if not v.strip():
#             raise ValueError('Message cannot be empty or whitespace')
#         return v.strip()


# class ToolCallResult(BaseModel):
#     tool: str
#     parameters: Dict[str, Any]
#     result: Dict[str, Any]


# class ChatResponse(BaseModel):
#     conversation_id: int
#     response: str
#     tool_calls: List[ToolCallResult] = []
#     message_id: Optional[int] = None


# class ConversationHistory(BaseModel):
#     id: int
#     role: str
#     content: str
#     created_at: datetime


# # Helper functions
# async def execute_mcp_tool(
#     tool_name: str,
#     parameters: Dict[str, Any],
#     user_id: str,
#     session: AsyncSession
# ) -> Dict[str, Any]:
#     """
#     Execute an MCP tool based on tool name and parameters.
    
#     Args:
#         tool_name: Name of the tool to execute
#         parameters: Tool parameters from Gemini
#         user_id: User identifier
#         session: Database session
    
#     Returns:
#         Tool execution result as dict
#     """
#     try:
#         if tool_name == "add_task":
#             result = await add_task(
#                 session=session,
#                 user_id=user_id,
#                 title=parameters.get("title", ""),
#                 description=parameters.get("description")
#             )
#         elif tool_name == "list_tasks":
#             result = await list_tasks(
#                 session=session,
#                 user_id=user_id,
#                 status=parameters.get("status", "all")
#             )
#         elif tool_name == "complete_task":
#             result = await complete_task(
#                 session=session,
#                 user_id=user_id,
#                 task_id=parameters.get("task_id", 0)
#             )
#         elif tool_name == "delete_task":
#             result = await delete_task(
#                 session=session,
#                 user_id=user_id,
#                 task_id=parameters.get("task_id", 0)
#             )
#         elif tool_name == "update_task":
#             result = await update_task(
#                 session=session,
#                 user_id=user_id,
#                 task_id=parameters.get("task_id", 0),
#                 title=parameters.get("title"),
#                 description=parameters.get("description")
#             )
#         else:
#             return {
#                 "success": False,
#                 "error": f"Unknown tool: {tool_name}"
#             }
        
#         # Convert SQLModel result to dict
#         return result.dict()
    
#     except Exception as e:
#         return {
#             "success": False,
#             "error": str(e)
#         }


# async def get_conversation_history(
#     conversation_id: int,
#     user_id: str,
#     session: AsyncSession,
#     limit: int = 20
# ) -> List[Dict[str, str]]:
#     """
#     Fetch conversation history from database.
    
#     Args:
#         conversation_id: Conversation ID
#         user_id: User identifier
#         session: Database session
#         limit: Max messages to return (default 20)
    
#     Returns:
#         List of message dicts with role and content
#     """
#     stmt = (
#         select(Message)
#         .where(
#             Message.conversation_id == conversation_id,
#             Message.user_id == user_id
#         )
#         .order_by(Message.created_at.asc())
#         .limit(limit)
#     )
#     result = await session.execute(stmt)
#     messages = result.scalars().all()
    
#     return [
#         {"role": msg.role, "content": msg.content}
#         for msg in messages
#     ]


# async def create_or_get_conversation(
#     conversation_id: Optional[int],
#     user_id: str,
#     session: AsyncSession
# ) -> Conversation:
#     """
#     Create new conversation or get existing one.
    
#     Args:
#         conversation_id: Existing conversation ID or None
#         user_id: User identifier
#         session: Database session
    
#     Returns:
#         Conversation object
#     """
#     if conversation_id:
#         # Get existing conversation
#         stmt = select(Conversation).where(
#             Conversation.id == conversation_id,
#             Conversation.user_id == user_id
#         )
#         result = await session.execute(stmt)
#         conversation = result.scalar_one_or_none()
        
#         if not conversation:
#             raise HTTPException(
#                 status_code=404,
#                 detail="Conversation not found or not authorized"
#             )
#     else:
#         # Create new conversation
#         conversation = Conversation(user_id=user_id)
#         session.add(conversation)
#         await session.commit()
#         await session.refresh(conversation)
    
#     return conversation


# async def store_message(
#     conversation_id: int,
#     user_id: str,
#     role: str,
#     content: str,
#     session: AsyncSession
# ) -> Message:
#     """
#     Store a message in the database.
    
#     Args:
#         conversation_id: Conversation ID
#         user_id: User identifier
#         role: "user" or "assistant"
#         content: Message content
#         session: Database session
    
#     Returns:
#         Created Message object
#     """
#     message = Message(
#         conversation_id=conversation_id,
#         user_id=user_id,
#         role=role,
#         content=content
#     )
#     session.add(message)
    
#     # Update conversation timestamp
#     stmt = sql_update(Conversation).where(
#         Conversation.id == conversation_id
#     ).values(updated_at=datetime.utcnow())
#     await session.execute(stmt)
    
#     await session.commit()
#     await session.refresh(message)
    
#     return message


# # Chat endpoint
# # @router.post("/", response_model=ChatResponse)
# @router.post("", response_model=ChatResponse)
# async def chat(
#     #user_id: str,
#     request: ChatRequest,
#     current_user: str = Depends(get_current_user),
#     session: AsyncSession = Depends(get_session)
# ):
#     """
#     Send a message to the AI chatbot and receive a response.
    
#     The chatbot can:
#     - Add tasks to your todo list
#     - List tasks (all, pending, completed)
#     - Mark tasks as complete
#     - Delete tasks
#     - Update task titles or descriptions
    
#     Conversations persist across server restarts.
#     """
#     # Verify authorization
#     # if current_user != user_id:
#     #     raise HTTPException(status_code=403, detail="Not authorized")

#     user_id = current_user 

#     try:
#         # Get or create conversation
#         conversation = await create_or_get_conversation(
#             conversation_id=request.conversation_id,
#             user_id=user_id,
#             session=session
#         )
        
#         # Store user message
#         user_message = await store_message(
#             conversation_id=conversation.id,
#             user_id=user_id,
#             role="user",
#             content=request.message,
#             session=session
#         )
        
#         # Get conversation history
#         history = await get_conversation_history(
#             conversation_id=conversation.id,
#             user_id=user_id,
#             session=session
#         )
        
#         # Get Gemini agent
#         agent = get_gemini_agent()
        
#         # Process message with AI agent
#         ai_result = await agent.process_message(
#             user_id=user_id,
#             message=request.message,
#             conversation_history=history,
#             execute_tool_callback=lambda tool, params, uid: execute_mcp_tool(
#                 tool, params, uid, session
#             )
#         )
        
#         # Format response
#         if ai_result.get("tool_calls"):
#             # Use formatted tool response
#             response_text = agent.format_tool_response(ai_result["tool_calls"])
#         else:
#             response_text = ai_result.get("response", "I'm here to help!")
        
#         # Store assistant response
#         assistant_message = await store_message(
#             conversation_id=conversation.id,
#             user_id=user_id,
#             role="assistant",
#             content=response_text,
#             session=session
#         )
        
#         # Build tool calls for response
#         tool_calls = [
#             ToolCallResult(
#                 tool=call["tool"],
#                 parameters=call["parameters"],
#                 result=call["result"]
#             )
#             for call in ai_result.get("tool_calls", [])
#         ]
        
#         return ChatResponse(
#             conversation_id=conversation.id,
#             response=response_text,
#             tool_calls=tool_calls,
#             message_id=assistant_message.id
#         )
    
#     except HTTPException:
#         raise
#     except Exception as e:
#         import traceback
#         traceback.print_exc()
#         raise HTTPException(
#             status_code=500,
#             detail=f"Chat processing failed: {str(e)}"
#         )


# @router.get("/history", response_model=List[ConversationHistory])
# async def get_chat_history(
#     #user_id: str,
#     conversation_id: Optional[int] = None,
#     current_user: str = Depends(get_current_user),
#     session: AsyncSession = Depends(get_session)
# ):
#     """
#     Get chat conversation history.
    
#     If conversation_id is provided, returns messages from that conversation.
#     Otherwise, returns list of user's conversations.
#     """
#     # if current_user != user_id:
#     #     raise HTTPException(status_code=403, detail="Not authorized")
    
#     user_id = current_user

#     if conversation_id:
#         # Get messages from specific conversation
#         history = await get_conversation_history(
#             conversation_id=conversation_id,
#             user_id=user_id,
#             session=session,
#             limit=100
#         )
#         return [
#             ConversationHistory(
#                 id=i,
#                 role=msg["role"],
#                 content=msg["content"],
#                 created_at=datetime.utcnow()
#             )
#             for i, msg in enumerate(history)
#         ]
#     else:
#         # Get list of conversations
#         stmt = (
#             select(Conversation)
#             .where(Conversation.user_id == user_id)
#             .order_by(Conversation.updated_at.desc())
#             .limit(50)
#         )
#         result = await session.execute(stmt)
#         conversations = result.scalars().all()
        
#         return [
#             ConversationHistory(
#                 id=conv.id,
#                 role="system",
#                 content=f"Conversation started at {conv.created_at}",
#                 created_at=conv.created_at
#             )
#             for conv in conversations
#         ]


# @router.delete("/conversation/{conversation_id}")
# async def delete_conversation(
#     #user_id: str,
#     conversation_id: int,
#     current_user: str = Depends(get_current_user),
#     session: AsyncSession = Depends(get_session)
# ):
#     """Delete a conversation and all its messages."""
#     # if current_user != user_id:
#     #     raise HTTPException(status_code=403, detail="Not authorized")
#     user_id = current_user

#     stmt = select(Conversation).where(
#         Conversation.id == conversation_id,
#         Conversation.user_id == user_id
#     )
#     result = await session.execute(stmt)
#     conversation = result.scalar_one_or_none()
    
#     if not conversation:
#         raise HTTPException(status_code=404, detail="Conversation not found")
    
#     await session.delete(conversation)
#     await session.commit()
    
#     return {"message": "Conversation deleted"}


##################################
############################


"""
Chat endpoint for AI-powered task management.
Handles natural language conversations with Gemini AI agent.
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, validator
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from db import get_session
from middleware.jwt import get_current_user
from models import Conversation, Message
from services.mcp_tools import (
    add_task,
    list_tasks,
    complete_task,
    delete_task,
    update_task
)
from services.gemini_agent import get_gemini_agent
from datetime import datetime
from sqlalchemy import update as sql_update
from typing import Optional, List, Dict, Any

router = APIRouter(prefix="/api/chat", tags=["chat"])


# -----------------------------
# Request / Response Models
# -----------------------------

class ChatRequest(BaseModel):
    conversation_id: Optional[int] = None
    message: str = Field(..., min_length=1, max_length=500)

    @validator("message")
    def message_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Message cannot be empty")
        return v.strip()


class ToolCallResult(BaseModel):
    tool: str
    parameters: Dict[str, Any]
    result: Dict[str, Any]


class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: List[ToolCallResult] = []
    message_id: Optional[int] = None


class ConversationHistory(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime


# -----------------------------
# MCP TOOL EXECUTION
# -----------------------------

async def execute_mcp_tool(
    tool_name: str,
    parameters: Dict[str, Any],
    user_id: str,
    session: AsyncSession
) -> Dict[str, Any]:

    try:
        if tool_name == "add_task":
            result = await add_task(
                session=session,
                user_id=user_id,
                title=parameters.get("title", ""),
                description=parameters.get("description")
            )

        elif tool_name == "list_tasks":
            result = await list_tasks(
                session=session,
                user_id=user_id,
                status=parameters.get("status", "all")
            )

        elif tool_name == "complete_task":
            result = await complete_task(
                session=session,
                user_id=user_id,
                task_id=parameters.get("task_id", 0)
            )

        elif tool_name == "delete_task":
            result = await delete_task(
                session=session,
                user_id=user_id,
                task_id=parameters.get("task_id", 0)
            )

        elif tool_name == "update_task":
            result = await update_task(
                session=session,
                user_id=user_id,
                task_id=parameters.get("task_id", 0),
                title=parameters.get("title"),
                description=parameters.get("description")
            )

        else:
            return {"success": False, "error": f"Unknown tool: {tool_name}"}

        return result.dict()

    except Exception as e:
        return {"success": False, "error": str(e)}


# -----------------------------
# CONVERSATION HISTORY
# -----------------------------

async def get_conversation_history(
    conversation_id: int,
    user_id: str,
    session: AsyncSession,
    limit: int = 20
) -> List[Dict[str, str]]:

    stmt = (
        select(Message)
        .where(
            Message.conversation_id == conversation_id,
            Message.user_id == user_id
        )
        .order_by(Message.created_at.asc())
        .limit(limit)
    )

    result = await session.execute(stmt)
    messages = result.scalars().all()

    return [{"role": msg.role, "content": msg.content} for msg in messages]


# -----------------------------
# CREATE OR GET CONVERSATION
# -----------------------------

async def create_or_get_conversation(
    conversation_id: Optional[int],
    user_id: str,
    session: AsyncSession
) -> int:

    if conversation_id:
        stmt = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )

        result = await session.execute(stmt)
        conversation = result.scalar_one_or_none()

        if not conversation:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found"
            )

        return conversation.id

    else:
        conversation = Conversation(user_id=user_id)

        session.add(conversation)
        await session.commit()
        await session.refresh(conversation)

        return conversation.id


# -----------------------------
# STORE MESSAGE
# -----------------------------

async def store_message(
    conversation_id: int,
    user_id: str,
    role: str,
    content: str,
    session: AsyncSession
) -> Message:

    message = Message(
        conversation_id=conversation_id,
        user_id=user_id,
        role=role,
        content=content
    )

    session.add(message)

    stmt = sql_update(Conversation).where(
        Conversation.id == conversation_id
    ).values(updated_at=datetime.utcnow())

    await session.execute(stmt)

    await session.commit()
    await session.refresh(message)

    return message


# -----------------------------
# CHAT ENDPOINT
# -----------------------------

@router.post("", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):

    user_id = current_user

    try:

        # create/get conversation
        conversation_id = await create_or_get_conversation(
            conversation_id=request.conversation_id,
            user_id=user_id,
            session=session
        )

        # store user message
        await store_message(
            conversation_id=conversation_id,
            user_id=user_id,
            role="user",
            content=request.message,
            session=session
        )

        # fetch history
        history = await get_conversation_history(
            conversation_id=conversation_id,
            user_id=user_id,
            session=session
        )

        # Gemini agent
        agent = get_gemini_agent()

        ai_result = await agent.process_message(
            user_id=user_id,
            message=request.message,
            conversation_history=history,
            execute_tool_callback=lambda tool, params, uid: execute_mcp_tool(
                tool, params, uid, session
            )
        )

        # response text
        if ai_result.get("tool_calls"):
            response_text = agent.format_tool_response(ai_result["tool_calls"])
        else:
            response_text = ai_result.get("response", "I'm here to help!")

        # store assistant message
        assistant_message = await store_message(
            conversation_id=conversation_id,
            user_id=user_id,
            role="assistant",
            content=response_text,
            session=session
        )

        tool_calls = [
            ToolCallResult(
                tool=call["tool"],
                parameters=call["parameters"],
                result=call["result"]
            )
            for call in ai_result.get("tool_calls", [])
        ]

        return ChatResponse(
            conversation_id=conversation_id,
            response=response_text,
            tool_calls=tool_calls,
            message_id=assistant_message.id
        )

    except HTTPException:
        raise

    except Exception as e:
        import traceback
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=f"Chat processing failed: {str(e)}"
        )


# -----------------------------
# GET CHAT HISTORY
# -----------------------------

@router.get("/history", response_model=List[ConversationHistory])
async def get_chat_history(
    conversation_id: Optional[int] = None,
    current_user: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):

    user_id = current_user

    if conversation_id:

        history = await get_conversation_history(
            conversation_id=conversation_id,
            user_id=user_id,
            session=session,
            limit=100
        )

        return [
            ConversationHistory(
                id=i,
                role=msg["role"],
                content=msg["content"],
                created_at=datetime.utcnow()
            )
            for i, msg in enumerate(history)
        ]

    else:

        stmt = (
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
            .limit(50)
        )

        result = await session.execute(stmt)
        conversations = result.scalars().all()

        return [
            ConversationHistory(
                id=conv.id,
                role="system",
                content=f"Conversation started at {conv.created_at}",
                created_at=conv.created_at
            )
            for conv in conversations
        ]


# -----------------------------
# DELETE CONVERSATION
# -----------------------------

@router.delete("/conversation/{conversation_id}")
async def delete_conversation(
    conversation_id: int,
    current_user: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):

    user_id = current_user

    stmt = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id
    )

    result = await session.execute(stmt)
    conversation = result.scalar_one_or_none()

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    await session.delete(conversation)
    await session.commit()

    return {"message": "Conversation deleted"}
