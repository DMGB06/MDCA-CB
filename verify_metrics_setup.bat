@echo off
REM Script para verificar la implementación de métricas

echo ========================================
echo VERIFICACION DE IMPLEMENTACION
echo ========================================
echo.

echo [1/5] Verificando archivos creados...
if exist "app\utils.py" (
    echo   - app\utils.py [OK]
) else (
    echo   - app\utils.py [FALTA]
)

if exist "app\middleware\metrics.py" (
    echo   - app\middleware\metrics.py [OK]
) else (
    echo   - app\middleware\metrics.py [FALTA]
)

if exist "tests\capture_baseline_metrics.py" (
    echo   - tests\capture_baseline_metrics.py [OK]
) else (
    echo   - tests\capture_baseline_metrics.py [FALTA]
)

if exist "docker-compose.monitoring.yml" (
    echo   - docker-compose.monitoring.yml [OK]
) else (
    echo   - docker-compose.monitoring.yml [FALTA]
)

echo.
echo [2/5] Verificando dependencias Python...
python -c "import requests; import json; import statistics" 2>nul
if %ERRORLEVEL% EQU 0 (
    echo   - Dependencias instaladas [OK]
) else (
    echo   - Faltan dependencias. Instala: pip install requests
)

echo.
echo [3/5] Probando importaciones...
python -c "from app.shared.observability.logging import setup_logging; from app.shared.observability.metrics import MetricsMiddleware; print('  - Imports OK')" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo   - ERROR: Verifica que los archivos estén correctamente creados
)

echo.
echo [4/5] Verificando estructura de logs...
echo   - Ejecuta: uvicorn app.main:app --reload
echo   - Deberías ver logs en formato JSON

echo.
echo [5/5] Siguientes pasos...
echo   1. Arrancar app: uvicorn app.main:app --reload
echo   2. Capturar métricas: python tests\capture_baseline_metrics.py
echo   3. Ver guía completa: docs\METRICS_IMPLEMENTATION_GUIDE.md

echo.
echo ========================================
echo VERIFICACION COMPLETA
echo ========================================
pause
