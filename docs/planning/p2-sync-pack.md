# P2 Team Sync Pack — agenda & operating rhythm

> **Owner:** Navin (Team Lead) · **Purpose:** make the first kickoff sync and
> every weekly sync after it fast, documented, and decision-driven.
> Companion docs: [p2-kickoff.md](p2-kickoff.md) · [integration-edge-cases.md](integration-edge-cases.md)
> · [contracts/](../contracts/) · [working-rules.md](../team/working-rules.md)

---

## 1. First kickoff sync (~60 min, before contracts freeze 2026-09-08)

### Pre-reads (each member, ~30 min)

| Member | Read |
|---|---|
| All | [local-setup.md](../development/local-setup.md) (machine setup) · [working-rules.md](../team/working-rules.md) · own [phase-plan](../members/) P2 row |
| Navin | — (runs the meeting) |
| Jega | [contracts/](../contracts/) all 3 files + [telemetry-model.md §3.5](../architecture/telemetry-model.md) |
| Gokul | [docker-compose.yml](../../docker-compose.yml) + [prometheus.yml](../../infra/prometheus/prometheus.yml) + edge cases #7/#12 |
| Dhanush | [contracts/README.md](../contracts/README.md) (mock-server + CORS) + edge cases #1/#13 |

### Agenda (timeboxed)

| # | Item | Time | Lead | Output |
|---|---|---|---|---|
| 1 | **Skeleton walkthrough** — run the [demo script](sync-demo-script.md) (repo tour, `make infra-up`, Grafana dashboard, `curl :9001/products`, CI + drift check live) | 10 min | Navin | Everyone can run the stack |
| 2 | **Contracts + event catalogue** — the 3 OpenAPI files, deployment state machine, freeze process (after 09-08: contract PR + lead review). CORS dev policy (edge case #1) is **already decided** — announce, don't debate | 15 min | Navin | Questions only; change requests as issues **before** freeze |
| 3 | **Close these decisions** (defaults proposed — confirm or override, then record; copy from the [D1–D9 draft](decision-log-draft-p2-sync.md)) | 15 min | all | Decision-log rows (same day) |
| 4 | **Track commitments** — each member states week-1 deliverable + branch name (e.g. `feat/jega-registry-health`) | 10 min | each | One line each in sync notes |
| 5 | **Edge-case register + demo-of-week intro** — how the register is walked; demo-of-week format (§3); PR template + CI jobs | 5 min | Navin | Shared understanding |
| 6 | **Open forum** — questions on setup/contracts/workflow | 5 min | all | — |

### Decision table to close (item 3)

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
> planning [decision log](README.md) the same day, or the sync is not done.

---

## 2. Standing weekly sync (30 min, Mondays)

| Slot | Time | Content |
|---|---|---|
| Status round | 5 min | One line each: done / blocked / next. **Blockers only get airtime** — nothing else |
| Edge-case register walk | 10 min | Navin reads rows whose `Due` is now; members report; new rows added from the week's PRs |
| Demo-of-week + drift | 10 min | One member demos (see §3); contract/catalogue diffs reviewed if any landed |
| Decisions & actions | 5 min | Close/open decision rows; assign owners + due dates; update decision log |

Standing rules (from [working-rules.md](../team/working-rules.md)):
- **No member blocked > 48 h** — escalate to Navin; he unblocks or re-plans that same week.
- Decisions are **recorded, not remembered** — decision-log rows, not chat.
- Missed sync = catch up on the notes; syncs are documented in this pack's
  format, not replays.

---

## 3. Demo-of-week format (≤ 5 min, one member per week, rotating)

A demo is *evidence of working software*, not a slide:

1. **What you built** — one line, maps to your P2 row.
2. **Show it live** — curl output, Grafana panel, console page, pytest run.
3. **Prove the boundary** — show the contract/edge case it touches (e.g. Jega:
   "deploy event POST → recorded → `GET /deployments` shows it, replay returns 200").
4. **What's next** — the next week's target, named in your phase-plan.

Rotation: Jega → Gokul → Dhanush → Navin (contracts/CI demos in his weeks).

---

## 4. The gate, previewed every week (2026-10-31)

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

## 5. One-line glossary (so everyone speaks the same language)

| Term | Means |
|---|---|
| Envelope | The universal event wrapper (`backend/libs/telemetry`, v0.2) — every event in the platform is one |
| Stream | Redis Streams topic per event type (`st:deployment`, …) — ADR-0004 |
| Contract | OpenAPI file in `docs/contracts/` — the agreed API shape, frozen 09-08 |
| Mock server | Generated from contracts — frontend's stand-in until real APIs land |
| Readiness | `/ready` = the service's real dependencies are up (not just the process) |
| DI-1 | Deployment tracking: every deploy is an event with a revision; the data source for DI-3/DI-4 |
| Demo-of-week | 5-minute live evidence of working software (§3) |
