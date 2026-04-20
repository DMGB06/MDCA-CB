from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class LLMChatRequest:
    prompt: str
    history: list[dict[str, str]] = field(default_factory=list)
    temperature: float = 0.2


@dataclass(slots=True)
class LLMChatResponse:
    text: str
    model: str
    tokens_used: int | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class LLMHealthResponse:
    ok: bool
    provider: str
    detail: str | None = None
