from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.domain.services.chat_service import process_message
router = APIRouter()


@router.websocket("/ws")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    history = []
    try:
        while True:
            data = await websocket.receive_text()
            try:
                respuesta = await process_message(data, history)
                history.append({"user": data, "bot": respuesta})
                await websocket.send_json({"response": respuesta})
            except Exception as e:
                await websocket.send_json(
                    {"error": f"Error al procesar mensaje: {str(e)}"}
                )
    except WebSocketDisconnect:

        pass
