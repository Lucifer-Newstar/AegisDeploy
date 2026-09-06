# Codebase Study Path — understand AegisDeploy in order

> **For Navin** — read the repo top-to-bottom so you can *explain* it to the
> team (and defend it). Each step says: **read** vs **skim**, how long, and
> what to take away. Tick the boxes as you go.
> Total ≈ 5–6 hours — doable in 2–3 evenings. **Meet is tomorrow? Jump to §0.**
> Companion: [kickoff-guide.md](kickoff-guide.md) (run the sync) ·
> [p2-tracker.md](../../planning/p2-tracker.md) (status board)

---

## §0. Emergency prep — the meet is TOMORROW (~45 min)

If you have one evening, do only this:

1. [../../../README.md](../../../README.md) — 5 min. Identity: what AegisDeploy is (SRE platform + Deployment Intelligence).
2. [../../README.md](../../README.md) — 5 min. The map of the docs (know where everything lives).
3. [§7 cheat sheet](#7-the-30-second-explainers) below — 10 min. The elevator pitch + 2-min version + vocab.
4. [kickoff-guide.md](kickoff-guide.md) §2 demo script — 10 min. The commands you'll run live.
5. Skim the demo app + contracts: [../../contracts/README.md](../../contracts/README.md) — 10 min.
6. Skim [member plans](../README.md) — 5 min. Who does what (so the handoff table makes sense).

That's enough to run the sync honestly; the full path below fills the gaps afterwards.

---

## 1. Orientation — what is this repo (~20 min)

| # | Doc | How | Takeaway |
|---|---|---|---|
| 1 | [../../../README.md](../../../README.md) | read | The project's identity: **AegisDeploy** (formerly AegisSRE) — an AI-powered autonomous SRE platform **plus** a Deployment Intelligence tier (DI-1…DI-7). Capability table, repo layout, quickstart. |
| 2 | [../../README.md](../../README.md) | read | The **map**: which folder explains WHAT (project), WHY (planning), HOW (architecture), conventions (development), measurement (operations). Bookmark this. |
| 3 | [.gitignore & root files](../../../) | skim (ls) | Feel the layout: `backend/` (libs + services), `demoapp/aegisshop/`, `docs/`, `infra/`, `scripts/`, `Makefile`, `pyproject.toml`. |

**Checkpoint:** you can say what the project is and where any topic lives.

## 2. The project — WHAT & WHY (~60 min)

| # | Doc | How | Takeaway |
|---|---|---|---|
| 4 | [../../project/proposal.md](../../project/proposal.md) | read (§1–4), skim rest | The original research proposal: the **core loop** (observe → detect → incident → RCA → remediate → verify), the 4 research questions, the metrics (MTTD/MTTR, precision/recall, RCA accuracy, autonomy success). **Addendum 1** (end) = the DI upgrade + rename record. |
| 5 | [../../planning/product-vision.md](../../planning/product-vision.md) | skim | What the final product *looks like*: 8-page console, the demo story (faulty deploy → auto-rollback). Vision anchors every explanation. |
| 6 | [../../planning/features.md](../../planning/features.md) | skim | The **locked scope**: Tier A (A1–A12 core loop), B (RAG/Ask Aegis), C (console pages), D (CI/CD + K8s + chaos), E (evaluation), **Tier DI** (the 7 DI capabilities), and the explicit cuts. Know A1–A12 + DI-1…DI-7 by letter. |
| 7 | [../../project/roadmap.md](../../project/roadmap.md) | skim | Milestone-level: how the tiers land over time (P2 → P8). |

**Checkpoint:** you can recite the core loop and name A1–A12 + DI-1…DI-7.

## 3. The plan & the people (~30 min)

| # | Doc | How | Takeaway |
|---|---|---|---|
| 8 | [../../planning/phases.md](../../planning/phases.md) | read §P2–P3, skim rest | **Phase-gated development** P1–P8: each phase ends in a working increment + gate. P2 (now) = Observability + Demo App v1. Non-disruption design (no member blocks another). |
| 9 | [../../planning/timeline.md](../../planning/timeline.md) | skim | Calendar + member assignments per phase. You'll quote this in planning chats. |
| 10 | [../../team/team-structure.md](../../team/team-structure.md) | read | The four roles + ownership rows (incl. DI ownership). |
| 11 | [../README.md](../README.md) then each member's [README](../jegatheesan-backend/README.md) + [phase-plan](../jegatheesan-backend/phase-plan.md) | read | Each member: role, responsibilities, P2 row, risks. **Read all four** — you must know the team's own plans to lead them. |

**Checkpoint:** you can say who builds what in P2 and why no one blocks anyone.

## 4. Architecture — HOW the platform works (~90 min)

| # | Doc | How | Takeaway |
|---|---|---|---|
| 12 | [../../architecture/system-architecture.md](../../architecture/system-architecture.md) | **read fully** | The centerpiece: component diagram (registry/incidents/evidence/remediation/ml/ai/deployments + AegisShop + observability stack), §3.11 = DI component. This is the doc to re-read before any deep question. |
| 13 | [../../architecture/telemetry-model.md](../../architecture/telemetry-model.md) | **read fully** | The **envelope v0.2** (every event in the platform is one) + **§3.5 event catalogue** (types, streams, retention) + §5 stream semantics. You wrote/own this — know it cold. |
| 14 | [../../architecture/autonomy-model.md](../../architecture/autonomy-model.md) | read | Autonomy levels (L4 approve / L5 auto), safety boundaries, the **safe-auto-rollback** example (DI-5). Explains *why* the platform is trustworthy. |
| 15 | [../../architecture/deployment-intelligence.md](../../architecture/deployment-intelligence.md) | read | The DI tier design: DI-1…DI-7 flow, risk/canary/rollout fields, the faulty-deploy demo scenario. Your upgrade — know it cold. |

**Checkpoint:** you can draw the data flow from AegisShop metric → anomaly → incident → RCA → (auto-)rollback, and name where DI hooks in.

## 5. Decisions & diagrams — why it is this way (~45 min)

| # | Doc | How | Takeaway |
|---|---|---|---|
| 16 | [ADR 0001 → 0006](../../architecture/adr/0001-monorepo-structure.md) | read each (they're short) | The **decision history**: 0001 monorepo · 0002 Python/FastAPI · 0003 Postgres+pgvector · 0004 Redis Streams event layer · 0005 compose-now-K8s-ready · 0006 DI tier. "Why?" questions = point here. |
| 17 | [uml/README.md](../../architecture/uml/README.md) | read | The 14-diagram UML set + the DI-coverage matrix. |
| 18 | Selected diagrams: [use-case-platform](../../architecture/uml/use-case-platform.md) · [class-platform](../../architecture/uml/class-diagram-platform.md) · [component](../../architecture/uml/component-diagram.md) · [sequence](../../architecture/uml/sequence-diagram.md) · [state-machine](../../architecture/uml/state-machine-diagram.md) | read | The two runtime scenarios (db-down + faulty-deploy) live in sequence/state diagrams — these are your "show the team how it behaves" assets. Skim the rest. |
| 19 | [../../operations/evaluation.md](../../operations/evaluation.md) | skim | How success is measured — incl. §7 DI metrics (CFR, detection latency, rollback success). |

**Checkpoint:** you can answer "why Redis Streams?" / "why K8s-ready now?" with an ADR number.

## 6. Conventions & running it (~30 min)

| # | Doc | How | Takeaway |
|---|---|---|---|
| 20 | [../../development/tech-stack.md](../../development/tech-stack.md) | skim | The stack + why (Python 3.12/FastAPI, Next.js/TS, kind, …). |
| 21 | [../../team/working-rules.md](../../team/working-rules.md) | read | The team's rules (docs, commits, branches, PRs) — you enforce these. |
| 22 | [../../development/contributing.md](../../development/contributing.md) | read | Contribution workflow: Conventional Commits scopes, `feat/<member>-<area>-<topic>` branches, Definition of Done. |
| 23 | [../../development/local-setup.md](../../development/local-setup.md) | read + do | Machine setup + every env var. Run the stack yourself. |

**Checkpoint:** your machine runs `make infra-up` and everything is green.

## 7. The 30-second explainers (recite these)

**Elevator pitch (30 s):**
> AegisDeploy is a platform that watches our own microservices app (AegisShop),
> automatically detects when something breaks, figures out why with AI that
> cites evidence, and fixes it — safely, with human approval above a risk
> threshold. It also tracks every deployment and learns which changes cause
> failures, so bad rollouts get detected and rolled back automatically. We
> measure it by MTTD/MTTR, anomaly and RCA accuracy, and safe-autonomy rates.

**Two-minute version — the core loop (with DI):**
1. **Observe** — AegisShop emits metrics/logs/traces → Prometheus/Loki/Tempo (A1).
2. **Detect** — ML detectors flag anomalies (A3) → incident created (A4) → MTTD.
3. **Explain** — RCA engine builds evidence-backed hypotheses; RAG grounds answers in past incidents/runbooks (A5/B1/B2).
4. **Act** — planner proposes actions; policy gates them; human approves (L4) or safe-auto executes (L5) (A6–A9).
5. **Verify + learn** — recovery verified, incident closed (A9), postmortem written (C4) → MTTR.
6. **Deployment Intelligence** — every deploy is tracked (DI-1), risk-scored (DI-2), correlated to incidents (DI-3), bad rollouts detected < 3 min (DI-4) and auto-rolled-back safely (DI-5); canary analysis (DI-6); change-failure rate reported (DI-7).

**State of the project:** M1 done (foundation + full docs + 14 UML diagrams + DI upgrade). Walking skeleton done (telemetry/eventbus libs, service template, catalog-service live in Grafana, CI green). **P2 running now** (team builds AegisShop v1 + registry + DI-1 + console; you lead contracts + integration). Gate 2026-10-31. Full calendar in [timeline.md](../../planning/timeline.md).

**Vocab (say these like you own them):** envelope · stream (ADR-0004) · contract (freeze 09-08) · readiness vs liveness · mock server · MTTD/MTTR · CFR · L4/L5 autonomy · DI-1…DI-7 · `_template`. (Full glossary: [kickoff-guide.md](kickoff-guide.md) §8.)

## 8. Current state & team-facing docs (~30 min)

| # | Doc | How | Takeaway |
|---|---|---|---|
| 24 | [../../contracts/README.md](../../contracts/README.md) | read | The 6 OpenAPI contracts (registry :8101, deployments :8701, catalog/cart/order/payment) + conventions + the drift check. Freeze **2026-09-08**. |
| 25 | [../../planning/p2-kickoff.md](../../planning/p2-kickoff.md) | read | P2 scope, tracks, contracts-first protocol, gate criteria. |
| 26 | [../../planning/integration-edge-cases.md](../../planning/integration-edge-cases.md) | skim → know | Your 15-row risk register (CORS, readiness honesty, duplicates, drift, …) — you walk this weekly. |
| 27 | [kickoff-guide.md](kickoff-guide.md) | read | Your sync kit (agenda, demo script, D1–D9, weekly rhythm). |
| 28 | [../../planning/p2-tracker.md](../../planning/p2-tracker.md) | read | Your 24-item board through the gate. |
| 29 | [../../architecture/port-register.md](../../architecture/port-register.md) | skim | Service ids/ports/DNS/metric conventions — the source of truth for names. |

**Checkpoint:** you can run the kickoff sync and the weekly rhythm without notes.

## 9. The actual code — read it top-to-bottom (~60 min)

Read in this order (each file has a docstring explaining *why* it exists):

| # | File | Why it matters |
|---|---|---|
| 30 | [../../../backend/libs/telemetry/telemetry/envelope.py](../../../backend/libs/telemetry/telemetry/envelope.py) | The envelope v0.2 — the single most important code file in the repo (every event is one). |
| 31 | [../../../backend/libs/eventbus/eventbus/eventbus.py](../../../backend/libs/eventbus/eventbus/eventbus.py) | Redis Streams producer/consumer (ADR-0004): publish / consumer groups / ack. |
| 32 | [../../../backend/services/_template/template_service/main.py](../../../backend/services/_template/template_service/main.py) | The service template: /health /ready /metrics, OTel tracing, per-service metrics registry. Every service copies this. |
| 33 | [../../../demoapp/aegisshop/catalog-service/catalog_service/main.py](../../../demoapp/aegisshop/catalog-service/catalog_service/main.py) | The vertical slice: catalog API + metrics + FaultHook stub. Then [catalog.py](../../../demoapp/aegisshop/catalog-service/catalog_service/catalog.py) (the model). |
| 34 | Their tests ([test_envelope.py](../../../backend/libs/telemetry/tests/test_envelope.py), [test_eventbus.py](../../../backend/libs/eventbus/tests/test_eventbus.py), [test_catalog.py](../../../demoapp/aegisshop/catalog-service/tests/test_catalog.py)) | Tests ARE documentation — they encode the contract. |
| 35 | [../../../docker-compose.yml](../../../docker-compose.yml) + [../../../infra/prometheus/prometheus.yml](../../../infra/prometheus/prometheus.yml) + [../../../infra/otel/otel-collector.yaml](../../../infra/otel/otel-collector.yaml) | The runtime: how the stack fits together; what scrapes what; the OTLP path. |
| 36 | [../../../scripts/check_contract_drift.py](../../../scripts/check_contract_drift.py) + [../../../scripts/validate_yaml.py](../../../scripts/validate_yaml.py) + [../../../.github/workflows/ci.yml](../../../.github/workflows/ci.yml) | The guards: drift check, YAML validation, and the 6 CI jobs. |
| 37 | [../../../Makefile](../../../Makefile) + [../../../pyproject.toml](../../../pyproject.toml) | Developer UX + tooling rules. |

**Checkpoint:** you can trace a request: browser → console/curl → catalog-service → metrics → Prometheus → Grafana, and an event: deploy → envelope → stream → deployments-service → Postgres.

---

**Done = you can explain any of these to a teammate, and point to the doc/code that proves it.**
When you've finished the path (or the emergency version), the [kickoff-guide.md](kickoff-guide.md) is your deliverable for tomorrow.
