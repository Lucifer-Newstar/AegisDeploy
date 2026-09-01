# API Contracts (P2) — `docs/contracts/`

> **Source of truth for every P2 API.** Contracts-first protocol (p2-kickoff.md
> §4): Dhanush's console builds against mock servers generated from these
> files; Jega implements against them; Gokul reads ports/DNS names from the
> same documents. **Freeze: 2026-09-08** — after that, changes go through a
> contract PR.
>
> Draft v1 by Navin (Team Lead) — final naming/tech confirmed with Jega at the
> P2 kickoff sync (phases.md §P2 note).

## Files

| Contract | Version | Service(s) | Port | Status |
|---|---|---|---|---|
| [registry-service.yaml](registry-service.yaml) | 1.0.0 | A2 registry + health | **8101** | pending (P2, Jega) |
| [deployments-service.yaml](deployments-service.yaml) | 1.0.0 | DI-1 deploy tracker | **8701** | pending (P2, Jega) |
| [catalog-service.yaml](catalog-service.yaml) | 1.0.0 | catalog | 9001 | **LIVE** (slice) |
| [cart-service.yaml](cart-service.yaml) | 1.0.0 | cart | 9002* | pending (P2, Jega) |
| [order-service.yaml](order-service.yaml) | 1.0.0 | order | 9003* | pending (P2, Jega) |
| [payment-service.yaml](payment-service.yaml) | 1.0.0 | payment | 9004* | pending (P2, Jega) |

\* cart/order/payment ports are **proposed** — confirmed at the kickoff sync.
[manifest.json](manifest.json) maps each service to its contract file for the
drift check — **add a row there when a service lands** (PR template).

## Conventions every contract obeys

1. **Health endpoints** — every service exposes `GET /health` (liveness) and
   `GET /ready` (readiness **with real dependency checks** — a service that
   needs Postgres must fail `/ready` while the DB is down; the registry
   aggregates this truth). `GET /metrics` (Prometheus) on every service.
2. **Errors** — FastAPI default shape `{"detail": "<human message>"}` with
   correct status codes: `404` unknown resource, `422` validation failure,
   `503` dependency unavailable. No bespoke error envelopes in v1.
3. **Timestamps** — ISO-8601 UTC (`2026-09-01T10:00:00Z`), always
   timezone-aware. Consumers never re-stamp.
4. **Events in APIs** — any event accepted/returned uses the telemetry
   envelope v0.2 (`backend/libs/telemetry`), never a bespoke shape. The
   deployments-service validates incoming envelopes with the shared lib
   (schema enforced at ingestion — P2 gate).
5. **CORS (dev policy)** — all services allow origin `http://localhost:3000`
   (Next.js dev server) in `dev` only. Applied via the service template when
   services are built. Production goes same-origin through the gateway (P6).
6. **Versioning** — contracts are additive-only; breaking changes require a
   contract PR even after freeze (the freeze is about *stability*, not
   immutability). Each file carries a `version` field + changelog comment.

## Mock server (frontend)

Dhanush generates client types + a mock server from these files (tool choice
is his; `openapi-typescript` + MSW/prism are the defaults). Mock server must
be regenerated on contract changes — a contract PR mentions the regeneration
in its description.

## Contract-drift guard (implemented — edge case #8)

`scripts/check_contract_drift.py` runs in CI (`python-quality` job): it
imports each built service's FastAPI app, reads its generated OpenAPI, and
compares it against this folder via `manifest.json` — **contract must be a
subset of the live API** (paths/methods, response codes, request-body
required fields). Additive live endpoints are allowed; a contract that
demands something the live API lacks fails the build.

Convention it enforces implicitly: **declare error responses in the route
decorator** (`responses={404: {...}}`) — FastAPI does not introspect handler
bodies, so undocumented errors silently vanish from the generated spec and
from the frontend mock server.
