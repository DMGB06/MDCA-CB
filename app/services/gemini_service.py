import logging
from google import genai
from app.config.settings import settings
import asyncio

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        if not settings.gemini_api_key:
            raise ValueError("Gemini API key no configurada.")
        
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model_name = settings.gemini_model

    async def chat(self, prompt: str) -> str:
        logger.info("Llamando a Gemini API")
        try:
            response = await asyncio.to_thread(
                self.client.models.generate_content,
                model=self.model_name,
                contents=prompt
            )
            resultado = response.text if response.text else "No pude generar una respuesta."
            logger.info("Respuesta de Gemini recibida correctamente.")
            return resultado
        except Exception as e:
            logger.error(f"Error en Gemini API: {str(e)}")
            raise Exception(f"Error en Gemini API: {str(e)}")

gemini_service = GeminiService()