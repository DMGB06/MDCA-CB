# Guía de Implementación: Línea Base de Métricas

## 📋 Resumen

Esta implementación establece observabilidad profesional con:
- ✅ Logging estructurado en JSON
- ✅ Captura automática de métricas (latencia, errores, throughput)
- ✅ Stack de monitoreo: Grafana + Loki + Promtail

---

## 🚀 Paso 1: Verificar cambios en código

Se han creado/modificado los siguientes archivos:

### Archivos nuevos:
- `app/utils.py` - Logging estructurado JSON
- `app/middleware/metrics.py` - Middleware de métricas
- `tests/capture_baseline_metrics.py` - Script de captura de métricas
- `docker-compose.monitoring.yml` - Stack de monitoreo
- `promtail-config.yml` - Configuración Promtail
- `grafana-datasources.yml` - Configuración Grafana

### Archivos modificados:
- `app/main.py` - Integración de logging + middleware

---

## 🧪 Paso 2: Probar logging estructurado

```bash
# Ejecutar la app
uvicorn app.main:app --reload

# En otra terminal, hacer un request
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hola"}'
```

**Resultado esperado**: Verás logs en formato JSON como:
```json
{
  "timestamp": "2026-04-08T14:53:45.123Z",
  "level": "INFO",
  "logger": "app.middleware.metrics",
  "message": "POST /chat - 200",
  "module": "metrics",
  "function": "dispatch",
  "line": 67,
  "method": "POST",
  "path": "/chat",
  "status_code": 200,
  "duration_ms": 1234.56,
  "client_ip": "127.0.0.1",
  "error_count": 0,
  "throughput": 5
}
```

---

## 📊 Paso 3: Capturar métricas baseline

```bash
# Asegúrate de que la app esté corriendo
uvicorn app.main:app --reload

# En otra terminal, ejecuta el script de captura
python tests/capture_baseline_metrics.py
```

Esto generará:
- Informe en consola con P50/P95/P99, tasa de error, throughput
- Archivo `docs/baseline_metrics.json` con datos completos

**Ejemplo de salida:**
```
📈 MÉTRICAS BASELINE: POST /chat
============================================================
🔢 RESUMEN:
  Total requests:     50
  Exitosos:           48
  Fallidos:           2
  Tasa de error:      4.0%
  
⏱️  LATENCIA:
  P50 (mediana):      1234.56 ms
  P95:                2345.67 ms
  P99:                3456.78 ms
  
🚀 THROUGHPUT:
  Requests/segundo:   2.5 req/s
```

---

## 📈 Paso 4: Configurar Grafana + Loki (Opcional)

### Opción A: Docker local (recomendado para desarrollo)

```bash
# Levantar el stack de monitoreo
docker-compose -f docker-compose.monitoring.yml up -d

# Verificar que estén corriendo
docker-compose -f docker-compose.monitoring.yml ps
```

**Acceder a Grafana:**
1. Abre http://localhost:3000
2. Login: `admin` / `admin`
3. Ve a **Explore** → selecciona **Loki**
4. Query ejemplo: `{container="chatbot"} |= "POST /chat"`

**Crear dashboard básico:**
1. En Grafana, ve a **Dashboards** → **New Dashboard**
2. Agrega panel con query:
   ```logql
   avg_over_time({container="chatbot"} | json | __error__="" | duration_ms > 0 [5m])
   ```
3. Visualización: Time series
4. Título: "Latencia promedio (5min)"

### Opción B: Grafana Cloud (gratis, sin instalación)

1. Registrarse en https://grafana.com/products/cloud/
2. Crear stack gratuito
3. Instalar Grafana Agent:
   ```bash
   # Windows: descargar desde
   # https://github.com/grafana/agent/releases
   ```
4. Configurar agent para enviar logs de Docker
5. Usar dashboards predefinidos

---

## 🎯 Paso 5: Métricas clave a monitorear

### Dashboard mínimo recomendado:

1. **Latencia P50/P95/P99**
   - Query: `quantile_over_time(0.95, {container="chatbot"} | json | duration_ms [5m])`
   - Threshold: P95 < 2000ms (verde), < 5000ms (amarillo), > 5000ms (rojo)

2. **Tasa de error**
   - Query: `sum(rate({container="chatbot"} | json | status_code >= 400 [5m]))`
   - Threshold: < 1% (verde), < 5% (amarillo), > 5% (rojo)

3. **Throughput**
   - Query: `sum(rate({container="chatbot"} [5m]))`
   - Objetivo: > 5 req/s (capacidad mínima)

4. **Errores por tipo**
   - Query: `sum by (status_code) (rate({container="chatbot"} | json | status_code >= 400 [5m]))`

---

## 📝 Paso 6: Documentar baseline

Crea `docs/baseline_metrics_report.md`:

```markdown
# Baseline Metrics Report

**Fecha:** 2026-04-08
**Versión:** v0.1.0-baseline

## Métricas capturadas

- **Latencia P50:** 1234ms
- **Latencia P95:** 2345ms  
- **Latencia P99:** 3456ms
- **Tasa de error:** 4%
- **Throughput:** 2.5 req/s

## Análisis

- ⚠️ Latencia alta (>1s) en P50 debido a llamadas a Gemini API
- ⚠️ Tasa de error del 4% causada por [razón específica]
- ✅ Throughput aceptable para MVP

## Objetivos de mejora

- Reducir P50 a <500ms (caché, optimización)
- Reducir error rate a <1%
- Aumentar throughput a >10 req/s
```

---

## ✅ Checklist final

- [ ] Logging JSON implementado y funcionando
- [ ] Middleware de métricas activo
- [ ] Script de captura ejecutado y métricas guardadas
- [ ] Stack Grafana + Loki corriendo (o alternativa en cloud)
- [ ] Dashboard básico creado
- [ ] Baseline documentado

---

## 🔧 Troubleshooting

**Problema:** Los logs no aparecen en formato JSON
- **Solución:** Verifica que `setup_logging()` se llame antes de cualquier log

**Problema:** Script de métricas falla con connection error
- **Solución:** Asegúrate de que la app esté corriendo en localhost:8000

**Problema:** Grafana no muestra logs
- **Solución:** Verifica que Promtail esté corriendo y conectado a Loki:
  ```bash
  docker logs promtail
  ```

---

## 📚 Recursos adicionales

- [Loki LogQL](https://grafana.com/docs/loki/latest/logql/)
- [Grafana Dashboards](https://grafana.com/grafana/dashboards/)
- [Observability Best Practices](https://sre.google/books/)
