# Phase Plan — Gates, Non-Disruption & Integration

> Development is split into **phases**. Every phase ends with a **ready-and-working
> increment** (the phase gate) — the project only moves to the next phase when the gate
> passes. Phases are designed so the four members' tracks **never block each other**,
> and every phase ends with an **integration checkpoint** where all tracks merge into a
> fully functioning project.
>
> Decided by Team Lead (2026-08-31). Schedule & member calendar: [timeline.md](timeline.md).
> Feature details: [features.md](features.md). Per-member detail: [docs/members/](../members/).

---

## 1. Phase Principles

| # | Principle | Meaning |
|---|---|---|
| 1 | **Working increment per phase** | No phase ends with half-built work — the gate proves the increment works. |
| 2 | **Contracts first** | Shared contracts (telemetry envelope, API schemas, event types, tool interfaces) are defined and committed *before* dependent tracks start, so members build in parallel. |
| 3 | **Non-blocking tracks** | Mock servers, seeded data, and interface stubs absorb dependencies — nobody waits on anybody. |
| 4 | **Integration at phase end** | The last 2–3 days of each phase are an integration window: all tracks merge, the integration demo runs, blockers get fixed. |
| 5 | **Gate review** | The Team Lead reviews the gate. A phase is **done** only when its gate criteria pass and docs are updated (E4). |

## 2. Phase Overview

| Phase | Focus | Ready & working at phase end (gate) | Integration checkpoint |
|---|---|---|---|
| **P1 Foundation** ✅ | Repo, docs, stack, CI | `docker compose up --wait` → healthy stack; CI green; docs indexed | — (solo) |
| **P2 Observability + Demo App v1** | A1 pipeline, AegisShop v1, A2 registry, **DI-1 deployment tracking**, console scaffold | AegisShop runs with metrics/logs/traces in Grafana; registry API works; **deploy events recorded**; console scaffold renders | **"One command shows every AegisShop service in Grafana AND the console"** |
| **P3 Detection + Incidents** | A3 anomaly detection, A4 incident manager, **DI-4 deploy-window evaluation (base)** | Injected fault → anomaly → incident with timeline | Live **fault-to-incident** demo |
| **P4 AI Reasoning** | A5 RCA, B1 RAG, B2 Ask Aegis, **DI-2 risk scoring, DI-3 change-incident correlation** | AI explains a fault with cited evidence; chat answers; **incidents attributed to deployments** | Incident detail shows AI reasoning live |
| **P5 Remediation + Autonomy** | A6 planner/policy, A7 approvals, A8 safe-auto, A9 verification, **DI-5 rollback intelligence** | Full approve → execute → verify → close cycle; safe-auto for low-risk; **safe auto-rollback**; kill switch | Complete **autonomous loop** demo |
| **P6 Product Complete** | C1 8 pages, C3/C4/C5, D5 CI/CD, D6 SLO dashboards, **DI-7 CFR dashboards** | Console complete on live data; CI/CD green; SLO panels live; **CFR panel live** | Full **product walkthrough** |
| **P7 Kubernetes + Chaos Lab** | D1 K8s (kind), A11 chaoslab (10 faults), **DI-6 canary analysis** | Whole platform + AegisShop on kind; all faults injectable with ground truth; **canary deployment analyzed** | **Cluster-wide** demo + fault injection show |
| **P8 Evaluation + Report** | A12 runs (N≥10/fault), E2 study, demo video | Evaluation report with statistics; submission-ready demo | Final **thesis demo** |

## 3. Phase Details

### P1 — Foundation ✅ (Aug–Sep 2026)
- **Deliverables:** repo layout, docs hub, ADR-0001..0005, compose observability stack, CI, team + planning docs.
- **Gate:** stack healthy, CI green, docs indexed. — *Passed 2026-08-31.*

