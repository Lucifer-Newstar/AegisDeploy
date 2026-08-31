# UML Diagrams — Index

> The complete **14-diagram UML documentation set** for AegisSRE (UML 2.5).
> All diagrams are authored in **Mermaid** and render natively on GitHub — edit the
> text, view the diagram, review via PR.
>
> Process: one diagram per reviewed exchange — the Team Lead (or the agent on his
> behalf) asks the questions needed for the diagram, the lead answers, the diagram is
> created and committed. Every diagram carries comments (`%%`) and an explanation
> section below it.
>
> Maintainer: Navin Jairam M (Team Lead).

---

## 1. Diagram Index (14)

| # | Diagram | Type | File(s) | Status |
|---|---------|------|---------|--------|
| 1 | Use Case | Behavioral | [use-case-platform.md](use-case-platform.md) · [use-case-aegisshop.md](use-case-aegisshop.md) | ✅ |
| 2 | Class | Structural | [class-diagram-platform.md](class-diagram-platform.md) · [class-diagram-aegisshop.md](class-diagram-aegisshop.md) | ✅ |
| 3 | Object | Structural | [object-diagram.md](object-diagram.md) | ✅ |
| 4 | Package | Structural | [package-diagram-platform.md](package-diagram-platform.md) · [package-diagram-aegisshop.md](package-diagram-aegisshop.md) · [package-diagram-infraops.md](package-diagram-infraops.md) | ✅ |
| 5 | Component | Structural | [component-diagram.md](component-diagram.md) | ✅ |
| 6 | Composite Structure | Structural | `composite-structure-diagram.md` | ⏳ planned |
| 7 | Deployment | Structural | `deployment-diagram.md` | ⏳ planned |
| 8 | Profile | Structural | `profile-diagram.md` | ⏳ planned |
| 9 | Activity | Behavioral | `activity-diagram.md` | ⏳ planned |
| 10 | State Machine | Behavioral | `state-machine-diagram.md` | ⏳ planned |
| 11 | Sequence | Behavioral | `sequence-diagram.md` | ⏳ planned |
| 12 | Communication | Behavioral | `communication-diagram.md` | ⏳ planned |
| 13 | Timing | Behavioral | `timing-diagram.md` | ⏳ planned |
| 14 | Interaction Overview | Behavioral | `interaction-overview-diagram.md` | ⏳ planned |

> Note: diagram #1 (Use Case) is split into two files — one for the AegisSRE platform
> and one for the AegisShop demo application (decision 2026-08-31).
> Planned files are shown as plain text and become links when each diagram lands
> (keeps the docs link check green at every commit).

## 2. Conventions

| Rule | Detail |
|---|---|
| Format | Mermaid (`flowchart` / `sequenceDiagram` / `stateDiagram-v2` / `classDiagram` as appropriate), one mermaid block per file |
| Comments | `%%` comments inside the diagram; explanation tables below it |
| Naming | `kebab-case` files matching the index above |
| Scope discipline | Diagrams describe the **locked scope** (features.md); new behavior must first be decided |
| Rendering | GitHub renders mermaid natively; also viewable via mermaid.live (paste the block) |
| Review | Each diagram is committed separately with a conventional message (`docs(architecture): add <diagram>`) |

## 3. Reading Order

1. **Use Case** — what the system does for whom (start here)
2. **Class** — the static structure
3. **Object** — a concrete snapshot
4. **Package** — module organization
5. **Component** — deployable units
6. **Composite Structure** — internal collaboration
7. **Deployment** — where things run
8. **Profile** — UML extensions used
9. **Activity** — workflows
10. **State Machine** — lifecycle states (incident!)
11. **Sequence** — key interactions
12. **Communication** — same as sequence, structure-focused
13. **Timing** — time constraints
14. **Interaction Overview** — the big picture of interactions
