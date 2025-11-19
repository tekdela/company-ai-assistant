"""Chat API routes"""
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from ..models.schemas import ChatMessage, ChatResponse
from ..services.ai_service import AIService
from typing import AsyncIterator
import json

router = APIRouter(prefix="/api/chat", tags=["chat"])


def get_ai_service() -> AIService:
    """Dependency to get AI service instance"""
    from ..main import ai_service
    return ai_service


@router.post("/message", response_model=ChatResponse)
async def send_message(
    chat_msg: ChatMessage,
    ai_service: AIService = Depends(get_ai_service)
):
    """Send a chat message and get AI response
    
    Args:
        chat_msg: Chat message request
        ai_service: AI service dependency
        
    Returns:
        Chat response with AI-generated message
    """
    try:
        result = await ai_service.process_message(
            message=chat_msg.message,
            session_id=chat_msg.session_id,
            stream=chat_msg.stream
        )
        
        return ChatResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")


@router.post("/stream")
async def stream_message(
    chat_msg: ChatMessage,
    ai_service: AIService = Depends(get_ai_service)
):
    """Stream chat message response (SSE)
    
    Args:
        chat_msg: Chat message request
        ai_service: AI service dependency
        
    Returns:
        Streaming response
    """
    async def generate() -> AsyncIterator[str]:
        """Generate streaming response"""
        try:
            # For now, return full response as single chunk
            # Future: implement true streaming from Gemini
            result = await ai_service.process_message(
                message=chat_msg.message,
                session_id=chat_msg.session_id,
                stream=False
            )
            
            # Send as SSE format
            yield f"data: {json.dumps(result)}\n\n"
            
        except Exception as e:
            error_msg = {"error": str(e)}
            yield f"data: {json.dumps(error_msg)}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


@router.get("/history/{session_id}")
async def get_history(
    session_id: str,
    ai_service: AIService = Depends(get_ai_service)
):
    """Get conversation history for a session
    
    Args:
        session_id: Session identifier
        ai_service: AI service dependency
        
    Returns:
        Session history
    """
    try:
        messages = ai_service.get_session_history(session_id)
        
        return {
            "session_id": session_id,
            "messages": messages,
            "count": len(messages)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving history: {str(e)}")


@router.delete("/history/{session_id}")
async def clear_history(
    session_id: str,
    ai_service: AIService = Depends(get_ai_service)
):
    """Clear conversation history for a session
    
    Args:
        session_id: Session identifier
        ai_service: AI service dependency
        
    Returns:
        Success status
    """
    try:
        success = ai_service.clear_session(session_id)
        
        return {
            "success": success,
            "message": f"Session {session_id} cleared" if success else "Session not found"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing history: {str(e)}")
