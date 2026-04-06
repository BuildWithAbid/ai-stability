"""OpenAI provider implementation."""

from __future__ import annotations

import os
from typing import Any

from openai import OpenAI, OpenAIError

from ai_stability.exceptions import ConfigurationError, ProviderError


class OpenAIProvider:
    """Generate outputs using the OpenAI Responses API."""

    def __init__(self, api_key: str | None = None) -> None:
        resolved_key = api_key or os.getenv("OPENAI_API_KEY")
        if not resolved_key:
            raise ConfigurationError("Missing OPENAI_API_KEY environment variable.")

        self._client = OpenAI(api_key=resolved_key)

    def generate(self, prompt: str, model: str, temperature: float) -> str:
        """Call the OpenAI Responses API and return plain text."""
        try:
            response = self._client.responses.create(
                model=model,
                input=prompt,
                temperature=temperature,
            )
        except OpenAIError as exc:
            raise ProviderError(f"OpenAI request failed: {exc}") from exc

        output_text = self._extract_output_text(response)
        if not output_text.strip():
            raise ProviderError("OpenAI returned an empty text response.")
        return output_text

    def _extract_output_text(self, response: Any) -> str:
        """Extract plain text from a Responses API result."""
        direct_output = getattr(response, "output_text", None)
        if isinstance(direct_output, str) and direct_output.strip():
            return direct_output.strip()

        output_blocks = getattr(response, "output", None)
        if not output_blocks:
            return ""

        text_chunks: list[str] = []
        for block in output_blocks:
            content_items = getattr(block, "content", []) or []
            for item in content_items:
                item_text = getattr(item, "text", None)
                if item_text:
                    text_chunks.append(str(item_text).strip())

        return "\n".join(chunk for chunk in text_chunks if chunk).strip()
