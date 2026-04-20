from app.shared.config.settings import settings
from app.domain.models.models import LLMChatRequest
from app.infrastructure.llm.providers.gemini_provider import GeminiProvider


class GeminiService:
    """
    Adaptador de compatibilidad para no romper imports existentes.
    La implementación real vive en GeminiProvider.
    """

    def __init__(self):
        self.settings = settings
        self._provider = GeminiProvider()
        self.client = self._provider.client
        self.model_name = self._provider.model_name
        self.breaker = self._provider.breaker

    async def chat(self, prompt: str) -> str:
        response = await self._provider.chat(LLMChatRequest(prompt=prompt))
        return response.text

    async def health_check(self) -> bool:
        health = await self._provider.health_check()
        return health.ok


gemini_service = GeminiService()
