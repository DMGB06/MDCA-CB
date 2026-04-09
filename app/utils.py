"""
Configuración de logging estructurado en formato JSON.
Diseñado para integración con Loki/Grafana y análisis automatizado.
"""
import logging
import json
import sys
from datetime import datetime
from typing import Any, Dict


class JSONFormatter(logging.Formatter):
    """
    Formatter que convierte logs a JSON estructurado.
    Incluye campos estándar + contexto adicional vía extra={}.
    """
    
    def format(self, record: logging.LogRecord) -> str:
        log_data: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Agregar excepción si existe
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Agregar campos personalizados del contexto (extra)
        # Campos comunes: duration_ms, status_code, path, method, user_id, etc.
        for key in ["duration_ms", "status_code", "path", "method", "client_ip", 
                    "user_id", "trace_id", "error_count", "throughput"]:
            if hasattr(record, key):
                log_data[key] = getattr(record, key)
        
        return json.dumps(log_data, ensure_ascii=False)


def setup_logging(level: int = logging.INFO) -> None:
    """
    Configura el sistema de logging global con formato JSON.
    
    Args:
        level: Nivel mínimo de logging (default: INFO)
    """
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())
    
    # Configurar root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers = [handler]  # Reemplazar handlers existentes
    
    # Suprimir logs muy verbosos de librerías externas
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
