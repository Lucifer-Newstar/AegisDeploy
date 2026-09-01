# Telemetry & Event Model

Every signal entering or flowing through AegisDeploy — metric samples, logs, traces,
Kubernetes events, deployments, anomalies, incidents, remediations — is wrapped in a
**single event envelope**. This contract is what lets the Event Layer, anomaly pipeline,
AI reasoning layer, and audit store interoperate without bespoke adapters.

> Status: **v0.2 (contract draft, + DI fields)** — extended 2026-09-01 for the
> Deployment Intelligence tier (additive fields: `deployment.risk_score`,
> `payload.canary`, `payload.rollout`; see
> [deployment-intelligence.md](deployment-intelligence.md)). Locked at M2 when
> ingestion lands. Changes are additive; breaking changes require an ADR.

## 1. The Envelope

```json
{
  "id": "evt_01J8V4X2F6...",
  "schema_version": "0.1",
  "timestamp": "2026-08-31T10:15:30.000Z",
  "source": "prometheus | loki | tempo | k8s | deployment | chaoslab | ml | ai | policy | executor",
  "type": "metric | log | trace | k8s_event | deployment | anomaly | incident | remediation | audit | health",
  "service": "api-gateway",
  "environment": "dev | staging | prod",
  "correlation_id": "corr_...",
  "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
  "severity": "info | warning | critical",
  "deployment": {
    "revision": "abc1234",
    "version": "v2.3.1",
    "changed_at": "2026-08-31T10:14:00.000Z"
  },
  "payload": {}
}
```

### Field rules

| Field | Rule |
|---|---|
| `id` | Unique, stable, ULID or UUIDv7 (sortable by time). |
| `timestamp` | RFC 3339 UTC. Producer time, not ingestion time. |
| `source` / `type` | Enum values (see below); unknown values are rejected at ingestion. |
| `correlation_id` | Propagated from the originating request/experiment; lets the AI reason across signals. |
| `trace_id` | W3C trace ID when a distributed trace exists. |
| `deployment` | Present when a deployment/revision is known for the emitting service. |
| `payload` | Type-specific body (below). |

## 2. Payload Schemas by Type

### 2.1 `metric`
```json
{
  "name": "http_server_request_duration_seconds",
  "labels": { "service": "api-gateway", "route": "/v1/orders", "method": "GET" },
  "value": 1.42,
  "unit": "seconds"
}
```

### 2.2 `log`
```json
{
  "message": "connection to postgres failed: timeout",
  "level": "ERROR",
  "attributes": { "db.system": "postgresql", "db.operation": "SELECT" }
}
```

### 2.3 `trace`
```json
{
  "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
  "root_service": "api-gateway",
  "duration_ms": 8420,
  "status": "error",
  "span_count": 18,
  "failed_spans": ["inventory-service/query-stock"]
}
```

### 2.4 `k8s_event`
```json
{
  "kind": "Pod",
  "name": "api-gateway-7d8f9c-4k2wz",
  "namespace": "production",
  "reason": "CrashLoopBackOff",
  "count": 12,
  "message": "back-off restarting failed container"
}
```

### 2.5 `deployment`
```json
{
  "service": "api-gateway",
  "action": "deploy | rollback | scale | restart",
  "revision": "abc1234",
  "previous_revision": "def5678",
  "triggered_by": "github-actions | human | executor",
  "status": "succeeded | failed | in_progress",
  "risk_score": 0.72,
  "risk_factors": ["large diff", "db-migration", "friday-17h"],
  "canary": { "enabled": true, "traffic_split": 0.1, "healthy": true },
  "rollout": { "status": "monitoring", "bad_after_s": null }
}
```

> **v0.2 additions (DI tier, 2026-09-01):** `risk_score` + `risk_factors` (DI-2),
> `canary` block (DI-6), `rollout` block (DI-4). All optional and backward-compatible
> — older producers that omit them remain valid.

### 2.6 `anomaly`
```json
{
  "metric": "http_server_request_duration_seconds_p95",
  "labels": { "service": "api-gateway" },
  "score": 0.97,
  "threshold": 0.9,
  "model": "isolation-forest-v1",
  "window": { "start": "2026-08-31T10:10:00Z", "end": "2026-08-31T10:15:00Z" },
  "baseline": { "mean": 0.35, "std": 0.08 }
}
```

### 2.7 `incident`
```json
{
  "id": "inc_01J8...",
  "status": "open | investigating | remediating | verifying | closed | escalated",
  "severity": "sev1 | sev2 | sev3 | sev4",
  "affected_services": ["api-gateway", "inventory-service"],
  "summary": "p95 latency spike after deploy abc1234",
  "root_cause": { "hypothesis": "...", "confidence": 0.82, "evidence": ["evt_...", "evt_..."] },
  "mttd_s", 120,
  "mttr_s": null,
  "related_anomalies": ["evt_..."]
}
```

### 2.8 `remediation`
```json
{
  "incident_id": "inc_01J8...",
  "action": "workload.restart | deployment.rollback | workload.scale | instance.replace | config.update | escalate",
  "risk_class": "low | medium | high | forbidden",
  "mode": "auto | approval",
  "status": "recommended | approved | rejected | executed | failed | cancelled",
  "approved_by": "user:navin | policy:auto",
  "execution": { "command": "kubectl rollout restart deploy/api-gateway", "result": "succeeded" }
}
```

### 2.9 `audit`
```json
{
  "actor": "user:navin | policy:auto | system:policy-engine",
  "action": "incident.create | remediation.approve | remediation.execute | autonomy.mode.set",
  "target": "inc_01J8...",
  "outcome": "success | denied | failed",
  "reason": "policy:rollback-deployment matched"
}
```

### 2.10 `health`
```json
{
  "service": "api-gateway",
  "checks": { "liveness": "ok", "readiness": "ok", "dependencies": { "postgres": "degraded" } },
  "slo": { "availability_30d": 0.9995, "budget_remaining": 0.62 }
}
```

## 3. Event Types by Producer

| Producer | Emits |
|---|---|
| OTel collector / Prometheus / Loki / Tempo | `metric`, `log`, `trace` |
| k8s watcher | `k8s_event`, `deployment` |
| Deployment tracker (CI webhook / poller) | `deployment` |
| Chaos lab | `metric`, `log`, `trace`, `k8s_event`, `health` (+ experiment metadata) |
| ML pipeline | `anomaly` |
| Incident manager | `incident` |
| AI reasoning layer | `incident` (evidence, root cause), `remediation` (recommended) |
| Policy engine / executor | `remediation`, `audit` |
| Recovery verifier | `incident` (closed/escalated), `health` |

## 4. Storage Mapping

| Event type | Primary store | Notes |
|---|---|---|
| `metric` | Prometheus (+ Postgres rollups later) | PromQL for windows; raw in Prometheus |
| `log`, `trace` | Loki / Tempo | queried via LogQL/Tempo API |
| `deployment`, `incident`, `remediation`, `audit` | PostgreSQL | relational, queryable |
| `anomaly` | PostgreSQL + Event Layer | replayable |
| Evidence attachments | PostgreSQL (JSONB) | immutable, append-only |
| Runbooks, past incidents, docs (RAG corpus) | pgvector | embedded at M4 |

## 5. Event Layer Semantics (Redis Streams, initial)

- One stream per event type (`st:metric`, `st:anomaly`, `st:incident`, ...).
- Consumer groups per logical consumer (anomaly pipeline, incident manager, AI reasoner).
- Events are retained per-stream with TTLs (metrics/health short, incident/remediation/audit long).
- At-least-once delivery; consumers must be idempotent on `id`.
