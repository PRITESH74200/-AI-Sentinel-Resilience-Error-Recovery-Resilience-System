from .base import ExternalService
from exceptions.transient import TimeoutError

class LLMService(ExternalService):
    def __init__(self):
        super().__init__("LLM")
        self.fail_next = False

    def process(self, prompt: str) -> str:
        if self.fail_next:
            raise TimeoutError("LLM Request Timeout", self.name)
        return f"LLM response to: {prompt}"
