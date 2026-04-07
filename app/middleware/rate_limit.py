from slowapi import Limiter
from slowapi.util import get_remote_address

# Instancia global de Limiter para toda la app
limiter = Limiter(key_func=get_remote_address)
