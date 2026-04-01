from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import settings
from app.routers import health
from app.routers import chat

app = FastAPI(
    title=settings.app_name,
    description="Asistente virtual inteligente para servicios municipales",
    version="0.1.0",
    debug=settings.debug
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
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
