from typing import Dict
from .breaker import CircuitBreaker
from config.settings import SERVICE_CONFIGS

class CircuitBreakerRegistry:
    _instances: Dict[str, CircuitBreaker] = {}

    @classmethod
    def get_breaker(cls, service_name: str) -> CircuitBreaker:
        if service_name not in cls._instances:
            settings = SERVICE_CONFIGS.get(service_name, {}).get("circuit_breaker", {})
            cls._instances[service_name] = CircuitBreaker(
                service_name=service_name,
                failure_threshold=settings.get("failure_threshold", 3),
                recovery_timeout=settings.get("recovery_timeout", 30)
            )
        return cls._instances[service_name]
