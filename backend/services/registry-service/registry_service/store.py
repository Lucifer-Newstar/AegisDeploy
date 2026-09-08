"""In-memory registry store (P2). Postgres persistence lands with Alembic."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta

HEARTBEAT_HEALTHY = timedelta(seconds=30)
HEARTBEAT_DEGRADED = timedelta(seconds=90)


def _now() -> datetime:
    return datetime.now(UTC)


@dataclass
class ServiceRecord:
    id: str
    name: str
    url: str
    version: str = "0.1.0"
    status: str = "healthy"
    registered_at: datetime = field(default_factory=_now)
    last_heartbeat_at: datetime | None = None

    def refresh_status(self, now: datetime | None = None) -> None:
        now = now or _now()
        stamp = self.last_heartbeat_at or self.registered_at
        age = now - stamp
        if age <= HEARTBEAT_HEALTHY:
            self.status = "healthy"
        elif age <= HEARTBEAT_DEGRADED:
            self.status = "degraded"
        else:
            self.status = "unknown"

    def as_dict(self, include_heartbeats: bool = True) -> dict[str, str | None]:
        self.refresh_status()
        payload: dict[str, str | None] = {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "version": self.version,
            "status": self.status,
            "registered_at": self.registered_at.isoformat().replace("+00:00", "Z"),
        }
        if include_heartbeats:
            payload["last_heartbeat_at"] = (
                self.last_heartbeat_at.isoformat().replace("+00:00", "Z")
                if self.last_heartbeat_at
                else None
            )
        return payload


class RegistryStore:
    """Process-local service catalogue."""

    def __init__(self) -> None:
        self._items: dict[str, ServiceRecord] = {}
        self._seed()

    def _seed(self) -> None:
        seeds = (
            ("catalog-service", "AegisShop Catalog", "http://catalog-service:9001"),
            ("cart-service", "AegisShop Cart", "http://cart-service:9002"),
            ("order-service", "AegisShop Order", "http://order-service:9003"),
            ("payment-service", "AegisShop Payment", "http://payment-service:9004"),
            ("registry-service", "AegisDeploy Registry", "http://registry-service:8101"),
            ("deployments-service", "AegisDeploy Deployments", "http://deployments-service:8701"),
        )
        for sid, name, url in seeds:
            rec = ServiceRecord(id=sid, name=name, url=url, last_heartbeat_at=_now())
            self._items[sid] = rec

    def reset(self) -> None:
        self._items.clear()
        self._seed()

    def list(self, status: str | None = None, include_heartbeats: bool = True) -> list[dict[str, str | None]]:
        out = [rec.as_dict(include_heartbeats) for rec in self._items.values()]
        if status:
            out = [row for row in out if row["status"] == status]
        return sorted(out, key=lambda row: row["id"] or "")

    def get(self, service_id: str) -> ServiceRecord | None:
        rec = self._items.get(service_id)
        if rec:
            rec.refresh_status()
        return rec

    def register(self, service_id: str, name: str, url: str, version: str = "0.1.0") -> ServiceRecord:
        rec = ServiceRecord(
            id=service_id,
            name=name,
            url=url,
            version=version,
            last_heartbeat_at=_now(),
        )
        self._items[service_id] = rec
        return rec

    def heartbeat(self, service_id: str) -> ServiceRecord | None:
        rec = self._items.get(service_id)
        if rec is None:
            return None
        rec.last_heartbeat_at = _now()
        rec.refresh_status()
        return rec


store = RegistryStore()
