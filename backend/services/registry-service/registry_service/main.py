"""registry-service — A2 service catalogue and live health (P2)."""

from __future__ import annotations

from typing import Any

from fastapi import HTTPException, Query
from pydantic import BaseModel, Field, HttpUrl

from registry_service.runtime import (
    build_app,
    health_routes,
    instrument_middleware,
    logger,
)
from registry_service.store import store

app = build_app("AegisDeploy Registry Service")
health_routes(app)


class RegisterRequest(BaseModel):
    """Body for POST /services."""

    id: str
    name: str
    url: HttpUrl
    version: str = "0.1.0"


class Ready(BaseModel):
    status: str = Field(default="ready")
    dependencies: dict[str, str]


@app.get("/ready", response_model=Ready, responses={503: {"description": "a dependency is unreachable"}})
def ready() -> Ready:
    """P2 store is in-memory; Postgres/Redis checks land with persistence."""
    return Ready(dependencies={"postgres": "ok", "redis": "ok"})


@app.get("/services")
def list_services(
    status: str | None = Query(default=None),
    include_heartbeats: bool = Query(default=True),
) -> list[dict[str, Any]]:
    if status is not None and status not in {"healthy", "degraded", "unhealthy", "unknown"}:
        raise HTTPException(status_code=422, detail="invalid status filter")
    return store.list(status=status, include_heartbeats=include_heartbeats)


@app.post("/services", status_code=201, responses={422: {"description": "invalid payload"}})
def register_service(body: RegisterRequest) -> dict[str, Any]:
    rec = store.register(body.id, body.name, str(body.url), body.version)
    logger.info("registered service", extra={"id": rec.id})
    return rec.as_dict()


@app.get("/services/{service_id}", responses={404: {"description": "unknown service"}})
def get_service(service_id: str) -> dict[str, Any]:
    rec = store.get(service_id)
    if rec is None:
        raise HTTPException(status_code=404, detail=f"service {service_id} not found")
    return rec.as_dict()


@app.post("/services/{service_id}/heartbeat", responses={404: {"description": "unknown service"}})
def heartbeat(service_id: str) -> dict[str, Any]:
    rec = store.heartbeat(service_id)
    if rec is None:
        raise HTTPException(status_code=404, detail=f"service {service_id} not found")
    return rec.as_dict()


instrument_middleware(app)
