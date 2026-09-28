# Dhanush · Frontend Phase Plan

> **Purpose:** my delivery and handoff by phase. Shared scope: [features](../../planning/features.md). Shared gates: [phases](../../planning/phases.md). Dates: [timeline](../../planning/timeline.md).

| Phase | I deliver | I need | Handoff / completion check |
|---|---|---|---|
| **P2 · Scaffold** | Console shell, dark design tokens, Command Center scaffold using mock data. | OpenAPI shapes and telemetry conventions; mocks are acceptable. | App starts; navigation and design tokens are documented; mock service data renders. |
| **P3 · Detection UI** | Service/incident list views; anomaly context and bands. | Registry and incident response shapes; mock server if APIs are pending. | Fault-to-incident checkpoint is visible in the UI. |
| **P4 · Reasoning UI** | Incident detail timeline, evidence cards, AI reasoning panel, Ask Aegis UI. | Incident/RCA APIs and Ask Aegis response contract. | Live incident shows cited evidence; chat displays answer and tool/evidence details. |
| **P5 · Action UI** | Approvals queue and autonomy-mode indicator. | Approval API and action-impact fields. | Approve/reject/defer and automatic-action status are demonstrated in the full loop. |
| **P6 · Product completion** | Complete C1 eight-page console; finish runbooks, postmortems, audit, and deployments views. | Runbook, postmortem, audit, deployment, and CFR APIs. | All eight pages render live data; product walkthrough passes. |
| **P7 · Cluster pass** | Fix layout/interaction issues at demo resolution on kind. | Integrated cluster from Gokul. | Cluster checkpoint can be followed without UI-blocking defects. |
| **P8 · Evaluation/demo** | Screenshots and demo video support. | Stable evaluation run and final scenario. | Demo assets are reproducible and ready for report/submission. |

## Working rules

- Build against OpenAPI-generated mocks until the real API is ready; swap without changing the contract silently.
- Keep AI-generated material visibly labeled and link claims to evidence.
- Prioritize the eight agreed pages; new pages or visual scope require a scope decision.

## Frontend completion check

- [ ] Required page states render from live APIs or have a clearly dated mock handoff.
- [ ] Empty, loading, error, and success states are covered.
- [ ] Design tokens and AI/evidence markers are used consistently.
- [ ] Lint, tests, and CI pass; this plan and product-vision page list are current.
