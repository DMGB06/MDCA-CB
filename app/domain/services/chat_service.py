import logging
import re
from app.infrastructure.knowledge.knowledge_service import search_knowledge
from app.infrastructure.llm.factory import (
    get_llm_provider,
    reset_llm_provider as reset_factory_llm_provider,
    set_llm_provider as set_factory_llm_provider,
)
from app.domain.models.models import LLMChatRequest
from app.domain.protocols.protocols import LLMProvider

# Configuración del logger para este archivo
logger = logging.getLogger(__name__)


def sanitize_input(text: str) -> str:
    text = text.replace("\x00", "")
    text = re.sub(r"[\x00-\x1f\x7f]", " ", text)
    text = " ".join(text.split())
    return text.strip()


def set_llm_provider(provider: LLMProvider) -> None:
    set_factory_llm_provider(provider)


def reset_llm_provider() -> None:
    reset_factory_llm_provider()


class _LegacyGeminiServiceAdapter:
    async def chat(self, prompt: str) -> str:
        request = LLMChatRequest(prompt=prompt)
        response = await get_llm_provider().chat(request)
        return response.text


# Compatibilidad temporal para tests existentes que parchean esta referencia.
gemini_service = _LegacyGeminiServiceAdapter()


async def process_message(message: str, history=None) -> str:
    if history is None:
        history = []

    safe_message = sanitize_input(message)
    logger.info(f"Mensaje recibido: {safe_message}")

    # 1. Buscar en la base local
    local_info = search_knowledge(safe_message)
    # 2. Siempre pasa por Gemini, pero con contexto diferente
    if local_info:
        logger.info("Respuesta usando base de conocimiento local.")
        prompt = f"""Eres el asistente virtual de la Municipalidad.
Usa SOLO la siguiente información para responder.
No inventes datos adicionales.

INFORMACIÓN MUNICIPAL:
{local_info}

PREGUNTA DEL CIUDADANO: {safe_message}"""
    else:
        logger.info("Respuesta usando Gemini (fallback).")
        prompt = f"""Eres el asistente virtual de
        la Municipalidad de Cerro Azul, Perú.
        Responde SOLO sobre Cerro Azul.
        No inventes datos, si no sabes dilo claramente.

PREGUNTA: {safe_message}"""
    try:
        llm_request = LLMChatRequest(prompt=prompt, history=history)
        llm_response = await get_llm_provider().chat(llm_request)
        respuesta = llm_response.text
        logger.info("Respuesta generada correctamente.")
        return respuesta
    except Exception as e:
        logger.error(f"Error al generar respuesta: {str(e)}")
        raise
