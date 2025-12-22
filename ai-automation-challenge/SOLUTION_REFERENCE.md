# AI Automation Challenge - Solution Reference

**For Evaluators Only** - Do not share with candidates

---

## Complete Solution

### 1. Fixed `models.py`

```python
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
    def validate_content_not_whitespace(cls, v):
        if not v or not v.strip():
            raise ValueError('Content cannot be empty or whitespace')
        return v.strip()

    @validator('creator_id')
    def validate_creator_id(cls, v):
        if not v or not v.strip():
            raise ValueError('creator_id cannot be empty')
        return v

class ModerationResult(BaseModel):
    """Structured AI moderation result"""
    is_safe: bool
    confidence: float = Field(..., ge=0.0, le=1.0)
    violation_type: ViolationType
    reasoning: str
    provider: str

    @validator('violation_type')
    def validate_safety_consistency(cls, v, values):
        if values.get('is_safe') and v != ViolationType.NONE:
            raise ValueError('Safe content must have violation_type=NONE')
        return v

class ModerationResponse(BaseModel):
    """API response model"""
    video_id: Optional[str]
    moderation: ModerationResult
    processing_time_ms: float
```

---

### 2. Fixed `moderation_service.py`

```python
import asyncio
import time
from typing import Optional
import json
from models import ModerationRequest, ModerationResult, ViolationType
from mock_clients import MockOpenAIClient, MockAnthropicClient


class ModerationService:
    def __init__(self, openai_key: str, anthropic_key: str):
        self.openai_client = MockOpenAIClient(api_key=openai_key)
        self.anthropic_client = MockAnthropicClient(api_key=anthropic_key)
        self.max_retries = 2
        self.timeout = 5.0

    async def moderate_content(self, request: ModerationRequest) -> ModerationResult:
        """Moderate content using OpenAI with Anthropic fallback."""
        try:
            # Try OpenAI first with timeout
            result = await asyncio.wait_for(
                self._moderate_with_openai(request.content),
                timeout=self.timeout
            )
            return result
        except (asyncio.TimeoutError, Exception) as e:
            # Fallback to Anthropic
            print(f"OpenAI failed ({e}), falling back to Anthropic")
            try:
                result = await asyncio.wait_for(
                    self._moderate_with_anthropic(request.content),
                    timeout=self.timeout
                )
                return result
            except Exception as fallback_error:
                raise Exception(f"All moderation providers failed: {fallback_error}")

    async def _moderate_with_openai(self, content: str) -> ModerationResult:
        """Call OpenAI moderation API"""
        response = await self.openai_client.moderations.create(input=content)
        result = response.results[0]

        # Extract actual violation type and confidence
        violation_type = ViolationType.NONE
        max_score = 0.0

        if result.flagged:
            # Find the highest scoring category
            for category, is_flagged in result.categories.items():
                if is_flagged:
                    score = getattr(result.category_scores, category, 0.0)
                    if score > max_score:
                        max_score = score
                        # Map OpenAI categories to our ViolationType
                        if category == "hate":
                            violation_type = ViolationType.HATE_SPEECH
                        elif category == "violence":
                            violation_type = ViolationType.VIOLENCE
                        elif category == "sexual":
                            violation_type = ViolationType.ADULT_CONTENT
                        elif category == "spam":
                            violation_type = ViolationType.SPAM

        # Get confidence from actual scores
        all_scores = [
            result.category_scores.hate,
            result.category_scores.violence,
            result.category_scores.sexual,
            result.category_scores.spam
        ]
        confidence = max(all_scores) if result.flagged else (1.0 - max(all_scores))

        reasoning = f"OpenAI detected {violation_type.value}" if result.flagged else "No violations detected"

        return ModerationResult(
            is_safe=not result.flagged,
            confidence=round(confidence, 2),
            violation_type=violation_type,
            reasoning=reasoning,
            provider="openai"
        )

    async def _moderate_with_anthropic(self, content: str) -> ModerationResult:
        """Call Anthropic Claude API as fallback"""
        prompt = f"""Analyze this content for policy violations. Return ONLY valid JSON with this exact structure:

{{
  "is_safe": boolean,
  "confidence": float between 0.0 and 1.0,
  "violation_type": one of ["hate_speech", "violence", "adult_content", "spam", "none"],
  "reasoning": "brief explanation of your decision"
}}

Policy violations to check:
- hate_speech: Hateful, discriminatory language
- violence: Violent or threatening content
- adult_content: Sexual or NSFW content
- spam: Spam or misleading content
- none: No violations

Content to analyze: "{content}"

Return ONLY the JSON object, no other text.
"""

        message = await self.anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )

        response_json = self._parse_llm_response(message.content[0].text)

        return ModerationResult(
            **response_json,
            provider="anthropic"
        )

    def _parse_llm_response(self, response_text: str) -> dict:
        """Parse structured JSON from LLM response"""
        try:
            # Try to parse as JSON
            return json.loads(response_text)
        except json.JSONDecodeError:
            # Try to extract JSON from markdown code blocks
            if "```json" in response_text:
                start = response_text.find("```json") + 7
                end = response_text.find("```", start)
                json_str = response_text[start:end].strip()
                return json.loads(json_str)
            elif "```" in response_text:
                start = response_text.find("```") + 3
                end = response_text.find("```", start)
                json_str = response_text[start:end].strip()
                return json.loads(json_str)
            else:
                raise ValueError(f"Could not parse JSON from response: {response_text}")
