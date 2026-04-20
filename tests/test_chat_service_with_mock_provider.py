import pytest

from app.domain.services.chat_service import (
    process_message,
    reset_llm_provider,
    set_llm_provider,
)
from app.infrastructure.llm.providers.mock_provider import MockLLMProvider


@pytest.mark.asyncio
async def test_process_message_uses_injected_mock_provider():
    set_llm_provider(MockLLMProvider(response_text="respuesta-desde-mock"))

    try:
        output = await process_message("hola")
    finally:
        reset_llm_provider()

    assert output == "respuesta-desde-mock"
