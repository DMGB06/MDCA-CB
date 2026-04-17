import pytest
from app.services.gemini_service import GeminiService


@pytest.mark.asyncio
async def test_retry_success_on_third_attempt(monkeypatch):
    svc = GeminiService()
    calls = {"n": 0}

    monkeypatch.setattr(
        "app.services.gemini_service.settings.gemini_timeout_seconds",
        0.1)
    monkeypatch.setattr(
        "app.services.gemini_service.settings.gemini_max_retries",
        3)
    monkeypatch.setattr(
        "app.services.gemini_service.settings.gemini_retry_wait_seconds",
        0)

    def flaky_generate_content(**kwargs):
        calls["n"] += 1
        if calls["n"] < 3:
            raise ConnectionError("transitorio")

        class R:
            text = "ok"

        return R()

    monkeypatch.setattr(
        svc.client.models, "generate_content", flaky_generate_content)

    out = await svc.chat("hola")
    assert out == "ok"
    assert calls["n"] == 3


@pytest.mark.asyncio
async def test_timeout_raises_fast(monkeypatch):
    svc = GeminiService()

    monkeypatch.setattr(
        "app.services.gemini_service.settings.gemini_timeout_seconds",
        0.1)
    monkeypatch.setattr(
        "app.services.gemini_service.settings.gemini_max_retries",
        2)
    monkeypatch.setattr(
        "app.services.gemini_service.settings.gemini_retry_wait_seconds",
        0)

    def always_fail(**kwargs):
        raise TimeoutError("timeout inmediato")

    monkeypatch.setattr(svc.client.models, "generate_content", always_fail)

    with pytest.raises(Exception):
        await svc.chat("hola")
