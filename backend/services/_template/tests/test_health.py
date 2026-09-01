"""Health/metrics tests for the reference service template.

Verifies the endpoints every AegisDeploy service must expose: /health,
/ready, /metrics, and the metadata root. Uses FastAPI's TestClient (httpx).
"""

from fastapi.testclient import TestClient
from template_service.main import app

client = TestClient(app)


class TestHealthEndpoints:
    """The contract every service inherits from the template."""

    def test_root_returns_service_metadata(self) -> None:
        resp = client.get("/")
        assert resp.status_code == 200
        body = resp.json()
        assert body["service"] == "_template"
        assert body["status"] == "ok"

    def test_health_returns_healthy(self) -> None:
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json() == {"status": "healthy"}

    def test_ready_returns_ready(self) -> None:
        resp = client.get("/ready")
        assert resp.status_code == 200
        assert resp.json() == {"status": "ready"}

    def test_metrics_expose_prometheus_format(self) -> None:
        """/metrics must return Prometheus text format with our counters."""
        resp = client.get("/metrics")
        assert resp.status_code == 200
        assert "text/plain" in resp.headers["content-type"]
        assert "http_server_requests_total" in resp.text
