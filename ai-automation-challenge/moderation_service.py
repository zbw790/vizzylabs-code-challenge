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
        """
        Moderate content using OpenAI with Anthropic fallback.
        Implements timeout and error handling with automatic fallback.
        """
        # Try OpenAI first with timeout
        try:
            result = await asyncio.wait_for(
                self._moderate_with_openai(request.content),
                timeout=self.timeout
            )
            return result
        except asyncio.TimeoutError:
            # OpenAI timed out, fallback to Anthropic
            print(f"OpenAI timeout after {self.timeout}s, falling back to Anthropic")
        except Exception as e:
            # OpenAI failed for other reasons, fallback to Anthropic
            print(f"OpenAI error: {str(e)}, falling back to Anthropic")
        
        # Fallback to Anthropic
        try:
            result = await asyncio.wait_for(
                self._moderate_with_anthropic(request.content),
                timeout=self.timeout
            )
            return result
        except asyncio.TimeoutError:
            raise Exception(f"Anthropic timeout after {self.timeout}s - both providers failed")
        except Exception as e:
            raise Exception(f"Both moderation providers failed. Anthropic error: {str(e)}")

    async def _moderate_with_openai(self, content: str) -> ModerationResult:
        """Call OpenAI moderation API"""
        response = await self.openai_client.moderations.create(input=content)
        result = response.results[0]

        # Extract violation type and confidence from actual API response
        violation_type = ViolationType.NONE
        max_confidence = 0.0
        reasoning_parts = []

        # Map OpenAI categories to our ViolationType
        category_mapping = {
            'hate': ViolationType.HATE_SPEECH,
            'violence': ViolationType.VIOLENCE,
            'sexual': ViolationType.ADULT_CONTENT,
            'spam': ViolationType.SPAM,
        }

        # Find the highest scoring violation
        for category, violation in category_mapping.items():
            if category in result.category_scores:
                score = result.category_scores[category]
                if score > max_confidence:
                    max_confidence = score
                    if result.categories.get(category, False):
                        violation_type = violation
                        reasoning_parts.append(f"{category}: {score:.2f}")

        # If no violation found, use low confidence score
        if violation_type == ViolationType.NONE:
            # Get the max score even if not flagged
            all_scores = result.category_scores.values() if hasattr(result.category_scores, 'values') else []
            max_confidence = max(all_scores) if all_scores else 0.05
            reasoning = f"No violations detected. Max score: {max_confidence:.2f}"
        else:
            reasoning = f"Detected violations: {', '.join(reasoning_parts)}"

        return ModerationResult(
            is_safe=not result.flagged,
            confidence=max_confidence,
            violation_type=violation_type,
            reasoning=reasoning,
            provider="openai"
        )

    async def _moderate_with_anthropic(self, content: str) -> ModerationResult:
        """Call Anthropic Claude API as fallback"""
        # Craft prompt for structured JSON output
        prompt = f"""Analyze the following content for policy violations and return your analysis as valid JSON.

Content to analyze: "{content}"

You must respond with ONLY valid JSON matching this exact structure (no additional text):
{{
  "is_safe": true or false,
  "confidence": a number between 0.0 and 1.0,
  "violation_type": one of ["hate_speech", "violence", "adult_content", "spam", "none"],
  "reasoning": "brief explanation of your decision"
}}

Policy guidelines:
- hate_speech: hateful, discriminatory, or harassing content
- violence: violent, threatening, or harmful content
- adult_content: sexual, NSFW, or adult content
- spam: promotional, repetitive, or spammy content
- none: safe, appropriate content

Respond only with the JSON object, no other text."""

        # Call Anthropic API
        response = await self.anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Extract text from response
        response_text = response.content[0].text

        # Parse JSON response
        parsed = self._parse_llm_response(response_text)

        return ModerationResult(
            is_safe=parsed["is_safe"],
            confidence=parsed["confidence"],
            violation_type=ViolationType(parsed["violation_type"]),
            reasoning=parsed["reasoning"],
            provider="anthropic"
        )

    def _parse_llm_response(self, response_text: str) -> dict:
        """Parse structured JSON from LLM response"""
        try:
            # Try to parse as JSON directly
            return json.loads(response_text)
        except json.JSONDecodeError:
            # Try to extract JSON from markdown code blocks
            import re
            json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1))
            
            # Try to find JSON object in text
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
            
            # If all parsing fails, return safe default
            return {
                "is_safe": True,
                "confidence": 0.5,
                "violation_type": "none",
                "reasoning": "Failed to parse LLM response"
            }
