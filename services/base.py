from abc import ABC, abstractmethod
from typing import Any

class ExternalService(ABC):
    def __init__(self, name: str):
        self.name = name
        self.is_healthy = True

    @abstractmethod
    def process(self, data: Any) -> Any:
        pass

    def check_health(self) -> bool:
        # Simulations might toggle this
        return self.is_healthy
