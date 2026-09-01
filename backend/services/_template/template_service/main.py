"""FastAPI app factory for AegisDeploy services (reference template).

Endpoints every service must expose (used by Compose/K8s probes and the
prometheus scrape job):
  * ``GET /health``   — liveness (no dependencies checked)
  * ``GET /ready``    — readiness (dependency checks go here per service)
  * ``GET /metrics``  — Prometheus-format metrics (prometheus-client)
  * ``GET /``         — service metadata (name, version, env)

Tracing: when ``OTEL_EXPORTER_OTLP_ENDPOINT`` is set, OpenTelemetry exports
traces to the OTel collector (gRPC); otherwise a no-op provider keeps the
service fully functional offline. Copy this module as the starting point
for every new platform service.
"""

from __future__ import annotations

from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    CollectorRegistry,
    Counter,
    Histogram,
    generate_latest,
)
from starlette.responses import Response

from template_service.config import settings
from template_service.logging import setup_logging

# ── Logging ───────────────────────────────────────────────────────────────────
logger = setup_logging(settings.service_name, settings.environment)

# ── Prometheus metrics ────────────────────────────────────────────────────────
# Names follow the platform metric conventions (see telemetry-model.md).
# Each service uses its OWN CollectorRegistry: several AegisDeploy services
# share identical metric names by convention, so a shared/global registry
# would collide when modules are imported in one process (e.g. CI test runs).
METRIC_REGISTRY = CollectorRegistry()

REQUESTS = Counter(
    "http_server_requests_total",
    "Total HTTP requests received",
    ["service", "method", "path", "status"],
    registry=METRIC_REGISTRY,
)
REQUEST_DURATION = Histogram(
    "http_server_request_duration_seconds",
    "HTTP request duration in seconds",
    ["service", "method", "path"],
    registry=METRIC_REGISTRY,
)

# ── OpenTelemetry (tracing) ───────────────────────────────────────────────────
def _init_tracing() -> None:
    """Wire OTLP trace export when an endpoint is configured; else no-op.

    No-op fallback keeps the service runnable in bare `uvicorn` dev mode
    without the observability stack (graceful degradation).
    """
    from opentelemetry import trace
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor

    if not settings.otel_exporter_otlp_endpoint:
        trace.set_tracer_provider(TracerProvider())  # no-op exporter
        return

    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

    provider = TracerProvider(
        resource=Resource.create({"service.name": settings.service_name, "deployment.environment": settings.environment})
    )
    provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=settings.otel_exporter_otlp_endpoint, insecure=True)))
    trace.set_tracer_provider(provider)
    FastAPIInstrumentor().instrument()


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Startup/shutdown hooks — tracing init happens here (after uvicorn boots)."""
    _init_tracing()
    logger.info("service starting", extra={"port": settings.service_port})
    yield
    logger.info("service stopped")


app = FastAPI(title=f"AegisDeploy {settings.service_name}", version="0.1.0", lifespan=lifespan)


@app.get("/")
def root() -> dict[str, str]:
    """Service metadata — handy for debugging and integration tests."""
    return {"service": settings.service_name, "environment": settings.environment, "status": "ok"}


@app.get("/health")
def health() -> dict[str, str]:
    """Liveness probe: the process is up. No dependencies checked."""
    REQUESTS.labels(settings.service_name, "GET", "/health", "200").inc()
    return {"status": "healthy"}


@app.get("/ready")
def ready() -> dict[str, str]:
    """Readiness probe: dependencies reachable.

    Services extend this with real dependency checks (e.g. Postgres ping);
    the template checks nothing besides process liveness.
    """
    REQUESTS.labels(settings.service_name, "GET", "/ready", "200").inc()
    return {"status": "ready"}


@app.get("/metrics")
def metrics() -> Response:
    """Prometheus scrape endpoint (content-type: text/plain; version=0.0.4)."""
    return Response(generate_latest(METRIC_REGISTRY), media_type=CONTENT_TYPE_LATEST)


@app.middleware("http")
async def instrument_requests(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    """Count and time every request (prometheus_client) — per-service standard."""
    import time

    start = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start
    method, path = request.method, request.url.path
    REQUESTS.labels(settings.service_name, method, path, str(response.status_code)).inc()
    REQUEST_DURATION.labels(settings.service_name, method, path).observe(duration)
    return response
