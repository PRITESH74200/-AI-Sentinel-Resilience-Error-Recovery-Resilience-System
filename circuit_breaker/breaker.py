import time
import logging
from .states import CircuitState
from exceptions.base import TransientError, AgentException

logger = logging.getLogger(__name__)

class CircuitBreaker:
    def __init__(self, service_name: str, failure_threshold: int, recovery_timeout: float):
        self.service_name = service_name
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = None

    def call(self, func, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            elapsed = time.time() - self.last_failure_time
            if elapsed > self.recovery_timeout:
                logger.info(f"Circuit for {self.service_name} moving to HALF_OPEN (timeout elapsed: {elapsed:.1f}s)")
                self.state = CircuitState.HALF_OPEN
            else:
                raise AgentException(f"Circuit Breaker for {self.service_name} is OPEN. Failing fast.", self.service_name)

        try:
            result = func(*args, **kwargs)
            self._handle_success()
            return result
        except TransientError:
            self._handle_failure()
            raise
        except Exception:
            raise

    def _handle_success(self):
        if self.state == CircuitState.HALF_OPEN:
            logger.info(f"Circuit for {self.service_name} reset to CLOSED after successful probe")
        self.state = CircuitState.CLOSED
        self.failure_count = 0

    def _handle_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        logger.warning(f"Circuit for {self.service_name} recorded failure {self.failure_count}/{self.failure_threshold}")
        
        if self.failure_count >= self.failure_threshold:
            if self.state != CircuitState.OPEN:
                logger.error(f"Circuit for {self.service_name} opened!")
                self.state = CircuitState.OPEN
