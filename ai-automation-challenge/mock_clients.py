"""
Mock API clients for testing without real API keys.
These simulate OpenAI and Anthropic API responses.
"""
from typing import List, Dict, Any
import json


class MockModerationResult:
    """Mock OpenAI moderation result"""
    def __init__(self, input_text: str):
        self.flagged = self._should_flag(input_text)
        self.categories = self._get_categories(input_text)
        self.category_scores = self._get_scores(input_text)

    def _should_flag(self, text: str) -> bool:
        """Simple keyword-based flagging"""
        keywords = ["violence", "hate", "nsfw", "spam", "attack"]
        return any(word in text.lower() for word in keywords)

    def _get_categories(self, text: str) -> Dict[str, bool]:
        """Return which categories are flagged"""
        text_lower = text.lower()
        return {
            "hate": "hate" in text_lower,
            "violence": "violence" in text_lower or "attack" in text_lower,
            "sexual": "nsfw" in text_lower or "adult" in text_lower,
            "spam": "spam" in text_lower,
        }

    def _get_scores(self, text: str) -> Dict[str, float]:
        """Return confidence scores for each category"""
        categories = self._get_categories(text)
        return {
            "hate": 0.85 if categories["hate"] else 0.05,
            "violence": 0.78 if categories["violence"] else 0.03,
            "sexual": 0.92 if categories["sexual"] else 0.02,
            "spam": 0.65 if categories["spam"] else 0.04,
        }


class MockModerationResponse:
    """Mock OpenAI moderation API response"""
    def __init__(self, input_text: str):
        self.results = [MockModerationResult(input_text)]


class MockOpenAIClient:
    """Mock OpenAI client that simulates moderation API"""

    class Moderations:
        async def create(self, input: str) -> MockModerationResponse:
            """Simulate OpenAI moderation endpoint"""
            return MockModerationResponse(input)

    def __init__(self, api_key: str = "mock-key"):
        self.api_key = api_key
        self.moderations = self.Moderations()


class MockMessageContent:
    """Mock Anthropic message content"""
    def __init__(self, text: str):
        self.text = text
        self.type = "text"


class MockMessage:
    """Mock Anthropic message response"""
    def __init__(self, response_text: str):
        self.content = [MockMessageContent(response_text)]
        self.model = "claude-3-5-sonnet-20241022"
        self.role = "assistant"


class MockAnthropicClient:
    """Mock Anthropic client for testing"""

    class Messages:
        async def create(self, model: str, messages: List[Dict], max_tokens: int) -> MockMessage:
            """Simulate Anthropic Claude API"""
            # Extract user's content from messages
            user_content = ""
            for msg in messages:
                if msg.get("role") == "user":
                    user_content = msg.get("content", "")

            # Simple keyword-based moderation response
            is_safe = not any(word in user_content.lower() for word in ["violence", "hate", "nsfw", "spam", "attack"])

            # Determine violation type
            violation_type = "none"
            if "hate" in user_content.lower():
                violation_type = "hate_speech"
            elif "violence" in user_content.lower() or "attack" in user_content.lower():
                violation_type = "violence"
            elif "nsfw" in user_content.lower() or "adult" in user_content.lower():
                violation_type = "adult_content"
            elif "spam" in user_content.lower():
                violation_type = "spam"

            # Create structured JSON response
            response_json = {
                "is_safe": is_safe,
                "confidence": 0.75 if not is_safe else 0.95,
                "violation_type": violation_type,
                "reasoning": f"Content analyzed for policy violations. {'Potential violation detected.' if not is_safe else 'No violations found.'}"
            }

            return MockMessage(json.dumps(response_json))

    def __init__(self, api_key: str = "mock-key"):
        self.api_key = api_key
        self.messages = self.Messages()
