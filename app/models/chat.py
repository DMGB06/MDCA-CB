from pydantic import BaseModel, Field
from typing import Optional

class ChatRequest(BaseModel):
    message: str = Field(..., description="Mensaje del usuario")

class ChatResponse(BaseModel):
    response: str = Field(..., description="Respuesta generada por Gemini")
    error: Optional[str] = Field(None, description="Mensaje de error si ocurre")
