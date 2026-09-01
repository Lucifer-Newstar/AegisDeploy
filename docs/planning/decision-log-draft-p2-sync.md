# D1–D9 Decision-Log Draft (kickoff sync)

> **How to use (5 minutes at the sync):** after the team confirms/overrides,
> copy the rows below into [docs/planning/README.md §2](../planning/README.md)
> (Decision Log table). Replace `[SYNC-DATE]` with the sync date. Rows marked
> **LOCKED** are lead pre-approvals — the sync records them, not re-debates.
> Overrides: edit the decision text before copying.
> Prepped 2026-09-01 by Navin.

| Date | Decision | Owner | Ref |
|---|---|---|---|
| [SYNC-DATE] | **D1 — AegisShop ports locked:** cart `9002` · order `9003` · payment `9004` (lead pre-approval; team confirmation). **LOCKED** | Navin Jairam (Team Lead) | [port-register.md](../architecture/port-register.md) |
| [SYNC-DATE] | **D2 — DB layer:** SQLAlchemy 2.x + Alembic; migrations versioned from P2. | Jegatheesan K | [sync pack](p2-sync-pack.md) |
| [SYNC-DATE] | **D3 — Frontend mock tooling:** openapi-typescript client types + MSW mocks (Prism fallback). | Dhanush Kumar S | [contracts README](../contracts/README.md) |
| [SYNC-DATE] | **D4 — Logs → Loki:** OTLP logs from services via the existing collector; no new component. | Gokul J | [edge cases #6](integration-edge-cases.md) |
| [SYNC-DATE] | **D5 — DI-1 deploy-event hook:** compose `make deploy-events` = gate path; CI hook best-effort (edge case #7). | Gokul J + Jegatheesan K | [edge cases #7](integration-edge-cases.md) |
| [SYNC-DATE] | **D6 — Registry status semantics:** `healthy` = /ready ok · `degraded` = ready slow · `unhealthy` = probe fail. | Jegatheesan K + Navin Jairam | [registry contract](../contracts/registry-service.yaml) |
| [SYNC-DATE] | **D7 — Contract-drift CI check:** implemented `scripts/check_contract_drift.py` (recorded as done). | Navin Jairam | [edge cases #8](integration-edge-cases.md) |
| [SYNC-DATE] | **D8 — Order ↔ cart coupling:** order-service reads the cart synchronously via `GET /cart/{user_id}` (v1 simple; client-passed items as fallback). | Jegatheesan K + Navin Jairam | [edge cases #15](integration-edge-cases.md) |
| [SYNC-DATE] | **D9 — "paid" status path:** payment-service calls explicit `POST /orders/{order_id}/paid` (sync v1; event-driven alternative from P3). | Jegatheesan K + Navin Jairam | [edge cases #15](integration-edge-cases.md) |

**After recording:** freeze contracts (2026-09-08) — post-freeze changes go
through a contract PR (contracts README §6).
