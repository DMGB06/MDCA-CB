import asyncio
import logging

from google import genai
from tenacity import (
    AsyncRetrying,
    retry_if_exception_type,
    stop_after_attempt,
    wait_fixed,
)

from app.shared.config.settings import settings
from app.infrastructure.resilience.circuit_breaker import CircuitBreaker
from app.domain.models.models import (
    LLMChatRequest,
    LLMChatResponse,
    LLMHealthResponse,
)

logger = logging.getLogger(__name__)

_GENAI_API_ERROR = getattr(getattr(genai, "errors", None),
                           "APIError", RuntimeError)


class GeminiProvider:
    def __init__(self):
        if not settings.gemini_api_key:
            raise ValueError("Gemini API key no configurada.")

        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model_name = settings.gemini_model
        self.breaker = CircuitBreaker(
            fail_max=settings.gemini_cb_fail_max,
            reset_timeout=settings.gemini_cb_reset_timeout_seconds,
        )

    async def _chat_with_retry(self, prompt: str) -> str:
        retries = max(1, settings.gemini_max_retries)
        retry_wait = max(0, settings.gemini_retry_wait_seconds)

        async for attempt in AsyncRetrying(
            stop=stop_after_attempt(retries),
            wait=wait_fixed(retry_wait),
            retry=retry_if_exception_type((
                TimeoutError,
                ConnectionError,
                _GENAI_API_ERROR,
            )),
            reraise=True,
        ):
            with attempt:
                response = await asyncio.wait_for(
                    asyncio.to_thread(
                        self.client.models.generate_content,
                        model=self.model_name,
                        contents=prompt,
                    ),
                    timeout=settings.gemini_timeout_seconds,
                )
                text = getattr(response, "text", None)
                return text if text else "No pude generar una respuesta."

        raise RuntimeError("No se pudo obtener respuesta de Gemini.")

    async def chat(self, request: LLMChatRequest) -> LLMChatResponse:
        logger.info("Llamando a Gemini API")
        self.breaker.before_call()

        try:
            text = await self._chat_with_retry(request.prompt)
            self.breaker.record_success()
            return LLMChatResponse(text=text, model=self.model_name)
        except asyncio.TimeoutError as e:
            self.breaker.record_failure()
            logger.error(f"Timeout al llamar a Gemini API: {str(e)}")
            raise TimeoutError("Timeout en Gemini API.") from e
        except Exception as e:
            self.breaker.record_failure()
            logger.error(f"Error en Gemini API: {str(e)}")
            raise

    async def health_check(self) -> LLMHealthResponse:
        if not settings.gemini_api_key:
            return LLMHealthResponse(
                ok=False,
                provider="gemini",
                detail="GEMINI_API_KEY no configurada",
            )
        return LLMHealthResponse(
            ok=True,
            provider="gemini",
            detail=f"model={self.model_name}",
        )
