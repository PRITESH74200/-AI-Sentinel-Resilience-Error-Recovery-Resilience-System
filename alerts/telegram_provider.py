import logging
from .base import AlertProvider
from config.settings import ALERTS_CONFIG

logger = logging.getLogger(__name__)

class TelegramAlertProvider(AlertProvider):
    def __init__(self):
        self.config = ALERTS_CONFIG["telegram"]

    def send(self, title: str, message: str):
        if not self.config["enabled"]:
            return
        
        chat_id = self.config["chat_id"]
        logger.info(f"[Alert] Sending Telegram message to {chat_id}: {title} - {message}")
