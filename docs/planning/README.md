# Planning

> Home of the **development-phase planning** documents for AegisSRE.
> Everything here is the *decision record* of the project: what we build, how the
> final product should look, and when we build it.
>
> These documents are living files — updated whenever a decision changes, with the
> change logged in §2 below.

---

## 1. Index

| Document | Purpose |
|---|---|
| [features.md](features.md) | The locked feature scope — what is in, what is out, who owns what, acceptance criteria. |
| [product-vision.md](product-vision.md) | How the final product should look and behave — console concept, pages, design language, demo story. |
| [timeline.md](timeline.md) | The 8–10 month development calendar, member assignments per phase, milestones, risks. |

Related: [docs/roadmap.md](../roadmap.md) is the milestone-level roadmap (kept in sync with
these documents); [docs/team/](../team/) defines who is on the team.

---

## 2. Decision Log

| Date | Decision | Decider | Recorded in |
|---|---|---|---|
| 2026-08-31 | Project objective confirmed (research question): AI-assisted SRE platform reducing MTTD/MTTR, accurate RCA, safe autonomous remediation. | Navin Jairam (Team Lead) | [proposal.md](../proposal.md) |
| 2026-08-31 | Runway: **8–10 months** (started Aug 2026 → delivery window Apr–Jun 2027). | Navin Jairam | [timeline.md](timeline.md) |
| 2026-08-31 | **Scope locked:** All Tier A (core loop) + B1 RAG + B2 Ask Aegis + C1/C3/C4/C5 + D1/D5/D6 + E2/E4. Explicit cuts: B3, B4, B6, C2, C6, D2, D3, D4, E3, E5 (B3 = optional buffer stretch). | Navin Jairam (on recommendation) | [features.md](features.md) |
| 2026-08-31 | **Demo subject:** build our **own demo microservices application** (fully controlled faults) rather than adapting an existing one. | Navin Jairam (on recommendation) | [features.md](features.md) §5 |

*New decisions are appended; nothing is silently edited.*
