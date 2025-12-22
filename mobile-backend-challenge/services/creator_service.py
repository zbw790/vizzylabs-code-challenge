from sqlalchemy.orm import Session
from models import Creator, Video
from typing import List


class CreatorService:
    def __init__(self, db: Session):
        self.db = db

    def get_feed(self, page: int, page_size: int) -> List[Creator]:
        """
        Get paginated creator feed

        PERFORMANCE ISSUES:
        1. N+1 query problem - queries each creator's videos separately
        2. No pagination offset - loads ALL creators
        3. Loading unnecessary relationships
        4. No query optimization

        Mobile team reports:
        - Response time: 3-5 seconds (should be <500ms)
        - Sometimes returns duplicate creators
        """
        # BUG: Gets ALL creators from database!
        creators = self.db.query(Creator).all()

        # BUG: N+1 query problem - separate query for each creator
        result = []
        for creator in creators:
            # This causes a separate database query for EACH creator!
            video_count = self.db.query(Video).filter(
                Video.creator_id == creator.id
            ).count()

            if video_count > 0:
                result.append(creator)

        # BUG: No pagination applied - returns everything
        # BUG: May have duplicates due to query structure
        return result
