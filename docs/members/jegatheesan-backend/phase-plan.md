# Jegatheesan · Backend Phase Plan

> **Purpose:** my delivery and handoff by phase. Shared scope: [features](../../planning/features.md). Shared gates: [phases](../../planning/phases.md). Dates: [timeline](../../planning/timeline.md).

| Phase | I deliver | I need | Handoff / completion check |
|---|---|---|---|
| **P2 · Service foundation** | A2 registry/health APIs; AegisShop service APIs and initial data models; DI-1 deployment-history API; OpenAPI contracts for my services. | Navin's shared telemetry/event contract; agreed ports and service list. | Registry/health acceptance passes; app services start; deploy/rollback events can be recorded and queried. |
| **P3 · Incidents** | A4 severity/state machine, append-only timeline, evidence storage, incident APIs, test event producer/fault hooks as needed. | Navin's anomaly-event schema (or test producer while it is in progress). | Injected test event creates an incident with valid transitions and a readable timeline. |
| **P4 · Evidence APIs** | APIs needed by RCA/incident views; deployment history detail for DI-3; harden AegisShop. | Read-only tool/API shapes agreed with Navin and Gokul. | AI and console can retrieve incident, service, evidence, and deploy data using the documented contracts. |
| **P5 · Governed actions** | A6 planner implementation, A7 approval API, A9 verification API, audit records. | Navin's risk/policy contract; Gokul's executor interface. | Approval → execution → verification path works; state transitions and audit records are correct. |
| **P6 · API completion** | API polish, OpenAPI client regeneration, integration fixes, authN/authZ baseline. | Frontend integration feedback and agreed API changes. | Console pages consume stable, documented APIs; generated clients are current. |
| **P7 · Cluster/app hardening** | AegisShop fault hooks, backend Kustomize support with Gokul, migration/startup hardening. | kind cluster and deployment conventions. | Backend and demo app run in kind; fault hooks are repeatable. |
| **P8 · Evaluation support** | Final API docs; support test runs and data checks. | Frozen experiment protocol and stable stack. | API docs match behavior and evaluation runs complete without data-shape ambiguity. |

## Working rules

- OpenAPI is the shared API contract; commit it before a consumer builds against an endpoint.
- Keep Pydantic models aligned with the shared telemetry envelope; use versioned database migrations.
- During dependency delays, use the test producer or mocks; do not block another track.

## Backend completion check

- [ ] API and event contracts are committed and validated.
- [ ] Services expose health checks and required telemetry.
- [ ] Unit/integration tests cover behavior and state transitions; CI passes.
- [ ] Migrations, API docs, and this plan reflect the implementation.
