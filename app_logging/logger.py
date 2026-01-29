import logging
import json
from datetime import datetime
from config.settings import LOGGING_CONFIG

def setup_logger():
    # Configure root logger to catch all logs from modules
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # Clear existing handlers
    root_logger.handlers = []
    
    # File Handler
    fh = logging.FileHandler(LOGGING_CONFIG["local_file"])
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    
    # Console Handler
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    
    root_logger.addHandler(fh)
    root_logger.addHandler(ch)
    
    return logging.getLogger("AI_Call_Agent")

class StructuredLogger:
    def __init__(self, logger):
        self.logger = logger

    def log_event(self, service_name: str, category: str, message: str, retry_count: int = 0, state: str = "CLOSED"):
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "service": service_name,
            "category": category,
            "message": message,
            "retry_count": retry_count,
            "cb_state": state
        }
        self.logger.info(json.dumps(log_data))
