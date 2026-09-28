# AegisDeploy Roadmap

> Short milestone view. Feature meaning and acceptance criteria: [feature scope](../planning/features.md). Phase gates and integration proof: [phase plan](../planning/phases.md). Calendar targets: [timeline](../planning/timeline.md).
>
> Dates are targets; the gate, not the date, determines completion. P6 is a parallel track during P5.

---

## P1 · Foundation — passed 2026-08-31
- Repo, documentation hub, ADRs, Compose observability stack, CI, and Makefile.
- **Gate:** healthy stack, green CI, indexed docs. **Status:** passed.

## P2 · Observability + AegisShop v1 — target 2026-10-31
- **Build:** A1 observability, A2 registry/health, AegisShop v1, DI-1 deploy history, console scaffold.
- **Prove:** app telemetry is queryable; registry and deploy history respond; scaffold runs on mocks; integrated app/platform startup works.

## P3 · Detection + incidents — target 2026-11-30
- **Build:** A3 anomaly detection, A4 incident manager, DI-4 deployment-window baseline.
- **Prove:** injected fault becomes a scored anomaly and a visible incident.

## P4 · AI reasoning — target 2026-12-31
- **Build:** A5 evidence/RCA, B1 RAG, B2 Ask Aegis, DI-2 risk scoring, DI-3 deployment correlation.
- **Prove:** live incident is explained with citations; deploy-related fault is attributed correctly.

## P5 · Remediation + autonomy — target 2027-01-31
- **Build:** A6 policy, A7 approvals, A8 safe-auto, A9 verification, DI-5 rollback intelligence.
- **Prove:** human-approved and eligible safe-auto actions both execute and verify recovery; safety checks pass.

## P6 · Product completion (parallel) — target 2027-01-31
- **Build:** eight console pages, C3–C5, D5 CI/CD, D6 SLOs, DI-7 CFR dashboard.
- **Prove:** live-data product walkthrough; pipeline, SLO, and CFR views work.

## P7 · Kubernetes + chaos lab — target 2027-02-28
- **Build:** D1 kind deployment, A11 ten-fault chaoslab, DI-6 canary analysis.
- **Prove:** platform/app run in kind; faults record ground truth; canary result appears in console.

## P8 · Evaluation + report — target 2027-03-31
- **Build:** A12 evaluation, E2 comparison, DI-7 CFR analysis.
- **Prove:** reproducible report includes MTTD, MTTR, RCA, autonomy, and CFR results.

## Report, demo, and buffer — Apr–Jun 2027
- Final report, demo video, and documentation pass.
- Viva preparation. B3 fine-tuning is optional and only proceeds if the core is on schedule and the Team Lead approves it.
