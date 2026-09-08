"""Tests for registry-service (A2)."""

from fastapi.testclient import TestClient
from registry_service.main import app
from registry_service.store import store

client = TestClient(app)


def setup_function() -> None:
    store.reset()


def test_health() -> None:
    assert client.get("/health").json() == {"status": "healthy"}


def test_ready() -> None:
    resp = client.get("/ready")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ready"


def test_list_includes_seed() -> None:
    rows = client.get("/services").json()
    ids = {row["id"] for row in rows}
    assert "catalog-service" in ids
    assert "registry-service" in ids


def test_register_and_get() -> None:
    resp = client.post(
        "/services",
        json={"id": "ml-service", "name": "ML", "url": "http://ml-service:8501"},
    )
    assert resp.status_code == 201
    got = client.get("/services/ml-service")
    assert got.status_code == 200
    assert got.json()["name"] == "ML"


def test_unknown_service_404() -> None:
    assert client.get("/services/no-such").status_code == 404


def test_heartbeat_unknown_404() -> None:
    assert client.post("/services/no-such/heartbeat").status_code == 404


def test_heartbeat_updates() -> None:
    before = client.get("/services/catalog-service").json()["last_heartbeat_at"]
    resp = client.post("/services/catalog-service/heartbeat")
    assert resp.status_code == 200
    assert resp.json()["last_heartbeat_at"] >= before
