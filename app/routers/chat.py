import logging
from fastapi import APIRouter, HTTPException, status, WebSocket, WebSocketDisconnect
from app.models.chat import ChatRequest, ChatResponse
from app.services.chat_service import process_message
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.extension import Limiter


from app.main import limiter

router = APIRouter(prefix="/chat", tags=["chat"])
logger = logging.getLogger(__name__)

@router.post("/", response_model=ChatResponse)
@limiter.limit("5/minute") 
async def chat_endpoint(payload: ChatRequest) -> ChatResponse:
    """
    Recibe un mensaje del usuario y responde usando Gemini.
    """
    try:
        respuesta = await process_message(payload.message)
        return ChatResponse(response=respuesta)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar mensaje: {str(e)}"
        )

@router.websocket("/ws")
async def websocket_chat(websocket: WebSocket):
    logger.info("Nueva conexión WebSocket establecida.")
    await websocket.accept()
    history = []
    try:
        while True:
            data = await websocket.receive_text()
            try:
                respuesta = await process_message(data, history)
                history.append({"user": data, "bot": respuesta})
                if len(history) > 10:
                    history = history[-10:]
                await websocket.send_json({"response": respuesta})
            except Exception as e:
                await websocket.send_json({"error": f"Error al procesar mensaje: {str(e)}"})
    except WebSocketDisconnect:
        pass