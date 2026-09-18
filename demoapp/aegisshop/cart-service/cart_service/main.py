"""cart-service — per-user shopping carts (P2, in-memory)."""

from __future__ import annotations

from typing import Any

from fastapi import HTTPException
from pydantic import BaseModel, Field

from cart_service.runtime import build_app, health_routes, instrument_middleware

PRICES: dict[str, float] = {'p-001': 39.99, 'p-002': 89.99, 'p-003': 329.0, 'p-004': 49.5, 'p-005': 24.99}

app = build_app("AegisShop Cart Service")
health_routes(app)

_CARTS: dict[str, dict[str, Any]] = {}


class AddItem(BaseModel):
    product_id: str
    quantity: int = Field(..., ge=1)


def _cart(user_id: str) -> dict[str, Any]:
    cart = _CARTS.setdefault(user_id, {"user_id": user_id, "items": []})
    total = sum(float(item["unit_price"]) * int(item["quantity"]) for item in cart["items"])
    cart["total"] = round(total, 2)
    return cart


def reset_carts() -> None:
    _CARTS.clear()


@app.get("/ready", responses={503: {"description": "Postgres unreachable"}})
def ready() -> dict[str, str]:
    return {"status": "ready"}


@app.get("/cart/{user_id}")
def get_cart(user_id: str) -> dict[str, Any]:
    return _cart(user_id)


@app.post("/cart/{user_id}/items", responses={404: {"description": "unknown product"}})
def add_item(user_id: str, body: AddItem) -> dict[str, Any]:
    if body.product_id not in PRICES:
        raise HTTPException(status_code=404, detail=f"product {body.product_id} not found")
    cart = _cart(user_id)
    for item in cart["items"]:
        if item["product_id"] == body.product_id:
            item["quantity"] = int(item["quantity"]) + body.quantity
            return _cart(user_id)
    cart["items"].append(
        {
            "product_id": body.product_id,
            "quantity": body.quantity,
            "unit_price": PRICES[body.product_id],
        }
    )
    return _cart(user_id)


instrument_middleware(app)
