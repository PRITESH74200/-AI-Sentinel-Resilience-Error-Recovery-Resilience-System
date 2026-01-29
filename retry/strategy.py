import time
import random
import logging
from typing import Callable, Any
from exceptions.base import TransientError

logger = logging.getLogger(__name__)

class RetryStrategy:
    def __init__(self, max_attempts: int, initial_delay: float, exponential_base: float):
        self.max_attempts = max_attempts
        self.initial_delay = initial_delay
        self.exponential_base = exponential_base

    def execute(self, func: Callable, *args, **kwargs) -> Any:
        attempts = 0
        last_exception = None

        while attempts < self.max_attempts:
            try:
                return func(*args, **kwargs)
            except TransientError as e:
                attempts += 1
                last_exception = e
                
                if attempts >= self.max_attempts:
                    logger.error(f"Max retry attempts ({self.max_attempts}) reached for {e.service_name}")
                    raise

                delay = self.initial_delay * (self.exponential_base ** (attempts - 1))
                # Add jitter to avoid thundering herd
                delay += random.uniform(0, 1)
                
                logger.warning(f"Transient error in {e.service_name}: {str(e)}. Retrying in {delay:.2f}s (Attempt {attempts}/{self.max_attempts})")
                time.sleep(delay)
            except Exception:
                # Permanent errors or unexpected exceptions are not retried
                raise
        
        if last_exception:
            raise last_exception
