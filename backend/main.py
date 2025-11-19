"""
FastAPI Backend for Vietnamese AI Assistant
"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import shutil
import os
from datetime import datetime
import pytz

from services.ai_service import ai_service
from services.knowledge_service import knowledge_service
from services.time_service import time_service

# Create FastAPI app
app = FastAPI(
    title="Vietnamese AI Assistant API",
    description="Trợ lý AI nội bộ hỗ trợ công việc cho công ty",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    intent: str
    timestamp: str

class TimeResponse(BaseModel):
    time: str
    date: str
    weekday: str
    timezone: str
    flag: str

# Create upload directory
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
async def root():
    """API status endpoint"""
    vn_tz = pytz.timezone("Asia/Ho_Chi_Minh")
    current_time = datetime.now(vn_tz).strftime("%Y-%m-%d %H:%M:%S")
    
    return {
        "status": "online",
        "service": "Vietnamese AI Assistant API",
        "version": "1.0.0",
        "current_time_vn": current_time,
        "knowledge_records": knowledge_service.get_all_count()
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint - handles all user messages
    """
    try:
        # Process message through AI service
        result = ai_service.process_message(request.message)
        
        # Add timestamp
        vn_tz = pytz.timezone("Asia/Ho_Chi_Minh")
        timestamp = datetime.now(vn_tz).strftime("%H:%M:%S")
        
        return ChatResponse(
            response=result["response"],
            intent=result["intent"],
            timestamp=timestamp
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")


@app.post("/api/upload-knowledge")
async def upload_knowledge(file: UploadFile = File(...)):
    """
    Upload CSV/TXT files for knowledge base
    """
    try:
        # Validate file type
        if not file.filename.endswith(('.csv', '.txt')):
            raise HTTPException(
                status_code=400, 
                detail="Chỉ hỗ trợ file .csv và .txt"
            )
        
        # Save uploaded file
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process file
        result = knowledge_service.upload_file(file_path, file.filename)
        
        # Clean up
        os.remove(file_path)
        
        if result["success"]:
            return {
                "success": True,
                "message": result["message"],
                "records_count": result["records_count"],
                "total_records": knowledge_service.get_all_count()
            }
        else:
            raise HTTPException(status_code=500, detail=result["message"])
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi upload file: {str(e)}")


@app.get("/api/time", response_model=TimeResponse)
async def get_time(timezone: Optional[str] = "vietnam"):
    """
    Get current time for specified timezone
    """
    try:
        time_info = time_service.get_time(timezone)
        return TimeResponse(**time_info)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting time: {str(e)}")


@app.get("/api/knowledge/count")
async def get_knowledge_count():
    """Get total number of records in knowledge base"""
    return {
        "count": knowledge_service.get_all_count()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
