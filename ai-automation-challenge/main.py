from fastapi import FastAPI, HTTPException, Depends
from contextlib import asynccontextmanager
import time
from models import ModerationRequest, ModerationResponse
from moderation_service import ModerationService
import os

# TODO: Implement proper lifespan context manager for service initialization
app = FastAPI(title="Content Moderation API")

# BUG: Service is not initialized properly (no API keys)
# BUG: Service should be dependency-injected, not global
moderation_service = None


@app.post("/moderate", response_model=ModerationResponse)
async def moderate_content(request: ModerationRequest):
    """
    Moderate content for policy violations.

    TODO: Add proper error handling
    TODO: Add request validation
    TODO: Track processing time
    """
    # BUG: No error handling
    # BUG: No timing tracking
    # BUG: Doesn't handle service being None

    result = await moderation_service.moderate_content(request)

    return ModerationResponse(
        video_id=request.video_id,
        moderation=result,
        processing_time_ms=0.0  # BUG: Should track actual time
    )


# TODO: Add health check endpoint
# TODO: Add lifespan event handlers
