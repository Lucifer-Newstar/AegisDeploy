# Planning

> Home of the **development-phase planning** documents for AegisDeploy.
> Everything here is the *decision record* of the project: what we build, how the
> final product should look, and when we build it.
>
> These documents are living files — updated whenever a decision changes, with the
> change logged in §2 below.

---

## 1. Index

| Document | Purpose |
|---|---|
| [features.md](features.md) | The locked feature scope — what is in, what is out, who owns what, acceptance criteria. |
| [product-vision.md](product-vision.md) | How the final product should look and behave — console concept, pages, design language, demo story. |
| [phases.md](phases.md) | The phase plan — gates ("ready & working" per phase), non-disruption design, integration checkpoints. |
| [timeline.md](timeline.md) | The 8–10 month development calendar, member assignments per phase, milestones, risks. |

Related: [docs/project/roadmap.md](../project/roadmap.md) is the milestone-level roadmap
(kept in sync with these documents); [docs/team/](../team/) defines who is on the team.

---

## 2. Decision Log

| Date | Decision | Decider | Recorded in |
|---|---|---|---|
| 2026-08-31 | Project objective confirmed (research question): AI-assisted SRE platform reducing MTTD/MTTR, accurate RCA, safe autonomous remediation. | Navin Jairam (Team Lead) | [proposal.md](../project/proposal.md) |
| 2026-08-31 | Runway: **8–10 months** (started Aug 2026 → delivery window Apr–Jun 2027). | Navin Jairam | [timeline.md](timeline.md) |
| 2026-08-31 | **Scope locked:** All Tier A (core loop) + B1 RAG + B2 Ask Aegis + C1/C3/C4/C5 + D1/D5/D6 + E2/E4. Explicit cuts: B3, B4, B6, C2, C6, D2, D3, D4, E3, E5 (B3 = optional buffer stretch). | Navin Jairam (on recommendation) | [features.md](features.md) |
| 2026-08-31 | **Demo subject:** build our **own demo microservices application** (fully controlled faults) rather than adapting an existing one. | Navin Jairam (on recommendation) | [features.md](features.md) §5 |
| 2026-08-31 | **Micro-decisions locked:** demo app named **AegisShop**; demo stack = Python/FastAPI + OTel + Postgres/Redis; B3 fine-tuning kept as gated buffer stretch; D1 cluster = **kind** (fallback k3s). | Navin Jairam (on agent recommendation) | [features.md](features.md) §4 |
| 2026-08-31 | **Phase-gated development:** project split into phases P1–P8; each phase ends with a **ready-and-working increment** (gate) + integration checkpoint; tracks designed to be **non-blocking** (contracts-first, mocks); moving on requires a Team Lead gate review. | Navin Jairam (Team Lead) | [phases.md](phases.md) |
| 2026-08-31 | **Per-member planning folders:** each member gets a designated folder under `docs/members/<member>/` containing their role and their own view of phases + deliverables. | Navin Jairam (Team Lead) | [docs/members/](../members/) |
| 2026-08-31 | **UML documentation set:** all 14 UML 2.5 diagram types, authored in **Mermaid** under `docs/architecture/uml/` (GitHub-rendered), one diagram per reviewed exchange; Use Case split into platform + AegisShop files. | Navin Jairam (on agent recommendation) | [docs/architecture/uml/](../architecture/uml/) |
| 2026-09-01 | **Project upgrade — Deployment Intelligence:** project renamed **AegisSRE → AegisDeploy**; added a first-class **Deployment Intelligence tier** (DI-1…DI-7: deployment tracking, risk scoring, change-incident correlation, bad-rollout detection, rollback intelligence, canary analysis, change-failure analytics) integrated into existing phases P2–P8 (no timeline change). Full capability set chosen. | Navin Jairam (on agent recommendation) | [features.md](features.md) · [deployment-intelligence.md](../architecture/deployment-intelligence.md) |
| 2026-09-01 | **Walking-skeleton base layer (before P2 ramp):** Navin + Gokul build a lean shared foundation first — root tooling config; `backend/libs/telemetry` (envelope v0.2); `backend/libs/eventbus` (Redis Streams); `backend/services/_template` (FastAPI service template); one vertical slice `demoapp/aegisshop/catalog-service` (in-memory, OTLP → Grafana via compose); compose + CI wiring. A3–A9 explicitly deferred to parallel P3–P5. Decisions: AegisShop lives in `demoapp/aegisshop/`; template is a copy-paste pattern (not the real gateway); slice = catalog-service. | Navin Jairam (on agent recommendation) | [phases.md](phases.md) · [demoapp/](../../demoapp/) |
| 2026-09-01 | **Contracts-first executed (P2):** P2 OpenAPI contract set drafted in `docs/contracts/` (registry :8101, deployments/DI-1 :8701, AegisShop v1); event catalogue v1 added to telemetry-model.md §3.5 (incl. deployment state machine for DI-4); CORS dev policy (allow `localhost:3000` in dev only); PR template with Definition-of-Done checklist; cross-member **integration edge-case register** opened; contract-drift CI check proposed (owner: Navin). Freeze 2026-09-08. | Navin Jairam (Team Lead) | [contracts/](../contracts/) · [integration-edge-cases.md](integration-edge-cases.md) · [../../.github/pull_request_template.md](../../.github/pull_request_template.md) |

*New decisions are appended; nothing is silently edited.*
