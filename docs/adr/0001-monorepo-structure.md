# ADR-0001: Monorepo Structure

- **Status:** Accepted
- **Date:** 2026-08-31
- **Deciders:** Navin Jairam, Arena Agent

## Context

AegisSRE spans frontend, backend services, ML pipeline, AI reasoning, IaC, observability
configs, and a chaos lab. We need a repository layout that keeps related code close,
allows independent CI for components, and stays navigable for a single engineer
(and future collaborators) without polyrepo overhead.

## Decision

Use a **single monorepo** with component directories:

```text
backend/      Python/FastAPI services (gateway, platform, incident)
frontend/     Next.js dashboard
ml/           anomaly detection pipeline
ai/           LLM reasoning, RAG, tool-calling
chaoslab/     failure injection experiments
infra/        docker, k8s, observability configs (shared by runtimes)
iac/          Terraform (cloud, later)
docs/         architecture, ADRs, telemetry model, evaluation
scripts/      cross-cutting dev utilities
```

All Docker Compose and K8s deployments reference `infra/` configs so local and cluster
behavior stays identical ("Compose now, K8s-ready").

## Consequences

### Positive

- Single `git clone` + `docker compose up` gets a full dev environment.
- Shared configs (`infra/`) can't drift between Compose and K8s.
- Atomic commits across backend + frontend + docs for a single feature.
- CI can run component-specific jobs from one pipeline.

### Negative / Trade-offs

- Repo grows large; mitigated by strict directory ownership rules (each component
  owns its subtree) and per-component CI jobs.
- Not all tools treat monorepos natively; GitHub Actions handles this well.

## Alternatives Considered

| Option | Why rejected |
|---|---|
| Polyrepo (one repo per service) | Coordination overhead, config drift, harder local dev; no external contributors to justify it yet. |
| Single flat repo | Unnavigable as scope grows (10+ components planned). |
