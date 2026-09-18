"""Runtime configuration (env-driven, ADR-0005)."""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration for payment-service."""

    model_config = SettingsConfigDict(env_prefix="", case_sensitive=False, extra="ignore")

    service_name: str = "payment-service"
    service_port: int = 9004
    environment: str = "dev"
    otel_exporter_otlp_endpoint: str = ""


settings = Settings()
