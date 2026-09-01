"""Tests for the catalog-service vertical slice.

Covers the API contract (list/get products, 404 handling) and the health/
metrics endpoints inherited from the service template conventions.
"""

from catalog_service.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


class TestCatalogApi:
    """The shop-facing catalog contract."""

    def test_list_products_returns_seed(self) -> None:
        resp = client.get("/products")
        assert resp.status_code == 200
        products = resp.json()
        assert len(products) >= 5
        assert any(p["id"] == "p-001" for p in products)

    def test_get_product_returns_item(self) -> None:
        resp = client.get("/products/p-001")
        assert resp.status_code == 200
        assert resp.json()["name"] == "Laptop Stand"
        assert resp.json()["price"] == 39.99

    def test_get_unknown_product_returns_404(self) -> None:
        resp = client.get("/products/p-999")
        assert resp.status_code == 404


class TestObservabilityContract:
    """The A1 observability contract every service must satisfy."""

    def test_health(self) -> None:
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json() == {"status": "healthy"}

    def test_ready(self) -> None:
        resp = client.get("/ready")
        assert resp.status_code == 200

    def test_metrics_prometheus_format(self) -> None:
        resp = client.get("/metrics")
        assert resp.status_code == 200
        assert "http_server_requests_total" in resp.text
        assert "catalog_products_total" in resp.text

    def test_fault_hook_advertised(self) -> None:
        """/faults documents the chaos-lab contract (A11)."""
        resp = client.get("/faults")
        assert resp.status_code == 200
        assert "planned" in resp.json()