```

---

### 3. Fixed `main.py`

```python
from fastapi import FastAPI, HTTPException, Depends
from contextlib import asynccontextmanager
import time
from models import ModerationRequest, ModerationResponse
from moderation_service import ModerationService
import os

# Global service instance
_moderation_service = None


def get_moderation_service() -> ModerationService:
    """Dependency to inject moderation service"""
    if _moderation_service is None:
        raise HTTPException(status_code=500, detail="Service not initialized")
    return _moderation_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize service on startup, cleanup on shutdown"""
    global _moderation_service

    # Initialize service with API keys
    openai_key = os.getenv("OPENAI_API_KEY", "mock-openai-key")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY", "mock-anthropic-key")

    _moderation_service = ModerationService(
        openai_key=openai_key,
        anthropic_key=anthropic_key
    )

    print("✅ Moderation service initialized")

    yield

    # Cleanup (if needed)
    print("🛑 Shutting down moderation service")


app = FastAPI(
    title="Content Moderation API",
    lifespan=lifespan
)


@app.post("/moderate", response_model=ModerationResponse)
async def moderate_content(
    request: ModerationRequest,
    service: ModerationService = Depends(get_moderation_service)
):
    """Moderate content for policy violations."""
    start_time = time.time()

    try:
        result = await service.moderate_content(request)

        processing_time = (time.time() - start_time) * 1000  # Convert to ms

        return ModerationResponse(
            video_id=request.video_id,
            moderation=result,
            processing_time_ms=round(processing_time, 2)
        )
    except Exception as e:
        raise HTTPException(
            status_code=503,
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
```

---

## Scoring Guide

### AI Coding Ability (25 points)
- **10 pts:** Used AI for boilerplate, validators, async patterns
- **10 pts:** Code quality (type hints, error handling, async/await)
- **5 pts:** Completion (all methods implemented)

### Prompting Ability (25 points)
- **15 pts:** Claude prompt structure
  - Returns valid JSON (5 pts)
  - Includes schema definition (5 pts)
  - Clear instructions (5 pts)
- **10 pts:** Prompt quality
  - Examples or constraints (5 pts)
  - Handles edge cases (5 pts)

### Debugging Ability (20 points)
- **8 pts:** Pydantic validators
  - Whitespace validator (3 pts)
  - creator_id validator (2 pts)
  - Safety consistency validator (3 pts)
- **7 pts:** OpenAI integration
  - Extract actual violation type (4 pts)
  - Calculate real confidence (3 pts)
- **5 pts:** Service initialization and dependency injection

### Multi-tasking (15 points)
- **5 pts:** Error handling (try-except blocks, proper exceptions)
- **5 pts:** Timeout implementation (asyncio.wait_for)
- **5 pts:** Fallback chain (OpenAI → Anthropic)

### System Thinking (15 points)
- **5 pts:** Smart trade-offs (when to retry vs fallback, timeout values)
- **5 pts:** Service layer pattern (separation of concerns)
- **5 pts:** Maintainability (readable, extendable code)

---

## Common Solutions & Partial Credit

### Acceptable Variations:

1. **Prompt Engineering:**
   - Few-shot examples (bonus points)
   - Chain-of-thought reasoning (bonus points)
   - Different JSON structures (as long as they work)

2. **Error Handling:**
   - More specific exception types (bonus)
   - Retry logic (bonus)
   - Logging (bonus)

3. **Validation:**
   - Additional validators (length limits, profanity check) = bonus
   - Different validation approaches (field validators vs root validators)

### Partial Credit Scenarios:

- **Incomplete but correct approach:** 60-70% of points
- **Working but messy code:** 70-80% of points
- **Complete with minor bugs:** 85-95% of points
- **Perfect solution:** 95-100% of points

---

## Red Flags (Deduct Points)

- ❌ No async/await (using sync code)
- ❌ No error handling at all
- ❌ Hardcoded values everywhere
- ❌ Ignoring the service layer pattern
- ❌ Not using the mock clients (trying to use real API keys)
- ❌ Copy-pasting without understanding
- ❌ No testing/verification of their code

---

## Interview Discussion Questions

After coding, ask:
1. "Walk me through your fallback logic - why did you structure it this way?"
2. "How would you improve this if you had more time?"
3. "What would you do differently in production?" (logging, metrics, retries)
4. "How did you use AI to help you? Show me your prompts."
5. "What was the hardest bug to fix and why?"
