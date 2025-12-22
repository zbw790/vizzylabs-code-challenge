# Mobile Backend Challenge - Solution Reference

**For Evaluators Only** - Do not share with candidates

---

## Complete Solution

### 1. Fixed `services/creator_service.py`

```python
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Creator, Video
from typing import List


class CreatorService:
    def __init__(self, db: Session):
        self.db = db

    def get_feed(self, page: int, page_size: int) -> List[Creator]:
        """
        Get paginated creator feed with optimized query

        Fixes:
        - N+1 query problem → Single JOIN query
        - No pagination → Proper offset/limit
        - Duplicates → GROUP BY
        - Performance → <500ms response time
        """
        offset = (page - 1) * page_size

        creators = (
            self.db.query(Creator)
            .join(Video, Creator.id == Video.creator_id)
            .group_by(Creator.id)  # Prevents duplicates
            .order_by(Creator.follower_count.desc())
            .offset(offset)
            .limit(page_size)
            .all()
        )

        return creators
```

**Alternative Solution (with subquery):**
```python
def get_feed(self, page: int, page_size: int) -> List[Creator]:
    offset = (page - 1) * page_size

    # Subquery to get creators with videos
    creators_with_videos_subq = (
        self.db.query(Video.creator_id.distinct())
        .subquery()
    )

    creators = (
        self.db.query(Creator)
        .filter(Creator.id.in_(
            self.db.query(creators_with_videos_subq.c.creator_id)
        ))
        .order_by(Creator.follower_count.desc())
        .offset(offset)
        .limit(page_size)
        .all()
    )

    return creators
```

---

### 2. Implemented `services/analytics_service.py`

```python
from sqlalchemy.orm import Session
from sqlalchemy import case, func, Float
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

        Optimizations:
        - Single query (no N+1)
        - Calculates engagement in SQL (not Python)
        - Only selects needed columns
        - Handles division by zero
        """
        # Calculate engagement rate with division by zero handling
        engagement_rate = case(
            (Video.view_count > 0,
             (Video.like_count + Video.comment_count).cast(Float) / Video.view_count),
            else_=0.0
        )

        videos = (
            self.db.query(
                Video.id.label('video_id'),
                Video.title,
                Video.view_count,
                engagement_rate.label('engagement_rate')
            )
            .filter(Video.creator_id == creator_id)
            .order_by(engagement_rate.desc())
            .limit(limit)
            .all()
        )

        return [
            {
                'video_id': v.video_id,
                'title': v.title,
                'view_count': v.view_count,
                'engagement_rate': round(v.engagement_rate, 4)
            }
            for v in videos
        ]
```

---

### 3. Implemented `schemas.py`

```python
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class CreatorBase(BaseModel):
    username: str
    display_name: str


class CreatorResponse(BaseModel):
    """Full creator response with all fields"""
    id: int
    follower_count: int
    total_views: int
    avg_engagement_rate: float

    class Config:
        from_attributes = True


class CreatorFeedResponse(BaseModel):
    """Mobile-optimized response - only essential fields for list view"""
    id: int
    username: str
    display_name: str
    follower_count: int

    class Config:
        from_attributes = True


class VideoAnalyticsResponse(BaseModel):
    """Video analytics with engagement metrics"""
    video_id: int
    title: str
    view_count: int
    engagement_rate: float = Field(..., description="(likes + comments) / views")

    class Config:
        from_attributes = True
```

---

### 4. Implemented `routes/analytics.py`

```python
from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from services.analytics_service import AnalyticsService
from schemas import VideoAnalyticsResponse

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/creator/{creator_id}/videos", response_model=List[VideoAnalyticsResponse])
async def get_creator_video_analytics(
    creator_id: int = Path(..., description="Creator ID", gt=0),
    db: Session = Depends(get_db)
):
    """
    Get video analytics for a creator's top performing videos

    Returns top 10 videos sorted by engagement rate
    """
    service = AnalyticsService(db)

    try:
        analytics = service.get_top_videos_by_engagement(creator_id)

        if not analytics:
            raise HTTPException(
                status_code=404,
                detail=f"No videos found for creator {creator_id}"
            )

        return analytics

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching analytics: {str(e)}"
        )
```

---

### 5. Optional: Updated `routes/creators.py` (Bonus)

```python
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas import CreatorFeedResponse  # Changed to mobile-optimized schema
from services.creator_service import CreatorService

router = APIRouter(prefix="/creators", tags=["creators"])


@router.get("/feed", response_model=List[CreatorFeedResponse])
async def get_creator_feed(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """
    Get paginated creator feed for mobile app (optimized)
    """
    service = CreatorService(db)
    creators = service.get_feed(page, page_size)
    return creators
```

---

## Scoring Guide

### Performance (40 points)

**Fixed N+1 Query Bug (15 pts):**
- Correct approach with JOIN (15 pts)
- Attempted JOIN but with issues (10 pts)
- Used subquery instead (12 pts)
- Still has N+1 but acknowledged issue (5 pts)
- No fix attempted (0 pts)

**Proper Pagination (10 pts):**
- Correct offset/limit calculation (10 pts)
- Has offset/limit but wrong calculation (6 pts)
- Manual slicing after query (3 pts)
- No pagination (0 pts)

