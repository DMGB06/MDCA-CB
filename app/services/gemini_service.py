import logging
from google import genai
from app.config.settings import settings
from tenacity import (
    retry,
    stop_after_attempt,
    wait_fixed,
    retry_if_exception_type)
import asyncio

from app.services.circuit_breaker import CircuitBreaker

logger = logging.getLogger(__name__)


class GeminiService:
    def __init__(self):
        if not settings.gemini_api_key:
            raise ValueError("Gemini API key no configurada.")

        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model_name = settings.gemini_model
        self.breaker = CircuitBreaker(
            fail_max=settings.gemini_cb_fail_max,
            reset_timeout=settings.gemini_cb_reset_timeout_seconds,
        )

    @retry(
        stop=stop_after_attempt(settings.gemini_max_retries),
        wait=wait_fixed(settings.gemini_retry_wait_seconds),
        retry=retry_if_exception_type((
            TimeoutError,
            ConnectionError,
            genai.errors.APIError)),
        reraise=True
    )
    async def _chat_with_retry(self, prompt: str) -> str:
        response = await asyncio.wait_for(
            asyncio.to_thread(
                self.client.models.generate_content,
                model=self.model_name,
                contents=prompt
            ),
            timeout=settings.gemini_timeout_seconds
        )
        return (response.text
                if response.text
                else "No pude generar una respuesta.")

    async def chat(self, prompt: str) -> str:
        logger.info("Llamando a Gemini API")
        self.breaker.before_call()

        try:
            result = await self._chat_with_retry(prompt)
            self.breaker.record_success()
            return result
        except asyncio.TimeoutError as e:
            self.breaker.record_failure()
            logger.error(f"Timeout al llamar a Gemini API: {str(e)}")
            raise TimeoutError("Timeout en Gemini API.") from e
        except Exception as e:
            self.breaker.record_failure()
            logger.error(f"Error en Gemini API: {str(e)}")
            raise


gemini_service = GeminiService()
