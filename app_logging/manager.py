from .logger import setup_logger, StructuredLogger
from .google_sheets_provider import GoogleSheetsProvider

class LogManager:
    def __init__(self):
        self.base_logger = setup_logger()
        self.structured_logger = StructuredLogger(self.base_logger)
        self.gs_provider = GoogleSheetsProvider()

    def info(self, message: str):
        self.base_logger.info(message)

    def error(self, service_name: str, category: str, message: str, retry_count: int = 0, state: str = "N/A"):
        # Log to local file
        self.structured_logger.log_event(service_name, category, message, retry_count, state)
        
        # Log to Google Sheets
        self.gs_provider.log({
            "service": service_name,
            "category": category,
            "message": message,
            "retry": retry_count,
            "state": state
        })
