# Dhanush Kumar S — Frontend Developer

> **Member 1** — Frontend track.

## Role

Build the AegisDeploy Console: the SRE team's single pane of glass and the face of the
final-year demonstration.

## Primary responsibilities

- Frontend application (Next.js / TypeScript)
- Dashboard & UI/UX design system (dark observability theme)
- System visualization (health grids, charts, anomaly bands)
- Incident visualization (timeline, evidence, AI reasoning panels)
- AI interaction interfaces ("Ask Aegis" chat, approvals)
- **Deployments page (DI):** deploy timeline, risk panel, bad-rollout banner, rollback view, canary view, CFR analytics (DI-1…DI-7)

## Repo areas owned

- `frontend/` (all)
- `docs/members/dhanush-frontend/` (this folder)

## Contracts I consume

| Contract | Provided by | Available |
|---|---|---|
| API schema / OpenAPI spec | Jegatheesan (backend) + Navin | P2 (contracts-first) |
| Telemetry envelope | Navin | P2 |
| Incident APIs | Jegatheesan | P3 end |
| RCA / evidence APIs | Navin | P4 |
| Ask Aegis engine API | Navin | P4 end |
| Approval workflow APIs | Jegatheesan | P5 |
| **Deploy / risk / CFR APIs (DI-1, DI-2, DI-7)** | Jegatheesan + Navin | P2/P4/P6 |

> Until each API lands, I develop against the **mock server** generated from the
> OpenAPI contract — my track never blocks (phases.md §4).

## My commitments

- Pages are demo-ready at the end of each phase they appear in.
- Design system tokens documented in the frontend README (rule 3: comments in code).
- Demo video for P8.
