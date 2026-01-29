import random
from .base import ExternalService
from exceptions.transient import ServiceUnavailableError
from exceptions.permanent import AuthenticationError, QuotaExceededError

class ElevenLabsService(ExternalService):
    def __init__(self):
        super().__init__("ElevenLabs")
        self.failure_mode = None # Can be set to simulate specific errors

    def process(self, text: str) -> str:
        if self.failure_mode == "503":
            raise ServiceUnavailableError("ElevenLabs 503 Service Unavailable", self.name)
        if self.failure_mode == "401":
            raise AuthenticationError("ElevenLabs 401 Unauthorized", self.name)
        
        # Default success simulation
        return f"Audio generated for: {text}"

    def simulate_outage(self):
        self.failure_mode = "503"
        self.is_healthy = False

    def simulate_recovery(self):
        self.failure_mode = None
        self.is_healthy = True
