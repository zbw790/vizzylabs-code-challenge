# Mobile Backend Engineer Coding Challenge

**Time Limit:** 10-15 minutes
**Position:** Full-Stack Mobile Backend Engineer
**Difficulty:** Intermediate

## Scenario

**URGENT:** The mobile team just reported critical issues with the Creator Discovery Feed API:

🚨 **Problems:**
- Feed endpoint timing out (3-5 seconds, should be <500ms)
- Sometimes returns duplicate creators
- Payload too large for mobile networks

📱 **Also Needed:**
- New video analytics endpoint for the mobile app
- Must show top performing videos by engagement rate

Your job: **Debug the performance issues and implement the analytics endpoint.**

---

## Setup

### 1. Install Dependencies
```bash
cd mobile-backend-challenge
pip install -r requirements.txt
```

### 2. Run the Application
```bash
uvicorn main:app --reload
```

The database will automatically seed with 100 creators and 1000 videos on startup.

### 3. Test the Buggy Endpoint
```bash
# This will be SLOW (3-5 seconds)
curl "http://localhost:8000/creators/feed?page=1&page_size=20"
```

---

## Your Tasks

### 🐛 Task 1: Fix Performance Issues (5-7 minutes)

**File:** `services/creator_service.py` → `get_feed()`

**Critical bugs causing 3-5 second response time:**

1. **N+1 Query Problem** ⚠️
   - Current code queries ALL creators: `self.db.query(Creator).all()`
   - Then loops through each creator with separate query for videos
   - Result: 1 query + 100 queries = 101 database queries!

2. **No Pagination** ⚠️
   - Loads ALL creators from database
   - Doesn't use `page` or `page_size` parameters
   - Mobile app can't efficiently scroll

3. **Duplicates** ⚠️
   - Query structure causes duplicate creators in results
   - Need to use `GROUP BY` or better join strategy

**Your fix should:**
- ✅ Use a single JOIN query (not N+1 queries)
- ✅ Apply proper pagination with offset/limit
- ✅ Eliminate duplicates with `group_by`
- ✅ Order by `follower_count` descending
- ✅ Response time < 500ms

**Hints:**
```python
# Use SQLAlchemy joins
.join(Video, Creator.id == Video.creator_id)
.group_by(Creator.id)  # Prevents duplicates
.offset((page - 1) * page_size)
.limit(page_size)
```

---

### ✨ Task 2: Implement Analytics Endpoint (4-5 minutes)

**Files:** `services/analytics_service.py` + `routes/analytics.py`

#### Part A: Service Layer
**File:** `services/analytics_service.py` → `get_top_videos_by_engagement()`

Implement efficient SQLAlchemy query that:
- Calculates engagement_rate = `(likes + comments) / views`
- Handles division by zero (when views = 0, rate should be 0)
- Returns top 10 videos ordered by engagement_rate
- Only selects needed columns (not full Video objects)
- Response time < 300ms

**Hints:**
```python
from sqlalchemy import case, func, Float

# Calculate engagement rate with div-by-zero handling
engagement_rate = case(
    (Video.view_count > 0,
     (Video.like_count + Video.comment_count).cast(Float) / Video.view_count),
    else_=0.0
)

# Query specific columns
self.db.query(
    Video.id.label('video_id'),
    Video.title,
    Video.view_count,
    engagement_rate.label('engagement_rate')
)
```

#### Part B: Route Layer
**File:** `routes/analytics.py` → `get_creator_video_analytics()`

Implement the endpoint:
- Call `AnalyticsService.get_top_videos_by_engagement()`
- Return results with proper response model
- Add error handling for invalid creator_id
- Use `VideoAnalyticsResponse` schema

---

### 📦 Task 3: Create Mobile-Optimized Schemas (2-3 minutes)

**File:** `schemas.py`

#### `CreatorFeedResponse`
For mobile list view, only include:
- `id`: int
- `username`: str
- `display_name`: str
- `follower_count`: int

*Don't include:* `total_views`, `avg_engagement_rate` (not shown in list view)

#### `VideoAnalyticsResponse`
For analytics, include:
- `video_id`: int
- `title`: str
- `view_count`: int
- `engagement_rate`: float

