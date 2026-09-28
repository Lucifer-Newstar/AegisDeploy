# Feature Scope & Acceptance

> **Purpose:** define what the team will build, who leads each item, what it depends on, and how completion is checked. This is the scope reference; phase order and gates are in [phases.md](phases.md).
>
> **Scope status:** `Core` = approved project scope · `Stretch` = optional only if the core is on schedule and the Team Lead approves · `Cut` = not planned. Reopening a cut item requires a decision-log entry.

---

## 1. How to read the catalogue

- **Feature ID** identifies the item. `A–E` and `DI` are separate ID families; for example, **D1** means Kubernetes, while **DI-1** means deployment tracking.
- **Priority tier** (P0/P1) is a feature priority, not development phase P0/P1/P2.
- Each item is separated into **Outcome**, **Lead / support**, **Needs**, and **Done when**. Leads coordinate delivery; support members contribute their named part.
- Numeric targets are acceptance thresholds, not promises about production-grade capability.

## 2. Approved scope at a glance

| Group | Included items | Purpose |
|---|---|---|
| **A · Core platform (P0)** | A1–A12 | Observe, detect, investigate, act safely, verify, and evaluate. |
| **B · AI depth (P1)** | B1–B2 | Grounded knowledge retrieval and read-only assistant. |
| **C · Product / UX (P1)** | C1, C3–C5 | Complete console and supporting views. |
| **D · DevOps / Cloud (P1)** | D1, D5–D6 | Kubernetes, CI/CD, and SLO monitoring. |
| **E · Academic (P1)** | E2, E4 | Comparative evaluation and milestone documentation. |
| **DI · Deployment Intelligence** | DI-1–DI-7 | Understand deployment risk, impact, rollback, canaries, and outcomes. |

**Demo application:** AegisShop, the team's own instrumented microservices app. Its service map is in [phases.md §7](phases.md#7-demo-application-aegisshop).

### Not planned

| Item | Status / reason |
|---|---|
| B3 · LoRA/QLoRA fine-tuning | **Stretch** in the final buffer only; drop it if core gates slip or hardware is unsuitable. |
| B4 · Time-series forecasting; B6 · incident clustering | **Cut:** not needed for the core research question. |
| C2 · topology map; C6 · notifications | **Cut:** not required for the agreed demo. |
| D2 · GitOps; D3 · cloud Terraform; D4 · chaos-mesh | **Cut:** local Kubernetes and the team's deterministic chaos lab cover the need. |
| E3 · literature survey; E5 · user study | **Cut:** outside the agreed evaluation plan. |

No cut feature is implicitly included as “nice to have.”

---

## 3. Tier A — Core platform (P0)

### A1 · Observability pipeline
- **Outcome:** collect app telemetry through OpenTelemetry; route metrics to Prometheus, logs to Loki, traces to Tempo; carry Kubernetes and deployment events on the shared event layer using the [telemetry envelope](../architecture/telemetry-model.md).
- **Lead / support:** Gokul / Navin (design and shared telemetry).
- **Needs:** shared infra stack.
- **Done when:** metrics appear in Grafana within 60 seconds of startup, logs are queryable, traces can be joined by `trace_id`, and required events are ingested.

### A2 · Service registry and health
- **Outcome:** API-managed service catalogue (owner, endpoints, SLOs) plus current health.
- **Lead / support:** Jegatheesan.
- **Needs:** A1.
- **Done when:** services can be created/read/updated/deleted through the API; health refreshes every 15 seconds; the console can read the result.

### A3 · Anomaly detection
- **Outcome:** detect unusual p95 latency, error rate, CPU/memory, and request rate using statistical baselines and Isolation Forest; publish `anomaly.score` events with model, threshold, window, and baseline context.
- **Lead / support:** Navin / Gokul (data plumbing).
- **Needs:** A1–A2.
- **Done when:** precision, recall, and F1 are each at least 0.85 on the agreed chaoslab evaluation set; detection latency is under 60 seconds from fault onset.

### A4 · Incident manager
- **Outcome:** group anomaly events into incidents, assign severity, enforce `open → investigating → remediating → verifying → closed | escalated`, and retain an append-only timeline.
- **Lead / support:** Jegatheesan / Navin (design).
- **Needs:** A3.
- **Done when:** an incident is created within 30 seconds of its qualifying anomaly; invalid state transitions are rejected; timeline API is usable. Postmortem generation is delivered under A5/C4.

