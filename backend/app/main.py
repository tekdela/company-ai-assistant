"""Main FastAPI Application"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from .services.gemini_service import GeminiService
from .services.knowledge_service import KnowledgeService
from .services.time_service import TimeService
from .services.translation_service import TranslationService
from .services.ai_service import AIService
from .routes import chat, upload, health

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Company AI Assistant API",
    description="AI-powered assistant with Google Gemini integration",
    version="1.0.0"
)

# CORS configuration
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    print("WARNING: GEMINI_API_KEY not set. AI features will not work properly.")
    gemini_api_key = "dummy_key"

gemini_service = GeminiService(api_key=gemini_api_key)
knowledge_service = KnowledgeService()
time_service = TimeService()
translation_service = TranslationService()

ai_service = AIService(
    gemini_service=gemini_service,
    knowledge_service=knowledge_service,
    time_service=time_service,
    translation_service=translation_service
)

# Include routers
app.include_router(health.router)
app.include_router(chat.router)
app.include_router(upload.router)


@app.on_event("startup")
async def startup_event():
    """Application startup event"""
    print("🚀 Company AI Assistant API starting...")
    print(f"📝 Gemini API Key configured: {bool(gemini_api_key and gemini_api_key != 'dummy_key')}")
    print(f"🌐 CORS Origins: {cors_origins}")
    print("✅ API ready at http://localhost:8000")
    print("📚 API Documentation at http://localhost:8000/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event"""
    print("👋 Company AI Assistant API shutting down...")


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("BACKEND_HOST", "0.0.0.0")
    port = int(os.getenv("BACKEND_PORT", "8000"))
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=True
    )
