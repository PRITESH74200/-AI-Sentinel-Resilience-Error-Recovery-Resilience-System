class AgentException(Exception):
    """Base exception for the AI Call Agent system."""
    def __init__(self, message: str, service_name: str = "Unknown"):
        super().__init__(message)
        self.service_name = service_name

class TransientError(AgentException):
    """Errors that are temporary and should be retried (e.g., 503, Timeouts)."""
    pass

class PermanentError(AgentException):
    """Errors that are fatal and should NOT be retried (e.g., 401, 400)."""
    pass
