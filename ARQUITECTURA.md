# 🏗️ ARQUITECTURA Y PASO A PASO DEL CHATBOT MUNICIPAL

## 📋 STACK DEFINITIVO

| Capa | Tecnología | Por qué |
|------|------------|---------|
| **Backend** | Python + FastAPI | Mejor ecosistema para IA/chatbots |
| **Chat tiempo real** | WebSockets (fastapi) | Nativo en FastAPI |
| **LLM** | Gemini API | Free tier generoso |
| **Knowledge Base** | Archivos Markdown | Sin base de datos al inicio |
| **Frontend Widget** | HTML + CSS + JS Vanilla | Un solo archivo embebible |
| **Deploy** | Render.com | Gratis y fácil |

---

## 📌 VISIÓN GENERAL - ¿Qué estamos construyendo?

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        LO QUE EL USUARIO VE                             │
│                                                                         │
│   Página de la Municipalidad (Astro)                                   │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                                                                 │  │
│   │    [Contenido normal de la página...]                          │  │
│   │                                                                 │  │
│   │                                              ┌──────────────┐  │  │
│   │                                              │  💬 Chat     │  │  │
│   │                                              │  ──────────  │  │  │
│   │                                              │  Hola, ¿en   │  │  │
│   │                                              │  qué puedo   │  │  │
│   │                                              │  ayudarle?   │  │  │
│   │                                              │              │  │  │
│   │                                              │  [Escribir]  │  │  │
│   │                                              └──────────────┘  │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🧩 LAS 3 PIEZAS DEL SISTEMA

---

## 🧠 ARQUITECTURA DE OPTIMIZACIÓN Y DETECCIÓN DE INTENCIÓN (MULTILINGÜE)

### 1. Preprocesamiento Ligero Multilingüe
- Normalización: minúsculas, quitar tildes, eliminar signos.
- Corrección ortográfica básica para palabras cortas y comunes.
- Tokenización flexible.

### 2. Detección de Idioma Eficiente
- Usa `langdetect` o `langid` (solo si el mensaje tiene >2 palabras).
- Cachea idioma por sesión si es consistente.

### 3. Clasificación de Intenciones
- Listas de frases clave multilingües (saludos, agradecimientos, despedidas, etc.) con variantes y errores comunes.
- Expresiones regulares y similitud de texto (Levenshtein/Jaccard) para tolerar errores.
- Heurísticas: mensajes muy cortos o solo emojis = "sin intención clara".

### 4. Flujo de Decisión
1. Recibe mensaje
2. Normaliza y detecta idioma
3. Clasifica intención:
   - Si es saludo/agradecimiento/despedida → responde localmente en el idioma detectado.
   - Si es pregunta frecuente → busca en base de conocimiento local (en el idioma del usuario).
   - Si no hay respuesta local clara → llama a la API externa (Gemini).
   - Si el mensaje es ambiguo o muy corto → pide aclaración antes de usar la API.

### 5. Ejemplo de Pseudo-código
```python
def procesar_mensaje(mensaje, session):
    msg = normalizar(mensaje)
    idioma = session.idioma or detectar_idioma(msg)
    intencion = clasificar_intencion(msg, idioma)
    if intencion in ["saludo", "agradecimiento", "despedida"]:
        return responder_local(intencion, idioma)
    respuesta = buscar_en_base_conocimiento(msg, idioma)
    if respuesta:
        return respuesta
    if es_ambigua(msg):
        return pedir_aclaracion(idioma)
    if session.cache.get(msg):
        return session.cache[msg]
    respuesta_api = llamar_api_ia(msg, idioma)
    session.cache[msg] = respuesta_api
    return respuesta_api
```

### 6. Técnicas para Minimizar Consumo de API
- Prioriza lógica local y caching.
- Rate limiting por usuario.
- Batching de mensajes si es necesario.
- Logs para mejorar reglas y reducir llamadas innecesarias.

