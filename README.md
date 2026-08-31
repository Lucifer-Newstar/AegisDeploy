# AegisSRE

**AI-Powered Autonomous Site Reliability Engineering Platform**

*Intelligent monitoring · Incident detection · Root-cause analysis · Controlled autonomous remediation*

![Status](https://img.shields.io/badge/status-foundation--phase-0f766e) ![CI](https://img.shields.io/badge/CI-github--actions-blue)

AegisSRE is a full-stack platform that continuously observes a deployed cloud-native
application, analyzes its telemetry, detects abnormal behavior, identifies and correlates
incidents, determines probable root causes, recommends evidence-backed remediation actions,
and verifies system recovery — while keeping **humans in control** of higher-risk operations.

> **Observe everything. Trust evidence. Reason over context. Act within boundaries. Verify the result.**
>
> The objective is not to replace the SRE. It is to allow the SRE to move from reactive
> firefighting toward intelligent, evidence-driven, and increasingly autonomous reliability
> engineering.

---

## 1. What the Platform Does

| Capability | Description |
|---|---|
| **Continuous Observability** | Collects metrics, logs, distributed traces, Kubernetes events, deployment history, and service health via OpenTelemetry, Prometheus, Loki, and Tempo. |
| **Anomaly Detection** | ML/statistical models (Isolation Forest + statistical baselines) detect latency spikes, error-rate increases, resource anomalies, and traffic shifts. |
| **Incident Management** | Correlates anomalies into incidents with severity, affected services, timestamps, telemetry evidence, deployment context, and status. |
| **Root-Cause Analysis** | An AI reasoning layer combines logs, metrics, traces, deployments, and runbooks to produce evidence-backed root-cause explanations — not just "latency is high." |
| **AI-Assisted Remediation** | Recommends actions: restart unhealthy workload, rollback deployment, scale service, replace instance, adjust configuration, or escalate. |
| **Controlled Autonomy** | Low-risk, predefined, reversible actions execute automatically; high-risk operations require human approval. |
| **Recovery Verification** | Confirms health, error rates, latency, and SLOs recovered before closing the incident. |
| **Postmortems** | AI-generated incident postmortems with timeline, evidence, and measured MTTD/MTTR. |

Autonomy pipeline: **Detect → Investigate → Explain → Recommend → Approve/Execute → Verify**

## 2. High-Level Architecture

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

## 3. Repository Layout

```
AegisSRE/
├── .github/workflows/    CI/CD pipelines (GitHub Actions)
├── ai/                   AI reasoning layer (LLM, RAG, tool-calling, runbooks)
├── backend/              Platform & incident services (Python / FastAPI)
├── chaoslab/             Controlled failure laboratory (chaos experiments)
├── docs/                 Architecture, ADRs, telemetry model, evaluation
│   ├── adr/              Architecture Decision Records
├── frontend/             SRE console / web dashboard (Next.js / TypeScript)
├── iac/                  Infrastructure as Code (Terraform, future)
├── infra/                Docker, Compose, Kubernetes, Prometheus/Grafana/Loki/Tempo configs
│   ├── docker/           Dockerfiles (per service)
│   ├── k8s/              Kubernetes manifests (Kustomize base)
│   └── ...
├── ml/                   Anomaly detection pipeline & models
├── scripts/              Dev/test utility scripts
├── docker-compose.yml    Local development stack (Compose now, K8s-ready)
└── Makefile              Common developer tasks
```

## 4. Quickstart (Local Development)

Prerequisites: Docker + Docker Compose v2.

```bash
# 1. Bring up the platform dependencies (Postgres, Redis, Prometheus, Grafana, Loki, Tempo, OTel Collector)
make infra-up

# 2. Verify the stack
docker compose ps

# 3. Open the dashboards
#    Grafana       → http://localhost:3000   (admin / aegis)
#    Prometheus    → http://localhost:9090
#    Loki          → http://localhost:3100
#    Tempo         → http://localhost:3200
#    OTLP endpoint → localhost:4317 (gRPC) / 4318 (HTTP)

# 4. Tear down
make infra-down
```

Application services (backend, frontend, ml, ai) are added incrementally as they are
implemented; the observability foundation above is version-pinned and fully functional now.

## 5. Documentation

| Document | Purpose |
|---|---|
| [docs/proposal.md](docs/proposal.md) | The original project proposal (full text). |
| [docs/architecture.md](docs/architecture.md) | Component architecture, responsibilities, data flows. |
| [docs/tech-stack.md](docs/tech-stack.md) | Selected technology stack and rationale. |
| [docs/autonomy-model.md](docs/autonomy-model.md) | Levels 1–5 autonomy, policy engine, approval matrix. |
| [docs/telemetry-model.md](docs/telemetry-model.md) | Unified telemetry/event envelope contract. |
| [docs/evaluation.md](docs/evaluation.md) | SRE, ML, and automation evaluation metrics. |
| [docs/adr/](docs/adr/) | Architecture Decision Records. |

## 6. Roadmap

| Milestone | Scope |
|---|---|
| **M1 — Foundation** *(current)* | Repo layout, architecture docs, ADRs, CI, Docker Compose observability stack, K8s-ready structure. |
| **M2 — Observability & Backend** | FastAPI services, telemetry ingestion, event layer, service registry. |
| **M3 — Anomaly Detection** | ML pipeline: feature engineering, Isolation Forest baselines, anomaly scores. |
| **M4 — Incidents & RCA** | Incident correlation, evidence collection, root-cause analysis framework. |
| **M5 — Remediation & Policy** | Remediation planner, policy engine, approval workflow, recovery verification. |
| **M6 — Dashboard** | Next.js SRE console: timelines, telemetry, AI reasoning, approvals, MTTD/MTTR. |
| **M7 — Chaos Lab** | Controlled failure injection and objective evaluation. |
| **M8 — Evaluation & Demo** | End-to-end failure demonstration, metrics report, postmortem generation. |

## 7. Core Research Question

> **Can an AI-assisted SRE platform reduce incident detection and recovery time while
> accurately identifying root causes and safely automating predefined remediation actions
> in cloud-native applications?**

## 8. Scope Boundary

AegisSRE is **not** a general-purpose autonomous agent administering arbitrary production
infrastructure. Autonomy is constrained by:

- predefined tools (read-only telemetry access; scoped execution actions);
- least-privilege permissions;
- remediation policies (risk-classified, reversible actions only);
- human approval for high-risk operations;
- complete audit logging;
- post-remediation verification.

## 9. Contributing & License

See [CONTRIBUTING](docs/contributing.md) for development conventions. Licensed under the
[MIT License](LICENSE). Copyright © 2026 Navin Jairam (Lucifer-Newstar).
