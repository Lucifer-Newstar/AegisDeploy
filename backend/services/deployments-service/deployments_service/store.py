"""In-memory deployment history (DI-1)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


def _now() -> datetime:
    return datetime.now(UTC)


@dataclass
class DeploymentRecord:
    event_id: str
    service: str
    revision: str
    status: str
    envelope: dict[str, Any]
    stored_at: datetime = field(default_factory=_now)

    def as_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "service": self.service,
            "revision": self.revision,
            "status": self.status,
            "envelope": self.envelope,
            "stored_at": self.stored_at.isoformat().replace("+00:00", "Z"),
        }


def _startup_envelope(service: str, revision: str = "v0.1.0") -> dict[str, Any]:
    ts = _now().isoformat().replace("+00:00", "Z")
    return {
        "id": f"evt_startup_{service}_{revision}",
        "schema_version": "0.2",
        "source": "deployment",
        "type": "deployment",
        "service": service,
        "environment": "dev",
        "severity": "info",
        "timestamp": ts,
        "payload": {
            "action": "deploy",
            "revision": revision,
            "triggered_by": "platform",
            "status": "succeeded",
        },
    }


class DeploymentStore:
    def __init__(self) -> None:
        self._items: dict[str, DeploymentRecord] = {}
        self.seed_startup_deploys()

    def seed_startup_deploys(self) -> None:
        """DI-1 pipeline hook: every process start records the running revision."""
        for service in (
            "catalog-service",
            "cart-service",
            "order-service",
            "payment-service",
            "registry-service",
            "deployments-service",
        ):
            envelope = _startup_envelope(service)
            rec = DeploymentRecord(
                event_id=str(envelope["id"]),
                service=service,
                revision="v0.1.0",
                status="succeeded",
                envelope=envelope,
            )
            self.put(rec)

    def reset(self) -> None:
        self._items.clear()

    def get(self, event_id: str) -> DeploymentRecord | None:
        return self._items.get(event_id)

    def put(self, rec: DeploymentRecord) -> tuple[DeploymentRecord, bool]:
        existing = self._items.get(rec.event_id)
        if existing is not None:
            return existing, False
        self._items[rec.event_id] = rec
        return rec, True

    def list(
        self, service: str | None = None, status: str | None = None, limit: int = 50
    ) -> list[DeploymentRecord]:
        rows = list(self._items.values())
        if service:
            rows = [r for r in rows if r.service == service]
        if status:
            rows = [r for r in rows if r.status == status]
        rows.sort(key=lambda r: r.stored_at, reverse=True)
        return rows[: max(0, min(limit, 500))]

    def latest(self, service: str) -> DeploymentRecord | None:
        rows = [r for r in self._items.values() if r.service == service]
        if not rows:
            return None
        rows.sort(key=lambda r: r.stored_at, reverse=True)
        return rows[0]


store = DeploymentStore()
