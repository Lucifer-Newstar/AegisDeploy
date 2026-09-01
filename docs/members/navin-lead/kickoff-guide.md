# Team Kickoff Guide — run the P2 kickoff sync

> **Owner:** Navin (Team Lead) · **Purpose:** everything needed to run the
> first kickoff sync and the weekly rhythm that follows — agenda, live demo
> script, decisions to close (D1–D9), and the decision-log rows to record.
> Consolidates the former `p2-sync-pack.md`, `sync-demo-script.md` and
> `decision-log-draft-p2-sync.md` (2026-09-01).
> Companion: [p2-kickoff.md](../../planning/p2-kickoff.md) ·
> [integration-edge-cases.md](../../planning/integration-edge-cases.md) ·
> [contracts/](../../contracts/) · [working-rules.md](../../team/working-rules.md)

---

## 1. First kickoff sync (~60 min, before contracts freeze 2026-09-08)

### Pre-reads (each member, ~30 min)

| Member | Read |
|---|---|
| All | [local-setup.md](../../development/local-setup.md) (machine setup) · [working-rules.md](../../team/working-rules.md) · own [phase-plan](../) P2 row |
| Navin | — (runs the meeting) |
| Jega | [contracts/](../../contracts/) all 3 files + [telemetry-model.md §3.5](../../architecture/telemetry-model.md) |
| Gokul | [docker-compose.yml](../../../docker-compose.yml) + [prometheus.yml](../../../infra/prometheus/prometheus.yml) + edge cases #7/#12 |
| Dhanush | [contracts/README.md](../../contracts/README.md) (mock-server + CORS) + edge cases #1/#13 |

### Agenda (timeboxed)

