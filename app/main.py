import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.config.settings import settings
from app.routers import health
from app.routers import chat
from app.utils import setup_logging
from app.middleware.metrics import MetricsMiddleware

# Configurar logging estructurado en JSON
setup_logging()

app = FastAPI(
    title=settings.app_name,
    description="Asistente virtual inteligente para servicios municipales",
    version="0.1.0",
    debug=settings.debug
)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Middleware de métricas (debe ir ANTES de CORS)
app.add_middleware(MetricsMiddleware)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(health.router)
# Registrar router de chat
app.include_router(chat.router)

@app.get("/")
async def root():
    """Endpoint raíz - información básica del servicio."""
    return {
        "message": "Chatbot Municipal API",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health"
    }