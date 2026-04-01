from fastapi import APIRouter
from datetime import datetime
from typing import Dict, Any

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    Endpoint de verificación de salud del servidor.
    
    Returns:
        Dict con estado del servidor y timestamp
    """
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "chatbot-municipal"
    }
