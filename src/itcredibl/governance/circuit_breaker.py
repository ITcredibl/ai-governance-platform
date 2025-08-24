"""
Basic Circuit Breaker pattern.
Compatible with Python 3.13.
"""
import time
from enum import Enum
from typing import Callable, Any
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)

class CircuitState(str, Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitOpenError(Exception):
    """Exception raised when circuit is open."""
    pass

class BasicCircuitBreaker:
    """Basic circuit breaker for resilience."""
    
    def __init__(self, name: str, failure_threshold: int = 5, reset_timeout: int = 60):
        self.name = name
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.failures = 0
        self.state = CircuitState.CLOSED
        self.last_failure_time = 0.0
    
    @contextmanager
    def protect(self):
        """Context manager for circuit breaker protection."""
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.reset_timeout:
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitOpenError(f"Circuit {self.name} is open")
        
        try:
            yield
            self._record_success()
        except Exception as e:
            self._record_failure()
            raise
    
    def _record_success(self):
        """Record a successful operation."""
        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.CLOSED
            self.failures = 0
    
    def _record_failure(self):
        """Record a failed operation."""
        self.failures += 1
        self.last_failure_time = time.time()
        
        if self.failures >= self.failure_threshold or self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.OPEN
            logger.warning(f"Circuit {self.name} tripped to OPEN state")