import logging
from config.settings import LOGGING_CONFIG

logger = logging.getLogger(__name__)

class GoogleSheetsProvider:
    """Mock implementation for Google Sheets logging."""
    def __init__(self):
        self.enabled = LOGGING_CONFIG["google_sheets"]["enabled"]
        self.spreadsheet_id = LOGGING_CONFIG["google_sheets"]["spreadsheet_id"]

    def log(self, data: dict):
        if not self.enabled:
            return
        
        # In a real implementation, this would use google-api-python-client
        logger.info(f"[Mock Google Sheets] Logging to {self.spreadsheet_id}: {data}")
