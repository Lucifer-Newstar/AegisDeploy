# Working Rules

> The non-negotiable rules of the AegisDeploy project, plus the git conventions the
> whole team must follow. Every member must read and follow this document.
>
> Maintainer: Member 4 (Team Lead).
>
> *Note: rules that govern only the lead's AI assistant (its private operating
> instructions) are intentionally **not** stored in this repository — they live
> outside the repo and do not concern team members.*

---

## 1. The Project Rules

| # | Rule | What it means in practice |
|---|------|---------------------------|
| 1 | **Document everything** | Every development step (design, code, config, experiments, decisions) is documented in `docs/` as part of the work — never as an afterthought. |
| 2 | **Keep the docs folder clean** | `docs/` is organized into sub-folders (and sub-sub-folders where needed). Every file has a purpose and a home; no loose/stale files; index updated when structure changes. |
| 3 | **Comment every codebase** | Every source file carries clear comments: module purpose, function docstrings, and notes on non-obvious logic — so future readers can find functions, read the flow, and edit safely. |
| 4 | **Good commit history** | Small, logical, well-messaged commits; commit at every completed step (see §2). |
| 5 | **Final-year project standard** | Academic rigor: traceable design, documented methodology, reproducible evaluation, professional presentation quality. |
| 6 | **Never break these rules** | These rules are permanent and override convenience. |

---

## 2. Commit Conventions (Conventional Commits)

Format: `<type>(<scope>): <subject>`

| Type | Use for |
|---|---|
| `feat` | new feature/component |
| `fix` | bug fix |
| `docs` | documentation only |
| `refactor` | code change with no behavior change |
| `test` | tests only |
| `ci` | CI/CD changes (`.github/`) |
| `chore` | tooling, deps, housekeeping |

**Scopes** (match repository areas): `backend`, `frontend`, `ml`, `ai`, `chaoslab`,
`infra`, `iac`, `ci`, `docs(<sub>)` (e.g. `docs(team)`, `docs(architecture)`,
`docs(adr)`), `meta` (root files).

**Examples:**

```text
feat(backend): add telemetry ingestion endpoint
fix(frontend): render incident timeline in chronological order
docs(adr): add ADR-0006 for approval workflow
ci: pin actions to commit SHAs
```

**Commit rules:**

- One logical change per commit; no unrelated edits in the same commit.
- Subject ≤ 72 chars, imperative mood, no trailing period.
- Body explains **why** (context) and **what**, not how.
- Always commit after each completed step (rule 4).

---

## 3. Branch Workflow

- `main` is always deployable — never commit broken work to it.
- Work happens on short-lived feature branches: `feat/<member>-<area>-<topic>`
  (e.g. `feat/member2-backend-ingestion`).
- Merge via **pull request** with a description that references docs/issues.
- Architecture-impacting PRs are reviewed by Member 4 (and must include an ADR if
  the change is architectural).
- Branches are deleted after merge; history stays linear-ish and readable
  (squash-merge for noisy branches, regular merge for meaningful units).

---

## 4. Definition of Done (per task)

- [ ] Code/config/docs written with comments (rule 3)
- [ ] Docs updated in the right `docs/` sub-folder (rules 1, 2)
- [ ] Committed with a Conventional Commit message (rule 4)
- [ ] CI green (when applicable)
- [ ] No unrelated changes included
- [ ] Lead informed; scope confirmed before starting
