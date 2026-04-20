import os
import pytest
from fastapi.testclient import TestClient

# Variables mínimas para que app/main importe sin romper
os.environ.setdefault("GEMINI_API_KEY", "test-gemini-key")
os.environ.setdefault("API_KEY", "test-api-key")
os.environ.setdefault(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://localhost:8080")
os.environ.setdefault("ALLOWED_CREDENTIALS", "false")
os.environ.setdefault("MAX_MESSAGE_LENGTH", "500")


@pytest.fixture
def client():
    from app.main import app
    from app.domain.services.chat_service import (
        reset_llm_provider,
        set_llm_provider,
    )
    from app.infrastructure.llm.providers.mock_provider import MockLLMProvider

    set_llm_provider(MockLLMProvider(response_text="respuesta-mock"))

    with TestClient(app) as test_client:
        yield test_client

    reset_llm_provider()
