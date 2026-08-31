# Jegatheesan K — Backend Developer

> **Member 2** — Backend track.

## Role

Build the platform's backend services and the AegisShop demo application — the APIs
that every other track consumes.

## Primary responsibilities

- Backend services (Python / FastAPI) — gateway, registry, incidents, approvals, verification
- APIs (OpenAPI-first) & database (PostgreSQL, Redis)
- Authentication / authorization
- Application business logic & backend integrations
- AegisShop demo app backend services

## Repo areas owned

- `backend/` (all)
- `demoapp/` — AegisShop services (location TBC at P2 kickoff)
- `docs/members/jegatheesan-backend/` (this folder)

## Contracts I consume / provide

| Contract | Direction | Counterpart |
|---|---|---|
| Telemetry envelope (Pydantic) | consume | Navin (P2 start) |
| Anomaly events (Redis Streams) | consume | Navin (P3) |
| Action catalog + policies | consume (design) | Navin (P5) |
| OpenAPI spec for every service | **provide** | Dhanush (P2 start) |
| Incident / evidence / approval APIs | **provide** | Dhanush + Navin |

> Until anomaly events land (P3), the incident manager consumes a **test event
> producer** — my track never blocks (phases.md §4).

## My commitments

- Contracts-first: OpenAPI schemas committed at phase start (P2).
- Pydantic models are the single source of truth for schemas (ADR-0002).
- Every service has health endpoints + OTel instrumentation (metrics/logs/traces).
