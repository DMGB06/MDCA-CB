"""
Middleware de métricas para captura automática de latencia, throughput y errores.
Diseñado para observabilidad y análisis de rendimiento.
"""
import time
import logging
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

logger = logging.getLogger(__name__)


class MetricsMiddleware(BaseHTTPMiddleware):
    """
    Middleware que captura métricas de cada request:
    - Latencia (duration_ms)
    - Status code
    - Path y método HTTP
    - IP del cliente
    
    Los logs se emiten en formato JSON estructurado.
    """
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.request_count = 0
        self.error_count = 0
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Timestamp de inicio
        start_time = time.time()
        
        # Incrementar contador de requests
        self.request_count += 1
        
        # Ejecutar el request
        try:
            response = await call_next(request)
        except Exception as e:
            # Capturar excepciones no manejadas
            self.error_count += 1
            duration_ms = (time.time() - start_time) * 1000
            
            logger.error(
                "Request failed with unhandled exception",
                extra={
                    "method": request.method,
                    "path": str(request.url.path),
                    "duration_ms": round(duration_ms, 2),
                    "client_ip": request.client.host if request.client else "unknown",
                    "error_type": type(e).__name__,
                    "error_count": self.error_count
                },
                exc_info=True
            )
            raise
        
        # Calcular duración
        duration_ms = (time.time() - start_time) * 1000
        
        # Incrementar contador de errores si status >= 400
        if response.status_code >= 400:
            self.error_count += 1
        
        # Log estructurado con métricas
        log_level = logging.WARNING if response.status_code >= 400 else logging.INFO
        logger.log(
            log_level,
            f"{request.method} {request.url.path} - {response.status_code}",
            extra={
                "method": request.method,
                "path": str(request.url.path),
                "status_code": response.status_code,
                "duration_ms": round(duration_ms, 2),
                "client_ip": request.client.host if request.client else "unknown",
                "error_count": self.error_count,
                "throughput": self.request_count
            }
        )
        
        # Agregar headers de métricas (opcional, útil para debugging)
        response.headers["X-Process-Time"] = str(round(duration_ms, 2))
        
        return response
