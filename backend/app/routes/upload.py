"""Upload API routes for file handling"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from ..models.schemas import UploadResponse
from ..services.knowledge_service import KnowledgeService

router = APIRouter(prefix="/api/upload", tags=["upload"])


def get_knowledge_service() -> KnowledgeService:
    """Dependency to get knowledge service instance"""
    from ..main import knowledge_service
    return knowledge_service


@router.post("/csv", response_model=UploadResponse)
async def upload_csv(
    file: UploadFile = File(...),
    knowledge_service: KnowledgeService = Depends(get_knowledge_service)
):
    """Upload CSV file to knowledge base
    
    Args:
        file: Uploaded CSV file
        knowledge_service: Knowledge service dependency
        
    Returns:
        Upload response with status and statistics
    """
    try:
        # Validate file type
        if not file.filename.endswith('.csv'):
            raise HTTPException(
                status_code=400,
                detail="Only CSV files are supported"
            )
        
        # Read file content
        content = await file.read()
        
        # Load into knowledge base
        success = await knowledge_service.load_csv(content, file.filename)
        
        if not success:
            raise HTTPException(
                status_code=500,
                detail="Failed to load CSV file"
            )
        
        # Get statistics
        stats = knowledge_service.get_stats()
        
        return UploadResponse(
            success=True,
            message=f"Successfully uploaded {file.filename}",
            filename=file.filename,
            stats=stats
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error uploading file: {str(e)}"
        )


@router.get("/stats")
async def get_knowledge_stats(
    knowledge_service: KnowledgeService = Depends(get_knowledge_service)
):
    """Get knowledge base statistics
    
    Args:
        knowledge_service: Knowledge service dependency
        
    Returns:
        Knowledge base statistics
    """
    try:
        stats = knowledge_service.get_stats()
        return stats
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving stats: {str(e)}"
        )
