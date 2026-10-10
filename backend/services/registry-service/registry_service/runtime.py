from __future__ import annotations

import time
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    CollectorRegistry,
    Counter,
    Histogram,
    generate_latest,
)
from starlette.responses import Response

from registry_service.config import settings
from registry_service.logging import setup_logging

logger = setup_logging(settings.service_name, settings.environment)

METRIC_REGISTRY = CollectorRegistry()

REQUESTS = Counter(
    "http_server_requests_total",
    "Total HTTP requests",
    ["service", "method", "path", "status"],
    registry=METRIC_REGISTRY,
)
REQUEST_DURATION = Histogram(
    "http_server_request_duration_seconds",
    "HTTP request duration",
    ["service", "method", "path"],
    registry=METRIC_REGISTRY,
)

DEV_CORS_ORIGINS = (
    "http://localhost:3000",
    "http://localhost:3030",
)


def _init_tracing() -> None:
    from opentelemetry import trace
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor

    if not settings.otel_exporter_otlp_endpoint:
        trace.set_tracer_provider(TracerProvider())
        return

    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

    provider = TracerProvider(
        resource=Resource.create(
            {
                "service.name": settings.service_name,
                "deployment.environment": settings.environment,
            }
        )
    )
    provider.add_span_processor(
        BatchSpanProcessor(
            OTLPSpanExporter(endpoint=settings.otel_exporter_otlp_endpoint, insecure=True)
        )
    )
    trace.set_tracer_provider(provider)
    FastAPIInstrumentor().instrument()



def _init_otel_logs() -> None:
    """Best-effort OTLP log export so Loki can query service logs (A1)."""
    if not settings.otel_exporter_otlp_endpoint:
        return
    try:
        import logging as _logging

        from opentelemetry._logs import set_logger_provider
        from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
        from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
        from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
        from opentelemetry.sdk.resources import Resource

        provider = LoggerProvider(
            resource=Resource.create(
                {
                    "service.name": settings.service_name,
                    "deployment.environment": settings.environment,
                }
            )
        )
        provider.add_log_record_processor(
            BatchLogRecordProcessor(
                OTLPLogExporter(endpoint=settings.otel_exporter_otlp_endpoint, insecure=True)
            )
        )
        set_logger_provider(provider)
        handler = LoggingHandler(level=_logging.INFO, logger_provider=provider)
        _logging.getLogger().addHandler(handler)
    except Exception as exc:  # logs SDK is optional at runtime
        logger.warning(f"otel log export unavailable: {exc}")



@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    _init_tracing()
    _init_otel_logs()
    logger.info("service starting", extra={"port": settings.service_port})
    yield
    logger.info("service stopped")


def build_app(title: str) -> FastAPI:
    application = FastAPI(title=title, version="0.1.0", lifespan=lifespan)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=list(DEV_CORS_ORIGINS),
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return application


def instrument_middleware(application: FastAPI) -> None:
    @application.middleware("http")
    async def instrument_requests(
        request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        start = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start
        REQUESTS.labels(
            settings.service_name, request.method, request.url.path, str(response.status_code)
        ).inc()
        REQUEST_DURATION.labels(
            settings.service_name, request.method, request.url.path
        ).observe(duration)
        return response


def health_routes(application: FastAPI) -> None:
    @application.get("/")
    def root() -> dict[str, str]:
        return {
            "service": settings.service_name,
            "environment": settings.environment,
            "status": "ok",
        }

    @application.get("/health")
    def health() -> dict[str, str]:
        return {"status": "healthy"}

    @application.get("/metrics")
    def metrics() -> Response:
        return Response(generate_latest(METRIC_REGISTRY), media_type=CONTENT_TYPE_LATEST)
