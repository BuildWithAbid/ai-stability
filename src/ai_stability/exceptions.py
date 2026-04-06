"""Custom exceptions for ai-stability."""


class AIStabilityError(Exception):
    """Base exception for user-facing CLI errors."""


class ConfigurationError(AIStabilityError):
    """Raised when required configuration is missing or invalid."""


class PromptError(AIStabilityError):
    """Raised when the prompt input cannot be used."""


class ProviderError(AIStabilityError):
    """Raised when a provider call fails."""
