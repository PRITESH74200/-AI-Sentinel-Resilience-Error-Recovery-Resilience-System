from .email_provider import EmailAlertProvider
from .telegram_provider import TelegramAlertProvider
from .webhook_provider import WebhookAlertProvider

class AlertManager:
    def __init__(self):
        self.providers = [
            EmailAlertProvider(),
            TelegramAlertProvider(),
            WebhookAlertProvider()
        ]

    def trigger(self, title: str, message: str):
        for provider in self.providers:
            provider.send(title, message)
