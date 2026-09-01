"""Service settings — env-driven configuration (pydantic-settings).

Rule: no hardcoded endpoints. Every value here can be overridden with an
environment variable so the same container runs identically in Docker
Compose and Kubernetes (ADR-0005). Environment variables win over defaults.
"""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration for a service built from this template."""

    model_config = SettingsConfigDict(env_prefix="", case_sensitive=False, extra="ignore")

    # ── Identity ─────────────────────────────────────────────────────────────
    service_name: str = "_template"  # overridden per service (env: SERVICE_NAME)
    service_port: int = 8000         # overridden per service (env: SERVICE_PORT)
    environment: str = "dev"         # dev | staging | prod (env: ENVIRONMENT)

    # ── Observability ────────────────────────────────────────────────────────
    otel_exporter_otlp_endpoint: str = ""  # e.g. http://otel-collector:4317
                                           # empty → tracing no-op (offline-safe)


settings = Settings()
