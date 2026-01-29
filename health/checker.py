import logging
import threading
import time
from typing import List
from services.base import ExternalService
from circuit_breaker.registry import CircuitBreakerRegistry
from circuit_breaker.states import CircuitState

logger = logging.getLogger(__name__)

class HealthChecker:
    def __init__(self, services: List[ExternalService]):
        self.services = services
        self.running = False
        self._thread = None

    def start(self, interval: int = 10):
        self.running = True
        self._thread = threading.Thread(target=self._run, args=(interval,), daemon=True)
        self._thread.start()

    def _run(self, interval: int):
        while self.running:
            for service in self.services:
                is_healthy = service.check_health()
                breaker = CircuitBreakerRegistry.get_breaker(service.name)
                
                if is_healthy and breaker.state == CircuitState.OPEN:
                    logger.info(f"Health Check: {service.name} is now healthy. Checking if we can half-open/reset.")
                    # Let the circuit breaker's own logic handle the transition 
                    # based on time, OR we can force it here if health is guaranteed.
                    # Usually, health check acts as a trigger.
            
            time.sleep(interval)

    def stop(self):
        self.running = False
