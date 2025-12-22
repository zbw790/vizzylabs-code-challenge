from sqlalchemy.orm import Session
from models import Video
from typing import List, Dict


class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db

    def get_top_videos_by_engagement(
        self,
        creator_id: int,
        limit: int = 10
    ) -> List[Dict]:
        """
        Get top videos by engagement rate for a creator

        TODO: Implement efficient query for mobile analytics

        Requirements:
        - Calculate engagement_rate = (likes + comments) / views
        - Return top 10 videos by engagement_rate
        - Handle division by zero (when views = 0)
        - Response time < 300ms
        - Only select needed fields (don't load full Video objects)

        Hints:
        - Use SQLAlchemy expressions for calculation (case, func, cast)
        - Use .query() with specific columns, not full models
        - Use .label() to name calculated fields
        - Order by engagement_rate descending
        - Apply limit
        """
        pass  # IMPLEMENT THIS