| # | Item | Time | Lead | Output |
|---|---|---|---|---|
| 1 | **Skeleton walkthrough** — run the demo script (§2): repo tour, `make infra-up`, Grafana dashboard, `curl :9001/products`, CI + drift check live | 10 min | Navin | Everyone can run the stack |
| 2 | **Contracts + event catalogue** — the OpenAPI files, deployment state machine, freeze process (after 09-08: contract PR + lead review). CORS dev policy (edge case #1) is **already decided** — announce, don't debate | 15 min | Navin | Questions only; change requests as issues **before** freeze |
| 3 | **Close these decisions** (defaults proposed — confirm or override, then record; rows ready in §4) | 15 min | all | Decision-log rows (same day) |
| 4 | **Track commitments** — each member states week-1 deliverable + branch name (e.g. `feat/jega-registry-health`) | 10 min | each | One line each in sync notes |
| 5 | **Edge-case register + demo-of-week intro** — how the register is walked; demo-of-week format (§5); PR template + CI jobs | 5 min | Navin | Shared understanding |
| 6 | **Open forum** — questions on setup/contracts/workflow | 5 min | all | — |

---

## 2. Live demo script (10 min)

**Before the demo (do this, not during):**

```bash
cd AegisDeploy
make infra-up                      # stack + catalog-service
curl -s localhost:9001/health      # expect {"status":"healthy"}
```

### Step 1 — Repo tour (1 min)

Show the map (docs/README.md tree), then:
```bash
ls backend/libs backend/services demoapp docs/contracts
```
**Talking points:** libs = shared contracts (telemetry envelope v0.2, eventbus
ADR-0004) · `_template` = the pattern every service copies · `catalog-service`
= the first AegisShop slice · `docs/contracts/` = the API contracts we freeze
09-08.

### Step 2 — It's real (2 min)

```bash
docker compose ps                                   # all healthy
curl -s localhost:9001/products | head -c 200       # 5 products
```
**Talking points:** catalog API works end-to-end today; this is the reference
for cart/order/payment (Jega).

### Step 3 — Telemetry in Grafana (2 min)

```bash
for i in $(seq 1 20); do curl -s localhost:9001/products > /dev/null; done   # traffic
```
Open Grafana **localhost:3000** (`admin` / `aegis`) → dashboards →
**"AegisShop — Catalog Service"** → show QPS / p95 / 5xx / catalog-size panels.
Then Prometheus **localhost:9090/targets** → `aegisshop-catalog` = UP.

**Talking points:** metrics flow service → /metrics → Prometheus → Grafana;
this is the P2 gate pattern ("visible < 60 s"), just with one service today.

### Step 4 — Traces (1 min, if time)

Grafana → Explore → Tempo → trace a `/products` request (service:
`catalog-service`). If traces don't show, skip with one line: "tracing is
no-op when OTLP endpoint is unset — Gokul's A1 task wires it per service."

### Step 5 — CI + drift check (2 min)

Open `.github/workflows/ci.yml` → name the 5 jobs. Then run the guard live:
```bash
python3 scripts/check_contract_drift.py
```
**Talking points:** the drift check compares each built service's OpenAPI
against `docs/contracts/` — it already caught a real bug (catalog 404 wasn't
declared in the route decorator). Rule for everyone: **contracts change
first, code follows** (freeze 09-08, then contract PRs).

### Step 6 — Handoff (2 min)

| Track | Starts with |
|---|---|
| Jega | `_template` + contracts (registry :8101, deployments :8701, cart/order/payment 9002–9004) + libs |
| Gokul | compose + prometheus.yml + edge cases #7/#12 (DI-1 hook decision D5) |
| Dhanush | contracts → mock server (openapi-typescript + MSW, D3) + console scaffold |
| Navin | port register + edge-case register + weekly syncs |

Close with: **"One command shows every service in Grafana AND the console"**
— the gate (2026-10-31), rehearsal 2026-10-15.

### Troubleshooting (if something breaks on stage)

| Symptom | Fix |
|---|---|
| `docker compose ps` not healthy | Docker Desktop not running — start it, `make infra-up` again |
| Grafana panels empty | Prometheus → Targets: target down? Check `make infra-logs` |
| Port 9001 busy | `docker ps` → conflicting container; or demo still works without the traffic loop |
| Drift check prints "skipped" | Expected — unbuilt services are skipped by design (their contracts are the forward spec) |

---

## 3. Decision table to close (agenda item 3)

| # | Decision | Proposed default | Decider | Blocks |
|---|---|---|---|---|
| D1 | cart/order/payment ports | `9002` / `9003` / `9004` — **locked 2026-09-01** (lead pre-approval); team confirms at sync | Jega + Navin | contracts freeze |
| D2 | DB layer | **SQLAlchemy 2.x + Alembic** (migrations versioned from P2) | Jega | AegisShop v1 models |
| D3 | Frontend mock tooling | `openapi-typescript` types + MSW mocks (Prism as fallback) | Dhanush | console scaffold |
| D4 | Logs → Loki path | **OTLP logs from services** via existing collector (no new component); promtail as fallback | Gokul | edge case #6 (trace_id in logs) |
| D5 | DI-1 deploy-event hook | Compose `make deploy-events` script = **gate path**; CI hook best-effort (edge case #7) | Gokul + Jega | DI-1 acceptance |
| D6 | Registry status semantics | `healthy` = `/ready` ok; `degraded` = ready but slow; `unhealthy` = probe fail (contracts/registry-service.yaml) | Jega + Navin | Command Center |
| D7 | Contract-drift CI check | Implemented by Navin in P2 (edge case #8) — **done 2026-09-01** (`scripts/check_contract_drift.py`) | Navin | freeze confidence |
| D8 | Order ↔ cart coupling | order-service reads the cart synchronously via `GET /cart/{user_id}` (simple v1); client-passed items as fallback | Jega + Navin | order contract |
| D9 | "paid" status path | payment-service calls `POST /orders/{order_id}/paid` (explicit endpoint, sync v1); event-driven alternative from P3 | Jega + Navin | order/payment contracts |

> Rule: **no decision leaves the room unrecorded.** Every row lands in the
> planning [decision log](../../planning/README.md) the same day, or the sync
> is not done.

---

## 4. Decision-log rows (record D1–D9 after the sync — ~5 min)

Copy into [docs/planning/README.md §2](../../planning/README.md) (Decision Log
table). Replace `[SYNC-DATE]` with the sync date. Rows marked **LOCKED** are
lead pre-approvals — the sync records them, not re-debates. Overrides: edit
the decision text before copying.

| Date | Decision | Owner | Ref |
|---|---|---|---|
| [SYNC-DATE] | **D1 — AegisShop ports locked:** cart `9002` · order `9003` · payment `9004` (lead pre-approval; team confirmation). **LOCKED** | Navin Jairam (Team Lead) | [port-register.md](../../architecture/port-register.md) |
| [SYNC-DATE] | **D2 — DB layer:** SQLAlchemy 2.x + Alembic; migrations versioned from P2. | Jegatheesan K | [kickoff guide](../navin-lead/kickoff-guide.md) |
| [SYNC-DATE] | **D3 — Frontend mock tooling:** openapi-typescript client types + MSW mocks (Prism fallback). | Dhanush Kumar S | [contracts README](../../contracts/README.md) |
| [SYNC-DATE] | **D4 — Logs → Loki:** OTLP logs from services via the existing collector; no new component. | Gokul J | [edge cases #6](../../planning/integration-edge-cases.md) |
| [SYNC-DATE] | **D5 — DI-1 deploy-event hook:** compose `make deploy-events` = gate path; CI hook best-effort (edge case #7). | Gokul J + Jegatheesan K | [edge cases #7](../../planning/integration-edge-cases.md) |
| [SYNC-DATE] | **D6 — Registry status semantics:** `healthy` = /ready ok · `degraded` = ready slow · `unhealthy` = probe fail. | Jegatheesan K + Navin Jairam | [registry contract](../../contracts/registry-service.yaml) |
| [SYNC-DATE] | **D7 — Contract-drift CI check:** implemented `scripts/check_contract_drift.py` (recorded as done). | Navin Jairam | [edge cases #8](../../planning/integration-edge-cases.md) |
| [SYNC-DATE] | **D8 — Order ↔ cart coupling:** order-service reads the cart synchronously via `GET /cart/{user_id}` (v1 simple; client-passed items as fallback). | Jegatheesan K + Navin Jairam | [edge cases #15](../../planning/integration-edge-cases.md) |
| [SYNC-DATE] | **D9 — "paid" status path:** payment-service calls explicit `POST /orders/{order_id}/paid` (sync v1; event-driven alternative from P3). | Jegatheesan K + Navin Jairam | [edge cases #15](../../planning/integration-edge-cases.md) |

**After recording:** freeze contracts (2026-09-08) — post-freeze changes go
through a contract PR (contracts README §6).

---

## 5. Standing weekly sync (30 min, Mondays)

| Slot | Time | Content |
|---|---|---|
| Status round | 5 min | One line each: done / blocked / next. **Blockers only get airtime** — nothing else |
| Edge-case register walk | 10 min | Navin reads rows whose `Due` is now; members report; new rows added from the week's PRs |
| Demo-of-week + drift | 10 min | One member demos (see §6); contract/catalogue diffs reviewed if any landed |
| Decisions & actions | 5 min | Close/open decision rows; assign owners + due dates; update decision log |

Standing rules (from [working-rules.md](../../team/working-rules.md)):
- **No member blocked > 48 h** — escalate to Navin; he unblocks or re-plans that same week.
- Decisions are **recorded, not remembered** — decision-log rows, not chat.
- Missed sync = catch up on the notes; syncs are documented in this guide's
  format, not replays.

---

## 6. Demo-of-week format (≤ 5 min, one member per week, rotating)

A demo is *evidence of working software*, not a slide:

1. **What you built** — one line, maps to your P2 row.
2. **Show it live** — curl output, Grafana panel, console page, pytest run.
3. **Prove the boundary** — show the contract/edge case it touches (e.g. Jega:
   "deploy event POST → recorded → `GET /deployments` shows it, replay returns 200").
4. **What's next** — the next week's target, named in your phase-plan.

Rotation: Jega → Gokul → Dhanush → Navin (contracts/CI demos in his weeks).

---

## 7. The gate, previewed every week (2026-10-31)

The P2 gate is one sentence: **"One command shows every AegisShop service in
Grafana AND the console."** Each weekly sync ends by checking progress toward
it:

- [ ] AegisShop services visible in Grafana (metrics), Loki (logs), Tempo (traces) < 60 s after start
- [ ] Registry + health API lists services; envelope schema enforced at ingestion
- [ ] Console renders Command Center from the mock server
- [ ] DI-1: deploy events recorded + queryable (replay idempotent)

Rehearsal (integration checkpoint) on **2026-10-15** — same script, so the
gate run is a repeat, not a first.

---

## 8. One-line glossary (so everyone speaks the same language)

| Term | Means |
|---|---|
| Envelope | The universal event wrapper (`backend/libs/telemetry`, v0.2) — every event in the platform is one |
| Stream | Redis Streams topic per event type (`st:deployment`, …) — ADR-0004 |
| Contract | OpenAPI file in `docs/contracts/` — the agreed API shape, frozen 09-08 |
| Mock server | Generated from contracts — frontend's stand-in until real APIs land |
| Readiness | `/ready` = the service's real dependencies are up (not just the process) |
| DI-1 | Deployment tracking: every deploy is an event with a revision; the data source for DI-3/DI-4 |
| Demo-of-week | 5-minute live evidence of working software (§6) |