### 7. Manejo de Errores y Multilingüismo
- Similitud de texto para errores ortográficos.
- Variantes informales y abreviaturas en listas de intenciones.
- Si mezcla idiomas, responde en el predominante o pide aclaración.

---


```
    PIEZA 1                    PIEZA 2                    PIEZA 3
    ────────                   ────────                   ────────
   
┌─────────────┐           ┌─────────────┐           ┌─────────────┐
│   WIDGET    │  ──────▶  │   BACKEND   │  ──────▶  │   GEMINI    │
│  (Frontend) │  ◀──────  │  (Servidor) │  ◀──────  │    (IA)     │
└─────────────┘           └─────────────┘           └─────────────┘
     │                          │                         │
     │                          │                         │
     ▼                          ▼                         ▼
   
 Un archivo             Tu servidor en              API de Google
 JavaScript que         Node.js que                 que genera las
 muestra el chat        procesa todo                respuestas
 en cualquier web                                   inteligentes
```

### ¿Qué hace cada pieza?

| Pieza | Responsabilidad | Tecnología |
|-------|-----------------|------------|
| **Widget** | Mostrar la ventana de chat, capturar mensajes del usuario, mostrar respuestas | HTML + CSS + JavaScript Vanilla |
| **Backend** | Recibir mensajes, buscar información relevante, llamar a Gemini, devolver respuesta | **Python + FastAPI** |
| **Gemini** | Generar respuestas inteligentes basadas en el contexto | API de Google (externo) |

---

## 🔄 FLUJO COMPLETO: ¿Qué pasa cuando un usuario escribe?

```
PASO 1: Usuario escribe "¿Cuánto cuesta la licencia de funcionamiento?"
        │
        ▼
┌───────────────────────────────────────────────────────────────────────┐
│ WIDGET (en el navegador del usuario)                                  │
│                                                                       │
│  1. Captura el texto que escribió                                    │
│  2. Lo envía al backend por WebSocket                                │
│  3. Muestra "escribiendo..." mientras espera                         │
└───────────────────────────────────────────────────────────────────────┘
        │
        │  WebSocket: { mensaje: "¿Cuánto cuesta la licencia..." }
        ▼
┌───────────────────────────────────────────────────────────────────────┐
│ BACKEND (tu servidor en Python + FastAPI)                             │
│                                                                       │
│  1. Recibe el mensaje                                                │
│  2. Busca en los archivos markdown si hay info sobre "licencia"      │
│  3. Encuentra: "licencia_funcionamiento.md" con precios y requisitos │
│  4. Construye un PROMPT para Gemini:                                 │
│     ┌─────────────────────────────────────────────────────────────┐  │
│     │ "Eres asistente de la Municipalidad. Contexto disponible:   │  │
│     │  - Licencia de funcionamiento cuesta S/150                  │  │
│     │  - Requisitos: DNI, contrato de alquiler...                 │  │
│     │                                                              │  │
│     │  Usuario pregunta: ¿Cuánto cuesta la licencia...?           │  │
│     │  Responde de forma amable y clara."                         │  │
│     └─────────────────────────────────────────────────────────────┘  │
│  5. Envía ese prompt a Gemini API                                    │
└───────────────────────────────────────────────────────────────────────┘
        │
        │  HTTP POST a api.google.com/gemini
        ▼
┌───────────────────────────────────────────────────────────────────────┐
│ GEMINI (API de Google)                                                │
│                                                                       │
│  1. Recibe el prompt con toda la información                         │
│  2. Genera una respuesta natural y amigable                          │
│  3. Devuelve: "La licencia de funcionamiento tiene un costo de       │
│               S/150. Los requisitos son..."                          │
└───────────────────────────────────────────────────────────────────────┘
        │
        │  Respuesta de Gemini
        ▼
┌───────────────────────────────────────────────────────────────────────┐
│ BACKEND                                                               │
│                                                                       │
│  1. Recibe la respuesta de Gemini                                    │
│  2. La guarda en el historial de la conversación                     │
│  3. La envía al widget por WebSocket                                 │
└───────────────────────────────────────────────────────────────────────┘
        │
        │  WebSocket: { respuesta: "La licencia de funcionamiento..." }
        ▼
┌───────────────────────────────────────────────────────────────────────┐
│ WIDGET                                                                │
│                                                                       │
│  1. Recibe la respuesta                                              │
│  2. La muestra en la ventana de chat                                 │
│  3. Usuario ve: "La licencia de funcionamiento tiene un costo..."    │
└───────────────────────────────────────────────────────────────────────┘
```

