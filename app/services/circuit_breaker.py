import time
from enum import Enum

class CircuitState(str, Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(self, fail_max: int, reset_timeout: int):
        self.fail_max = fail_max
        self.reset_timeout = reset_timeout
        self.fail_count = 0
        self.last_failure_time = 0.0
        self.state = CircuitState.CLOSED

    def before_call(self):
        if self.state == CircuitState.OPEN:
            if (time.time() - self.last_failure_time) >= self.reset_timeout:
                self.state = CircuitState.HALF_OPEN
            else:
                raise RuntimeError("Circuit breaker OPEN")

    def record_success(self):
        self.fail_count = 0
        self.state = CircuitState.CLOSED

    def record_failure(self):
        self.fail_count += 1
        self.last_failure_time = time.time()
        if self.fail_count >= self.fail_max:
            self.state = CircuitState.OPEN