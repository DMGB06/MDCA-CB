# 🏛️ Chatbot Municipal Inteligente

Asistente virtual avanzado para municipalidades, diseñado para ofrecer atención ciudadana eficiente, segura y escalable mediante IA generativa y arquitectura moderna.

---

## Descripción

El Chatbot Municipal es una plataforma robusta de atención digital, capaz de responder consultas, guiar trámites y brindar información municipal 24/7. Incorpora IA generativa (Gemini/OpenAI), validación avanzada, seguridad de nivel producción y una arquitectura desacoplada, lista para escalar y evolucionar.

---

## Problema que Resuelve

- Saturación de canales tradicionales de atención ciudadana.
- Dificultad para acceder a información municipal clara y actualizada.
- Riesgos de seguridad y caídas por integraciones directas con IA.
- Necesidad de una solución modular, auditable y fácil de mantener.

---

## Características Principales

- 🔒 **Seguridad avanzada:** API Key interna, CORS estricto, validación de origen y rate limiting.
- 🧑‍💻 **Validación y sanitización de inputs:** Pydantic, limpieza de mensajes y protección contra inyecciones.
- 🔁 **Resiliencia:** Reintentos automáticos, timeouts y circuit breaker para servicios de IA.
- ⚡ **Arquitectura desacoplada:** Abstracción de proveedor IA (Gemini/OpenAI) y configuración por entorno.
- 🧩 **Extensible:** Fácil integración de nuevos proveedores, módulos o canales.
- 📊 **Métricas y monitoreo:** Middleware para observabilidad y salud del sistema.
- 🧪 **Testing exhaustivo:** Cobertura de seguridad, resiliencia y validación.
- 🌐 **Frontend desacoplado:** Widget JS seguro, sin exponer secretos.

---

## Tecnologías Utilizadas

- **Backend:** FastAPI, Pydantic, Tenacity, pybreaker/custom breaker, SlowAPI, Google Generative AI, OpenAI (opcional)
- **Frontend:** Vanilla JS Widget
- **Infraestructura:** Docker, Uvicorn, Prometheus/Grafana (monitoring)
- **Testing:** Pytest, HTTPX

---

## Arquitectura del Sistema

- **API Layer:** FastAPI, endpoints REST y WebSocket, protegidos por API Key y CORS.
- **Service Layer:** Abstracción de proveedor IA, lógica de negocio, validación y resiliencia.
- **Circuit Breaker:** Custom o pybreaker, protege contra caídas de IA.
- **Config Management:** `.env.dev`, `.env.prod`, validación estricta en startup.
- **Frontend Widget:** Conexión segura vía WebSocket, sin exponer secretos.
- **Observabilidad:** Logging estructurado, métricas y health checks.

---

## Estructura de Carpetas

chat-bot/
│
├── app/
│ ├── config/ # Configuración y settings por entorno
│ ├── models/ # Esquemas Pydantic
│ ├── routers/ # Endpoints HTTP y WebSocket
│ ├── services/ # Lógica de negocio, IA, breaker, validación
│ ├── middleware/ # Métricas, rate limiting, seguridad
│ ├── utils/ # Utilidades generales
│
├── widget/ # Frontend JS desacoplado
│
├── tests/ # Pruebas unitarias y de integración
│
├── .env.example # Plantilla de variables de entorno
├── .env.dev # Configuración desarrollo (no versionar)
├── .env.prod # Configuración producción (no versionar)
├── Dockerfile
├── docker-compose.yml
├── README.md