---

## 📁 ESTRUCTURA DE ARCHIVOS DEL PROYECTO

```
chat-bot/
│
├── 📁 app/                        # Todo el código fuente Python
│   │
│   ├── 📄 main.py                 # ENTRADA PRINCIPAL - arranca FastAPI
│   │
│   ├── 📁 config/                 # Configuraciones
│   │   ├── 📄 __init__.py
│   │   └── 📄 settings.py         # Variables de entorno con Pydantic
│   │
│   ├── 📁 routers/                # Endpoints de la API
│   │   ├── 📄 __init__.py
│   │   ├── 📄 health.py           # GET /health (verificar que funciona)
│   │   └── 📄 chat.py             # POST /chat + WebSocket /ws/chat
│   │
│   ├── 📁 services/               # Lógica de negocio
│   │   ├── 📄 __init__.py
│   │   ├── 📄 gemini_service.py   # Comunicación con Gemini API
│   │   ├── 📄 knowledge_service.py # Búsqueda en archivos markdown
│   │   └── 📄 chat_service.py     # Orqueswta todo el flujo
│   │
│   ├── 📁 models/                 # Modelos Pydantic (esquemas de datos)
│   │   ├── 📄 __init__.py
│   │   └── 📄 chat.py             # ChatMessage, ChatResponse, etc.
│   │
│   └── 📁 knowledge/              # Base de conocimiento (MARKDOWN)
│       ├── 📄 tramites.md         # Info sobre trámites
│       ├── 📄 horarios.md         # Horarios de atención
│       ├── 📄 contactos.md        # Teléfonos, direcciones
│       └── 📄 faqs.md             # Preguntas frecuentes
│
├── 📁 widget/                     # El chat embebible
│   ├── 📄 chatbot.js              # TODO el widget en un solo archivo
│   └── 📄 chatbot.min.js          # Versión minificada para producción
│
├── 📁 tests/                      # Tests del proyecto
│   ├── 📄 __init__.py
│   ├── 📄 test_health.py
│   └── 📄 test_chat.py
│
├── 📄 .env                        # Variables secretas (NO subir a git)
├── 📄 .env.example                # Ejemplo de variables (SÍ subir a git)
├── 📄 requirements.txt            # Dependencias Python
├── 📄 pyproject.toml              # Configuración del proyecto (opcional)
├── 📄 Dockerfile                  # Para deploy en contenedor
├── 📄 render.yaml                 # Configuración de Render.com
└── 📄 README.md                   # Documentación
```

---

## 🔧 PASO A PASO DETALLADO DE IMPLEMENTACIÓN

### ══════════════════════════════════════════════════════════════════
### FASE 1: FUNDAMENTOS (Semanas 1-2)
### ══════════════════════════════════════════════════════════════════

**Objetivo:** Tener un servidor FastAPI básico funcionando

