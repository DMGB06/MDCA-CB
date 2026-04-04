from app.services.knowledge_service import search_knowledge
from app.services.gemini_service import gemini_service

async def process_message(message: str, history=None) -> str:
    if history is None:
        history = []

    # 1. Buscar en la base local
    local_info = search_knowledge(message)

    # 2. Siempre pasa por Gemini, pero con contexto diferente
    if local_info:
        # Modo estricto: Gemini usa solo la info del municipio
        prompt = f"""Eres el asistente virtual de la Municipalidad.
Usa SOLO la siguiente información para responder. 
No inventes datos adicionales.

INFORMACIÓN MUNICIPAL:
{local_info}

PREGUNTA DEL CIUDADANO: {message}"""
    else:
        # Modo libre: Gemini responde con conocimiento general
        prompt = f"""Eres el asistente virtual de la Municipalidad.
No tienes información específica sobre esta consulta.
Responde de forma útil y sugiere contactar al municipio para consultas específicas.

PREGUNTA: {message}"""

    return await gemini_service.chat(prompt)