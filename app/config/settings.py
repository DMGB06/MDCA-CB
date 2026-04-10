from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """Configuración global de la aplicación."""
    
    # Gemini API
    gemini_api_key: str = ""
    gemini_model: str = "models/gemini-2.5-flash"
    
    # CORS
    allowed_origins: str = "http://localhost:3000,http://localhost:8080"
    allowed_credentials: bool = False
    
    #API Key para autenticación
    api_key: str = ""
    
    # App
    debug: bool = True
    app_name: str = "Chatbot Municipal"
    
    # Rate Limiting
    rate_limit_per_minute: int = 10
    max_message_length: int = 500
    
    #Gemini resiliencia
    gemini_timeout_seconds: int = 20
    gemini_max_retries: int = 3
    gemini_retry_wait_seconds: int = 2
    
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    @property
    def origins_list(self) -> List[str]:
        """Convierte string de orígenes separados por coma a lista."""
        if self.allowed_origins == "*":
            return ["*"]
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]
    
    @model_validator(mode="after")
    def validate_cors_config(self):
        if self.allowed_origins == "*" and self.allowed_credentials:
            raise ValueError("No se permite ALLOWED_ORIGINS='*' con ALLOW_CREDENTIALS=True")
        return self


settings = Settings()
