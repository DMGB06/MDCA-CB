import pytest
from app.infrastructure.resilience.circuit_breaker import CircuitBreaker, CircuitState


def test_breaker_opens_after_fail_max():
    cb = CircuitBreaker(fail_max=3, reset_timeout=30)

    cb.record_failure()
    cb.record_failure()
    assert cb.state == CircuitState.CLOSED

    cb.record_failure()
    assert cb.state == CircuitState.OPEN


def test_breaker_blocks_when_open():
    cb = CircuitBreaker(fail_max=1, reset_timeout=30)

    cb.record_failure()  # abre circuito
    assert cb.state == CircuitState.OPEN

    with pytest.raises(RuntimeError, match="Circuit breaker OPEN"):
        cb.before_call()


def test_breaker_half_open_then_close_on_success():
    cb = CircuitBreaker(fail_max=1, reset_timeout=30)

    cb.record_failure()
    assert cb.state == CircuitState.OPEN

    # Simula que ya pasó el reset_timeout
    cb.last_failure_time -= 31

    cb.before_call()
    assert cb.state == CircuitState.HALF_OPEN

    cb.record_success()
    assert cb.state == CircuitState.CLOSED
    assert cb.fail_count == 0
