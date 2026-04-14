import logging
from fastapi import APIRouter, HTTPException, status, WebSocket, WebSocketDisconnect, Request, Depends
from app.models.chat import ChatRequest, ChatResponse
from app.services.chat_service import process_message
from app.middleware.rate_limit import limiter
from app.auth import verify_api_key
from app.config.settings import settings

router = APIRouter(prefix="/chat", tags=["chat"])
logger = logging.getLogger(__name__)


@router.post("/", response_model=ChatResponse, dependencies=[Depends(verify_api_key)])
@limiter.limit("5/minute")
async def chat_endpoint(payload: ChatRequest, request: Request) -> ChatResponse:
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
    origin = websocket.headers.get("origin")
    allowed_origins = settings.origins_list

    # Rechaza origen no permitido (si no usas "*")
    if allowed_origins != ["*"] and origin not in allowed_origins:
        await websocket.close(code=1008, reason="Origin no permitido")
        return

    await websocket.accept()
    history = []

    try:
        while True:
            data = await websocket.receive_text()

            if not data.strip():
                await websocket.send_json({"error": "Mensaje vacío"})
                continue

            if len(data) > settings.max_message_length:
                await websocket.send_json({"error": "Mensaje demasiado largo"})
                continue

            respuesta = await process_message(data, history)
            history.append({"user": data, "bot": respuesta})
            if len(history) > 10:
                history = history[-10:]

            await websocket.send_json({"response": respuesta})
    except WebSocketDisconnect:
        logger.info("WebSocket desconectado")
    except Exception:
        logger.exception("Error interno en WebSocket")
        await websocket.send_json({"error": "Error interno del servidor"})