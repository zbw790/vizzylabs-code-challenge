from pydantic import BaseModel, Field, validator
from typing import Optional, List
from enum import Enum

class ViolationType(str, Enum):
    HATE_SPEECH = "hate_speech"
    VIOLENCE = "violence"
    ADULT_CONTENT = "adult_content"
    SPAM = "spam"
    NONE = "none"

class ModerationRequest(BaseModel):
    """Request model for content moderation"""
    content: str = Field(..., min_length=1)
    creator_id: str
    video_id: Optional[str] = None

    # BUG: Missing validator to ensure content isn't just whitespace
    # BUG: creator_id should be validated (not empty string)
    # TODO: Add validators here

class ModerationResult(BaseModel):
    """Structured AI moderation result"""
    is_safe: bool
    confidence: float = Field(..., ge=0.0, le=1.0)
    violation_type: ViolationType
    reasoning: str
    provider: str  # "openai" or "anthropic"

    # BUG: Missing validation - if is_safe=True, violation_type should be NONE
    # TODO: Add validator here

class ModerationResponse(BaseModel):
    """API response model"""
    video_id: Optional[str]
    moderation: ModerationResult
    processing_time_ms: float
