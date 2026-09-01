# Feature Specification

> The **locked scope** of AegisDeploy, decided 2026-08-31 (see [README.md](README.md) §2).
> This is the contract between the four members: what gets built, who owns it, and
> what "done" means for each feature.
>
> Status legend: ✅ locked · 🧪 stretch (buffer only) · ❌ out of scope

---

## 1. Scope Statement

**In scope (approved combo):**

```
Tier A — Core platform ......... A1–A12 (the complete detect→verify loop)
Tier B — AI depth .............. B1 RAG knowledge base, B2 "Ask Aegis" assistant
Tier C — Product/UX ............ C1 full console, C3 runbooks, C4 postmortems, C5 audit viewer
Tier D — DevOps/Cloud .......... D1 Kubernetes, D5 CI/CD, D6 SLO dashboards & burn-rate alerts
Tier E — Academic .............. E2 comparison study, E4 thesis-ready documentation
Tier DI — Deployment Intelligence DI-1…DI-7 (upgrade 2026-09-01; see
           docs/architecture/deployment-intelligence.md)
Demo subject ................... our own microservices demo application ("AegisShop", name TBC)
```

**Out of scope (explicitly cut at planning):**

| Cut item | Reason |
|---|---|
| B3 LoRA/QLoRA fine-tuning | Risky (GPU/hardware), uncertain payoff — **optional stretch in the final buffer month** if the core is ahead of schedule. |
| B4 Time-series forecasting | Peripheral to the core loop. |
| B6 Incident clustering | Nice-to-have; evaluation already covers false-alarm reduction. |
| C2 Service topology map | Heavy for Member 1; not required to answer the research question. |
| C6 Notifications | Can be added post-demo if time permits. |
| D2 GitOps (ArgoCD/Flux) | Ops credibility, not core. |
| D3 Terraform cloud provisioning | Needs cloud account + cost; local cluster suffices for the demo. |
| D4 Advanced chaos tooling (chaos-mesh) | Our own chaoslab scripts cover the required fault types deterministically. |
| E3 Literature survey | Thesis background can cite existing surveys instead. |
| E5 User study | Optional; evaluation protocol (§A12) already gives objective data. |

> Re-opening any cut item requires a Team Lead decision and a note in the Decision Log.

---

## 2. Feature Catalogue

### Tier A — Core platform (P0)

#### A1 — Observability pipeline
- **What:** OpenTelemetry collector receives OTLP from the demo app; metrics → Prometheus, logs → Loki, traces → Tempo; Kubernetes events and deployment events become first-class signals on the Event Layer. All signals use the telemetry envelope (see `docs/architecture/telemetry-model.md`).
- **Owner:** Gokul J (design: Navin J). **Dependencies:** M1 infra stack (done).
- **Acceptance criteria:** demo-app metrics visible in Grafana within 60 s of startup; logs queryable in Loki; traces joinable via `trace_id`; k8s + deployment events present on the event layer.

#### A2 — Service registry & live health
- **What:** catalog of monitored services (name, owner, SLOs, endpoints) + live health state per service.
- **Owner:** Jegatheesan K. **Dependencies:** A1.
- **Acceptance criteria:** CRUD via API; health polled every 15 s; dashboard reads registry + health.

#### A3 — Anomaly detection
- **What:** statistical baselines (z-score/EWMA) + Isolation Forest over latency p95, error rate, CPU/mem, RPS; emits `anomaly.score` events with score, threshold, model, window, baseline.
- **Owner:** Navin J (ML) — with Gokul on data plumbing. **Dependencies:** A1, A2.
- **Acceptance criteria:** precision/recall/F1 ≥ 0.85 on the chaoslab evaluation set; detection latency < 60 s from fault onset.

#### A4 — Incident manager
- **What:** correlates anomaly events into incidents; severity (sev1–sev4), state machine `open → investigating → remediating → verifying → closed | escalated`, full incident timeline; AI postmortem generation at close (delivered with A5).
- **Owner:** Jegatheesan K (design: Navin J). **Dependencies:** A3.
- **Acceptance criteria:** anomaly → incident created < 30 s; state transitions enforced; timeline API complete.

#### A5 — Evidence collection & root-cause analysis
- **What:** the reasoning layer collects evidence via read-only tools (`get_metrics`, `get_logs`, `get_traces`, `get_service_health`, `get_deployment_history`, `get_kubernetes_events`, `get_runbook`); produces root-cause hypotheses **with cited evidence and confidence scores**; generates postmortems on incident close.
- **Owner:** Navin J. **Dependencies:** A1–A4, B1 (grounding).
- **Acceptance criteria:** top-1 RCA accuracy ≥ 70% on evaluation faults; every hypothesis cites evidence; postmortem rendered after close.

