# P2 Kickoff — Observability + Demo App v1 (Sep–Oct)

> **Status:** proposed for team review · **Kickoff window:** 2026-09-01 (skeleton done)
> **Phase gate:** 2026-10-31 — checkpoint §P2 green ([timeline.md](timeline.md))
> Source of truth: [phases.md](phases.md) §P2 · [features.md](../planning/features.md) · member phase-plans

## 1. Where we are (what the skeleton already delivered)

The walking-skeleton base layer (committed 2026-09-01) already gives P2 its
foundation, so the phase starts **ahead of its original plan**:

| Skeleton deliverable | P2 impact |
|---|---|
| `backend/libs/telemetry` — envelope **v0.2** (incl. `deployment_payload` DI fields) | Jega's services emit events from day one; **DI-1 has its schema now** (no v0.1→v0.2 migration) |
| `backend/libs/eventbus` — Redis Streams (ADR-0004) | Registry/incidents/deploy-tracker events flow with at-least-once semantics |
| `backend/services/_template` — FastAPI pattern | Every P2 service copies it (health/ready/metrics/OTLP, per-service registry) |
| `demoapp/aegisshop/catalog-service` — vertical slice | Proves OTLP → Grafana end-to-end; catalog is the reference for cart/order/payment |
| Compose + CI + K8s base | Stack runs; `python-quality` CI job live; catalog has a Kustomize base (ADR-0005) |

**Consequently, Navin's original P2 row** ("envelope + event layer design") is
**already complete** — his P2 track is re-scoped below to contracts governance
+ integration protocol.

## 2. P2 scope (unchanged from phases.md)

**Objective:** the platform can see the demo app, and every member has a
running scaffold. **Gate:** "One command shows every AegisShop service in
Grafana AND the console."

- A1 observability pipeline complete for all AegisShop v1 services
- AegisShop v1 (catalog + cart + order + payment, Postgres persistence)
- A2 service registry & live health API
- **DI-1 deployment tracking** — deploy events recorded (envelope v0.2, ready)
- Console scaffold (Next.js + TS) with design system on mock data
- OpenAPI contracts committed (contracts-first, non-blocking tracks)

## 3. Track plan

### Navin J — Team Lead / Contracts (re-scoped; skeleton absorbed the old row)

| Deliverable | Detail | Acceptance |
|---|---|---|
| API contract set (OpenAPI) | Registry, health, deploy-tracker (DI-1), cart/order/payment — committed in [`docs/contracts/`](../contracts/) (drafted) | Contracts frozen by 2026-09-08; mock server generated from them |
| Event catalogue v1 | Documented event types + payloads per service (envelope v0.2; `st:<type>` streams) — **done in [telemetry-model.md §3.5](../architecture/telemetry-model.md)** | One table in `docs/architecture/telemetry-model.md` |
| Port + naming register | Services, ports, DNS names, metric/label conventions (extend `_template` README) | Every P2 service matches the register |
| Integration protocol + edge cases | Weekly sync cadence, checkpoint definition, **cross-member edge-case register ([integration-edge-cases.md](integration-edge-cases.md))** | Register walked at every weekly sync |
| Lead duties | Gate reviews, PR review backlog < 48 h, unblocking | No track blocked > 48 h |

### Jegatheesan K — Backend (AegisShop v1 + A2 + DI-1)

| Deliverable | Detail | Acceptance |
|---|---|---|
| AegisShop v1 services | `cart-service`, `order-service`, `payment-service` (copy `_template`); catalog gets Postgres persistence + DB models; SQLAlchemy migration versioned from P2 | All four services healthy in compose; DB migrations versioned |
| A2 registry + health | `registry-service` (:8101): register/heartbeat/list APIs; health aggregation from `/health` `/ready` | Registry lists all services; heartbeat reflects real state |
| **DI-1 deploy tracker API** | `deployments-service` (:8701): POST deploy events (envelope v0.2 `deployment_payload`), GET history; persisted to Postgres | Deploy event → recorded → queryable (< 1 s); schema enforced |
| Events + OpenAPI | Events via eventbus; OpenAPI published per service; client regenerated | Frontend mock server builds from contracts |

### Gokul J — DevOps (A1 completion + DI-1 pipeline hook)

