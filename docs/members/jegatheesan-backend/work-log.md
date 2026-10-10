# Jegatheesan · Work log

> Dated record of backend delivery. Keep newest entries at the bottom.

| Date | What I shipped | Notes |
|---|---|---|
| 2026-09-08 | A2 `registry-service` skeleton (in-memory catalogue, `/services`, heartbeat) | Port 8101. Persistence deferred; `/ready` documents Postgres/Redis. |
| 2026-09-12 | DI-1 `deployments-service` (envelope ingest, idempotent replay, history + latest) | Port 8701. Validates deployment envelopes at ingestion. |
| 2026-09-18 | AegisShop `cart-service` | Port 9002. In-memory carts; product ids match catalog seed. |
| 2026-09-22 | AegisShop `order-service` | Port 9003. Demo checkout for `user-01`; optional cart HTTP lookup. |
| 2026-09-25 | AegisShop `payment-service` | Port 9004. Simulated charge; 402/404 hooks for tests. |
| 2026-10-08 | Tests + OpenAPI alignment for all P2 services | Contract-drift check now loads live modules. |
| 2026-10-10 | Live `/ready` probes in registry; DI-1 startup deploy seed | Probe is opt-in via `REGISTRY_PROBE`. |
