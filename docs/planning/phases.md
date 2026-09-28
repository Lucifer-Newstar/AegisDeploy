# Development Phases & Integration Gates

> **Purpose:** show the order of work and the proof required to finish each phase. Feature definitions and owners are in [features.md](features.md); dates are in [timeline.md](timeline.md); each member's assignments are in their [member plan](../members/README.md).
>
> A phase is complete only when its gate and integration checkpoint pass, tests/CI are appropriate, and documentation is updated. Dates are targets; gates are the completion rule.

---

## 1. How phase planning works

- **Phase:** a time-boxed delivery stage (P1–P8). Do not confuse these labels with feature priority tiers P0/P1.
- **Track:** one member's work inside a phase. Members can build in parallel against agreed contracts and mocks.
- **Gate:** the minimum working result required to finish a phase.
- **Integration checkpoint:** an end-to-end demonstration of that result with the tracks connected.
- **Feature IDs:** refer to [features.md](features.md). `D1` is Kubernetes; `DI-1` is deployment tracking.

### Working rules

1. Commit shared API, event, and telemetry contracts before consumers implement against them.
2. Use mock servers, test producers, and seeded fixtures when a dependency is not ready.
3. Reserve the final 2–3 days of a phase for fixes, integration, and gate review; do not add scope then.
4. Shared Compose/infra changes go through PRs. A passed gate and a decision-log entry open the next phase.

---

## 2. Phase summary

| Phase | Focus | Gate result | Integration checkpoint |
|---|---|---|---|
| **P1 · Foundation** ✅ | Repo, documentation, base stack, CI | Stack starts healthy; CI and docs checks pass. | Passed 2026-08-31. |
| **P2 · Observability + AegisShop v1** | A1, A2, DI-1, app v1, console scaffold | App telemetry is queryable; registry/health and deploy history work; console scaffold runs on mocks. | One command starts the app/platform; services appear in Grafana and console. |
| **P3 · Detection + incidents** | A3, A4, DI-4 base | Injected fault produces anomaly and incident with timeline; target detection metrics pass. | Fault-to-incident demo. |
| **P4 · AI reasoning** | A5, B1, B2, DI-2, DI-3 | Cited RCA and read-only Q&A work; faulty deployment can be correlated. | Live incident shows evidence and reasoning. |
| **P5 · Remediation + autonomy** | A6–A9, DI-5 | Approval and safe-auto paths execute within policy and verify recovery. | Demonstrate one approval action and one eligible auto action. |
| **P6 · Product completion (parallel)** | C1, C3–C5, D5–D6, DI-7 dashboard | Eight console pages use live APIs; CI/CD, SLO, and CFR views work. | Live-data product walkthrough. |
| **P7 · Kubernetes + chaos lab** | D1, A11, DI-6 | Platform/app run on kind; ten faults produce ground truth; canary is analyzed. | Cluster demo with fault injection. |
| **P8 · Evaluation + report** | A12, E2, DI-7 evaluation | Reproducible evaluation report and demo materials are ready. | Final thesis demonstration. |

P6 overlaps P5 in the calendar; it is a parallel product track, not a prerequisite that blocks the P5 gate.

---

## 3. Phase assignments and gates

### P1 · Foundation — passed
- **Work:** repo structure, ADRs, Compose observability stack, CI, and planning docs.
- **Gate:** stack healthy, CI green, docs indexed.
- **Result:** passed 2026-08-31.

### P2 · Observability + AegisShop v1
- **Goal:** make the demo app observable and give every track a usable starting point.
- **Tracks:**
  - **Gokul:** A1 pipeline, Grafana dashboards, Compose wiring.
  - **Jegatheesan:** A2 registry/health, AegisShop backend, DI-1 history API.
  - **Navin:** shared telemetry/event design, contract coordination, integration protocol.
  - **Dhanush:** console scaffold and design system using mock data.
- **Gate:** AegisShop metrics/logs/traces are queryable; registry and health API respond; deploy events/history are recorded; console scaffold runs on mocks.
- **Checkpoint:** start app and platform together; verify services in Grafana and console.

### P3 · Detection + incidents
- **Goal:** turn a controlled fault into a tracked incident.
- **Tracks:** Navin—A3 detector and tuning; Jegatheesan—A4 incident state machine/timeline; Gokul—metric plumbing and fault validation; Dhanush—service/incident views with anomaly context.
- **DI work:** establish the DI-4 deployment evaluation window.
- **Gate:** CPU/latency test fault produces `anomaly.score`, then an incident within 30 seconds; precision/recall/F1 meet A3 thresholds on the agreed validation set.
- **Checkpoint:** run a fault-to-incident demo from the test hooks.

### P4 · AI reasoning
- **Goal:** explain incidents using traceable evidence.
- **Tracks:** Navin—A5, B1, B2, DI-2, DI-3; Jegatheesan—evidence/incident APIs and deploy history; Gokul—read-only query proxies; Dhanush—incident reasoning and Ask Aegis UI.
- **Gate:** top-1 RCA accuracy ≥70%; every hypothesis cites evidence; Ask Aegis answers a health question with citations; DI-3 top-1 accuracy ≥0.8 on faulty-deploy tests.
- **Checkpoint:** inspect a live incident in the UI and ask a question answered from live evidence.

