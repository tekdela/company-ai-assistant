"""Health check and system routes"""
from fastapi import APIRouter
from ..models.schemas import HealthResponse
from datetime import datetime

router = APIRouter(prefix="/api", tags=["system"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint
    
    Returns:
        System health status
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        services={
            "api": True,
            "gemini": True,
            "knowledge_base": True
        }
    )


@router.get("/")
async def root():
    """Root endpoint
    
    Returns:
        API information
    """
    return {
        "name": "Company AI Assistant API",
        "version": "1.0.0",
        "description": "AI-powered assistant with Gemini integration",
        "endpoints": {
            "chat": "/api/chat/message",
            "upload": "/api/upload/csv",
            "health": "/api/health",
            "docs": "/docs"
        }
    }
