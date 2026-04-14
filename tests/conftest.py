import os
import pytest
from fastapi.testclient import TestClient

# Variables mínimas para que app/main importe sin romper
os.environ.setdefault("GEMINI_API_KEY", "test-gemini-key")
os.environ.setdefault("API_KEY", "test-api-key")
os.environ.setdefault("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8080")
os.environ.setdefault("ALLOWED_CREDENTIALS", "false")
os.environ.setdefault("MAX_MESSAGE_LENGTH", "500")


@pytest.fixture
def client(monkeypatch):
    from app.main import app

    async def fake_chat(_prompt: str) -> str:
        return "respuesta-mock"

    # Evita llamadas reales a Gemini
    monkeypatch.setattr("app.services.chat_service.gemini_service.chat", fake_chat)

    return TestClient(app)