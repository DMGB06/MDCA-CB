import pytest

from app.domain.models.models import LLMChatRequest
from app.infrastructure.llm.providers.mock_provider import MockLLMProvider


@pytest.mark.asyncio
async def test_mock_provider_returns_configured_response():
    provider = MockLLMProvider(response_text="ok-mock")
    response = await provider.chat(LLMChatRequest(prompt="hola"))

    assert response.text == "ok-mock"
    assert response.model == "mock-llm"
    assert len(provider.calls) == 1


@pytest.mark.asyncio
async def test_mock_provider_can_simulate_failure():
    provider = MockLLMProvider(should_fail=True)

    with pytest.raises(RuntimeError, match="Mock provider configurado para fallar"):
        await provider.chat(LLMChatRequest(prompt="hola"))


@pytest.mark.asyncio
async def test_mock_provider_health_check():
    provider = MockLLMProvider()
    health = await provider.health_check()

    assert health.ok is True
    assert health.provider == "mock"
