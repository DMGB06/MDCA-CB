import logging
import re
from app.services.knowledge_service import search_knowledge
from app.services.gemini_service import gemini_service

# Configuración del logger para este archivo
logger = logging.getLogger(__name__)


def sanitize_input(text: str) -> str:
    text = text.replace("\x00", "")
    text = re.sub(r"[\x00-\x1f\x7f]", " ", text)
    text = " ".join(text.split())
    return text.strip()


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
        respuesta = await gemini_service.chat(prompt)
        logger.info("Respuesta generada correctamente.")
        return respuesta
    except Exception as e:
        logger.error(f"Error al generar respuesta: {str(e)}")
        raise
