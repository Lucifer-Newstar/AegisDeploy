"""Tests for cart-service."""

from cart_service.main import app, reset_carts
from fastapi.testclient import TestClient

client = TestClient(app)


def setup_function() -> None:
    reset_carts()


def test_health() -> None:
    assert client.get("/health").json() == {"status": "healthy"}


def test_empty_cart() -> None:
    resp = client.get("/cart/user-01")
    assert resp.status_code == 200
    assert resp.json()["items"] == []


def test_add_item() -> None:
    resp = client.post("/cart/user-01/items", json={"product_id": "p-001", "quantity": 2})
    assert resp.status_code == 200
    body = resp.json()
    assert body["items"][0]["quantity"] == 2
    assert body["total"] == 79.98


def test_unknown_product_404() -> None:
    resp = client.post("/cart/user-01/items", json={"product_id": "p-999", "quantity": 1})
    assert resp.status_code == 404
