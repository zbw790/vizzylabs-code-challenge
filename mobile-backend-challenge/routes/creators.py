from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas import CreatorResponse, CreatorFeedResponse
from services.creator_service import CreatorService

router = APIRouter(prefix="/creators", tags=["creators"])


@router.get("/feed", response_model=List[CreatorResponse])
async def get_creator_feed(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """
    Get paginated creator feed for mobile app

    BUG REPORT from Mobile Team:
    - Response time: 3-5 seconds (should be <500ms)
    - Sometimes returns duplicate creators
    - Payload size too large for mobile (should optimize)

    TODO: After fixing CreatorService bugs, consider:
    - Using CreatorFeedResponse instead of CreatorResponse
    - This will reduce payload size for mobile
    """
    service = CreatorService(db)
    creators = service.get_feed(page, page_size)
    return creators
