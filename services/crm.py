from .base import ExternalService

class CRMService(ExternalService):
    def __init__(self):
        super().__init__("CRM")

    def process(self, data: dict) -> bool:
        return True
