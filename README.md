# AegisDeploy

**AI-Powered Autonomous Site Reliability & Software Deployment Incident Intelligence Platform**

*Intelligent monitoring · Deployment risk intelligence · Incident detection · Root-cause analysis · Controlled autonomous remediation*

> ⚠️ **Renamed:** formerly **AegisSRE** (decision 2026-09-01 — the project was upgraded
> with a first-class **Deployment Intelligence** tier; see
> [docs/architecture/deployment-intelligence.md](docs/architecture/deployment-intelligence.md)).
> The GitHub repository may keep its old name until renamed in repository settings.

![Status](https://img.shields.io/badge/status-foundation--phase-0f766e) ![CI](https://img.shields.io/badge/CI-github--actions-blue)

AegisDeploy is a full-stack platform that continuously observes a deployed cloud-native
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
| **Deployment Intelligence** | Tracks every deployment; ML risk scoring, bad-rollout detection, change-incident correlation ("caused by deploy `abc1234`"), policy-gated safe rollback, canary analysis, and change-failure analytics (DI-1…DI-7). |
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
AegisDeploy/
├── .github/workflows/    CI/CD pipelines (GitHub Actions)
├── ai/                   AI reasoning layer (LLM, RAG, tool-calling, runbooks)
├── backend/              Platform & incident services (Python / FastAPI)
├── chaoslab/             Controlled failure laboratory (chaos experiments)
├── docs/                 Documentation hub (index: docs/README.md)
│   ├── project/          Proposal & roadmap
│   ├── planning/         Features, product vision, phases, timeline
│   ├── team/             Team structure & working rules
│   ├── members/          Per-member role & phase plans
│   ├── architecture/     System design + ADRs
│   ├── development/      Contributing & tech stack
│   └── operations/       Evaluation methodology
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
| [docs/README.md](docs/README.md) | **Documentation index** — navigation hub & reading order. |
| [docs/project/](docs/project/) | **Project** — proposal & roadmap. |
| [docs/planning/](docs/planning/) | **Planning** — locked feature scope, product vision, phases & gates, timeline, decision log. |
| [docs/team/](docs/team/) | **Team** — structure, ownership, working rules. |
| [docs/members/](docs/members/) | **Member folders** — each member's role & phase plan. |
| [docs/architecture/](docs/architecture/) | **Architecture** — system architecture, autonomy model, telemetry model, ADRs. |
| [docs/development/](docs/development/) | **Development** — contributing guide & tech stack. |
| [docs/operations/](docs/operations/) | **Operations** — evaluation metrics & protocol. |

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

AegisDeploy is **not** a general-purpose autonomous agent administering arbitrary production
infrastructure. Autonomy is constrained by:

- predefined tools (read-only telemetry access; scoped execution actions);
- least-privilege permissions;
- remediation policies (risk-classified, reversible actions only);
- human approval for high-risk operations;
- complete audit logging;
- post-remediation verification.

## 9. Contributing & License

See [CONTRIBUTING](docs/development/contributing.md) for development conventions.
Licensed under the [MIT License](LICENSE). Copyright © 2026 Navin Jairam (Lucifer-Newstar).
