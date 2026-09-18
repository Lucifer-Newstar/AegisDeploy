"""payment-service — simulated charges (P2, in-memory)."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from fastapi import HTTPException
from pydantic import BaseModel, Field

from payment_service.runtime import build_app, health_routes, instrument_middleware

app = build_app("AegisShop Payment Service")
health_routes(app)

_PAYMENTS: dict[str, dict[str, Any]] = {}


class Charge(BaseModel):
    order_id: str
    amount: float = Field(..., gt=0)


def reset_payments() -> None:
    _PAYMENTS.clear()


@app.get("/ready", responses={503: {"description": "Postgres unreachable"}})
def ready() -> dict[str, str]:
    return {"status": "ready"}


@app.post(
    "/payments",
    status_code=201,
    responses={402: {"description": "payment declined"}, 404: {"description": "unknown order"}},
)
def charge(body: Charge) -> dict[str, Any]:
    if body.order_id in {"missing", "unknown"}:
        raise HTTPException(status_code=404, detail=f"order {body.order_id} not found")
    if body.amount == 0.01:
        raise HTTPException(status_code=402, detail="payment declined")
    payment_id = f"pay-{uuid4().hex[:8]}"
    payment = {
        "id": payment_id,
        "order_id": body.order_id,
        "status": "succeeded",
        "amount": body.amount,
        "paid_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
    }
    _PAYMENTS[payment_id] = payment
    return payment


@app.get("/payments/{payment_id}", responses={404: {"description": "unknown payment"}})
def get_payment(payment_id: str) -> dict[str, Any]:
    payment = _PAYMENTS.get(payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail=f"payment {payment_id} not found")
    return payment


instrument_middleware(app)
