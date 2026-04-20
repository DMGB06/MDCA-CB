from app.shared.config.settings import settings
from app.domain.protocols.protocols import LLMProvider
from app.infrastructure.llm.providers.gemini_provider import GeminiProvider
from app.infrastructure.llm.providers.mock_provider import MockLLMProvider

_provider_instance: LLMProvider | None = None


def create_llm_provider(provider_name: str | None = None) -> LLMProvider:
    selected_provider = (provider_name or settings.llm_provider).strip().lower()

    if selected_provider == "gemini":
        return GeminiProvider()
    if selected_provider == "mock":
        return MockLLMProvider()

    raise ValueError(f"LLM provider no soportado: {selected_provider}")


def get_llm_provider() -> LLMProvider:
    global _provider_instance
    if _provider_instance is None:
        _provider_instance = create_llm_provider()
    return _provider_instance


def set_llm_provider(provider: LLMProvider) -> None:
    global _provider_instance
    _provider_instance = provider


def reset_llm_provider() -> None:
    global _provider_instance
    _provider_instance = None