### P5 · Remediation + autonomy
- **Goal:** execute permitted actions and prove recovery without bypassing safeguards.
- **Tracks:** Jegatheesan—A6 implementation, A7 approval API, A9 verification API; Navin—policy/risk matrix, A8 mode and kill switch, verification logic, DI-5 policy; Gokul—scoped restart/rollback/scale executors; Dhanush—approval UI and autonomy indicator.
- **Gate:** approve → execute → verify → close works; only allowed low-risk actions auto-run; low-risk rollback restores service; kill switch is immediate; safety violations = 0.
- **Checkpoint:** show one human-approved and one policy-approved automatic action end-to-end.

### P6 · Product completion (parallel)
- **Goal:** finish the console and operational views on real APIs while P5 proceeds.
- **Tracks:** Dhanush—C1 eight pages, C3–C5; Gokul—D5 pipeline, D6 SLOs, DI-7 dashboards; Jegatheesan—API polish/client generation; Navin—SLO definitions and integration coordination.
- **Gate:** all eight pages use live data; CI/CD is green; SLO and burn-rate views work; CFR dashboard is live.
- **Checkpoint:** walkthrough of the product using live data.

### P7 · Kubernetes + chaos lab
- **Goal:** run the integrated platform in a reproducible cluster and validate controlled experiments.
- **Tracks:** Gokul—D1 kind/Kustomize, A11 implementation, DI-6; Navin—fault specs/manifests/ground truth; Jegatheesan—AegisShop fault hooks and hardening; Dhanush—cluster UX pass.
- **Gate:** platform and app start on kind; all ten fault types inject and restore state with labeled ground truth; canary analysis appears in console.
- **Checkpoint:** cluster-wide demo with a live fault injection.

### P8 · Evaluation + report
- **Goal:** answer the research question with reproducible evidence.
- **Tracks:** Navin—A12/E2 and results; all members—at least ten runs per fault; Dhanush—demo video/screenshots; Jegatheesan—API docs; Gokul—cluster stability.
- **Gate:** report includes at least ten runs per fault type and MTTD, MTTR, RCA, autonomy, and CFR results with mean ± standard deviation; demo materials and milestone docs are complete.
- **Checkpoint:** final thesis demonstration.

---

## 4. Non-blocking work and handoffs

| Consumer | Needs | Target | If late |
|---|---|---|---|
| Jegatheesan · registry | Shared envelope/event contract from Navin | P2 start | Use committed stub package. |
| Jegatheesan · incidents | Anomaly event from Navin | P3 | Use test event producer. |
| Navin · RCA | Query APIs from Gokul/Jegatheesan | P4 | Use seeded evidence fixtures. |
| Dhanush · UI | OpenAPI/API responses | Per page phase | Continue on generated mock server. |
| Gokul · executors | Action catalog and policies | P5 | Use dry-run mode. |
| All tracks | Shared Compose/infra stack | Available baseline | Propose shared changes by PR; keep local setup reproducible. |

**Handoff rule:** provider commits the contract and a sample response/event; consumer confirms it against a mock or test; the real implementation replaces the mock without changing the agreed shape silently.

---

## 5. End-of-phase integration routine

1. Freeze new feature work for the final 2–3 days; fix defects only.
2. Merge member branches by PR with CI passing.
3. Run the phase checkpoint from a clean environment and record evidence.
4. Review the gate checklist; record pass/fail and decisions in the planning log.
5. If a gate fails, record owner and next check date; do not label the phase complete.

### Gate checklist

- [ ] Gate behavior demonstrated and acceptance targets checked.
- [ ] Integration checkpoint passed; evidence linked.
- [ ] Tests and CI pass where applicable.
- [ ] Contracts, diagrams, runbooks, and member plans updated as needed.
- [ ] Decisions and risks recorded; Team Lead signs off.

---

## 6. Autonomy and safety boundary

All remediation—including rollback—uses the same policy and execution path. The AI may gather evidence and recommend actions; it does not receive unrestricted write access. High-risk actions require approval, automatic actions must be predefined, low-risk, reversible, rate-limited, and auditable; recovery verification is required before closing an incident. See [features.md](features.md) A6–A9 and the autonomy ADRs.

---

## 7. Demo application: AegisShop

AegisShop is the team's instrumented retail microservices app, used as the target for telemetry, faults, and evaluation. It is not part of the AegisDeploy control plane.

| Service | Responsibility | Stack | Example fault target |
|---|---|---|---|
| `shop-gateway` | Public API entry | FastAPI | HTTP 5xx, traffic spike, latency |
| `catalog-service` | Product catalogue | FastAPI | CPU saturation |
| `cart-service` | Shopping cart | FastAPI + Redis | Redis unavailable |
| `order-service` | Order processing | FastAPI + PostgreSQL | DB unavailable, faulty deployment |
| `payment-service` | Simulated payments | FastAPI | Container crash, latency |

All services emit metrics, logs, and traces. PostgreSQL supports orders; Redis supports cart. Confirm final service contracts with the backend owner before implementation changes.
