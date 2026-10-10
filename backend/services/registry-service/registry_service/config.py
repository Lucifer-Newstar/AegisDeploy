"""Runtime configuration (env-driven, ADR-0005)."""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration for registry-service."""

    model_config = SettingsConfigDict(env_prefix="", case_sensitive=False, extra="ignore")

    service_name: str = "registry-service"
    service_port: int = 8101
    environment: str = "dev"
    otel_exporter_otlp_endpoint: str = ""
    registry_probe: bool = False


settings = Settings()
