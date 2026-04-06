"""Provider registry."""

from __future__ import annotations

from ai_stability.exceptions import ConfigurationError
from ai_stability.providers.base import ModelProvider
from ai_stability.providers.openai_provider import OpenAIProvider


def get_provider(provider_name: str) -> ModelProvider:
    """Resolve the configured provider."""
    normalized_name = provider_name.strip().lower()
    if normalized_name == "openai":
        return OpenAIProvider()

    raise ConfigurationError(
        f"Unsupported provider '{provider_name}'. Supported providers: openai."
    )
