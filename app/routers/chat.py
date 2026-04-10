import logging
from fastapi import APIRouter, HTTPException, status, WebSocket, WebSocketDisconnect, Request, Depends
from app.models.chat import ChatRequest, ChatResponse
from app.services.chat_service import process_message
from app.middleware.rate_limit import limiter
from app.auth import verify_api_key, verify_api_key_value

router = APIRouter(prefix="/chat", tags=["chat"])
logger = logging.getLogger(__name__)

@router.post("/", response_model=ChatResponse, dependencies=[Depends(verify_api_key)])
@limiter.limit("5/minute")
async def chat_endpoint(payload: ChatRequest, request: Request) -> ChatResponse:
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
    api_key = websocket.query_params.get("api_key")
    try:
        verify_api_key_value(api_key)
    except HTTPException:
        await websocket.close(code=1008, reason="API key inválida o ausente")
        return

    await websocket.accept()
    history = []

    try:
        while True:
            data = await websocket.receive_text()
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