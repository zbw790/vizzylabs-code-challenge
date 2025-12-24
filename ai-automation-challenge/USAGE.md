# Content Moderation API - Usage Guide

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd ai-automation-challenge
pip install -r requirements.txt
```

### 2. Start the Server
```bash
uvicorn main:app --reload
```

You should see:
```
✅ Moderation service initialized
INFO:     Uvicorn running on http://127.0.0.1:8000
```

---

## 📡 API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "content-moderation",
  "providers": ["openai", "anthropic"]
}
```

---

### Moderate Content

**Endpoint:** `POST /moderate`

**Request Body:**
```json
{
  "content": "Check out my awesome video!",
  "creator_id": "creator123",
  "video_id": "video456"
}
```

**Example - Safe Content:**
```bash
curl -X POST "http://localhost:8000/moderate" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Check out my awesome video!",
    "creator_id": "creator123",
    "video_id": "video456"
  }'
```

**Response:**
```json
{
  "video_id": "video456",
  "moderation": {
    "is_safe": true,
    "confidence": 0.05,
    "violation_type": "none",
    "reasoning": "No violations detected. Max score: 0.05",
    "provider": "openai"
  },
  "processing_time_ms": 2.34
}
```

---

**Example - Unsafe Content:**
```bash
curl -X POST "http://localhost:8000/moderate" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "I hate everyone and want violence",
    "creator_id": "creator789",
    "video_id": "video999"
  }'
```

**Response:**
```json
{
  "video_id": "video999",
  "moderation": {
    "is_safe": false,
    "confidence": 0.85,
    "violation_type": "hate_speech",
    "reasoning": "Detected violations: hate: 0.85",
    "provider": "openai"
  },
  "processing_time_ms": 3.12
}
```

---

## 🛡️ Validation Rules

### Content Field
- ✅ Must not be empty
- ✅ Must not be whitespace only
- ❌ `""` → Error
- ❌ `"   "` → Error
- ❌ `"\n\t"` → Error

### Creator ID Field
- ✅ Must not be empty
- ✅ Must not be whitespace only
- ❌ `""` → Error
- ❌ `"   "` → Error

### Example Validation Error:
```bash
curl -X POST "http://localhost:8000/moderate" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "   ",
    "creator_id": "creator123"
  }'
```

**Response (422 Error):**
```json
{
  "detail": [
    {
      "loc": ["body", "content"],
      "msg": "Content cannot be empty or whitespace only",
      "type": "value_error"
    }
  ]
}
```

---

## 🔄 Fallback Behavior

The service automatically handles failures:

1. **OpenAI Primary**: Tries OpenAI moderation first
2. **Timeout Protection**: 5-second timeout per provider
3. **Automatic Fallback**: Falls back to Anthropic if OpenAI fails
4. **Error Handling**: Returns descriptive errors if both fail

**Example Fallback Response:**
```json
{
  "video_id": "video123",
  "moderation": {
    "is_safe": true,
    "confidence": 0.95,
    "violation_type": "none",
    "reasoning": "Content analyzed for policy violations. No violations found.",
    "provider": "anthropic"  ← Notice fallback provider
  },
  "processing_time_ms": 1050.23
}
```

---

## 📊 Violation Types

| Type | Description | Example |
|------|-------------|---------|
| `none` | Safe content | "Check out my video!" |
| `hate_speech` | Hateful, discriminatory content | "I hate [group]" |
| `violence` | Violent, threatening content | "I will attack..." |
| `adult_content` | Sexual, NSFW content | "NSFW content" |
| `spam` | Promotional, spammy content | "Buy now! Click here!" |

---

## 🧪 Testing

### Python Test
```python
import requests

response = requests.post(
    "http://localhost:8000/moderate",
    json={
        "content": "Check out my awesome video!",
        "creator_id": "creator123",
        "video_id": "video456"
    }
)

print(response.json())
```

### JavaScript Test
```javascript
fetch('http://localhost:8000/moderate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    content: 'Check out my awesome video!',
    creator_id: 'creator123',
    video_id: 'video456'
  })
})
.then(r => r.json())
.then(data => console.log(data));
```

---

## 🔧 Configuration

### Environment Variables

```bash
# Optional: Use real API keys
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."

# Start server
uvicorn main:app --reload
```

**Note:** If not set, the service uses mock clients for testing.

### Timeout Configuration

Edit `moderation_service.py`:
```python
self.timeout = 5.0  # Change to desired timeout in seconds
```

---

## 📝 Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `video_id` | string | Video identifier from request |
| `moderation.is_safe` | boolean | Whether content is safe |
| `moderation.confidence` | float | Confidence score (0.0-1.0) |
| `moderation.violation_type` | string | Type of violation detected |
| `moderation.reasoning` | string | Explanation of decision |
| `moderation.provider` | string | AI provider used (openai/anthropic) |
| `processing_time_ms` | float | Processing time in milliseconds |

---

## ⚠️ Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 422 | Validation error (invalid input) |
| 500 | Moderation failed (both providers failed) |
| 503 | Service not initialized |

---

## 🎯 Best Practices

1. **Always validate input** before sending to API
2. **Check `is_safe` field** for moderation decision
3. **Use `confidence` score** for threshold-based decisions
4. **Log `provider` field** to monitor fallback frequency
5. **Monitor `processing_time_ms`** for performance

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenAI Moderation API](https://platform.openai.com/docs/guides/moderation)
- [Anthropic Claude API](https://docs.anthropic.com/)

---

## 🐛 Troubleshooting

**Port already in use:**
```bash
uvicorn main:app --port 8001
```

**Module not found:**
```bash
pip install -r requirements.txt
```

**Service not initialized (503):**
- Restart the server
- Check startup logs for errors

---

## ✅ Features

- ✅ Dual AI provider support (OpenAI + Anthropic)
- ✅ Automatic fallback on failure
- ✅ Timeout protection (5s default)
- ✅ Comprehensive input validation
- ✅ Detailed confidence scores
- ✅ Processing time tracking
- ✅ Health check endpoint
- ✅ Production-ready error handling

---

**Need help?** Check `IMPLEMENTATION_SUMMARY.md` for technical details.

