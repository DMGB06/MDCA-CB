# 🚀 FASE 1 COMPLETADA - INSTRUCCIONES DE PRUEBA

## ✅ Archivos Creados:

1. **pyproject.toml** - Dependencias del proyecto
2. **app/main.py** - Aplicación FastAPI principal
3. **app/config/settings.py** - Configuración con Pydantic
4. **app/routers/health.py** - Endpoint de salud
5. **.env.example** - Plantilla de variables de entorno
6. **.env** - Archivo de configuración local
7. **.dockerignore** - Archivos excluidos de Docker

---

## 📦 PASO 1: Instalar Dependencias

Abre tu terminal en la carpeta del proyecto y ejecuta:

```bash
pip install -e .
```

Esto instalará:
- FastAPI
- Uvicorn (servidor ASGI)
- Pydantic Settings
- Google Generative AI (Gemini)
- WebSockets
- Python-dotenv

---

## 🔥 PASO 2: Arrancar el Servidor

```bash
uvicorn app.main:app --reload
```

O de forma alternativa:

```bash
python -m uvicorn app.main:app --reload
```

**Deberías ver:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

## ✅ PASO 3: Probar los Endpoints

### Opción 1: Navegador Web
Abre tu navegador en:

- **Raíz**: http://127.0.0.1:8000/
- **Health Check**: http://127.0.0.1:8000/health
- **Documentación Interactiva**: http://127.0.0.1:8000/docs

### Opción 2: cURL (Terminal)

```bash
# Endpoint raíz
curl http://127.0.0.1:8000/

# Health check
curl http://127.0.0.1:8000/health
```

### Opción 3: PowerShell

```powershell
# Endpoint raíz
Invoke-WebRequest http://127.0.0.1:8000/ | Select-Object -Expand Content

# Health check
Invoke-WebRequest http://127.0.0.1:8000/health | Select-Object -Expand Content
```

---

## 📊 Respuestas Esperadas

### GET /
```json
{
  "message": "Chatbot Municipal API",
  "version": "0.1.0",
  "docs": "/docs",
  "health": "/health"
}
```

### GET /health
```json
{
  "status": "ok",
  "timestamp": "2026-04-01T14:35:00.123456",
  "service": "chatbot-municipal"
}
```

---

## 🎨 Características Implementadas

### ✅ Código Limpio y Buenas Prácticas:
- **Type hints** en todas las funciones
- **Docstrings** para documentación
- **Pydantic Settings** para configuración type-safe
- **CORS** configurado correctamente
- **Separation of Concerns** (routers, config, servicios)
- **Environment Variables** para configuración sensible
- **.dockerignore** para optimizar imagen Docker

### ✅ Estructura:
```
app/
├── main.py                 # FastAPI app + middlewares
├── config/
│   └── settings.py         # Configuración centralizada
└── routers/
    └── health.py           # Endpoint de salud
```

---

## 🔧 Configuración Actual (.env)

```env
GEMINI_API_KEY=              # Vacío por ahora (se usará en Fase 2)
ALLOWED_ORIGINS=*            # Acepta todas las origines (solo desarrollo)
DEBUG=True                   # Modo debug activado
RATE_LIMIT_PER_MINUTE=10     # 10 peticiones por minuto
```

---

## 🐛 Troubleshooting

### Error: "No module named 'app'"
**Solución**: Asegúrate de estar en la carpeta raíz del proyecto al ejecutar uvicorn.

### Error: "ModuleNotFoundError: No module named 'fastapi'"
**Solución**: Ejecuta `pip install -e .` primero.

### Error: Puerto 8000 en uso
**Solución**: Usa otro puerto: `uvicorn app.main:app --reload --port 8001`

---

## 🎯 Siguiente Fase

Una vez que veas que funciona:
- ✅ GET / responde correctamente
- ✅ GET /health responde correctamente
- ✅ /docs muestra Swagger UI

Estaremos listos para **Fase 2: Integración con Gemini** 🚀

---

## 📝 Notas del Código

### app/main.py
- Crea la aplicación FastAPI
- Configura CORS automáticamente desde settings
- Registra el router de health
- Endpoint raíz con información básica

### app/config/settings.py
- Usa `pydantic-settings` para validación
- Carga variables desde `.env` automáticamente
- Property `origins_list` convierte string a lista
- Type-safe y con defaults razonables

### app/routers/health.py
- Endpoint simple para health checks
- Responde con timestamp UTC
- Útil para monitoreo y Docker healthchecks

---

**¡La Fase 1 está completa y lista para probar!** 🎉
