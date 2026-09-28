# Gokul · DevOps / Cloud Phase Plan

> **Purpose:** my delivery and handoff by phase. Shared scope: [features](../../planning/features.md). Shared gates: [phases](../../planning/phases.md). Dates: [timeline](../../planning/timeline.md).

| Phase | I deliver | I need | Handoff / completion check |
|---|---|---|---|
| **P2 · Observability** | A1 collector/backend wiring, Prometheus/Loki/Tempo dashboards, Compose additions, service image support. | Telemetry contract and service ports. | App metrics/logs/traces are queryable within 60 seconds; integrated startup works. |
| **P3 · Data plumbing** | Clean metric streams, alert/health wiring, mini-fault validation. | Navin's detector input/event shape. | Detector receives expected metrics; validation fault produces usable data. |
| **P4 · Read-only tools** | Least-privilege query adapters for metrics, logs, traces, and Kubernetes evidence. | Tool/API contract from Navin and service access. | RCA can retrieve the required evidence without write permissions. |
| **P5 · Executors** | Scoped restart/rollback/scale executors, dry-run path, audit integration, DI-5 execution. | Versioned action catalog and policy from Navin; APIs from Jegatheesan. | Approved actions work end-to-end; no broad admin credentials; rollback path is tested. |
| **P6 · Delivery/operations** | D5 CI/CD, D6 SLO/burn-rate dashboards, DI-7 CFR dashboard. | Buildable services and metric definitions. | PR pipeline is green; SLO and CFR panels show live or evaluation data. |
| **P7 · Cluster/chaos** | D1 kind/Kustomize deployment, A11 fault injection, DI-6 canary analysis. | Service images/manifests, fault specs from Navin, app hooks from Jegatheesan. | Stack runs on kind; ten faults produce ground truth and restore state; canary analysis is visible. |
| **P8 · Evaluation support** | Keep evaluation cluster stable and support repeatable runs. | Frozen experiment manifests and report protocol. | At least ten runs per fault can complete and be retained. |

## Working rules

- Keep Compose and Kubernetes behavior/configuration aligned; shared stack changes go through PRs.
- Pin images, validate manifests, and use least privilege. Executors must be auditable and support dry run.
- Use deterministic experiment durations and restore state after chaos tests.

## DevOps completion check

- [ ] Configs are versioned and mounted by the intended runtime.
- [ ] CI validates Compose, images, and Kubernetes manifests as applicable.
- [ ] No admin credentials are exposed to the AI layer.
- [ ] Operational notes/runbooks and this plan are updated; relevant CI checks pass.
