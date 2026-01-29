from .base import PermanentError

class AuthenticationError(PermanentError):
    """Mapped to 401 errors."""
    pass

class InvalidPayloadError(PermanentError):
    """Mapped to 400 errors."""
    pass

class QuotaExceededError(PermanentError):
    """Mapped to 403 or quota specific errors."""
    pass
