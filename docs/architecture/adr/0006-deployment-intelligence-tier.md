# ADR-0006: Deployment Intelligence Tier

- **Status:** Accepted
- **Date:** 2026-09-01
- **Deciders:** Navin Jairam (Team Lead), Arena Agent

## Context

The project (renamed AegisDeploy) already collects deployment events and treats
deployments as first-class signals, but deployments are only *evidence* — the platform
does not actively manage them. In cloud-native systems, most production incidents are
**change-caused**: a bad deployment is the single most common root cause. The team
decided (2026-09-01) to upgrade the platform with a first-class **Deployment
Intelligence (DI) tier** that turns every software deployment into a monitored, scored,
and learnable event — without weakening the SRE platform's scope or safety boundaries.

## Decision

Add a **Deployment Intelligence tier (DI-1…DI-7)** on top of the existing autonomous
SRE platform, integrated into the existing phases P2–P8 (no timeline change):

| ID | Capability |
|---|---|
| DI-1 | Deployment tracking & registry (deploy events, history API, deploy timeline) |
| DI-2 | Deployment risk scoring (ML) — predict risky deployments |
| DI-3 | Change-incident correlation — RCA attributes incidents to the causing deployment |
| DI-4 | Bad-rollout detection — deploy-window anomaly evaluation (< 3 min) |
| DI-5 | Rollback intelligence — policy-gated rollbacks incl. safe auto-rollback (Level 5) |
| DI-6 | Canary / progressive delivery analysis |
| DI-7 | Change-failure analytics — CFR dashboards, deployment postmortems, CFR metric |

Concrete integration rules:

1. **Reuse, don't duplicate:** DI consumes the existing event layer, ML pipeline,
   policy engine, executor layer, and evaluation framework — no parallel subsystems.
2. **Envelope additive only:** telemetry envelope becomes **v0.2** with optional
   fields (`deployment.risk_score`, `risk_factors`, `canary`, `rollout`) —
   backward-compatible; older producers remain valid.
3. **Autonomy boundaries hold:** auto-rollback (DI-5) only for low-risk, reversible,
   recent rollouts matching an approved policy; higher-risk rollbacks need human
   approval; kill switch applies; every action audit-logged.
4. **New AI tool surface:** exactly one new read-only tool added —
   `GetDeployRiskTool` (deploy history + risk) — the tool registry stays compiled-in.
5. **Evaluation:** CFR, correlation accuracy, rollout detection latency, rollback
   success rate, risk prediction recall, and auto-rollback safety join the A12 metrics.

Full design: `docs/architecture/deployment-intelligence.md`.
Feature spec: `docs/planning/features.md` (Tier DI).
Phase integration: `docs/planning/phases.md`, `docs/planning/timeline.md`.

## Consequences

### Positive

- Deployments become a **managed lifecycle** (track → score → monitor → correlate →
  rollback → learn), directly addressing the #1 cause of incidents.
- The second demo story (faulty deploy → bad rollout → auto-rollback → CFR) makes the
  final demonstration richer and more relevant to real SRE work.
- Reuses existing machinery, so the 8–10 month timeline is unaffected.
- CFR and correlation metrics strengthen the research question's evaluation.

### Negative / Trade-offs

- More scope: 7 new capabilities must be woven into member plans (done — see
  `docs/members/`).
- Risk of auto-rollback mistakes — mitigated by the policy gate, reversibility
  requirement, recent-revision-only rule, recovery verification, and audit trail.
- Extra dependency: DI-3/DI-5 require the deployment tracker to be reliable — it is
  on the critical path from P2.

## Alternatives Considered

| Option | Why rejected |
|---|---|
| Pivot the whole project to deployment incidents | Loses the platform's SRE breadth; the research question spans the full lifecycle |
| Rebrand only, no functional change | Cosmetic; does not deliver the "deployment incident intelligence" the lead asked for |
| Separate deployment-intelligence subsystem | Duplicates event layer, policy, executors; more to operate |
| Add DI as a new phase after P8 | Pushes the report/demo window; integration into existing phases is free |
