# Pull Request Checklist (AegisDeploy)

> Every PR into `main` must satisfy the Definition of Done
> ([working-rules.md](docs/team/working-rules.md), [contributing.md](docs/development/contributing.md)).
> CI enforces what it can; the Team Lead reviews the rest.

## Title & branch

- [ ] Conventional Commit: `feat|fix|docs|chore(<scope>): <summary>` (scopes: backend, frontend, ml, ai, chaoslab, demoapp, infra, ci, meta, docs(architecture|planning|adr))
- [ ] Branch: `feat/<member>-<area>-<topic>`

## Quality gates (must be green)

- [ ] CI: `yaml-and-compose`, `k8s-lint`, `docs`, `python-quality`
- [ ] Tests added/updated for new behavior (pytest)
- [ ] `ruff check backend demoapp` and `mypy` (strict) clean

## Contracts & conventions (Team Lead review)

- [ ] Uses the shared libs (`telemetry`, `eventbus`) — **no bespoke event shapes**
- [ ] New event type? → **event catalogue updated** (`docs/architecture/telemetry-model.md` §3.5)
- [ ] New/changed API? → **OpenAPI contract in `docs/contracts/`** (or contract PR first — freeze exceptions only via contract PR)
- [ ] New service? → **row added to `docs/contracts/manifest.json`** (drift check)
- [ ] Envelope changes? → additive-only; defaults for new fields
- [ ] Env vars via `config.py` + compose/K8s **parity** (ADR-0005) — same names in both runtimes
- [ ] New service? → compose service + Kustomize base + `python-quality` CI entry + **port register** updated

## Docs & demo

- [ ] Member phase-plan / integration edge-case register updated if behavior changed
- [ ] PR description notes mock-server regeneration for the frontend (if contracts changed)
- [ ] No `.env` / secrets committed (dev creds stay dev-only)

---

*Additions to this checklist go through the Team Lead — it is the shared
Definition of Done for every member.*
