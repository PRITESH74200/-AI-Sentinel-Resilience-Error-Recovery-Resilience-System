import logging
from .base import AlertProvider
from config.settings import ALERTS_CONFIG

logger = logging.getLogger(__name__)

class WebhookAlertProvider(AlertProvider):
    def __init__(self):
        self.config = ALERTS_CONFIG["webhook"]

    def send(self, title: str, message: str):
        if not self.config["enabled"]:
            return
        
        url = self.config["url"]
        logger.info(f"[Alert] Sending Webhook to {url}: {title} - {message}")
