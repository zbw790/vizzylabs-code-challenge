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

    @validator('content')
    def content_not_whitespace(cls, v):
        """Validate that content is not just whitespace"""
        if not v or not v.strip():
            raise ValueError('Content cannot be empty or whitespace only')
        return v
    
    @validator('creator_id')
    def creator_id_not_empty(cls, v):
        """Validate that creator_id is not empty"""
        if not v or not v.strip():
            raise ValueError('Creator ID cannot be empty')
        return v

class ModerationResult(BaseModel):
    """Structured AI moderation result"""
    is_safe: bool
    confidence: float = Field(..., ge=0.0, le=1.0)
    violation_type: ViolationType
    reasoning: str
    provider: str  # "openai" or "anthropic"

    @validator('violation_type')
    def validate_safe_violation_consistency(cls, v, values):
        """Validate that is_safe=True means violation_type=NONE"""
        if 'is_safe' in values and values['is_safe'] is True:
            if v != ViolationType.NONE:
                raise ValueError('When is_safe=True, violation_type must be NONE')
        return v

class ModerationResponse(BaseModel):
    """API response model"""
    video_id: Optional[str]
    moderation: ModerationResult
    processing_time_ms: float
