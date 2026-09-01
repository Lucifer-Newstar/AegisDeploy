# Member Folders

> One designated folder per team member. Each folder contains:
>
> - **README.md** — who the member is, their role, the repository areas they own,
>   and the contracts they consume/provide.
> - **phase-plan.md** — the member's *own view* of the phases: what they deliver in
>   each phase, what they depend on, what they hand over at integration, and what
>   "done" means for their track.
>
> Maintained by each member; reviewed by the Team Lead. Team-level roles & ownership:
> [docs/team/team-structure.md](../team/team-structure.md).

---

## 1. Member Index

| Member | Role | Folder | Primary tracks |
|---|---|---|---|
| **Dhanush Kumar S** | Frontend Developer | [dhanush-frontend/](dhanush-frontend/) | Console (8 pages incl. deployments), design system, visualization, AI/approval UIs, demo video |
| **Jegatheesan K** | Backend Developer | [jegatheesan-backend/](jegatheesan-backend/) | APIs, AegisShop backend, incident manager, approvals/verification services, DB |
| **Gokul J** | DevOps / Cloud Engineer | [gokul-devops/](gokul-devops/) | Observability infra, Docker/CI-CD, Kubernetes, chaoslab, executors infra |
| **Navin Jairam M** | Team Lead — SRE / DevOps / Architecture | [navin-lead/](navin-lead/) | Architecture, contracts, AI-SRE (anomaly, RCA, RAG, policy), evaluation, integration |

## 2. Quick Dependency Map

```text
Navin ──contracts/envelope──▶ everyone (P2 start)
Navin ──anomaly events──────▶ Jega (P3)     Jega ──incident APIs──▶ Dhanush (P3 end)
Navin ──RCA/RAG/Ask engine──▶ Dhanush (P4)  Jega ──approval APIs──▶ Dhanush (P5)
Gokul ──observability stack──▶ everyone      Gokul ──executors─────▶ A6/A8 (P5)
Gokul ──K8s + chaoslab──────▶ everyone (P7)  All  ──integration────▶ Navin (gate review)
```

> **Rule:** nobody blocks. Every arrow above has a mock/stub alternative until the
> real contract lands (see [docs/planning/phases.md](../planning/phases.md) §4).

## 3. How to Use Your Folder

1. Read `docs/planning/phases.md` first — your phase-plan mirrors the phases there.
2. Keep your `phase-plan.md` **updated as you work** — it is your commitment for each
   phase and the input to the gate review.
3. Update your README when your role/ownership changes (tell the Team Lead).
4. Everything here is docs-only — implementation lives in your code folders
   (`frontend/`, `backend/`, `infra/`, `ml/`+`ai/`+`chaoslab/`).
