"""In-memory catalog data for the vertical slice.

Deliberately no database yet (Postgres persistence lands in P2 with the full
AegisShop build). A small seed set keeps the demo meaningful and tests simple.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class Product(BaseModel):
    """A catalog product (matches the AegisShop class diagram entity)."""

    id: str = Field(..., description="Product id (stable, e.g. 'p-001')")
    name: str
    price: float = Field(..., gt=0)
    stock: int = Field(default=0, ge=0)
    category: str = "general"


#: Seed catalog — a small set of shop products used by the demo + tests.
CATALOG: dict[str, Product] = {
    "p-001": Product(id="p-001", name="Laptop Stand", price=39.99, stock=120, category="accessories"),
    "p-002": Product(id="p-002", name="Mechanical Keyboard", price=89.99, stock=60, category="accessories"),
    "p-003": Product(id="p-003", name="4K Monitor 27in", price=329.0, stock=25, category="displays"),
    "p-004": Product(id="p-004", name="USB-C Hub", price=49.5, stock=200, category="accessories"),
    "p-005": Product(id="p-005", name="Ergonomic Mouse", price=24.99, stock=150, category="accessories"),
}
