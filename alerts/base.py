from abc import ABC, abstractmethod

class AlertProvider(ABC):
    @abstractmethod
    def send(self, title: str, message: str):
        pass
