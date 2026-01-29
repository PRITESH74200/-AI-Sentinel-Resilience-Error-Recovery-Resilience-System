from .base import TransientError

class ServiceUnavailableError(TransientError):
    """Mapped to 503 errors."""
    pass

class TimeoutError(TransientError):
    """Mapped to network or request timeouts."""
    pass

class RateLimitError(TransientError):
    """Mapped to 429 errors (if retryable)."""
    pass
