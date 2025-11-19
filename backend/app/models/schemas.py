"""Pydantic models for API requests and responses"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class ChatMessage(BaseModel):
    """Chat message request model"""
    message: str = Field(..., description="User's message")
    session_id: str = Field(default="default", description="Session identifier")
    stream: bool = Field(default=False, description="Enable streaming response")


class ChatResponse(BaseModel):
    """Chat message response model"""
    response: str = Field(..., description="AI response")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Response metadata")
    session_id: str = Field(..., description="Session identifier")


class UploadResponse(BaseModel):
    """File upload response model"""
    success: bool = Field(..., description="Upload success status")
    message: str = Field(..., description="Status message")
    filename: str = Field(default="", description="Uploaded filename")
    stats: Dict[str, Any] = Field(default_factory=dict, description="File statistics")


class HealthResponse(BaseModel):
    """Health check response model"""
    status: str = Field(..., description="Service status")
    timestamp: str = Field(..., description="Current timestamp")
    services: Dict[str, bool] = Field(default_factory=dict, description="Service availability")


class SessionHistoryResponse(BaseModel):
    """Session history response model"""
    session_id: str = Field(..., description="Session identifier")
    messages: List[Dict[str, Any]] = Field(default_factory=list, description="Conversation messages")
    count: int = Field(..., description="Message count")