### A5 · Evidence and root-cause analysis
- **Outcome:** gather evidence through read-only tools (metrics, logs, traces, service health, deployment history, Kubernetes events, runbooks); return ranked cause hypotheses with citations and confidence; generate a postmortem when an incident closes.
- **Lead / support:** Navin; Jegatheesan and Gokul provide APIs/tools.
- **Needs:** A1–A4; B1 retrieval context is integrated when available. RCA must still run against seeded evidence if retrieval is delayed.
- **Done when:** top-1 cause accuracy is at least 70% on evaluation faults, each hypothesis cites evidence, and a postmortem is available after closure.

### A6 · Remediation planner and policy engine
- **Outcome:** define actions (restart, rollback, scale, replace instance, config update, escalate), risk levels (low/medium/high/forbidden), and versioned policies. This component alone decides approval versus automatic execution.
- **Lead / support:** Navin (policy design) / Jegatheesan (implementation).
- **Needs:** A4–A5.
- **Done when:** risk classification passes the agreed evaluation set with zero safety violations; policies can be changed without code edits.

### A7 · Approval workflow (Level 4)
- **Outcome:** let an authorized person approve, reject, or defer an action with an impact summary; record actor, reason, and decision.
- **Lead / support:** Jegatheesan (API) / Dhanush (UI).
- **Needs:** A6.
- **Done when:** a decision takes at most three UI clicks and every decision is audit-logged.

### A8 · Safe autonomous execution (Level 5)
- **Outcome:** run only policy-approved, low-risk, reversible actions automatically; enforce cooldowns, rate limits, and a global autonomy-mode kill switch.
- **Lead / support:** Gokul (execution) / Navin (policy and safety).
- **Needs:** A6–A7.
- **Done when:** at least 80% of eligible evaluation actions succeed; the kill switch takes effect immediately; no policy-violating action runs.

### A9 · Recovery verification
- **Outcome:** check health, errors, latency, and SLO status after remediation; close only when recovered, otherwise escalate.
- **Lead / support:** Navin (logic) / Jegatheesan (API).
- **Needs:** A4 and A8.
- **Done when:** verdict accuracy is at least 90% against ground truth; no unrecovered incident is closed.

### A10 · Core dashboard
- **Outcome:** live overview, service detail, incident detail, and approvals views, including MTTD/MTTR and incident evidence.
- **Lead / support:** Dhanush.
- **Needs:** A2, A4–A7 APIs.
- **Done when:** core views render live API data; incident detail shows timeline, reasoning, and evidence. The complete eight-page scope is C1.

### A11 · Chaos lab
- **Outcome:** deterministic CLI fault injection for CPU saturation, memory exhaustion, container crash, database outage, network latency, HTTP 5xx, dependency failure, config error, faulty deployment, and traffic spike; restore state after each experiment.
- **Lead / support:** Gokul / Navin (fault definitions and ground truth).
- **Needs:** AegisShop.
- **Done when:** all ten faults are injectable; each run records fault label, start/end time, and restoration result for A12.

### A12 · Evaluation framework
- **Outcome:** compare conventional monitoring/manual response with AegisDeploy on identical faults; automate MTTD, MTTR, RCA, autonomy, and summary statistics.
- **Lead / support:** Navin / all members (runs and validation).
- **Needs:** A11 and E4.
- **Done when:** one documented command produces a reproducible report with at least ten runs per fault type and mean ± standard deviation.

---

## 4. Tier B — AI depth (P1)

### B1 · RAG knowledge base
- **Outcome:** index runbooks, prior incidents, service metadata, and known failure patterns in pgvector for retrieval by the reasoning layer.
- **Lead / support:** Navin.
- **Needs:** A4 and PostgreSQL/pgvector.
- **Done when:** relevant runbooks achieve recall@5 of at least 0.8 on evaluation faults and retrieved context is available to RCA.

### B2 · Ask Aegis
- **Outcome:** answer natural-language health questions using read-only tools; show tool calls and cited evidence. No write tools are exposed.
- **Lead / support:** Navin (engine) / Dhanush (UI).
- **Needs:** B1 and the read-only tool layer.
- **Done when:** health/metric/log questions receive evidence-cited answers, tool calls are visible, and write-tool exposure is zero.

