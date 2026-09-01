# Navin Jairam M — Team Lead / SRE / DevOps Architecture

> **Member 4** — Team Lead. SRE · DevOps · Cloud architecture · Observability ·
> AI-SRE integration · MLOps · Autonomous remediation · Chaos engineering ·
> System integration.

## Role

Own the technical architecture and the AI-SRE track; coordinate the integration of all
four members' work; drive the research question to an evidence-backed answer.

## Primary responsibilities

- System / infrastructure architecture + Architecture Decision Records
- Telemetry envelope & event layer design (the shared contracts)
- ML anomaly detection pipeline (A3), RCA engine (A5), RAG (B1), Ask Aegis engine (B2)
- Remediation policy engine design (A6/A8/A9), autonomy model & safety boundaries
- **Deployment Intelligence design (DI-1…DI-7):** risk scoring (DI-2), change correlation (DI-3), bad-rollout detection (DI-4), rollback policy (DI-5), CFR evaluation (DI-7)
- Chaos/failure engineering specs (A11), evaluation protocol + comparison study (A12/E2)
- Integration coordination: contracts-first, phase gates, weekly syncs
- Thesis-ready documentation (E4)

## Repo areas owned

- `docs/architecture/`, `docs/planning/`, `docs/team/`, `docs/members/navin-lead/`
- `ml/`, `ai/` (+ design of `chaoslab/`); integration across `backend/`, `frontend/`, `infra/`

## Team-facing guides

- **[kickoff-guide.md](kickoff-guide.md)** — run the P2 kickoff sync: agenda, live demo script, D1–D9 decisions + decision-log rows, weekly sync rhythm, demo-of-week format, gate checklist.

## Personal learning goal

Build strong practical knowledge in **SRE + DevOps + Cloud + Architecture** while
working deeply with the **AI/ML side** of the platform — this project is the vehicle.

## Contracts I provide

| Contract | Consumers | Available |
|---|---|---|
| Telemetry envelope v0.1 (Pydantic) | everyone | P2 start |
| Event layer semantics (Redis Streams) | backend/ml | P2 |
| Anomaly events | incident manager (Jega) | P3 |
| RCA/evidence APIs + Ask Aegis engine | frontend (Dhanush) | P4 |
| **DI design: risk scoring (DI-2), correlation (DI-3), rollout window (DI-4), rollback policy (DI-5)** | backend + executors (Jega, Gokul) | P4–P5 |
| Action catalog, policies, risk matrix | backend + executors (Jega, Gokul) | P5 |
| Fault specs + evaluation protocol | chaoslab (Gokul), all | P7–P8 |