```
Día 1-2: Crear estructura del proyecto
─────────────────────────────────────────
□ Crear carpeta del proyecto
□ Crear entorno virtual: python -m venv venv
□ Activar entorno: venv\Scripts\activate (Windows)
□ Instalar dependencias:
  - fastapi (Framework web)
  - uvicorn (Servidor ASGI)
  - python-dotenv (Variables de entorno)
  - pydantic-settings (Configuración tipada)

Día 3-4: Configurar estructura de carpetas
─────────────────────────────────────────
□ Crear carpeta app/ con __init__.py
□ Crear subcarpetas: config/, routers/, services/, models/
□ Crear requirements.txt con dependencias

Día 5-7: Crear servidor FastAPI básico
─────────────────────────────────────────
□ app/main.py - Entrada principal
□ app/config/settings.py - Configuración con Pydantic
□ app/routers/health.py - Endpoint de salud

Día 8-10: Probar que funciona
─────────────────────────────────────────
□ uvicorn app.main:app --reload
□ Abrir http://localhost:8000/health
□ Ver respuesta: { "status": "ok" }
□ Revisar docs automáticos: http://localhost:8000/docs
```

**Dependencias (requirements.txt):**
```
fastapi==0.109.0
uvicorn[standard]==0.27.0
python-dotenv==1.0.0
pydantic-settings==2.1.0
```

**Entregable Fase 1:**
```bash
curl http://localhost:8000/health
# Respuesta: {"status":"ok","timestamp":"2026-04-01T00:00:00Z"}
```

---

### ══════════════════════════════════════════════════════════════════
### FASE 2: EL CEREBRO DEL BOT (Semanas 3-4)
### ══════════════════════════════════════════════════════════════════

**Objetivo:** Conectar con Gemini y tener conversaciones básicas

```
Día 1-3: Obtener API key de Gemini
─────────────────────────────────────────
□ Ir a https://makersuite.google.com/app/apikey
□ Crear API key
□ Guardarla en .env: GEMINI_API_KEY=tu_key_aqui

Día 4-7: Crear servicio de Gemini
─────────────────────────────────────────
□ Instalar: pip install google-generativeai
□ app/services/gemini_service.py
□ Función async para enviar mensaje y recibir respuesta
□ Manejo de errores (rate limit, API caída)

Día 8-10: Crear endpoint de chat
─────────────────────────────────────────
□ app/routers/chat.py
□ POST /api/chat que recibe mensaje
□ Llama a Gemini y devuelve respuesta
□ app/models/chat.py - Esquemas Pydantic

Día 11-14: Manejar historial de conversación
─────────────────────────────────────────
□ Guardar últimos 10 mensajes en memoria (dict)
□ Enviar historial a Gemini para contexto
□ Así el bot "recuerda" la conversación
```

**Dependencias adicionales:**
```
google-generativeai==0.3.2
```

**Ejemplo de código (gemini_service.py):**
```python
import google.generativeai as genai
from app.config.settings import settings

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

async def chat(message: str, history: list[dict]) -> str:
    chat_session = model.start_chat(history=history)
    response = await chat_session.send_message_async(message)
    return response.text
```

**Entregable Fase 2:**
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hola, ¿qué servicios ofrece la municipalidad?"}'

# Respuesta: {"response": "¡Hola! La municipalidad ofrece..."}
```

---

### ══════════════════════════════════════════════════════════════════
### FASE 3: CONOCIMIENTO MUNICIPAL (Semanas 5-6)
### ══════════════════════════════════════════════════════════════════

**Objetivo:** El bot responde con información REAL del municipio

```
Día 1-4: Crear base de conocimiento
─────────────────────────────────────────
□ app/knowledge/tramites.md
  - Lista de trámites
  - Requisitos de cada uno
  - Costos y tiempos

□ app/knowledge/horarios.md
  - Horarios por área
  - Días de atención

□ app/knowledge/contactos.md
  - Teléfonos
  - Direcciones
  - Correos

□ app/knowledge/faqs.md
  - Preguntas frecuentes
  - Respuestas oficiales

Día 5-8: Sistema de búsqueda simple
─────────────────────────────────────────
□ app/services/knowledge_service.py
□ Función que busca palabras clave en los markdown
□ Retorna el contenido relevante

