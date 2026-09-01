# P2 Status Tracker (Team Lead view)

> **Owner:** Navin Jairam · **Updated:** 2026-09-01 · **Source:** pending-work
> review (24 items). Checked items move to the decision log / PRs; this file
> is the lead's board through the P2 gate (2026-10-31).

## A. Environment setup (complete the env)

- [ ] A1 — Your machine: Python 3.12 + uv + Docker Desktop (Compose v2) + Make + Git (Node 22 optional)
- [ ] A2 — SSH key / PAT for GitHub auth
- [ ] A3 — Download workspace folder (with `.git/`, 43 commits) → place locally
- [ ] A4 — Re-add what `.git/config` doesn't carry: `git remote add origin <AegisDeploy URL>` + `git config user.name/email`
- [ ] A5 — venv + editable installs (telemetry, eventbus, _template, catalog-service `[dev]`)
- [ ] A6 — `cp .env.example .env`
- [ ] A7 — `make infra-up` + verify: `curl localhost:9001/products`, Grafana `admin/aegis`, Prometheus target UP, pytest 27 green
- [ ] A8 — **Rename GitHub repo** `AegisSRE` → `AegisDeploy` (Settings → General)
- [ ] A9 — `git push -u origin main`
- [ ] A10 — Invite team collaborators: Jega, Gokul, Dhanush
- [ ] A11 — Members' machine setup per `docs/development/local-setup.md`
- [ ] A12 — Dhanush: Node 22 + frontend scaffold setup (his P2 branch)
- [ ] A13 — Jega: DB tooling (Alembic/migrations with first models)
- [ ] A14 — Gokul: Docker tooling + compose additions

## B. Getting it to the team

- [ ] B1 — Send kickoff-guide pre-reads to members (`docs/members/navin-lead/kickoff-guide.md` §1)
- [ ] B2 — **Kickoff sync** (~60 min): skeleton demo → contracts walk → close D1–D9 → track commitments + branch names
- [ ] B3 — Record D1–D9 in the planning decision log (same day — "no decision leaves the room unrecorded")
- [ ] B4 — **Freeze contracts 2026-09-08** (after: changes only via contract PR)
- [ ] B5 — Members cut first branches `feat/<member>-<area>-<topic>`; PRs via template + CI

## C. Navin's lead track (P2)

- [x] C1 — **Port/naming register** consolidation (`docs/architecture/port-register.md` — done 2026-09-01)
- [ ] C2 — Contract freeze review with Jega (D1–D9 incl. D8/D9 coupling decisions, edge case #15)
- [ ] C3 — Weekly syncs (Mon, 30 min) through Oct: status round → register walk → demo-of-week → decisions
- [ ] C4 — Integration checkpoint rehearsal **2026-10-15** (one command: Grafana + console)
- [ ] C5 — P2 gate review **2026-10-31** (4 criteria + DI-1 events recorded)

## D. Done baseline (not pending)

- [x] D1 — M1/P1 foundation complete
- [x] D2 — Walking skeleton: libs (telemetry v0.2, eventbus), template, catalog slice, compose, CI, K8s base
- [x] D3 — CI tuned: enforced k8s-lint, full docs links, real docker-build, drift check live (edge case #8)
- [x] D4 — P2 OpenAPI contracts drafted (registry :8101, deployments/DI-1 :8701, AegisShop v1 per-service)
- [x] D5 — Event catalogue v1 (telemetry-model §3.5) + deployment state machine
- [x] D6 — Integration edge-case register (15 rows) + PR template + CORS policy
- [x] D7 — Sync pack (kickoff agenda, D1–D9, weekly format, demo-of-week)
- [x] D8 — Local setup guide + env var reference
- [x] D9 — Handover zip removed (folder with `.git/` is the deliverable)
- [x] D10 — Sync prep: team kickoff guide consolidated in `docs/members/navin-lead/kickoff-guide.md` (agenda + demo script + D1–D9 draft + weekly rhythm) — prepped 2026-09-01

## Calendar (this stage)

| Date | Event |
|---|---|
| 2026-09-01 | Skeleton + contracts + CI + sync pack done (43 commits) |
| before 09-08 | Push · repo rename · kickoff sync · D1–D9 recorded |
| **2026-09-08** | Contracts freeze |
| Mon weekly | 30-min sync (sync pack format) |
| **2026-10-15** | Integration checkpoint rehearsal |
| **2026-10-31** | P2 gate review |
