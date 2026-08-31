# ADR-0002: Python/FastAPI Backend

- **Status:** Accepted
- **Date:** 2026-08-31
- **Deciders:** Navin Jairam, Arena Agent

## Context

The control plane needs multiple services (gateway, service registry, telemetry
ingestion, incident manager, deployment tracker, policy engine, recovery verifier).
The ML and AI layers are Python-based. A single language across backend + ML + AI
minimizes context switching, lets shared schema definitions (Pydantic) be reused
everywhere, and keeps the project feasible for one engineer.

## Decision

Backend services are written in **Python 3.12 + FastAPI**, with:

- **Pydantic v2** models as the single source of truth for API schemas and the
  telemetry envelope (`docs/architecture/telemetry-model.md`).
- **Uvicorn** as the ASGI server; each service is its own deployable unit in
  `backend/services/<name>/` sharing `backend/libs/` for common code.
- **Async SQLAlchemy 2** for PostgreSQL access; **redis-py** for Redis/Streams.
- **pytest + httpx** for tests; **ruff + mypy** enforced in CI.
- OpenAPI generated from FastAPI used to generate the TypeScript API client for the
  frontend (single source of truth for the HTTP contract).

## Consequences

### Positive

- One language for services, ML, AI, and tooling.
- FastAPI's OpenAPI gives free docs and a typed frontend client.
- Pydantic v2 validates every telemetry envelope at ingestion — contract enforcement.
- Fast to iterate for a solo developer.

### Negative / Trade-offs

- Python performance is lower than Go/Rust for high-throughput ingestion; acceptable at
  this scale; the hot path (OTLP → stores) is handled by the OTel Collector, not Python.
- GIL constraints for CPU-heavy work; anomaly scoring is batch-based in `ml/` and fine.

## Alternatives Considered

| Option | Why rejected |
|---|---|
| Go (single binary, fast) | Splits language across AI/ML layers; slower iteration for the AI-heavy parts of this project. |
| Node.js/TypeScript backend | Weaker typing for ML/data work; Python is the ecosystem of choice for the intelligence layers. |
| Spring Boot | Heavyweight; Java tooling adds complexity without benefit here. |
