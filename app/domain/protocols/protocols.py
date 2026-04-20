from typing import Protocol

from app.domain.models.models import (
    LLMChatRequest,
    LLMChatResponse,
    LLMHealthResponse,
)


class LLMProvider(Protocol):
    async def chat(self, request: LLMChatRequest) -> LLMChatResponse:
        ...

    async def health_check(self) -> LLMHealthResponse:
        ...
