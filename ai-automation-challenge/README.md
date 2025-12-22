# AI Automation Engineer Coding Challenge

**Time Limit:** 10-15 minutes
**Position:** AI Automation Engineer (Intern/Junior)
**Difficulty:** Intermediate

## Scenario

You're building a **content moderation service** for Vizzy Labs that analyzes creator video descriptions for policy violations. The service needs to:
- Use multiple AI providers (OpenAI primary, Anthropic Claude fallback)
- Return structured results with confidence scores
- Handle errors, timeouts, and rate limits gracefully

Your predecessor left the code incomplete with several bugs. Your job is to **fix the bugs and complete the implementation**.

---

## Setup

### 1. Install Dependencies
```bash
cd ai-automation-challenge
pip install -r requirements.txt
```

### 2. Run the Application
```bash
uvicorn main:app --reload
```

### 3. Test the API
```bash
curl -X POST "http://localhost:8000/moderate" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Check out my awesome video!",
    "creator_id": "creator123",
    "video_id": "video456"
  }'
```

---

## Your Tasks

### 🐛 Task 1: Fix Validation Bugs (3-4 minutes)

**File:** `models.py`

**Issues to fix:**
1. Content can be whitespace-only (add validator)
2. `creator_id` can be empty string (add validator)
3. No validation that `is_safe=True` must have `violation_type=NONE` (add validator)

**Hints:**
- Use `@validator` decorator from Pydantic
- Use `validator('field_name')` for single fields
- Use `validator('field', 'field2')` with `values` parameter for cross-field validation

---

### 🔧 Task 2: Fix OpenAI Integration (2-3 minutes)

**File:** `moderation_service.py` → `_moderate_with_openai()`

**Issues to fix:**
1. Confidence is hardcoded to `0.9` (should use actual scores from API)
2. Violation type is always `NONE` (should extract from categories)
3. Reasoning is generic (should be specific)

**Hints:**
- Check `result.category_scores` for confidence values
- Check `result.categories` dictionary for flagged categories
- Map OpenAI categories to `ViolationType` enum values

---

### ✨ Task 3: Implement Anthropic Fallback (4-5 minutes)

**File:** `moderation_service.py`

**Implement these methods:**

#### `_moderate_with_anthropic(content: str) -> ModerationResult`
- Call Anthropic Claude API with a prompt
- Parse the structured JSON response
- Return `ModerationResult` with `provider="anthropic"`

#### `_parse_llm_response(response_text: str) -> dict`
- Parse JSON from LLM response text
- Handle JSON parsing errors gracefully
- Return parsed dictionary

**Prompt Engineering:**
Your prompt should:
- Ask for structured JSON output
- Match the `ModerationResult` schema
- Include field descriptions
- Handle edge cases

**Example Prompt Structure:**
```
Analyze this content for policy violations. Return JSON with this exact structure:
{
  "is_safe": boolean,
  "confidence": float (0.0-1.0),
  "violation_type": "hate_speech" | "violence" | "adult_content" | "spam" | "none",
  "reasoning": "brief explanation"
}

Content: {content}

Respond only with valid JSON.
```

---

### 🔗 Task 4: Implement Fallback Chain (3-4 minutes)

**File:** `moderation_service.py` → `moderate_content()`

**Implement:**
1. Try OpenAI first with timeout (`asyncio.wait_for`)
2. If OpenAI fails/times out, fallback to Anthropic
3. If both fail, raise appropriate error
4. Handle all exceptions properly

**Hints:**
- Use `asyncio.wait_for(coro, timeout=self.timeout)`
- Catch specific exceptions: `asyncio.TimeoutError`, `Exception`
- Log errors for debugging

---

### 🚀 Task 5: Fix FastAPI Setup (2-3 minutes)

**File:** `main.py`

**Issues to fix:**
1. Service is not initialized (it's `None`)
2. No API keys loaded (use environment variables or defaults)
3. No timing tracking in endpoint
4. No error handling in endpoint

**Implement:**
- Lifespan context manager to initialize service on startup
- Dependency injection pattern for service
- Track processing time (start time → end time)
- Add try-except in endpoint

---

## Evaluation Criteria

### AI Coding Ability (25 points)
- [ ] Used AI assistant effectively (10 pts)
- [ ] Production-quality async code (10 pts)
- [ ] Completion rate (5 pts)

### Prompting Ability (25 points)
- [ ] Claude prompt structure is correct (15 pts)
- [ ] Prompt quality and clarity (10 pts)

### Debugging Ability (20 points)
- [ ] Fixed Pydantic validation bugs (8 pts)
- [ ] Fixed OpenAI integration issues (7 pts)
- [ ] Fixed initialization bugs (5 pts)

### Multi-tasking (15 points)
- [ ] Error handling across layers (5 pts)
- [ ] Timeout implementation (5 pts)
- [ ] Fallback chain logic (5 pts)

### System Thinking (15 points)
- [ ] Smart trade-offs and prioritization (5 pts)
- [ ] Follows service layer pattern (5 pts)
- [ ] Code is maintainable (5 pts)

**Minimum Passing Score:** 70/100

---

## Tips for Success

1. **Start with the obvious bugs** - Fix validation first, it's quickest
2. **Use AI effectively** - Let it generate boilerplate, you focus on logic
3. **Test incrementally** - Fix one thing, test it, move on
4. **Prioritize completion** - A working partial solution beats perfect incomplete code
5. **Communicate your thinking** - Explain your approach as you code

---

## Files Overview

- `models.py` - Pydantic models with validation **[HAS BUGS]**
- `moderation_service.py` - Core business logic **[INCOMPLETE + BUGS]**
- `main.py` - FastAPI application **[INCOMPLETE]**
- `mock_clients.py` - Mock OpenAI/Anthropic clients **[PROVIDED, WORKING]**
- `requirements.txt` - Dependencies **[PROVIDED]**

---

## Expected Behavior

After your fixes, the API should:
- ✅ Reject whitespace-only content
- ✅ Reject empty creator_id
- ✅ Return accurate confidence scores from OpenAI
- ✅ Extract actual violation types from OpenAI
- ✅ Fall back to Anthropic when OpenAI fails
- ✅ Handle timeouts gracefully
- ✅ Track processing time accurately
- ✅ Validate that safe content has violation_type=NONE

---

## Good Luck!

Remember: This challenge tests your **AI coding**, **debugging**, **prompting**, and **system thinking** skills. Use your AI assistant wisely and show us how you approach real-world problems!

**Questions during the interview?** Just ask! We're here to help clarify (but not solve it for you 😉).