#### A6 — Remediation planner & policy engine
- **What:** action catalog (restart, rollback, scale, replace instance, config update, escalate); risk classes (low/medium/high/forbidden); declarative, versioned policies; the *only* component allowed to decide execution mode (auto vs approval).
- **Owner:** Navin J (design) + Jegatheesan K (implementation). **Dependencies:** A4, A5.
- **Acceptance criteria:** correct risk classification on the evaluation set; safety violations = 0; policies loadable without code changes.

#### A7 — Approval workflow (Level 4)
- **What:** approve / reject / defer actions with impact summary; full audit trail; approval UI in the console.
- **Owner:** Jegatheesan K + Dhanush Kumar S (UI). **Dependencies:** A6.
- **Acceptance criteria:** an approval can be completed in ≤ 3 clicks; every decision audit-logged with actor + reason.

#### A8 — Safe autonomous execution (Level 5)
- **What:** low-risk, reversible actions execute automatically when an approved policy matches; cooldowns, rate limits, global autonomy-mode kill switch (observe / recommend / approval / safe-auto).
- **Owner:** Gokul J + Navin J. **Dependencies:** A6, A7.
- **Acceptance criteria:** auto-execution success rate ≥ 80% on eligible faults; kill switch takes effect immediately; never auto-executes a policy-violating action.

#### A9 — Recovery verification
- **What:** post-remediation checks (health, error rate, latency, SLO budget) → `closed` or `escalated`; incident cannot close without it.
- **Owner:** Navin J. **Dependencies:** A4, A8.
- **Acceptance criteria:** verification verdict accuracy ≥ 90% vs ground truth; zero unrecovered incidents closed.

#### A10 — Dashboard core
- **What:** console pages for overview (command center), service detail, incident detail, approvals queue — live from APIs, MTTD/MTTR panels.
- **Owner:** Dhanush Kumar S. **Dependencies:** A2, A4–A7 APIs.
- **Acceptance criteria:** all core pages render from live API data; incident detail shows timeline + AI reasoning + evidence.

#### A11 — Chaos lab
- **What:** deterministic failure injection for 10 fault types (CPU saturation, memory exhaustion, container crash, DB unavailable, network latency, HTTP 5xx, dependency failure, config error, faulty deployment, traffic spike); experiment manifests; automatic state restoration.
- **Owner:** Gokul J + Navin J. **Dependencies:** demo app.
- **Acceptance criteria:** every fault injectable via CLI (later UI); each experiment produces labeled ground truth (fault, start time, end time) used by A12.

#### A12 — Evaluation framework
- **What:** baseline (conventional monitoring + manual response) vs platform runs on identical faults; N ≥ 10 runs per fault type; automated metrics report (MTTD, MTTR, RCA accuracy, autonomy success rates, mean ± std).
- **Owner:** Navin J (lead; all members support runs). **Dependencies:** A11, E4.
- **Acceptance criteria:** one command generates the full evaluation report; results reproducible.

### Tier B — AI depth (P1)

#### B1 — RAG knowledge base
- **What:** runbooks (markdown), past incidents, service metadata, known failure patterns → embedded into pgvector; retrieval API for the reasoning layer.
- **Owner:** Navin J. **Dependencies:** A4, Postgres pgvector.
- **Acceptance criteria:** retrieval returns the relevant runbook for evaluation faults (recall@5 ≥ 0.8); RCA context includes retrieved knowledge.

#### B2 — "Ask Aegis" assistant
- **What:** chat interface where the user asks natural-language questions; the assistant answers using **read-only tools only**, showing tool calls and evidence citations. No write tools are ever exposed.
- **Owner:** Navin J (engine) + Dhanush Kumar S (UI). **Dependencies:** B1, tool layer.
- **Acceptance criteria:** questions about health/metrics/logs answered with cited evidence; UI displays tool calls; write-tool exposure = 0.

### Tier C — Product / UX (P1)

| ID | Feature | Owner | Depends on | Acceptance criteria |
|---|---|---|---|---|
| C1 | Full console — 8 pages (command center, service, incident, approvals, postmortem, runbooks, Ask Aegis, **deployments**) | Dhanush K | A10, B2 | Pages match [product-vision.md](product-vision.md); demo-ready at M7 |
| C3 | Runbook repository UI (list + viewer, linked to incidents) | Dhanush K | B1 | runbook opens in console; incident links to runbook |
| C4 | Postmortem viewer | Dhanush K | A5 | rendered AI postmortem with timeline + metrics |
| C5 | Audit log viewer | Dhanush K | audit store | filterable audit trail rendered |

### Tier D — DevOps / Cloud (P1)

