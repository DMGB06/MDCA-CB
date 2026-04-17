import os
from typing import List, Literal
from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = f".env.{os.getenv('APP_ENV', 'dev')}"


class Settings(BaseSettings):
    app_env: Literal["dev", "prod"] = "dev"

    # Gemini API
    gemini_api_key: str = ""
    gemini_model: str = "models/gemini-2.5-flash"

    # CORS
    allowed_origins: str = "http://localhost:3000,http://localhost:8080"
    allowed_credentials: bool = False

    # API Key interna (no exponer en frontend)
    api_key: str = ""

    # App
    debug: bool = True
    app_name: str = "Chatbot Municipal"

    # Rate limiting / input
    rate_limit_per_minute: int = 10
    max_message_length: int = 500

    # Circuit Breaker Gemini
    gemini_cb_fail_max: int = 5
    gemini_cb_reset_timeout_seconds: int = 30

    # Resiliencia Gemini
    gemini_timeout_seconds: int = 20
    gemini_max_retries: int = 3
    gemini_retry_wait_seconds: int = 2

    model_config = SettingsConfigDict(
        env_file=(ENV_FILE, ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def origins_list(self) -> List[str]:
        if self.allowed_origins == "*":
            return ["*"]
        return [o.strip()
                for o
                in self.allowed_origins.split(",")
                if o.strip()
                ]

    @model_validator(mode="after")
    def validate_config(self):
        if self.allowed_origins == "*" and self.allowed_credentials:
            raise ValueError(
                "No se permite ALLOWED_ORIGINS='*' con ALLOW_CREDENTIALS=True"
                )

        if self.app_env == "prod":
            if self.debug:
                raise ValueError("En producción DEBUG debe ser False")
            if not self.gemini_api_key:
                raise ValueError("Falta GEMINI_API_KEY en producción")
            if not self.api_key:
                raise ValueError("Falta API_KEY en producción")
            if self.allowed_origins == "*":
                raise ValueError(
                    "En producción ALLOWED_ORIGINS no puede ser '*'"
                    )
        return self


settings = Settings()
