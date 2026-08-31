# Contributing

> **Read first:** [docs/team/team-structure.md](team/team-structure.md) — who owns what.
> [docs/team/working-rules.md](team/working-rules.md) — the project rules and the git
> conventions (Conventional Commits, branch + PR workflow, Definition of Done).

## Workflow Summary

1. **Branches** — work on `feat/<member>-<area>-<topic>`; merge to `main` via pull
   request. `main` is always deployable.
2. **Commits** — Conventional Commits with scopes
   (`feat(backend): ...`, `docs(architecture): ...`). See `working-rules.md` §2.
3. **PRs** — small, reviewable; CI must pass; architecture changes need an ADR reviewed
   by the Team Lead.
4. **ADRs** — any architectural or tech-stack decision requires an ADR in
   `docs/architecture/adr/` (copy `adr-template.md`).

## Conventions

- **Python (backend, ml, ai):** 3.12, `ruff` + `mypy`, type hints required, Pydantic
  models for all schemas, comments per working-rules rule 3.
- **TypeScript (frontend):** strict mode, `prettier` + `eslint`.
- **YAML (infra, ci):** 2-space indent, explicit image tags/versions in Compose and K8s
  manifests; every Compose service has a healthcheck.
- **Secrets:** never commit; use `.env` locally, secrets managers in K8s.
- **Telemetry:** all events conform to the envelope in
  `docs/architecture/telemetry-model.md` — no bespoke event shapes.

## Definition of Done

See `docs/team/working-rules.md` §4.
