from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """Configuración global de la aplicación."""
    
    # Gemini API
    gemini_api_key: str = ""
    gemini_model: str = "models/gemini-2.5-flash"
    
    # CORS
    allowed_origins: str = "*"
    
    # App
    debug: bool = True
    app_name: str = "Chatbot Municipal"
    
    # Rate Limiting
    rate_limit_per_minute: int = 10
    
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
        return [origin.strip() for origin in self.allowed_origins.split(",")]


settings = Settings()
