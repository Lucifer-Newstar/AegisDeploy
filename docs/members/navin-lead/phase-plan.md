# Navin · Team Lead / SRE / AI-SRE Phase Plan

> **Purpose:** my delivery and handoff by phase. Shared scope: [features](../../planning/features.md). Shared gates: [phases](../../planning/phases.md). Dates: [timeline](../../planning/timeline.md). I coordinate each gate review but do not replace feature owners.

| Phase | I deliver | I need | Handoff / completion check |
|---|---|---|---|
| **P1 · Foundation** | Repo/docs structure, ADRs, planning baseline, CI foundation. | — | Passed 2026-08-31. |
| **P2 · Shared contracts** | Telemetry envelope/event semantics, architecture decisions, API contract coordination, integration protocol. | Service requirements from all tracks. | Shared contracts are committed and consumers can use sample events/mock APIs. |
| **P3 · Detection** | A3 feature pipeline, statistical/Isolation Forest detectors, thresholds, validation. | Gokul's metric streams; A2 service context. | `anomaly.score` reaches incident track; precision/recall/F1 meet agreed targets. |
| **P4 · Reasoning** | A5 RCA/evidence logic, B1 retrieval, B2 read-only assistant, DI-2 risk and DI-3 correlation. | Incident/deploy APIs from Jegatheesan; query tools from Gokul. | Cited RCA reaches ≥70% top-1; DI-3 reaches ≥0.8 top-1 on agreed faulty-deploy tests; UI can consume outputs. |
| **P5 · Safety and policy** | A6 policy/risk design, A8 autonomy modes/kill switch, A9 verification logic, DI-5 rollback policy and safety docs. | Action API from Jegatheesan; scoped executors from Gokul. | Policies are testable; zero safety violations; recovery decisions are auditable. |
| **P6 · Integration** | Define SLOs with Gokul, coordinate cross-track fixes, review live-data product checkpoint. | Live service/API and dashboard data. | SLO definitions are documented; product gate evidence and decisions are recorded. |
| **P7 · Evaluation design** | A11 fault definitions, experiment manifests, ground-truth schema, faulty-deploy/canary scenarios. | Gokul's chaoslab; Jegatheesan's fault hooks. | Ten deterministic scenarios produce labeled, recoverable runs. |
| **P8 · Results** | Lead A12/E2 runs, CFR analysis, research results and thesis chapter. | All members' repeatable runs and raw results. | Report is reproducible, limitations are recorded, and results answer the research question. |
| **Buffer** | Viva preparation; B3 only as an approved stretch. | Core gates on schedule and suitable hardware/time. | B3 is omitted if it threatens core delivery; no buffer item changes locked scope by itself. |

## Lead responsibilities across phases

- Keep scope, contracts, decisions, and dependencies clear; update the relevant record when a decision changes.
- Facilitate weekly syncs and gate reviews; record pass/fail, evidence, owners, and follow-up dates.
- Enforce the safety boundary: the AI recommends; policy and scoped executors control actions; verification precedes closure.

## AI / research completion check

- [ ] AI claims cite evidence; read-only tools remain separate from action execution.
- [ ] Policies, thresholds, and evaluation protocol are versioned and testable.
- [ ] Raw experiment results and scripts are retained for reproducibility.
- [ ] Decision log, phase gate evidence, and this plan are current.