### P2 — Observability + Demo App v1 (Sep–Oct)
- **Objective:** the platform can see the demo app, and every member has a running scaffold.
- **Tracks:** Gokul (A1 pipeline: OTel configs, dashboards, compose additions), Jega (AegisShop backend services + A2 registry/health + **DI-1 deployment tracker API**), Navin (telemetry envelope v0.1 + event layer design + **API contracts**), Dhanush (console scaffold + design system on mock data).
- **Gate criteria:**
  - AegisShop services visible in Grafana (metrics), Loki (logs), Tempo (traces) within 60 s of start.
  - Registry + health API returns service list; envelope schema enforced at ingestion.
  - Console scaffold renders Command Center from the mock server.
- **Integration checkpoint:** one command runs AegisShop + platform; Grafana and console both show all services.

### P3 — Detection + Incidents (Oct–Nov)
- **Objective:** the platform notices when something breaks.
- **Tracks:** Navin (A3 detectors + feature pipeline + threshold tuning), Jega (A4 incident manager + timeline API + evidence store), Gokul (metric plumbing, mini-fault validation), Dhanush (service detail page w/ anomaly bands).
- **DI hook:** deploy-window evaluation seeded in P3 (DI-4 base) — post-deploy metrics evaluated as a first-class window.
- **Gate criteria:** injected CPU/latency spike → `anomaly.score` event → incident created in < 30 s; detection precision/recall ≥ 0.85 on validation set.
- **Integration checkpoint:** fault-to-incident demo run from the chaos hooks.

### P4 — AI Reasoning (Nov–Dec)
- **Objective:** the platform explains *why*.
- **Tracks:** Navin (A5 evidence collection + RCA engine, B1 RAG on pgvector, B2 Ask Aegis engine, **DI-2 risk scoring + DI-3 change-incident correlation**), Jega (evidence APIs, incident APIs for reasoning, **deploy history API**), Dhanush (incident detail w/ AI reasoning panel + Ask Aegis UI), Gokul (read-only query proxies for AI tools).
- **Gate criteria:** top-1 RCA accuracy ≥ 70% on seeded evaluation faults; every hypothesis cites evidence; Ask Aegis answers a health question with citations; **DI-3 attributes faulty-deploy faults to the correct revision (≥ 0.8)**.
- **Integration checkpoint:** live incident shows AI reasoning; chat answers from live data.

### P5 — Remediation + Autonomy (Dec–Jan)
- **Objective:** the platform acts — within boundaries.
- **Tracks:** Jega (A6 planner impl, A7 approval workflow API, A9 verification API), Navin (policy engine design, risk matrix, A8 kill switch, A9 logic, **DI-5 rollback policy**), Gokul (executors: restart/**rollback**/scale with least-privilege creds), Dhanush (approvals UI, autonomy mode indicator).
- **Gate criteria:** approve → execute → verify → close works end-to-end; safe-auto fires only for policy-approved low-risk actions; **safe auto-rollback works for low-risk rollbacks**; kill switch immediate; safety violations = 0.
- **Integration checkpoint:** full-loop demo with both a Level 4 (approval) and a Level 5 (auto) action.

### P6 — Product Complete (Nov–Jan, parallel)
- **Objective:** the console is a complete product on live data.
- **Tracks:** Dhanush (C1 pages 4–8, C3 runbooks, C4 postmortems, C5 audit), Gokul (D5 CI/CD full: tests/build/images; D6 SLO dashboards + burn-rate alerts; **DI-7 CFR dashboards**), Jega (API polish, OpenAPI client regen), Navin (integration lead, SLO definitions).
- **Gate criteria:** all 8 pages live from real APIs; CI/CD green on every PR; SLO panels + burn-rate alerts working; **change-failure-rate panel live**.
- **Integration checkpoint:** full product walkthrough (page-by-page from live data).

### P7 — Kubernetes + Chaos Lab (Jan–Feb)
- **Objective:** production-shaped deployment + objective failure injection.
- **Tracks:** Gokul (D1 kind cluster + Kustomize bases for every service, A11 chaoslab implementation, **DI-6 canary analysis**), Navin (fault specs, experiment manifests, ground-truth schema), Jega (fault hooks in AegisShop), Dhanush (final UX pass on cluster).
- **Gate criteria:** entire platform + AegisShop runs on kind via `kubectl apply`; all 10 fault types injectable with labeled ground truth; **canary deployment runs and its analysis is visible in the console**.
- **Integration checkpoint:** cluster-wide run + live fault injection.

