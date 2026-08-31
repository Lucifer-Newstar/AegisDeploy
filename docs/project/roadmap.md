# Roadmap

Milestone plan for AegisSRE. **Scope locked 2026-08-31** — see
[../planning/features.md](../planning/features.md) for the full feature specification,
[../planning/product-vision.md](../planning/product-vision.md) for the product target, and
[../planning/timeline.md](../planning/timeline.md) for the member-level calendar.
Each phase ends with a ready-and-working increment and an integration checkpoint
([../planning/phases.md](../planning/phases.md)).

## M1 — Foundation ✅ (2026-08-31)
- Repository layout, project docs, ADRs 0001–0005
- Docker Compose observability stack (Postgres, Redis, Prometheus, Grafana, Loki, Tempo, OTel)
- CI (YAML/compose validation, k8s lint, docs checks), Makefile
- Team docs (structure, working rules), planning docs (features, product vision, timeline)

## M2 — Observability & Backend (Sep–Oct)
- A1 observability pipeline (OTel → Prometheus/Loki/Tempo + event layer)
- A2 service registry & live health
- Demo application scaffold (own microservices app)
- Telemetry envelope v0.1 (Pydantic) shared across services
- Checkpoint: demo-app metrics/logs/traces flow into Grafana/Loki/Tempo

## M3 — Detection & Incidents (Oct–Nov)
- A3 anomaly detection (statistical baselines + Isolation Forest)
- A4 incident manager (state machine, severity, timeline)
- Demo app fully instrumented; faults → anomalies → incidents
- Checkpoint: injected fault appears as an incident on screen

## M4 — RCA & AI (Nov–Dec)
- A5 evidence collection + root-cause analysis with citations
- B1 RAG knowledge base (pgvector: runbooks, past incidents)
- B2 "Ask Aegis" assistant (read-only tools, cited answers)
- Checkpoint: AI explains a fault with cited evidence; chat works

## M5 — Remediation & Policy (Dec–Jan)
- A6 remediation planner + policy engine (risk classes, declarative policies)
- A7 human approval workflow (Level 4)
- A8 safe autonomous execution (Level 5, low-risk reversible)
- A9 recovery verification
- Checkpoint: full approve → execute → verify cycle

## M6 — Console Complete (Nov–Jan, parallel)
- C1 full console (7 pages), C3 runbooks UI, C4 postmortem viewer, C5 audit viewer
- Checkpoint: every page live from real APIs

## M7 — K8s & Chaos Lab (Jan–Feb)
- D1 Kubernetes deployment (Kustomize bases, ADR-0005)
- D5 CI/CD (test, lint, build, images), D6 SLO dashboards + burn-rate alerts
- A11 chaoslab: 10 fault types, experiment manifests, ground truth
- Checkpoint: platform + demo app on cluster; faults injectable

## M8 — Evaluation (Feb–Mar)
- A12 evaluation framework (baseline vs platform, N ≥ 10 per fault)
- E2 comparison study writeup
- Checkpoint: evaluation report with MTTD/MTTR statistics

## Report & Demo (Mar–Apr)
- Thesis report, demo video, console polish, E4 documentation final pass

## Buffer / Stretch (Apr–Jun)
- B3 LoRA fine-tune experiment (if approved), viva preparation, optional E1 dataset release