Día 9-14: Integrar conocimiento con Gemini
─────────────────────────────────────────
□ Modificar chat_service.py
□ Antes de llamar a Gemini:
  1. Buscar info relevante en knowledge/
  2. Agregar esa info al prompt
  3. Gemini responde usando esa info
```

**Ejemplo de búsqueda simple (knowledge_service.py):**
```python
from pathlib import Path

KNOWLEDGE_DIR = Path(__file__).parent.parent / "knowledge"

def search_knowledge(query: str) -> str:
    """Busca información relevante en los archivos markdown."""
    keywords = query.lower().split()
    results = []
    
    for md_file in KNOWLEDGE_DIR.glob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        content_lower = content.lower()
        
        # Si alguna palabra clave está en el archivo, lo incluimos
        if any(keyword in content_lower for keyword in keywords):
            results.append(content)
    
    return "\n\n---\n\n".join(results) if results else ""
```

**Entregable Fase 3:**
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "¿Qué necesito para sacar licencia de funcionamiento?"}'

# Respuesta con información REAL:
# {"response": "Para obtener su licencia de funcionamiento necesita:
#  1. DNI del titular
#  2. Contrato de alquiler o título de propiedad
#  3. Pago de S/150 en caja
#  El trámite demora 5 días hábiles..."}
```

---

### ══════════════════════════════════════════════════════════════════
### FASE 4: WIDGET EMBEBIBLE + WEBSOCKET (Semanas 7-8)
### ══════════════════════════════════════════════════════════════════

**Objetivo:** Un solo archivo JS que muestra el chat en cualquier web

```
Día 1-3: Agregar WebSocket al backend
─────────────────────────────────────────
□ FastAPI soporta WebSocket nativamente
□ Agregar endpoint ws://localhost:8000/ws/chat
□ Manejar conexiones, mensajes, desconexiones

Día 4-7: Crear interfaz del chat
─────────────────────────────────────────
□ widget/chatbot.js
□ HTML del chat (se crea con JavaScript)
□ CSS del chat (estilos institucionales)
□ Botón flotante para abrir/cerrar

Día 8-11: Conectar widget con WebSocket
─────────────────────────────────────────
□ Conexión WebSocket en chatbot.js
□ Enviar mensaje → Recibir respuesta en tiempo real
□ Reconexión automática si se pierde conexión

Día 12-14: Pulir experiencia de usuario
─────────────────────────────────────────
□ Indicador de "escribiendo..."
□ Scroll automático
□ Animaciones suaves
□ Manejo de errores
□ Responsive (funciona en móvil)
```

**Ejemplo WebSocket en FastAPI (chat.py):**
```python
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()

@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    session_id = str(uuid.uuid4())
    
    try:
        while True:
            # Recibir mensaje del cliente
            data = await websocket.receive_json()
            message = data.get("message", "")
            
            # Procesar con Gemini
            response = await chat_service.process_message(
                session_id=session_id,
                message=message
            )
            
            # Enviar respuesta
            await websocket.send_json({
                "type": "response",
                "content": response
            })
    except WebSocketDisconnect:
        # Cliente se desconectó
        pass
```

**Entregable Fase 4:**
```html
<!-- Esto es TODO lo que necesita el frontend Astro -->
<script src="https://tu-servidor.com/widget/chatbot.js"></script>

<!-- O con configuración personalizada -->
<script>
  window.MunicipalidadChat = {
    serverUrl: 'wss://tu-servidor.com',
    theme: 'light',
    position: 'bottom-right',
    welcomeMessage: '¡Hola! ¿En qué puedo ayudarle?'
  };
</script>
<script src="https://tu-servidor.com/widget/chatbot.js"></script>
```

---

### ══════════════════════════════════════════════════════════════════
### FASE 5: DEPLOY Y PRESENTACIÓN (Semanas 9-10)
### ══════════════════════════════════════════════════════════════════

