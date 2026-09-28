# Member Plans

Each member folder contains two documents:

- **README.md — role and interfaces:** responsibility, owned repository areas, and contracts provided or consumed.
- **phase-plan.md — delivery commitment:** that member's work by phase, dependencies, handoff, and completion check.

Team-level ownership is in [team-structure.md](../team/team-structure.md). Shared scope is in [features.md](../planning/features.md); phase gates are in [phases.md](../planning/phases.md).

---

## 1. Member index

| Member | Role | Folder | Main areas |
|---|---|---|---|
| **Dhanush Kumar S** | Frontend developer | [dhanush-frontend](dhanush-frontend/) | Console, design system, charts, AI/approval UI, demo materials |
| **Jegatheesan K** | Backend developer | [jegatheesan-backend](jegatheesan-backend/) | APIs, AegisShop, incidents, approvals, verification, persistence |
| **Gokul J** | DevOps / cloud engineer | [gokul-devops](gokul-devops/) | Observability, containers, CI/CD, Kubernetes, chaoslab, executors |
| **Navin Jairam M** | Team lead / SRE / AI-SRE | [navin-lead](navin-lead/) | Architecture, shared contracts, AI-SRE, evaluation, integration |

## 2. Main handoffs

```text
Navin: shared telemetry/events ──▶ backend + platform tracks (P2)
Navin: anomaly events ────────────▶ Jegatheesan's incident manager (P3)
Jegatheesan: service/incident APIs ▶ Dhanush's console (P2–P5)
Gokul: observability + query tools ▶ all tracks (P2–P4)
Navin: action policies ───────────▶ Jegatheesan + Gokul (P5)
Gokul: cluster + chaoslab ────────▶ all tracks (P7)
All members: integrated result ───▶ phase gate review (each phase)
```

Use the contracts and mocks described in [phases.md §4](../planning/phases.md#4-non-blocking-work-and-handoffs) while an implementation is pending. Do not silently change an interface used by another member.

## 3. Keeping plans current

1. Check the shared phase gate and feature acceptance criteria before starting work.
2. In your `phase-plan.md`, keep each phase's deliverable, dependency, handoff, and completion check current.
3. Update your README when role ownership or interfaces change; tell the Team Lead.
4. Record scope/interface decisions in the decision log. Implementation lives in code, not in this folder.
