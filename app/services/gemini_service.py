import google.generativeai as genai
from app.config.settings import settings
from typing import Optional
import asyncio

class GeminiService:
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.gemini_api_key
        self.model_name = model or settings.gemini_model
        if not self.api_key:
            raise ValueError("Gemini API key no configurada.")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)

    async def chat(self, prompt: str) -> str:
        try:
            # Ejecuta en un thread separado para no bloquear FastAPI
            response = await asyncio.to_thread(
                self.model.generate_content, prompt
            )
            return response.text if response.text else "No pude generar una respuesta."
        except Exception as e:
            raise Exception(f"Error en Gemini API: {str(e)}")

gemini_service = GeminiService()