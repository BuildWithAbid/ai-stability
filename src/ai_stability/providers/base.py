"""Provider interface."""

from __future__ import annotations

from typing import Protocol


class ModelProvider(Protocol):
    """Minimal provider contract for repeated text generation."""

    def generate(self, prompt: str, model: str, temperature: float) -> str:
        """Generate text for the given prompt."""
