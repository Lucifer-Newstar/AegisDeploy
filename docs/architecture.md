# Architecture

This document describes the component architecture of AegisSRE, the responsibilities of
each component, and the data flows between them. It is the source of truth that
implementation must conform to; deviations should be recorded as ADRs
(see [docs/adr/](adr/)).

## 1. Design Principles

| Principle | Meaning |
|---|---|
| **Observe everything** | All telemetry (metrics, logs, traces, events, deployments) is captured centrally with consistent structure. |
| **Trust evidence** | Every AI claim must cite telemetry evidence. No claim without evidence. |
| **Separate detection, reasoning, execution** | ML models detect; the LLM reasons; the policy engine decides; scoped executors act. No component performs another's role. |
| **Act within boundaries** | Execution is limited to predefined tools, least-privilege permissions, and policy-approved actions. |
| **Verify the result** | Every remediation ends with recovery verification before an incident can close. |
| **Compose now, K8s-ready** | Local development uses Docker Compose; all services map 1:1 to Kubernetes manifests under `infra/k8s/`. |

## 2. Component Map

```text
                         USER
                          │
                          ▼
                ┌───────────────────┐
                │   Web Dashboard   │
                │ React / Next.js   │
                └─────────┬─────────┘
                          │
                     API Gateway
                          │
              ┌───────────┴───────────┐
              │                       │
              ▼                       ▼
       Platform Services        Incident Services
              │                       │
              └───────────┬───────────┘
                          │
                     Event Layer
                          │
       ┌──────────────────┼──────────────────┐
       │                  │                  │
       ▼                  ▼                  ▼
     CI/CD            Deployment       Observability
       │                  │          ┌───────┼───────┐
       │                  │          │       │       │
       │                  │        Logs   Metrics  Traces
       └──────────────────┼──────────┴───────┴───────┘
                          │
                 Intelligence Engine
                          │
              ┌───────────┴───────────┐
              │                       │
              ▼                       ▼
       ML Anomaly Detection       AI Reasoning
              │                       │
              │                ┌──────┴──────┐
              │                │             │
              │               RAG        Tool Access
              └────────────────┴─────────────┘
                               │
                               ▼
                       Incident Analysis
                               │
                               ▼
                     Remediation Planner
                               │
                         Policy Engine
                               │
                    ┌──────────┴──────────┐
                    │                     │
              Human Approval       Safe Autonomous
                    │                 Actions
                    └──────────┬──────────┘
                               │
                               ▼
                         Remediation
                               │
                               ▼
                     Recovery Verification
                               │
                               ▼
                         Incident Closed
```

## 3. Component Responsibilities

### 3.1 Web Dashboard (frontend/)
Next.js + TypeScript console showing service health, telemetry, active incidents, AI
reasoning trails, remediation actions, approval UI, and measured MTTD/MTTR. Consumes the
API Gateway only — never talks to backends directly.

### 3.2 API Gateway
Single entry point for the dashboard and external integrations. Responsibilities:
routing, authentication, rate limiting, and request correlation. Implemented as a thin
service in front of the platform services (initially FastAPI; may be replaced by a
gateway proxy later — see ADR-0002).

### 3.3 Platform Services (backend/)
Core domain services of the control plane:

- **Service Registry** — catalog of monitored services, their owners, SLOs, and topology.
- **Telemetry Ingestion** — receives OTLP/metrics/log/trace/event data, validates it
  against the envelope contract (see [telemetry-model.md](telemetry-model.md)), and
  persists it.
- **Deployment Tracker** — records deployments/rollbacks as first-class events so RCA can
  correlate failures with changes.

### 3.4 Incident Services (backend/)
- **Incident Manager** — creates, updates, correlates, and closes incidents; owns the
  incident state machine (`open → investigating → remediating → verifying → closed/escalated`).
- **Evidence Store** — immutable append-only record of every piece of evidence attached to
  an incident (metric windows, log excerpts, trace IDs, k8s events, deployment records).
- **Audit Log** — append-only record of every action taken by the system or by a human
  through the platform (who/what/when/result).

### 3.5 Event Layer
The backbone that decouples producers (telemetry, deployments, chaoslab) from consumers
(anomaly detection, incident manager, AI reasoning). First implementation: Redis Streams
(ADR-0004). Every event uses the shared envelope (see telemetry-model.md).

### 3.6 Observability Stack (infra/)
- **OpenTelemetry Collector** — single ingestion point for OTLP; fans out to Prometheus,
  Loki, Tempo.
- **Prometheus** — metrics storage and querying (PromQL).
- **Loki** — log storage and querying (LogQL).
- **Tempo** — distributed trace storage and querying.
- **Grafana** — unified visualization and dashboards.

