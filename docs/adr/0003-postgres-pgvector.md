# ADR-0003: PostgreSQL + pgvector as Primary Store and Vector DB

- **Status:** Accepted
- **Date:** 2026-08-31
- **Deciders:** Navin Jairam, Arena Agent

## Context

The control plane needs a relational core (services, incidents, deployments, audit
logs, evidence) and, later, a vector store for RAG over runbooks/past incidents/
failure patterns. Running two storage systems (e.g., Postgres + Qdrant/Weaviate)
doubles operational surface area for little benefit at this stage.

## Decision

**PostgreSQL 16** is the primary relational store, and **pgvector** (installed as an
extension on the same instance) is the RAG vector store. Redis remains the cache +
event layer (ADR-0004), Prometheus/Loki/Tempo remain the telemetry stores — Postgres
does *not* absorb metrics/logs/traces.

## Consequences

### Positive

- One database to operate, back up, and learn; huge ecosystem and K8s maturity.
- pgvector supports HNSW/IVFFlat indexes, distance operators, and hybrid
  vector + relational queries (e.g., "past incidents with similar root cause in same
  service") in one query — ideal for RCA.
- JSONB columns handle semi-structured evidence and event payloads.

### Negative / Trade-offs

- pgvector is not as specialized as dedicated vector DBs at very large scale;
  irrelevant at this project's corpus size.
- Migration between environments (local Compose vs cluster) must include the extension;
  handled by pinned images and init scripts.

## Alternatives Considered

| Option | Why rejected |
|---|---|
| Dedicated vector DB (Qdrant, Weaviate, Milvus) | Extra service to run; no hybrid relational advantage; overkill for the corpus size. |
| MongoDB | Schema flexibility but weaker relational integrity for incidents/audit; JSONB covers our needs. |
| SQLite | Good for unit tests; not for a multi-service control plane. |
