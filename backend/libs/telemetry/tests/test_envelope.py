"""Tests for the telemetry envelope contract (v0.2).

Verifies: defaults, required fields, source/type validation, deployment
context, and the v0.2 Deployment Intelligence payload fields (DI-2/DI-4/DI-6).
"""

from datetime import UTC, datetime
from typing import Any

import pytest
from pydantic import ValidationError
from telemetry import EventEnvelope, anomaly_payload, deployment_payload, metric_payload


def make_envelope(**overrides: Any) -> EventEnvelope:
    """Build a minimal valid envelope, overriding fields for specific tests."""
    base: dict[str, Any] = {"id": "evt_01J8A2TEST", "source": "prometheus", "type": "metric", "service": "catalog-service"}
    base.update(overrides)
    return EventEnvelope(**base)


class TestEnvelopeBasics:
    """Core envelope behavior: defaults, required fields, validation."""

    def test_minimal_envelope_has_defaults(self) -> None:
        """A minimal envelope gets schema_version 0.2, UTC timestamp, dev env."""
        env = make_envelope()
        assert env.schema_version == "0.2"
        assert env.environment == "dev"
        assert env.severity == "info"
        assert env.payload == {}
        assert env.deployment is None
        assert env.timestamp.tzinfo is not None  # timezone-aware (UTC)

    def test_required_fields_enforced(self) -> None:
        """Missing id/source/type/service must raise ValidationError."""
        for missing in ("id", "source", "type", "service"):
            data: dict[str, Any] = {"id": "evt_x", "source": "prometheus", "type": "metric", "service": "svc"}
            data.pop(missing)
            with pytest.raises(ValidationError):
                EventEnvelope(**data)

    def test_unknown_source_rejected(self) -> None:
        with pytest.raises(ValidationError):
            make_envelope(source="not-a-producer")

    def test_unknown_type_rejected(self) -> None:
        with pytest.raises(ValidationError):
            make_envelope(type="not-a-type")

    def test_extra_fields_rejected(self) -> None:
        """extra='forbid' keeps producers from smuggling bespoke top-level fields."""
        with pytest.raises(ValidationError):
            make_envelope(hacked="field")


class TestDeploymentContext:
    """The deployment block attached to the envelope (DI-1)."""

    def test_deployment_context_accepted(self) -> None:
        env = make_envelope(
            deployment={"revision": "abc1234", "version": "v2.3.1", "changed_at": datetime(2026, 9, 1, tzinfo=UTC)}
        )
        assert env.deployment is not None
        assert env.deployment.revision == "abc1234"
        assert env.deployment.version == "v2.3.1"


class TestPayloadBuilders:
    """Canonical payload shapes produced by the lib."""

    def test_metric_payload_shape(self) -> None:
        payload = metric_payload("http_server_request_duration_seconds", {"service": "catalog-service"}, 1.42, "seconds")
        assert payload["name"] == "http_server_request_duration_seconds"
        assert payload["value"] == 1.42
        assert payload["labels"]["service"] == "catalog-service"

    def test_anomaly_payload_shape(self) -> None:
        payload = anomaly_payload(
            metric="http_server_request_duration_seconds_p95",
            labels={"service": "catalog-service"},
            score=0.97,
            threshold=0.9,
            model="isolation-forest-v1",
            window={"start": "2026-09-01T10:10:00Z", "end": "2026-09-01T10:15:00Z"},
            baseline={"mean": 0.35, "std": 0.08},
        )
        assert payload["score"] == 0.97
        assert payload["window"]["start"] == "2026-09-01T10:10:00Z"

    def test_deployment_payload_v02_fields(self) -> None:
        """DI-2/DI-4/DI-6 fields ride the deployment event (v0.2 contract)."""
        payload = deployment_payload(
            action="deploy",
            revision="abc1234",
            previous_revision="def5678",
            risk_score=0.72,
            risk_factors=["large diff", "db-migration"],
            canary={"enabled": True, "traffic_split": 0.1, "healthy": True},
            rollout={"status": "monitoring", "bad_after_s": None},
        )
        assert payload["risk_score"] == 0.72
        assert payload["risk_factors"] == ["large diff", "db-migration"]
        assert payload["canary"]["traffic_split"] == 0.1
        assert payload["rollout"]["status"] == "monitoring"

    def test_deployment_payload_backward_compatible(self) -> None:
        """Omitting the v0.2 fields yields the plain v0.1-shaped payload."""
        payload = deployment_payload(action="deploy", revision="abc1234")
        assert set(payload) == {"action", "revision", "previous_revision", "triggered_by", "status"}
        assert payload["previous_revision"] is None