---

## 5. Tier C — Product / UX (P1)

| ID | Outcome | Lead / support | Needs | Done when |
|---|---|---|---|---|
| **C1** | Eight-page console: command center, service, incident, approvals, postmortem, runbooks, Ask Aegis, deployments. | Dhanush | A10, B2, supporting APIs | All eight pages work on live APIs and match [product-vision.md](product-vision.md). |
| **C3** | Runbook list and viewer linked to incidents. | Dhanush | B1 | Runbook opens in console from its incident link. |
| **C4** | Postmortem viewer. | Dhanush | A5 | Timeline, evidence, actions, and metrics render after incident close. |
| **C5** | Audit-log viewer. | Dhanush | Audit store | Audit entries can be filtered and inspected. |

---

## 6. Tier D — DevOps / Cloud (P1)

| ID | Outcome | Lead / support | Needs | Done when |
|---|---|---|---|---|
| **D1** | Run platform and AegisShop on kind using Kustomize bases (k3s fallback). | Gokul | Containerized services | `kubectl apply` brings up the stack with behavior/config aligned to Compose. |
| **D5** | CI/CD: test, lint, build, publish images; deployment is optional. | Gokul | Service components | PR pipeline is green and images are published to the agreed registry. |
| **D6** | Per-service SLO dashboards and burn-rate alerts. | Gokul / Navin (SLO definitions) | A1 | Grafana panels are live and alerts fire in evaluation scenarios. |

---

## 7. Tier E — Academic (P1)

| ID | Outcome | Lead / support | Needs | Done when |
|---|---|---|---|---|
| **E2** | Compare conventional and AI-assisted workflows using MTTD, MTTR, and correctness. | Navin | A12 | Statistical results are documented and committed. |
| **E4** | Keep implementation, decisions, and results documented at each milestone. | Navin / all owners update their docs | All tracks | Milestone docs are current, linked, and understandable without verbal context. |

---

## 8. Deployment Intelligence (DI)

> Detailed design: [deployment-intelligence.md](../architecture/deployment-intelligence.md). DI is integrated into P2–P8; it does not add a phase.

| ID | Outcome | Lead / support | Needs | Done when |
|---|---|---|---|---|
| **DI-1** | Record deploy/rollback events; expose history and per-service timeline. | Jegatheesan (API) / Gokul (pipeline event) | A1, envelope | Each deploy/rollback is recorded and history API is available at P2 gate. |
| **DI-2** | Score deployment risk before/after rollout. | Navin | DI-1, A3 | Every demo deployment gets a score; recall ≥0.7 on faulty-deploy faults. |
| **DI-3** | Attribute incidents to likely causing deployments. | Navin / Jegatheesan (history API) | A5, DI-1 | Top-1 correlation accuracy ≥0.8 on faulty-deploy faults. |
| **DI-4** | Evaluate anomalies in a deployment window and flag bad rollouts. | Navin / Gokul (telemetry) | DI-1, A3 | `rollout.bad` is flagged within three minutes on faulty-deploy tests. |
| **DI-5** | Recommend rollback and execute only under the A6/A8 policy. | Navin (policy) / Gokul (executor) | A6, A8, DI-4 | Health is restored in ≥80% of faulty-deploy runs, with zero safety violations. |
| **DI-6** | Compare canary and stable metrics to assess a progressive rollout. | Gokul | D1, DI-4 | Demo canary is analyzed and result is visible in console. |
| **DI-7** | Calculate change-failure rate (CFR), show trends, and include deployment postmortems. | Jegatheesan (data) / Gokul (dashboard) / Dhanush (UI) / Navin (evaluation) | DI-1 for dashboard data; A12 for evaluation | CFR panel is live and the metric appears in evaluation report. |

---

## 9. Delivery map

| Phase | Feature IDs delivered or advanced |
|---|---|
| P2 | A1, A2, DI-1; console scaffold |
| P3 | A3, A4, DI-4 base |
| P4 | A5, B1, B2, DI-2, DI-3 |
| P5 | A6–A9, DI-5 |
| P6 (parallel) | A10, C1, C3–C5, D5, D6, DI-7 dashboards |
| P7 | D1, A11, DI-6 |
| P8 | A12, E2, DI-7 evaluation |

For acceptance gates and integration demonstrations, use [phases.md](phases.md).