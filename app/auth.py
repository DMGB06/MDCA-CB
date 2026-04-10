from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from app.config.settings import settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

def verify_api_key_value(api_key: str | None):
    if not settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="API Key no configurada en el servidor"
        )
    if not api_key or api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key no proporcionada o inválida"
        )
    return api_key


def verify_api_key(api_key: str = Security(api_key_header)):
    return verify_api_key_value(api_key)