**Feed Response Time (10 pts):**
- <500ms consistently (10 pts)
- 500-1000ms (7 pts)
- 1-2 seconds (4 pts)
- >2 seconds (0 pts)

**Analytics Efficiency (5 pts):**
- Single optimized query (5 pts)
- Works but inefficient (3 pts)
- Has N+1 or loads full objects (1 pt)

---

### Correctness (30 points)

**No Duplicates (10 pts):**
- No duplicates, uses GROUP BY (10 pts)
- No duplicates, alternative approach (10 pts)
- Still has duplicates (0 pts)

**Engagement Calculation (10 pts):**
- Correct SQL calculation with div-by-zero handling (10 pts)
- Correct calculation but no div-by-zero handling (7 pts)
- Calculates in Python (loads data then computes) (4 pts)
- Incorrect formula (0 pts)

**Error Handling (10 pts):**
- Proper exception handling, HTTPException, edge cases (10 pts)
- Basic try-except (6 pts)
- No error handling (0 pts)

---

### Mobile Optimization (20 points)

**Response Schemas (10 pts):**
- CreatorFeedResponse: only essential fields (5 pts)
- VideoAnalyticsResponse: proper fields (5 pts)
- Partial implementation (3-7 pts)
- Using full schemas (0 pts)

**Pagination for Mobile (5 pts):**
- Proper offset/limit with page numbers (5 pts)
- Works but not ideal (3 pts)
- No pagination (0 pts)

**Understanding Mobile Constraints (5 pts):**
- Evidence in code choices (minimal fields, efficient queries) (5 pts)
- Some awareness (3 pts)
- No consideration (0 pts)

---

### Code Quality (10 points)

**Follows Pattern (4 pts):**
- Route → Service → Database (4 pts)
- Mixed logic (2 pts)
- All in routes (0 pts)

**Pydantic Usage (3 pts):**
- Proper schemas with Config (3 pts)
- Basic schemas (2 pts)
- Dict responses (0 pts)

**SQLAlchemy Quality (3 pts):**
- Clean, efficient queries (3 pts)
- Works but messy (2 pts)
- Poor practices (0 pts)

---

## Common Solutions & Variations

### Acceptable Query Variations:

1. **JOIN with GROUP BY** (Preferred)
```python
.join(Video).group_by(Creator.id)
```

2. **Subquery with IN**
```python
.filter(Creator.id.in_(
    select(Video.creator_id).distinct()
))
```

3. **EXISTS clause**
```python
.filter(
    exists().where(Video.creator_id == Creator.id)
)
```

All are acceptable if they avoid N+1!

---

## Red Flags (Deduct Points)

- ❌ Still has N+1 queries after "fix"
- ❌ Loads all data then filters in Python
- ❌ No pagination implementation
- ❌ Calculates engagement in Python loop
- ❌ Returns full ORM objects without schema
- ❌ No GROUP BY (still has duplicates)
- ❌ Doesn't handle division by zero
- ❌ No type hints or documentation

---

## Bonus Points (Up to +5)

- ✅ Added indexes for common queries
- ✅ Implemented caching layer
- ✅ Added comprehensive error messages
- ✅ Added logging for debugging
- ✅ Added query result count in response
- ✅ Implemented cursor-based pagination instead of offset
- ✅ Added response time tracking/metrics

---

## Performance Benchmarks

**Before Fix:**
- Query count: ~101 queries (1 + 100 N+1)
- Response time: 3-5 seconds
- Duplicates: Yes

**After Fix:**
- Query count: 1 query
- Response time: <500ms (typically 50-200ms)
- Duplicates: No

**Analytics Endpoint:**
- Should be <300ms
- Single query with calculation
- No N+1 issues

---

## Interview Discussion Questions

After coding, ask:

1. **"Why did you use GROUP BY instead of DISTINCT?"**
   - Good answer: GROUP BY is more efficient and semantic for this use case
   - Acceptable: Either works, GROUP BY prevents duplicates from joins

2. **"How would you handle this query if you had millions of creators?"**
   - Good answer: Cursor-based pagination, caching, database indexes, read replicas
   - Acceptable: Indexes, caching

3. **"Why calculate engagement_rate in SQL instead of Python?"**
   - Good answer: Reduces data transfer, allows sorting in DB, more efficient
   - Acceptable: Performance, cleaner code

4. **"What if a creator has no videos?"**
   - Good answer: LEFT JOIN or handle in query, return empty list
   - Current solution: They won't appear (inner join filters them out)

5. **"How would you test this in production?"**
   - Good answer: Load testing, query explain plans, monitoring, metrics
   - Acceptable: Manual testing, timing requests

---

## Time Expectations

**Fast Track (10 min):**
- Fixes N+1 immediately
- Implements analytics quickly
- May skip schemas

**Normal Track (12-15 min):**
- Debugs N+1 with some trial
- Implements analytics fully
- Completes schemas

**Slow Track (15+ min):**
- Struggles with N+1
- Partial implementation
- May not finish schemas

All are acceptable for passing if core issues are addressed!
