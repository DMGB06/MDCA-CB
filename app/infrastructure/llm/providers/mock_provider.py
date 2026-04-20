from app.domain.models.models import (
    LLMChatRequest,
    LLMChatResponse,
    LLMHealthResponse,
)


class MockLLMProvider:
    def __init__(self,
                 response_text: str = "respuesta-mock",
                 should_fail: bool = False):
        self.response_text = response_text
        self.should_fail = should_fail
        self.calls: list[LLMChatRequest] = []

    async def chat(self, request: LLMChatRequest) -> LLMChatResponse:
        self.calls.append(request)
        if self.should_fail:
            raise RuntimeError("Mock provider configurado para fallar")

        return LLMChatResponse(
            text=self.response_text,
            model="mock-llm",
            tokens_used=0,
        )

    async def health_check(self) -> LLMHealthResponse:
        return LLMHealthResponse(
            ok=not self.should_fail,
            provider="mock",
            detail=None if not self.should_fail else "mock-failure-enabled",
        )