### 3.7 Intelligence Engine

#### ML Anomaly Detection (ml/)
Quantitative detection only. Consumes metric streams from the event layer, builds
features (rolling means, rates, residuals), and emits **anomaly scores** via statistical
baselines and Isolation Forest (initial models). Output: `anomaly.score` events — it does
**not** decide incident severity or cause.

#### AI Reasoning (ai/)
LLM-based reasoning over evidence. Responsibilities:

- incident summarization;
- evidence collection planning (which telemetry to fetch);
- root-cause hypothesis generation & explanation;
- remediation recommendation;
- runbook interpretation;
- postmortem generation.

**Retrieval-Augmented Generation (RAG):** retrieves previous incidents, runbooks, service
metadata, deployment history, and known failure patterns from a vector store (pgvector)
to ground the model in system-specific context.

**Controlled Tool Access:** the model can only invoke predefined read-only tools
(`get_metrics`, `get_logs`, `get_traces`, `get_service_health`, `get_deployment_history`,
`get_kubernetes_events`, `get_runbook`). It has **no** write access to infrastructure.

### 3.8 Remediation Planner & Policy Engine
- **Remediation Planner** — maps a root cause + recommended action to a concrete,
  executable remediation plan with risk classification.
- **Policy Engine** — the single decision point on *whether* and *how* an action may be
  executed: risk class, reversibility, required approval, blast radius, rate limits.
  Policies are declarative (see [autonomy-model.md](autonomy-model.md)).

### 3.9 Execution Layer
- **Human Approval** — approval UI + API; approvals are recorded in the audit log.
- **Safe Autonomous Actions** — scoped executors (e.g., restart workload, rollback
  deployment) using least-privilege credentials. Reversible actions only.
- **Recovery Verifier** — after execution, re-checks health/error/latency/SLOs and decides
  `incident.closed` or `incident.escalated`.

### 3.10 Chaos Lab (chaoslab/)
A controlled failure-injection environment (CPU saturation, memory exhaustion, container
crashes, DB unavailability, network latency, 5xx errors, dependency failures, config
errors, faulty deployments, traffic spikes) used to generate the SRE telemetry/incident
dataset and to evaluate the platform objectively.

## 4. Data Flows

### 4.1 Runtime telemetry (steady state)

```text
Monitored app ──OTLP──▶ otel-collector ──▶ Prometheus / Loki / Tempo
       │                                        │
       └──▶ Event Layer ◀───────────────────────┘
                  │
                  ▼
         ML Anomaly Detection ──anomaly.score──▶ Event Layer
                  │
                  ▼
            Incident Manager (if score ≥ threshold)
```

### 4.2 Incident lifecycle

```text
anomaly.score event
        │
        ▼
Incident created (open)
        │
        ▼
AI Reasoning: collect evidence (tools) + RAG context
        │
        ▼
Root-cause analysis (hypothesis + evidence citations)
        │
        ▼
Remediation planner → remediation.recommended
        │
        ▼
Policy engine → risk class
        ├── low risk + reversible → auto-execute (Level 5)
        └── high risk → approval required (Level 4)
        │
        ▼
Executor runs action (audit logged)
        │
        ▼
Recovery verifier: health/error/latency/SLO checks
        ├── recovered → incident.closed + postmortem
        └── not recovered → incident.escalated (human on-call)
```

## 5. Cross-Cutting Concerns

- **Correlation** — every event carries `trace_id`/`correlation_id`; incidents reference
  the evidence set.
- **Auditability** — AI recommendations, approvals, executions, and verifications are all
  audit-logged; the dashboard renders the full timeline.
- **Failure isolation** — the control plane must remain available when the monitored app
  fails; control-plane components get independent health checks and restart policies.
- **Security** — least privilege everywhere; AI tool layer is read-only; executors use
  scoped credentials; secrets never reach the LLM context.

## 6. Repository Mapping

| Architecture area | Repository path |
|---|---|
| Web Dashboard | `frontend/` |
| API Gateway, Platform & Incident Services | `backend/` |
| Event Layer | `backend/` (initial: Redis Streams) |
| Observability configs | `infra/` (prometheus/, grafana/, loki/, tempo/, otel/) |
| ML Anomaly Detection | `ml/` |
| AI Reasoning / RAG / Tools | `ai/` |
| Remediation planner & policy | `backend/` + `ai/` (policy data under `infra/policies/` eventually) |
| Chaos Lab | `chaoslab/` |
| K8s deployment | `infra/k8s/` |
| IaC (cloud) | `iac/terraform/` |
