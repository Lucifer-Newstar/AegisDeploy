"""AegisDeploy telemetry envelope contract (v0.2).

The single source of truth for every event that flows through the platform
(see docs/architecture/telemetry-model.md). Everything — metrics, logs, traces,
deployments, anomalies, incidents, remediations, audit — is wrapped in an
``EventEnvelope`` so producers and consumers never need bespoke adapters.

v0.2 (2026-09-01) adds the Deployment Intelligence fields (risk_score,
risk_factors, canary, rollout) — all optional and backward-compatible.
"""

from telemetry.envelope import (
    DeploymentContext,
    EventEnvelope,
    anomaly_payload,
    deployment_payload,
    log_payload,
    metric_payload,
)

__all__ = [
    "EventEnvelope",
    "DeploymentContext",
    "anomaly_payload",
    "deployment_payload",
    "log_payload",
    "metric_payload",
]
