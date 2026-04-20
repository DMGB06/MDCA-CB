from pydantic import BaseModel, Field, field_validator
from typing import Optional
from app.shared.config.settings import settings


class ChatRequest(BaseModel):
    message: str = Field(...,
                         min_length=1,
                         max_length=settings.max_message_length,
                         description="Mensaje del usuario")

    @field_validator("message")
    @classmethod
    def normalize_message(cls, value: str) -> str:
        normalized = " ".join(value.split())
        if not normalized:
            raise ValueError("El mensaje no puede estar vacío")
        return normalized


class ChatResponse(BaseModel):
    response: str = Field(..., description="Respuesta generada por Gemini")
    error: Optional[str] = Field(None,
                                 description="Mensaje de error si ocurre")