| Deliverable | Detail | Acceptance |
|---|---|---|
| A1 pipeline complete | OTel configs per AegisShop service; **logs → Loki** (log collection enabled); traces → Tempo verified per service; dashboards for all services | Telemetry visible in Grafana/Loki/Tempo **< 60 s** after start (gate) |
| Compose + Dockerfiles | cart/order/payment/registry/deployments in compose; images built via CI | One command starts platform + full AegisShop |
| **DI-1 pipeline hook** | Compose/CI deploy step emits `deploy_started` / `deploy_finished` events (risk fields optional now) | Every `make infra-up`/PR deploy produces recorded deploy events |
| K8s-ready | Kustomize bases for the new services (ADR-0005, extend the skeleton pattern) | Bases land with each service PR |

### Dhanush K — Frontend (console scaffold)

| Deliverable | Detail | Acceptance |
|---|---|---|
| Console scaffold | Next.js + TS app in `frontend/`, CI build job, dark-theme design tokens | Scaffold runs; tokens documented |
| Command Center page | Service list/health from mock server (registry OpenAPI) | Renders all AegisShop services (mock) |
| Service page | Per-service health/metrics summary from mocks | Page navigates from Command Center |
| Mock server | Generated from OpenAPI contracts | UI never blocked by API timing |

## 4. Contracts-first protocol (non-blocking design)

1. **Contracts freeze 2026-09-08** — OpenAPI + event catalogue committed by Navin
   (drafted with Jega's input); after freeze, changes go through a contract PR.
2. Dhanush builds against **mock server from contracts**; Jega against the same contracts.
3. Gokul consumes only ports/endpoints from the register — code-independent track.
4. Envelope schema is **enforced at ingestion** (registry/deployments validate v0.2).

## 5. Branch + PR workflow (unchanged rules)

- Branches: `feat/<member>-<area>-<topic>` (e.g. `feat/jega-registry-health`)
- PRs into `main`; main always deployable; CI (`yaml-and-compose`, `k8s-lint`,
  `docs`, `python-quality`) must pass before merge
- New Python packages join the `python-quality` job when they land
- First PRs per track land as **feature branches**, never direct commits

## 6. Checkpoints & gate

| When | What |
|---|---|
| 2026-09-08 | Contracts freeze + first branches cut |
| Weekly (Mon) | 30-min sync per the [team sync pack](p2-sync-pack.md): status round, edge-case register walk, demo-of-week, decisions recorded |
| 2026-10-15 | Integration checkpoint rehearsal (one command, Grafana + console) |
| 2026-10-31 | **Gate review** — criteria below |

**Gate criteria (from phases.md):**
- [ ] AegisShop services visible in Grafana (metrics), Loki (logs), Tempo (traces) within 60 s of start
- [ ] Registry + health API returns service list; envelope schema enforced at ingestion
- [ ] Console scaffold renders Command Center from the mock server
- [ ] **DI-1:** deploy events recorded and queryable via the deploy tracker API

**DI hook for P2 (from the DI design):** deploy events use the v0.2
`deployment_payload` (status `started`/`finished`/`failed`, optional risk
fields); the risk-scoring (DI-2) and correlation (DI-3) work in P4 consumes
this history — **so the quality of P2's deploy events decides P4's accuracy.**

## 7. Risks & mitigations

| Risk | Mitigation |
|---|---|
| Four AegisShop services + 3 platform services is a lot for one backend track | Catalog already exists (slice); cart/order/payment share the template; registry/deployments are small CRUD + events; DB models are the only heavy lift |
| Frontend blocked on contracts | Mock server from OpenAPI (freeze 09-08) |
| Logs→Loki config drift | Gokul's pipeline verified per service at the checkpoint |
| Lead bandwidth | Contracts-first + weekly syncs; implementation delegated to members (skeleton pattern proven) |
| DI-1 events too thin for P4 | Deploy-event acceptance includes at least: service, version, status, timestamps, commit ref |

## 8. First actions (week of 2026-09-01)

1. Navin: draft OpenAPI contracts + event catalogue; open `docs/contracts/`
2. Jega: `cart-service` branch (copy `_template`); registry design notes
3. Gokul: logs→Loki config for catalog; AegisShop v1 service list in compose
4. Dhanush: `frontend/` scaffold branch; design tokens
5. Team: kickoff sync to confirm naming/ports (per phases.md §P2 note)
