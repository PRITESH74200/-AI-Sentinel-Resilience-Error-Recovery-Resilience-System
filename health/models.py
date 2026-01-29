from dataclasses import dataclass
from datetime import datetime

@dataclass
class HealthStatus:
    service_name: str
    is_healthy: bool
    last_check: datetime
    details: str = ""
