from fastapi import FastAPI, HTTPException, Depends
from contextlib import asynccontextmanager
import time
from models import ModerationRequest, ModerationResponse
from moderation_service import ModerationService
import os

# Global service instance
moderation_service = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize service on startup, cleanup on shutdown"""
    global moderation_service
    
    # Load API keys from environment or use defaults for mock clients
    openai_key = os.getenv("OPENAI_API_KEY", "mock-openai-key")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY", "mock-anthropic-key")
    
    # Initialize the moderation service
    moderation_service = ModerationService(
        openai_key=openai_key,
        anthropic_key=anthropic_key
    )
    
    print("✅ Moderation service initialized")
    
    yield
    
    # Cleanup (if needed)
    print("🔄 Shutting down moderation service")


app = FastAPI(
    title="Content Moderation API",
    lifespan=lifespan
)


def get_moderation_service() -> ModerationService:
    """Dependency injection for moderation service"""
    if moderation_service is None:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return moderation_service


@app.post("/moderate", response_model=ModerationResponse)
async def moderate_content(
    request: ModerationRequest,
    service: ModerationService = Depends(get_moderation_service)
):
    """
    Moderate content for policy violations.
    Returns structured moderation result with timing information.
    """
    # Track processing time
    start_time = time.time()
    
    try:
        # Perform moderation
        result = await service.moderate_content(request)
        
        # Calculate processing time in milliseconds
        processing_time_ms = (time.time() - start_time) * 1000
        
        return ModerationResponse(
            video_id=request.video_id,
            moderation=result,
            processing_time_ms=round(processing_time_ms, 2)
        )
    
    except Exception as e:
        # Handle errors gracefully
        processing_time_ms = (time.time() - start_time) * 1000
        raise HTTPException(
            status_code=500,
            detail=f"Moderation failed: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "content-moderation",
        "providers": ["openai", "anthropic"]
    }
