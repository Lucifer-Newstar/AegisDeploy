# Object Diagram — Active Incident Snapshot (db-down)

> **Diagram 3 (UML 2.5 — Structural).** A concrete **snapshot of instances** at
> `2026-08-31T10:17:02Z` during the database-failure demo scenario: the moment the
> AI has produced a root-cause hypothesis and the remediation is **pending approval**.
> Realistic values from the demo scenario; instances map 1:1 to the classes of
> Diagram 2a. Decided 2026-08-31.

```mermaid
---
title: "Object Diagram — db-down incident snapshot @ 10:17:02Z"
---
classDiagram
    direction TB

    %% ═══ INSTANCES (object : class) ════════════════════════
    class orderSvc["orderSvc : Service"]
    orderSvc : +str id = svc-order-01
    orderSvc : +str name = order-service
    orderSvc : +str owner = backend-team
    orderSvc : +str environment = dev
    orderSvc : +str health = degraded

    class inc1["inc1 : Incident"]
    inc1 : +str id = inc_01J8A2
    inc1 : +IncidentStatus status = INVESTIGATING
    inc1 : +int severity = 1
    inc1 : +datetime created_at = 2026-08-31T10:15:41Z
    inc1 : +list~str~ affected_service_ids = [svc-order-01]
    inc1 : +float mttd_s = 69

    class anom1["anom1 : Anomaly"]
    anom1 : +str id = anom_01J8A1
    anom1 : +str metric = http_server_request_duration_seconds_p95
    anom1 : +dict labels = {service: order-service}
    anom1 : +float score = 0.97
    anom1 : +float threshold = 0.9
    anom1 : +str model = isolation-forest-v1
    anom1 : +str window = 10:10:00Z – 10:15:00Z

    class evMetric["evMetric : Evidence"]
    evMetric : +str id = evt_01J8A3
    evMetric : +str type = metric_window
    evMetric : +str source = prometheus
    evMetric : +dict content = {query: http_server_request_duration_seconds_p95{service=order-service}, p95: 1.42s}

    class evLogs["evLogs : Evidence"]
    evLogs : +str id = evt_01J8A4
    evLogs : +str type = log_excerpt
    evLogs : +str source = loki
    evLogs : +dict content = {message: connection to postgres failed: timeout, count: 12}

    class evTrace["evTrace : Evidence"]
    evTrace : +str id = evt_01J8A5
    evTrace : +str type = trace_sample
    evTrace : +str source = tempo
    evTrace : +str trace_id = 4bf92f3577b34da6
    evTrace : +dict content = {failed_span: order-service/place-order, duration_ms: 8420}

    class hyp1["hyp1 : RootCauseHypothesis"]
    hyp1 : +str summary = postgres-unreachable-since-10:14:32
    hyp1 : +float confidence = 0.84
    hyp1 : +str failure_pattern = dependency-db-down
    hyp1 : +str runbook_id = rb-004

    class ra1["ra1 : RemediationAction"]
    ra1 : +str id = ra_01J8A6
    ra1 : +str incident_id = inc_01J8A2
    ra1 : +ActionType action_type = RESTART
    ra1 : +RiskClass risk_class = LOW
    ra1 : +str mode = approval
    ra1 : +str status = recommended

    class pol1["pol1 : Policy"]
    pol1 : +str id = restart-unhealthy-workload
    pol1 : +list~str~ actions = [workload.restart]
    pol1 : +RiskClass risk_class = LOW
    pol1 : +bool reversible = true
    pol1 : +bool requires_approval = true
    pol1 : +int max_blast_radius = 1

    class ap1["ap1 : ApprovalRequest"]
    ap1 : +str id = apr_01J8A7
    ap1 : +str action_id = ra_01J8A6
    ap1 : +str requested_by = system:reasoning
    ap1 : +str status = pending

    class aud1["aud1 : AuditLogEntry"]
    aud1 : +str id = aud_01J8A8
    aud1 : +str actor = system:reasoning
    aud1 : +str action = incident.create
    aud1 : +str target = inc_01J8A2
    aud1 : +str outcome = success

    %% ═══ OBJECT LINKS (labeled) ════════════════════════════
    orderSvc ---|affected by| inc1
    inc1 ---|caused by| anom1
    inc1 ---|contains| evMetric
    inc1 ---|contains| evLogs
    inc1 ---|contains| evTrace
    inc1 ---|has| hyp1
    hyp1 ---|cites| evLogs
    hyp1 ---|cites| evMetric
    inc1 ---|proposes| ra1
    ra1 ---|evaluated by| pol1
    ra1 ---|requires| ap1
    inc1 ---|creation logged in| aud1

    %% ═══ COLOR CODING ══════════════════════════════════════
    classDef svc fill:#dbeafe,stroke:#2563eb,color:#1e3a8a;
    classDef domain fill:#ecfdf5,stroke:#059669,color:#064e3b;
    classDef action fill:#fef3c7,stroke:#d97706,color:#78350f;
    class orderSvc svc;
    class inc1,anom1,evMetric,evLogs,evTrace,hyp1,aud1 domain;
    class ra1,pol1,ap1 action;
```

---

## 1. Scenario Timeline (what this snapshot shows)

| Time (2026-08-31) | Event |
|---|---|
| 10:14:32 | Chaoslab injects `db-down` fault — Postgres becomes unreachable for `order-service` |
| 10:15:00 | p95 latency spikes (0.31 s → 1.42 s); error rate 8.1% |
| 10:15:24 | Isolation Forest flags anomaly `anom1` (score 0.97 > 0.9) |
| 10:15:41 | Incident `inc1` created (sev1) — **MTTD = 69 s** |
| 10:16:05 | Evidence collected: metric window, log excerpt (×12 timeouts), failing trace |
| 10:16:40 | Hypothesis `hyp1` generated (confidence 0.84) citing the evidence |
| 10:17:02 | Remediation `ra1` (restart, LOW risk) recommended; policy matches → **pending approval** |
| 📸 | **Snapshot shown in this diagram** |

## 2. Object Inventory

| Object | Class (Diagram 2a) | Role in snapshot |
|---|---|---|
| `orderSvc` | Service | The affected service (health: degraded) |
| `inc1` | Incident | The open incident (INVESTIGATING, sev1) |
| `anom1` | Anomaly | The detected anomaly that triggered the incident |
| `evMetric` / `evLogs` / `evTrace` | Evidence | The three evidence items collected (Prometheus / Loki / Tempo) |
| `hyp1` | RootCauseHypothesis | The AI's top hypothesis, citing evidence |
| `ra1` | RemediationAction | Recommended restart (LOW risk) |
| `pol1` | Policy | The policy that evaluated the action (approval required) |
| `ap1` | ApprovalRequest | The pending human approval |
| `aud1` | AuditLogEntry | The audit record of incident creation |

## 3. Link Semantics

| Link | Meaning |
|---|---|
| `orderSvc —affected by→ inc1` | The incident affects exactly this service |
| `inc1 —contains→ ev*` | Evidence is composed into the incident (append-only) |
| `hyp1 —cites→ ev*` | The hypothesis is **grounded** in evidence (rule: no claim without evidence) |
| `ra1 —evaluated by→ pol1` | The policy engine decides the execution mode |
| `ra1 —requires→ ap1` | Approval pending — the exact moment of human governance |

> Next state (not shown): `ap1.approve(user: navin)` → `ra1.execute()` → recovery
> verification → incident `CLOSED` (see state machine diagram, #10).
