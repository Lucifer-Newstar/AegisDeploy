"""Tests for payment-service."""

from fastapi.testclient import TestClient
from payment_service.main import app, reset_payments

client = TestClient(app)


def setup_function() -> None:
    reset_payments()


def test_health() -> None:
    assert client.get("/health").status_code == 200


def test_charge_succeeds() -> None:
    resp = client.post("/payments", json={"order_id": "ord-1", "amount": 39.99})
    assert resp.status_code == 201
    assert resp.json()["status"] == "succeeded"
    pid = resp.json()["id"]
    assert client.get(f"/payments/{pid}").status_code == 200


def test_unknown_order_404() -> None:
    assert client.post("/payments", json={"order_id": "missing", "amount": 1}).status_code == 404


def test_declined_402() -> None:
    assert client.post("/payments", json={"order_id": "ord-1", "amount": 0.01}).status_code == 402


def test_unknown_payment_404() -> None:
    assert client.get("/payments/nope").status_code == 404
