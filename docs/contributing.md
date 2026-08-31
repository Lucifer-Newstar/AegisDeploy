# Contributing

## Workflow

1. **Branches** — work on feature branches (`feat/<name>`, `fix/<name>`, `docs/<name>`);
   `main` is always deployable.
2. **Commits** — conventional commits (`feat:`, `fix:`, `docs:`, `chore:`, `refactor:`).
3. **PRs** — small, reviewable PRs; CI must pass; update docs/ADRs when behavior or
   architecture changes.
4. **ADRs** — any architectural decision or tech-stack change requires an ADR in
   `docs/adr/` (copy `adr-template.md`).

## Conventions

- Python: 3.12, `ruff` + `mypy`, type hints required, `pydantic` models for all schemas.
- TypeScript: strict mode, `prettier` + `eslint`.
- YAML: 2-space indent, explicit tags/versions in compose and K8s manifests.
- Secrets: never commit; use `.env` locally and secrets managers in K8s.
- Telemetry: all events conform to the envelope in `docs/telemetry-model.md`.

## Definition of Done (per milestone feature)

- [ ] Code merged to `main` with passing CI
- [ ] Unit tests for new logic
- [ ] Telemetry envelope respected (no bespoke event shapes)
- [ ] Docs/ADRs updated where relevant
- [ ] Audit events for any new action type