**Remember:** Add `class Config: from_attributes = True` for SQLAlchemy compatibility

---

## Evaluation Criteria

### Performance (40 points)
- [ ] Fixed N+1 query bug (15 pts)
- [ ] Proper pagination implemented (10 pts)
- [ ] Feed response time improved (10 pts)
- [ ] Analytics endpoint efficiency (5 pts)

### Correctness (30 points)
- [ ] No duplicate creators (10 pts)
- [ ] Engagement rate calculation correct (10 pts)
- [ ] Error handling and edge cases (10 pts)

### Mobile Optimization (20 points)
- [ ] Response schemas optimized (10 pts)
- [ ] Pagination suitable for mobile (5 pts)
- [ ] Understanding of mobile constraints (5 pts)

### Code Quality (10 points)
- [ ] Follows route → service → database pattern (4 pts)
- [ ] Proper Pydantic usage (3 pts)
- [ ] SQLAlchemy query quality (3 pts)

**Minimum Passing Score:** 70/100

---

## Tips for Success

1. **Fix the N+1 bug first** - It's the biggest performance issue
2. **Test your queries** - Run the endpoint and measure response time
3. **Use SQLAlchemy expressions** - Don't fetch data and calculate in Python
4. **Think mobile-first** - Smaller payloads = faster loading
5. **Handle edge cases** - Division by zero, invalid IDs, etc.

---

## Files Overview

**Complete (no changes needed):**
- `main.py` - FastAPI app with routes included
- `database.py` - Connection pool and session management
- `models.py` - SQLAlchemy Creator and Video models
- `seed_data.py` - Populates test data

**Has Bugs/Incomplete:**
- `services/creator_service.py` - **N+1 query bug, no pagination**
- `services/analytics_service.py` - **Stub only, needs implementation**
- `routes/analytics.py` - **Incomplete, needs implementation**
- `schemas.py` - **Missing mobile-optimized response models**

---

## Testing Your Solution

### Test Creator Feed Performance
```bash
# Should return results in <500ms with proper pagination
time curl "http://localhost:8000/creators/feed?page=1&page_size=20"

# Test pagination
curl "http://localhost:8000/creators/feed?page=2&page_size=10"
```

### Test Analytics Endpoint
```bash
# Get top videos for creator_id=1
curl "http://localhost:8000/analytics/creator/1/videos"

# Should return JSON like:
# [
#   {
#     "video_id": 42,
#     "title": "Creator 1's Video #7",
#     "view_count": 523801,
#     "engagement_rate": 0.1234
#   },
#   ...
# ]
```

---

## Expected Behavior After Fixes

### Creator Feed Endpoint
- ✅ Response time < 500ms
- ✅ No duplicate creators
- ✅ Proper pagination (20 creators per page)
- ✅ Ordered by follower_count descending
- ✅ Only essential fields in response

### Analytics Endpoint
- ✅ Returns top 10 videos by engagement rate
- ✅ Engagement rate calculated correctly
- ✅ Handles videos with 0 views (rate = 0)
- ✅ Response time < 300ms
- ✅ Mobile-optimized payload

---

## Common Pitfalls to Avoid

❌ **Don't** use `.all()` then slice in Python - use SQL LIMIT/OFFSET
❌ **Don't** calculate engagement in Python - use SQLAlchemy expressions
❌ **Don't** load full ORM objects if you only need specific fields
❌ **Don't** forget to handle division by zero
❌ **Don't** return all creator fields for mobile feed (payload bloat)

✅ **Do** use joins to avoid N+1 queries
✅ **Do** use `.query(specific, columns)` instead of `.query(Model)`
✅ **Do** use `case()` for conditional SQL expressions
✅ **Do** test your queries with timing
✅ **Do** think about what mobile apps actually need

---

## Good Luck!

This challenge tests your ability to:
- 🔍 **Debug performance issues** (N+1 queries, missing indexes)
- 🚀 **Write efficient SQL** (joins, aggregations, calculations)
- 📱 **Think mobile-first** (payload optimization, response times)
- 🏗️ **Follow patterns** (service layer, proper separation)

**Questions during the interview?** Just ask! We're here to help clarify.
