from typing import Any, Dict

# Service Configurations
SERVICE_CONFIGS = {
    "ElevenLabs": {
        "retry": {
            "max_attempts": 3,
            "initial_delay": 5,
            "exponential_base": 2,
        },
        "circuit_breaker": {
            "failure_threshold": 3,
            "recovery_timeout": 30, # seconds
        },
        "health_check": {
            "interval": 60, # seconds
        }
    },
    "LLM": {
        "retry": {
            "max_attempts": 3,
            "initial_delay": 2,
            "exponential_base": 1.5,
        },
        "circuit_breaker": {
            "failure_threshold": 5,
            "recovery_timeout": 60,
        },
        "health_check": {
            "interval": 30,
        }
    },
    "CRM": {
        "retry": {
            "max_attempts": 2,
            "initial_delay": 1,
            "exponential_base": 2,
        },
        "circuit_breaker": {
            "failure_threshold": 3,
            "recovery_timeout": 120,
        },
        "health_check": {
            "interval": 120,
        }
    }
}

# Alerting Configurations
ALERTS_CONFIG = {
    "email": {
        "enabled": True,
        "recipient": "admin@example.com",
    },
    "telegram": {
        "enabled": True,
        "bot_token": "MOCK_TOKEN",
        "chat_id": "MOCK_CHAT_ID",
    },
    "webhook": {
        "enabled": True,
        "url": "https://hooks.example.com/alerts",
    }
}

# Logging Configuration
LOGGING_CONFIG = {
    "local_file": "app_errors.log",
    "google_sheets": {
        "enabled": True,
        "spreadsheet_id": "MOCK_SPREADSHEET_ID",
    }
}
