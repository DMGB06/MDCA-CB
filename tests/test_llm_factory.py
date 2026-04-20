import pytest

from app.infrastructure.llm.factory import create_llm_provider
from app.infrastructure.llm.providers.mock_provider import MockLLMProvider


def test_factory_returns_mock_provider():
    provider = create_llm_provider("mock")
    assert isinstance(provider, MockLLMProvider)


def test_factory_rejects_unknown_provider():
    with pytest.raises(ValueError, match="LLM provider no soportado"):
        create_llm_provider("desconocido")
