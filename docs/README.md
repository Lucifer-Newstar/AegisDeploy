# AegisDeploy — Documentation

> **The navigation hub for all project documentation.**
> If you are looking for *anything* about AegisDeploy, start here.
>
> Maintainer: Navin Jairam M (Team Lead). Updated whenever the structure changes
> (rule 2: the docs folder stays clean).

---

## 1. Document Tree

```text
docs/
├── README.md                    ← you are here (index & reading order)
│
├── project/                     ← WHAT & WHY (the big picture)
│   ├── proposal.md              ← the original project proposal (full text)
│   └── roadmap.md               ← milestone-level roadmap
│
├── contracts/                   ← P2 API contracts (OpenAPI, freeze 2026-09-08)
│   ├── README.md                ← conventions + mock-server + CORS policy
│   ├── registry-service.yaml    ← A2 registry + health (:8101)
│   ├── deployments-service.yaml ← DI-1 deploy tracker (:8701)
│   └── aegisshop-v1.yaml        ← catalog/cart/order/payment (9001–9004)
│
├── planning/                    ← HOW WE DECIDE (development-phase planning)
│   ├── README.md                ← planning index + decision log
│   ├── features.md              ← locked feature scope (A1–A12, B, C, D, E)
│   ├── product-vision.md        ← how the final product looks & behaves
│   ├── phases.md                ← phase plan: gates, non-disruption, integration
│   ├── timeline.md              ← 8–10 month calendar, member assignments
│   ├── p2-kickoff.md            ← P2 kickoff: tracks, contracts-first, gate
│   ├── p2-sync-pack.md          ← team sync agenda + operating rhythm
│   └── integration-edge-cases.md← cross-member risk register (Team Lead)
│
├── team/                        ← WHO & HOW WE WORK
│   ├── team-structure.md        ← members, roles, ownership matrix
│   └── working-rules.md         ← project rules + git conventions
│
├── members/                     ← PER-MEMBER PLANNING (each member's folder)
│   ├── README.md                ← member index + cross-member dependencies
│   ├── dhanush-frontend/        ← Member 1 — frontend
│   ├── jegatheesan-backend/     ← Member 2 — backend
│   ├── gokul-devops/            ← Member 3 — DevOps / cloud
│   └── navin-lead/              ← Member 4 — team lead / SRE / AI-SRE
│
├── architecture/                ← SYSTEM DESIGN (how the platform works)
│   ├── system-architecture.md   ← components, responsibilities, data flows
│   ├── deployment-intelligence.md ← DI tier: deployment risk, correlation, rollback, CFR
│   ├── autonomy-model.md        ← Levels 1–5 autonomy, policy engine, safety
│   ├── telemetry-model.md       ← unified telemetry/event envelope contract
│   ├── uml/                     ← the 14-diagram UML set (Mermaid, GitHub-rendered)
│   └── adr/                     ← Architecture Decision Records (ADRs)
│
├── development/                 ← HOW TO BUILD (engineering conventions)
│   ├── contributing.md          ← contribution workflow + conventions
│   ├── local-setup.md           ← one-time machine setup + env variables
│   └── tech-stack.md            ← selected technology stack & rationale
│
└── operations/                  ← HOW TO RUN & MEASURE
    └── evaluation.md            ← SRE/ML/automation metrics & protocol
```

## 2. Index by Topic

| Topic | Go to |
|---|---|
| What is this project? | [project/proposal.md](project/proposal.md) |
| What are we building? (locked scope) | [planning/features.md](planning/features.md) |
| What does the final product look like? | [planning/product-vision.md](planning/product-vision.md) |
| What are the phases & gates? | [planning/phases.md](planning/phases.md) |
| What is the schedule? | [planning/timeline.md](planning/timeline.md) |
| Who is on the team & who owns what? | [team/team-structure.md](team/team-structure.md) |
| My role's phase plan | [members/](members/) — your folder |
| How the platform works | [architecture/system-architecture.md](architecture/system-architecture.md) |
| How autonomy/remediation works | [architecture/autonomy-model.md](architecture/autonomy-model.md) |
| The telemetry/event contract | [architecture/telemetry-model.md](architecture/telemetry-model.md) |
| P2 API contracts (OpenAPI) | [contracts/](contracts/) |
| Why we chose the stack | [development/tech-stack.md](development/tech-stack.md) |
| How to contribute | [development/contributing.md](development/contributing.md) |
| Machine setup + env vars | [development/local-setup.md](development/local-setup.md) |
| How we evaluate success | [operations/evaluation.md](operations/evaluation.md) |
| Decision history | [planning/README.md](planning/README.md) §2 · [architecture/adr/](architecture/adr/) |

## 3. Reading Order for a New Member

1. **Start here** — get the map.
2. **team/** — who we are and how we work (rules first!).
3. **planning/features.md** — what we are building (scope is locked — read before writing code).
4. **planning/phases.md + timeline.md** — when things happen and what "done" means per phase.
5. **members/<your-folder>/** — your personal phase plan.
6. **architecture/** — how the system is designed (read before touching interfaces).
7. **development/** — stack + conventions before your first commit.
8. **operations/** — how the whole thing will be judged.

## 4. Housekeeping Rules (rule 2 in practice)

- **One purpose per file** — every document answers one question; new topics get a new
  file in the right folder.
- **No orphans** — every file is reachable from this index; when you add a file, add its
  row to §2.
- **Living documents** — planning docs evolve; changes are logged in the decision log
  (planning/README.md §2), never silently.
- **ADRs for architecture** — interface/stack changes require an ADR
  (see [development/contributing.md](development/contributing.md)).
- **Path discipline** — links inside docs use relative paths; repo-root paths are
  written as `docs/<folder>/...` in code comments/README.