### P8 — Evaluation + Report (Feb–Mar)
- **Objective:** answer the research question with data.
- **Tracks:** Navin (A12 evaluation lead, E2 comparison study, **DI-7 CFR metric in the report**), all members (experiment runs, N ≥ 10 per fault), Dhanush (demo video, screenshots), Jega (API docs finalization), Gokul (cluster stability).
- **Gate criteria:** evaluation report committed (MTTD/MTTR, RCA accuracy, autonomy success rates, **change failure rate**, mean ± std); demo video ready; docs final pass (E4).
- **Integration checkpoint:** final thesis demo.

## 4. Non-Disruption Design

The phase split is built so no member's track blocks another's:

| Track | Never blocks on | Because |
|---|---|---|
| Frontend (Dhanush) | Backend/AI APIs | OpenAPI contract → generated client + **mock server**; each page works on mocks until its API lands |
| Backend (Jega) | AI features | Incident manager accepts events from a **test producer** until A3 detectors ship; AI consumes APIs, not the reverse |
| DevOps (Gokul) | Application code | Observability stack + compose/K8s configs are code-independent; Dockerfiles land with each service PR |
| Lead/AI (Navin) | Frontend | AI outputs are APIs + events; UI is Dhanush's consumption point, designed against the same contracts |

**Cross-track dependency table:**

| Consumer | Needs from | Available by | Late-mitigation |
|---|---|---|---|
| Jega (registry/health) | envelope + event lib (Navin) | P2 start | contract stub package |
| Jega (incident manager) | anomaly events (Navin) | P3 | test event producer |
| Navin (RCA tools) | query APIs (Gokul/Jega) | P4 | seeded evidence fixtures |
| Dhanush (incident UI) | incident APIs (Jega) | P3 end | mock server keeps UI moving |
| Dhanush (Ask Aegis UI) | B2 engine API (Navin) | P4 end | mock responses |
| Gokul (executors) | action catalog + policies (Navin) | P5 | dry-run mode |
| All | shared stack (Gokul) | P1 ✅ | compose configs versioned via PRs |

**Shared-stack rule:** changes to `docker-compose.yml` / `infra/` configs land via PRs
(never direct-to-main pushes), so nobody's local stack breaks mid-phase (ADR-0005).

## 5. Integration Protocol (end of every phase)

1. **Feature freeze** — last 2–3 days of the phase: no new features, fixes only.
2. **Merge tracks** — all member branches merged to `main` via PRs; CI must pass.
3. **Integration demo** — the checkpoint script for the phase runs end-to-end
   (checkpoint criteria in §3); Team Lead runs it, members fix their own failures.
4. **Gate review** — checklist (§6) reviewed by the Team Lead; result recorded in the
   planning decision log.
5. **Move on** — only a passed gate opens the next phase.

## 6. Phase Gate Checklist (used by the Team Lead)

```text
[ ] Working increment demonstrated (gate criteria in §3)
[ ] Integration checkpoint passed
[ ] CI green (where applicable)
[ ] Tests pass (where applicable)
[ ] Docs updated for this phase (E4) — no documentation debt
[ ] ADRs / decision log current
[ ] Phase artifacts committed with conventional messages
[ ] Team Lead sign-off
```

## 7. Demo Application (AegisShop) — v1 Service Map

AegisShop is our own microservices demo app (decision 2026-08-31). v1 services:

| Service | Role | Stack | Fault hooks (chaos targets) |
|---|---|---|---|
| `shop-gateway` | public API entry | FastAPI | HTTP 5xx injection, traffic spike, latency |
| `catalog-service` | product catalog | FastAPI | CPU saturation |
| `cart-service` | shopping cart | FastAPI + Redis | Redis unavailable |
| `order-service` | order processing | FastAPI + Postgres | DB unavailable, faulty deployment |
| `payment-service` | simulated payments | FastAPI | container crash, latency |

Shared infra: Postgres (orders), Redis (cart). All services OTel-instrumented
(metrics + logs + traces). Final naming/tech confirmed by Jegatheesan at P2 kickoff.
