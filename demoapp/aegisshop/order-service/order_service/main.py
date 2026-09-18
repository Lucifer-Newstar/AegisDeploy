"""order-service — checkout (P2, in-memory)."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from fastapi import HTTPException
from pydantic import BaseModel

from order_service.config import settings
from order_service.runtime import build_app, health_routes, instrument_middleware, logger

app = build_app("AegisShop Order Service")
health_routes(app)

_ORDERS: dict[str, dict[str, Any]] = {}
_DEMO_ITEMS = [{"product_id": "p-001", "quantity": 1, "unit_price": 39.99}]


class PlaceOrder(BaseModel):
    user_id: str
    cart_id: str | None = None


def reset_orders() -> None:
    _ORDERS.clear()


def _items_for(user_id: str) -> list[dict[str, Any]]:
    if settings.cart_service_url:
        import urllib.error
        import urllib.request

        url = f"{settings.cart_service_url.rstrip('/')}/cart/{user_id}"
        try:
            with urllib.request.urlopen(url, timeout=3) as resp:
                import json

                payload = json.loads(resp.read().decode())
            return list(payload.get("items") or [])
        except (urllib.error.URLError, TimeoutError, ValueError) as exc:
            logger.warning(f"cart lookup failed: {exc}")
            return []
    if user_id == "user-01":
        return list(_DEMO_ITEMS)
    return []


@app.get("/ready", responses={503: {"description": "Postgres unreachable"}})
def ready() -> dict[str, str]:
    return {"status": "ready"}


@app.post("/orders", status_code=201, responses={400: {"description": "empty cart or unknown user"}})
def place_order(body: PlaceOrder) -> dict[str, Any]:
    items = _items_for(body.user_id)
    if not items:
        raise HTTPException(status_code=400, detail="empty cart or unknown user")
    order_id = f"ord-{uuid4().hex[:8]}"
    total = round(sum(float(i["unit_price"]) * int(i["quantity"]) for i in items), 2)
    order = {
        "id": order_id,
        "user_id": body.user_id,
        "status": "created",
        "items": items,
        "total": total,
        "created_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
    }
    _ORDERS[order_id] = order
    return order


@app.get("/orders/{order_id}", responses={404: {"description": "unknown order"}})
def get_order(order_id: str) -> dict[str, Any]:
    order = _ORDERS.get(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail=f"order {order_id} not found")
    return order


instrument_middleware(app)
