"""
Script para capturar métricas baseline del sistema.
Mide: latencia P50/P95/P99, tasa de error, throughput.

Uso:
    1. Asegúrate de que la app esté corriendo: uvicorn app.main:app --reload
    2. Ejecuta: python tests/capture_baseline_metrics.py
"""
import requests
import time
import statistics
import json
from typing import List, Dict, Any
from datetime import datetime


BASE_URL = "http://localhost:8000"
NUM_REQUESTS = 100  # Número de requests para medir


def measure_endpoint(
    endpoint: str,
    method: str = "GET",
    payload: Dict[str, Any] = None,
    iterations: int = NUM_REQUESTS
) -> Dict[str, Any]:
    """
    Mide métricas de un endpoint específico.

    Args:
        endpoint: Path del endpoint (ej: /chat)
        method: Método HTTP (GET, POST)
        payload: Body del request (para POST)
        iterations: Número de requests a enviar

    Returns:
        Dict con métricas: latencias, tasa de error, throughput
    """
    latencies: List[float] = []
    errors = 0
    start_time = time.time()

    print(f"\n📊 Midiendo {method} {endpoint} ({iterations} requests)...")

    for i in range(iterations):
        try:
            request_start = time.time()

            if method == "POST":
                response = requests.post(
                    f"{BASE_URL}{endpoint}",
                    json=payload,
                    timeout=30
                )
            else:
                response = requests.get(
                    f"{BASE_URL}{endpoint}",
                    timeout=30
                )

            duration_ms = (time.time() - request_start) * 1000

            if response.status_code < 400:
                latencies.append(duration_ms)
            else:
                errors += 1
                print(f"  ⚠️  Request {i+1}: Error {response.status_code}")

        except requests.exceptions.RequestException as e:
            errors += 1
            print(f"  ❌ Request {i+1}: {type(e).__name__}")

        # Pequeña pausa para evitar saturar (5 req/min = 12s entre requests)
        # Pero para testing rápido usamos 0.1s
        time.sleep(0.1)

    total_time = time.time() - start_time

    # Calcular métricas
    if latencies:
        latencies.sort()
        p50 = latencies[len(latencies) // 2]
        p95 = (latencies[int(len(latencies) * 0.95)]
               if len(latencies) > 20
               else latencies[-1])
        p99 = (latencies[int(len(latencies) * 0.99)]
               if len(latencies) > 100
               else latencies[-1])

        metrics = {
            "endpoint": endpoint,
            "method": method,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "total_requests": iterations,
            "successful_requests": len(latencies),
            "failed_requests": errors,
            "error_rate_percent": round((errors / iterations) * 100, 2),
            "latency_p50_ms": round(p50, 2),
            "latency_p95_ms": round(p95, 2),
            "latency_p99_ms": round(p99, 2),
            "latency_avg_ms": round(statistics.mean(latencies), 2),
            "latency_min_ms": round(min(latencies), 2),
            "latency_max_ms": round(max(latencies), 2),
            "latency_stddev_ms": round(statistics.stdev(latencies),
                                       2) if len(latencies) > 1 else 0,
            "throughput_req_per_sec": round(iterations / total_time, 2),
            "total_time_sec": round(total_time, 2)
        }

        return metrics
    else:
        print(" No se pudieron obtener métricas válidas")
        return {
            "endpoint": endpoint,
            "method": method,
            "error": "All requests failed",
            "total_requests": iterations,
            "failed_requests": errors
        }


def print_metrics(metrics: Dict[str, Any]) -> None:
    """Imprime métricas en formato legible."""
    print(f"\n{'='*60}")
    print(f"📈 MÉTRICAS BASELINE: {metrics['method']} {metrics['endpoint']}")
    print(f"{'='*60}")

    if "error" in metrics:
        print(f"❌ ERROR: {metrics['error']}")
        return

    print("\n🔢 RESUMEN:")
    print(f"  Total requests:     {metrics['total_requests']}")
    print(f"  Exitosos:           {metrics['successful_requests']}")
    print(f"  Fallidos:           {metrics['failed_requests']}")
    print(f"  Tasa de error:      {metrics['error_rate_percent']}%")
    print(f"  Tiempo total:       {metrics['total_time_sec']}s")

    print("\n⏱️  LATENCIA:")
    print(f"  Mínima:             {metrics['latency_min_ms']} ms")
    print(f"  P50 (mediana):      {metrics['latency_p50_ms']} ms")
    print(f"  P95:                {metrics['latency_p95_ms']} ms")
    print(f"  P99:                {metrics['latency_p99_ms']} ms")
    print(f"  Máxima:             {metrics['latency_max_ms']} ms")
    print(f"  Promedio:           {metrics['latency_avg_ms']} ms")
    print(f"  Desv. estándar:     {metrics['latency_stddev_ms']} ms")

    print("\n🚀 THROUGHPUT:")
    print(f"  Requests/segundo:   {metrics['throughput_req_per_sec']} req/s")
    print(f"{'='*60}\n")


def main():
    """Ejecuta captura de métricas para todos los endpoints clave."""

    print("🎯 CAPTURA DE MÉTRICAS BASELINE")
    print("=" * 60)
    print("⚠️  IMPORTANTE: Asegúrate de que la app esté corriendo en:")
    print(f"   {BASE_URL}")
    print("=" * 60)

    # Verificar que la app esté corriendo
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ App detectada y funcionando\n")
        else:
            print(f"⚠️  App responde pero con status {response.status_code}\n")
    except requests.exceptions.RequestException:
        print("❌ ERROR: No se puede conectar a la app.")
        print("   Ejecuta primero: uvicorn app.main:app --reload")
        return

    input("Presiona ENTER para comenzar la medición...")

    all_metrics = []

    # 1. Medir endpoint de health (simple, sin payload)
    metrics_health = measure_endpoint("/health", method="GET", iterations=50)
    print_metrics(metrics_health)
    all_metrics.append(metrics_health)

    # 2. Medir endpoint de chat (complejo, con payload)
    metrics_chat = measure_endpoint(
        "/chat",
        method="POST",
        payload={"message": "¿Cuál es el horario de atención?"},
        iterations=50
    )
    print_metrics(metrics_chat)
    all_metrics.append(metrics_chat)

    # 3. Guardar resultados
    output_file = "docs/baseline_metrics.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump({
            "capture_date": datetime.utcnow().isoformat() + "Z",
            "version": "v0.1.0-baseline",
            "metrics": all_metrics
        }, f, indent=2, ensure_ascii=False)

    print(f"💾 Métricas guardadas en: {output_file}")
    print("\n✅ CAPTURA COMPLETADA\n")


if __name__ == "__main__":
    main()
