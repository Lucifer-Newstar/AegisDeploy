"""Tests for deployments-service (DI-1)."""

from copy import deepcopy
from typing import Any

from deployments_service.main import app
from deployments_service.store import store
from fastapi.testclient import TestClient

client = TestClient(app)

ENVELOPE: dict[str, Any] = {
    "id": "evt_01J8B2ABC",
    "schema_version": "0.2",
    "source": "deployment",
    "type": "deployment",
    "service": "catalog-service",
    "timestamp": "2026-09-08T10:00:00Z",
    "payload": {
        "action": "deploy",
        "revision": "v0.1.0",
        "triggered_by": "pipeline",
        "status": "succeeded",
    },
}


def setup_function() -> None:
    store.reset()


def test_health() -> None:
    assert client.get("/health").status_code == 200


def test_record_and_get() -> None:
    created = client.post("/deployments", json=ENVELOPE)
    assert created.status_code == 201
    got = client.get("/deployments/evt_01J8B2ABC")
    assert got.status_code == 200
    assert got.json()["revision"] == "v0.1.0"


def test_idempotent_replay() -> None:
    assert client.post("/deployments", json=ENVELOPE).status_code == 201
    replay = client.post("/deployments", json=ENVELOPE)
    assert replay.status_code == 200
    assert replay.json()["event_id"] == "evt_01J8B2ABC"


def test_list_newest_first() -> None:
    first = deepcopy(ENVELOPE)
    second = deepcopy(ENVELOPE)
    second["id"] = "evt_02"
    second["payload"]["revision"] = "v0.1.1"
    client.post("/deployments", json=first)
    client.post("/deployments", json=second)
    rows = client.get("/deployments", params={"service": "catalog-service"}).json()
    assert [row["event_id"] for row in rows] == ["evt_02", "evt_01J8B2ABC"]


def test_latest() -> None:
    client.post("/deployments", json=ENVELOPE)
    resp = client.get("/deployments/catalog-service/latest")
    assert resp.status_code == 200
    assert resp.json()["service"] == "catalog-service"


def test_unknown_404() -> None:
    assert client.get("/deployments/missing").status_code == 404


def test_invalid_envelope_422() -> None:
    bad = dict(ENVELOPE)
    bad["type"] = "metric"
    assert client.post("/deployments", json=bad).status_code == 422