**Objetivo:** Todo funcionando en internet, listo para mostrar

```
Día 1-3: Preparar para producción
─────────────────────────────────────────
□ Variables de entorno de producción
□ Configurar CORS para dominio del municipio
□ Rate limiting para proteger API
□ Logs estructurados

Día 4-7: Deploy en Render.com
─────────────────────────────────────────
□ Crear cuenta en Render
□ Crear render.yaml con configuración
□ Conectar repositorio de GitHub
□ Configurar variables de entorno
□ Deploy automático

Día 8-10: Documentación y demo
─────────────────────────────────────────
□ README profesional
□ Instrucciones de integración para frontend
□ Demo grabada o página de presentación
```

**Archivo render.yaml:**
```yaml
services:
  - type: web
    name: chatbot-municipal
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: GEMINI_API_KEY
        sync: false  # Se configura manualmente en Render
      - key: ALLOWED_ORIGINS
        value: https://municipalidad.gob.pe
```

**Entregable Final:**
```
✅ URL del backend: https://chatbot-municipal.onrender.com
✅ Widget embebible funcionando
✅ Documentación para el equipo de frontend
✅ Demo lista para mostrar al municipio
```

---

## 🎯 CÓMO SE INTEGRA CON EL FRONTEND ASTRO (REPO SEPARADO)

### Lo que tú entregas al equipo de Frontend:

```
1. URL del servidor:     https://chatbot-municipal.onrender.com
2. Archivo del widget:   https://chatbot-municipal.onrender.com/widget/chatbot.js
3. Documentación:        README.md con instrucciones
```

### Lo que ellos hacen (2 minutos de trabajo):

```astro
---
// src/layouts/Layout.astro (el layout principal de Astro)
---

<!DOCTYPE html>
<html>
<head>
  <title>Municipalidad</title>
</head>
<body>
  <slot />
  
  <!-- ESTO ES TODO - Una línea para agregar el chatbot -->
  <script src="https://chatbot-municipal.onrender.com/widget/chatbot.js"></script>
</body>
</html>
```

### Resultado:

El chatbot aparece automáticamente en todas las páginas del sitio municipal.

---

## ❓ PREGUNTAS FRECUENTES

### ¿Por qué WebSocket y no solo HTTP?

```
HTTP (petición normal):
Usuario envía mensaje → Espera → Espera → Espera → Recibe respuesta completa

WebSocket (tiempo real):
Usuario envía mensaje → Ve "escribiendo..." → Ve la respuesta aparecer palabra por palabra

WebSocket da mejor experiencia de usuario, como en ChatGPT.
```

### ¿Qué pasa si Gemini se cae?

```python
# En tu código tendrás algo así:
async def get_response(message: str) -> str:
    try:
        response = await gemini_service.chat(message)
        return response
    except Exception as e:
        logger.error(f"Error Gemini: {e}")
        # Respuesta de emergencia
        return (
            "Lo siento, estoy teniendo problemas técnicos. "
            "Por favor contacte directamente al 01-234-5678."
        )
```

### ¿Cómo actualizo la información del municipio?

```
Solo editas los archivos markdown:

app/knowledge/tramites.md     ← Agregar nuevo trámite
app/knowledge/horarios.md     ← Cambiar horario
app/knowledge/contactos.md    ← Nuevo teléfono

No necesitas tocar código. El bot usa automáticamente la info nueva.
```

### ¿Es seguro? ¿Qué datos se guardan?

```
✅ Las conversaciones se guardan solo en memoria (se pierden al reiniciar)
✅ No se guarda información personal
✅ API key de Gemini está en variables de entorno (no en código)
✅ CORS configurado solo para el dominio de la municipalidad
```

---

## 🚀 ¿LISTO PARA EMPEZAR?

El siguiente paso es crear la estructura del proyecto y el código de la Fase 1.

¿Empezamos?
