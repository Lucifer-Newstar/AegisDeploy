"""catalog-service settings (env-driven — same rules as the service template)."""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration for the catalog service."""

    model_config = SettingsConfigDict(env_prefix="", case_sensitive=False, extra="ignore")

    service_name: str = "catalog-service"
    service_port: int = 9001
    environment: str = "dev"
    otel_exporter_otlp_endpoint: str = ""  # e.g. http://otel-collector:4317


settings = Settings()
