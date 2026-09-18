"""Tests for order-service."""

from fastapi.testclient import TestClient
from order_service.main import app, reset_orders

client = TestClient(app)


def setup_function() -> None:
    reset_orders()


def test_health() -> None:
    assert client.get("/health").status_code == 200


def test_place_demo_order() -> None:
    resp = client.post("/orders", json={"user_id": "user-01"})
    assert resp.status_code == 201
    body = resp.json()
    assert body["status"] == "created"
    assert body["total"] == 39.99
    got = client.get(f"/orders/{body['id']}")
    assert got.status_code == 200


def test_empty_cart_400() -> None:
    assert client.post("/orders", json={"user_id": "nobody"}).status_code == 400


def test_unknown_order_404() -> None:
    assert client.get("/orders/missing").status_code == 404
