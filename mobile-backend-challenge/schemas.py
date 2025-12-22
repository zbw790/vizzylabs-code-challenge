from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class CreatorBase(BaseModel):
    username: str
    display_name: str


class CreatorResponse(CreatorBase):
    """Full creator response with all fields"""
    id: int
    follower_count: int
    total_views: int
    avg_engagement_rate: float

    class Config:
        from_attributes = True


# TODO: Create mobile-optimized response model
# Should include only essential fields for mobile list view
# Mobile apps need smaller payloads for better performance
class CreatorFeedResponse(BaseModel):
    """
    TODO: Implement this for mobile feed optimization

    Hints:
    - Only include fields needed for list view (not detail view)
    - Keep payload size minimal for mobile networks
    - Think about what a user sees scrolling through creators
    """
    pass  # IMPLEMENT THIS


# TODO: Implement analytics response schemas
# Need: VideoAnalyticsResponse with engagement metrics
# Should be optimized for mobile payload size
class VideoAnalyticsResponse(BaseModel):
    """
    TODO: Implement this for video analytics endpoint

    Should include:
    - video_id: int
    - title: str
    - view_count: int
    - engagement_rate: float (calculated field)

    Hints:
    - engagement_rate = (likes + comments) / views
    - This will be calculated in the service layer
    """
    pass  # IMPLEMENT THIS
