# Roadmap

Phase-based roadmap for AegisSRE. **Scope locked 2026-08-31** — see
[../planning/features.md](../planning/features.md) for the full feature specification,
[../planning/phases.md](../planning/phases.md) for gates & integration checkpoints,
[../planning/product-vision.md](../planning/product-vision.md) for the product target, and
[../planning/timeline.md](../planning/timeline.md) for the calendar.
Every phase ends with a **ready-and-working increment** + integration checkpoint.

## P1 — Foundation ✅ (2026-08-31)
- Repo layout, docs hub, ADRs 0001–0005, team + planning docs
- Docker Compose observability stack (Postgres, Redis, Prometheus, Grafana, Loki, Tempo, OTel)
- CI (YAML/compose validation, k8s lint, docs checks), Makefile

## P2 — Observability & Demo App v1 (Sep–Oct)
- A1 observability pipeline; AegisShop v1 (5 services, OTel-instrumented)
- A2 service registry & live health; telemetry envelope v0.1 (Pydantic)
- Console scaffold + design system (mock data)
- **Gate:** AegisShop telemetry in Grafana; registry + console live

## P3 — Detection & Incidents (Oct–Nov)
- A3 anomaly detection (statistical baselines + Isolation Forest)
- A4 incident manager (state machine, severity, timeline); evidence store
- **Gate:** injected fault → anomaly → incident on screen

## P4 — RCA & AI (Nov–Dec)
- A5 evidence collection + root-cause analysis with citations
- B1 RAG knowledge base (pgvector); B2 "Ask Aegis" assistant (read-only tools)
- **Gate:** AI explains a fault with cited evidence; chat works

## P5 — Remediation & Autonomy (Dec–Jan)
- A6 remediation planner + policy engine; A7 human approval workflow
- A8 safe autonomous execution (low-risk, reversible); A9 recovery verification
- **Gate:** full approve → execute → verify → close cycle

## P6 — Console Complete (Nov–Jan, parallel)
- C1 full console (7 pages), C3 runbooks UI, C4 postmortem viewer, C5 audit viewer
- D5 CI/CD full pipeline; D6 SLO dashboards + burn-rate alerts
- **Gate:** every page live from real APIs; CI/CD green

## P7 — K8s & Chaos Lab (Jan–Feb)
- D1 Kubernetes deployment (kind, Kustomize bases per ADR-0005)
- A11 chaoslab: 10 fault types, experiment manifests, ground truth
- **Gate:** platform + AegisShop on cluster; faults injectable

## P8 — Evaluation (Feb–Mar)
- A12 evaluation framework (baseline vs platform, N ≥ 10 per fault); E2 comparison study
- **Gate:** evaluation report with MTTD/MTTR statistics committed

## Report & Demo (Mar–Apr)
- Thesis report, demo video, console polish, E4 documentation final pass

## Buffer / Stretch (Apr–Jun)
- B3 LoRA fine-tune experiment (gated), viva preparation, optional E1 dataset release
