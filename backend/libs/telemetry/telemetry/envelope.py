"""Event envelope models — the AegisDeploy telemetry contract (v0.2).

Design notes
------------
* Every event carries a stable ``id``, a producer ``timestamp`` (RFC 3339 UTC),
  ``source``/``type``/``service`` routing fields, optional correlation/trace
  ids, an optional deployment context, and a type-specific ``payload`` dict.
* The payload helpers below construct the canonical payload shapes for the
  core event types (metric, log, anomaly, deployment) so producers do not
  invent ad-hoc shapes (working-rules: no bespoke event shapes).
* v0.2 additions (Deployment Intelligence tier, ADR-0006): the deployment
  payload gains ``risk_score``, ``risk_factors`` (DI-2), ``canary`` (DI-6) and
  ``rollout`` (DI-4) blocks — all optional, so older producers stay valid.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

#: The current envelope schema version (must match docs/architecture/telemetry-model.md).
SCHEMA_VERSION: Literal["0.2"] = "0.2"

#: Allowed values for the routing fields (unknown values are rejected at ingestion).
EVENT_SOURCES = {"prometheus", "loki", "tempo", "k8s", "deployment", "chaoslab", "ml", "ai", "policy", "executor", "registry"}
EVENT_TYPES = {"metric", "log", "trace", "k8s_event", "deployment", "anomaly", "incident", "remediation", "audit", "health"}
SEVERITIES = {"info", "warning", "critical"}


def _utcnow() -> datetime:
    """Return the current time as an UTC-aware datetime (producer timestamp)."""
    return datetime.now(UTC)


class DeploymentContext(BaseModel):
    """Which deployment/revision the emitting service was running at event time.

    Present whenever the producer knows its current revision (DI-1 makes this
    available to every service once the deployment tracker lands in P2).
    """

    model_config = ConfigDict(extra="forbid")

    revision: str = Field(..., description="Deployment revision (e.g. git sha / image tag)")
    version: str | None = Field(default=None, description="Semantic version of the release")
    changed_at: datetime | None = Field(default=None, description="When this revision went live")


class EventEnvelope(BaseModel):
    """The universal wrapper for every event in the platform."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(..., min_length=1, description="Unique, stable event id (ULID or UUIDv7)")
    schema_version: Literal["0.2"] = Field(default=SCHEMA_VERSION, description="Envelope contract version")
    timestamp: datetime = Field(default_factory=_utcnow, description="Producer time (not ingestion time)")
    source: str = Field(..., description="Producer of the event (see EVENT_SOURCES)")
    type: str = Field(..., description="Event type (see EVENT_TYPES)")
    service: str = Field(..., min_length=1, description="Emitting service name")
    environment: str = Field(default="dev", description="Environment (dev | staging | prod)")
    correlation_id: str | None = Field(default=None, description="Correlates events from one request/experiment")
    trace_id: str | None = Field(default=None, description="W3C trace id when a distributed trace exists")
    severity: Literal["info", "warning", "critical"] = Field(default="info")
    deployment: DeploymentContext | None = Field(default=None, description="Deployment context (DI-1)")
    payload: dict[str, Any] = Field(default_factory=dict, description="Type-specific body")

    @field_validator("source")
    @classmethod
    def _source_must_be_known(cls, value: str) -> str:
        if value not in EVENT_SOURCES:
            raise ValueError(f"unknown event source: {value!r}")
        return value

    @field_validator("type")
    @classmethod
    def _type_must_be_known(cls, value: str) -> str:
        if value not in EVENT_TYPES:
            raise ValueError(f"unknown event type: {value!r}")
        return value


# ── Payload builders ──────────────────────────────────────────────────────────
# Each builder returns the canonical ``payload`` dict for its event type.
# Keeping them here (instead of in every service) is what enforces the contract.


def metric_payload(name: str, labels: dict[str, str], value: float, unit: str = "") -> dict[str, Any]:
    """Canonical payload for a single metric sample (type: ``metric``)."""
    return {"name": name, "labels": labels, "value": value, "unit": unit}


def log_payload(message: str, level: str = "INFO", attributes: dict[str, Any] | None = None) -> dict[str, Any]:
    """Canonical payload for a log line (type: ``log``)."""
    return {"message": message, "level": level.upper(), "attributes": attributes or {}}


def anomaly_payload(
    metric: str,
    labels: dict[str, str],
    score: float,
    threshold: float,
    model: str,
    window: dict[str, str],
    baseline: dict[str, float],
) -> dict[str, Any]:
    """Canonical payload for an anomaly event (type: ``anomaly``, produced by ml/)."""
    return {
        "metric": metric,
        "labels": labels,
        "score": score,
        "threshold": threshold,
        "model": model,
        "window": window,    # {"start": ..., "end": ...} RFC 3339
        "baseline": baseline,  # {"mean": ..., "std": ...}
    }


def deployment_payload(
    action: str,
    revision: str,
    previous_revision: str | None = None,
    triggered_by: str = "github-actions",
    status: str = "succeeded",
    # ── v0.2 Deployment Intelligence fields (all optional) ──
    risk_score: float | None = None,
    risk_factors: list[str] | None = None,
    canary: dict[str, Any] | None = None,
    rollout: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Canonical payload for a deployment event (type: ``deployment``, DI-1).

    v0.2 additions map to the DI tier:
      * ``risk_score``/``risk_factors``  → DI-2 (deployment risk scoring)
      * ``canary``                       → DI-6 (canary/progressive delivery)
      * ``rollout``                      → DI-4 (deploy-window evaluation state)
    """
    payload: dict[str, Any] = {
        "action": action,          # deploy | rollback | scale | restart
        "revision": revision,
        "previous_revision": previous_revision,
        "triggered_by": triggered_by,
        "status": status,          # succeeded | failed | in_progress
    }
    if risk_score is not None:
        payload["risk_score"] = risk_score
    if risk_factors:
        payload["risk_factors"] = risk_factors
    if canary is not None:
        payload["canary"] = canary
    if rollout is not None:
        payload["rollout"] = rollout
    return payload