| ID | Feature | Owner | Depends on | Acceptance criteria |
|---|---|---|---|---|
| D1 | Kubernetes deployment of platform + demo app (Kustomize bases per ADR-0005; kind/k3s cluster) | Gokul J | all services containerized | full stack runs via `kubectl apply`; same configs as Compose |
| D5 | CI/CD — test, lint, build, push images, (optional) deploy | Gokul J | components | green pipeline on every PR; images in registry |
| D6 | SLO dashboards + burn-rate alerts per service | Gokul J + Navin J | A1 | SLO panels live in Grafana; burn-rate alerts fire on evaluation faults |

### Tier E — Academic (P1)

| ID | Item | Owner | Depends on | Acceptance criteria |
|---|---|---|---|---|
| E2 | Comparison study: conventional vs AI-assisted workflow (MTTD/MTTR, correctness) | Navin J | A12 | report with statistics, committed to repo |
| E4 | Thesis-ready documentation at every milestone | Navin J | all | docs complete + indexed at each M-milestone |

---

### Tier DI — Deployment Intelligence (upgrade 2026-09-01)

> Design: [docs/architecture/deployment-intelligence.md](../architecture/deployment-intelligence.md).
> Full set of 7 capabilities, integrated into existing phases (no timeline change).

| ID | Capability | Owner | Depends on | Acceptance criteria |
|---|---|---|---|---|
| DI-1 | Deployment tracking & registry (deploy events, history API, per-service deploy timeline) | Jegatheesan K (API) + Gokul J (pipeline hook) | A1, envelope | every deploy/rollback recorded; history API live by P2 gate |
| DI-2 | Deployment risk scoring (ML: pre-deploy prediction + post-deploy risk) | Navin J | DI-1, A3 | risk score for every deploy; prediction recall ≥ 0.7 on faulty-deploy faults |
| DI-3 | Change-incident correlation (RCA attributes incidents to deployments) | Navin J | A5, DI-1 | top-1 correlation accuracy ≥ 0.8 on faulty-deploy faults |
| DI-4 | Bad-rollout detection (deploy-window anomaly evaluation) | Navin J + Gokul J | DI-1, A3 | rollout.bad flagged < 3 min on faulty-deploy faults |
| DI-5 | Rollback intelligence (recommend + policy-gated execution, safe auto-rollback for low-risk) | Navin J (design) + Gokul J (executor) | A6, A8, DI-4 | rollback restores health in ≥ 80% of faulty-deploy runs; safety violations = 0 |
| DI-6 | Canary / progressive delivery analysis (canary vs stable metric comparison) | Gokul J | D1, DI-4 | canary deployment in demo; analysis visible in console |
| DI-7 | Change-failure analytics (CFR dashboards, deployment postmortems, CFR evaluation metric) | Navin J + Gokul J (dashboards), Jegatheesan K (backend), Dhanush K (UI) | A12, DI-1 | CFR panel live; CFR included in evaluation report |

---

## 3. Dependency Graph

```text
A1 ──▶ A2 ──▶ A3 ──▶ A4 ──▶ A5 ──▶ A6 ──▶ A7 ──▶ A8 ──▶ A9
                │        │       │       │       │
                │        │       ▼       │       │
                │        │      B1 ◀─────┘       │
                │        │       │              │
                │        │       ▼              │
                │        │      B2 ─────────────┘
                │        │
                ▼        ▼
              A10 ◀───── C1 (C3◀B1, C4◀A5, C5◀audit)
Demo app ──▶ A11 ──▶ A12 ──▶ E2
A1 ──▶ D6     all ──▶ D1, D5     E4 (ongoing)
```

- **Critical path:** A1 → A2 → A3 → A4 → A5 → A6 → A8 → A9 → A12 → E2.
- **Parallel tracks:** Dhanush (C1 UI) runs alongside the critical path; Gokul (D1/D5/D6/A11) overlaps after A1.

---

## 4. Micro-Decisions (decided 2026-08-31)

| # | Decision | Chosen | Rationale |
|---|---|---|---|
| 1 | Demo app name | **AegisShop** | Brand-consistent; retail microservices is the industry-standard SRE demo pattern (evaluators recognize it instantly). |
| 2 | Demo app tech | **Python/FastAPI microservices, OTel-instrumented, Postgres + Redis** | One language across the whole repo; first-class Python OTel; Postgres/Redis already in the compose stack (zero new infra). |
| 3 | B3 LoRA/QLoRA fine-tuning | **Keep as gated buffer stretch** (Apr–May 2027) | Free optional upside (MLOps depth for the thesis). Gate: core milestones M1–M8 on schedule; otherwise dropped. Never on the critical path. |
| 4 | Cluster for D1 (Kubernetes) | **kind** | Fastest startup, offline-capable, CI-friendly, native Kustomize support. Fallback: k3s on constrained machines. |

> Decider: Navin Jairam (Team Lead), on agent recommendation, 2026-08-31.
> Re-opening any decision requires a Team Lead call + Decision Log entry.
