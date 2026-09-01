# Deployment Intelligence — Design

> **The Deployment Intelligence (DI) tier** — the project upgrade decided 2026-09-01.
> A first-class module on top of the AegisDeploy SRE platform that turns **every
> software deployment** into a monitored, scored, and learnable event: predict risk
> before deploy, detect bad rollouts fast, correlate incidents to changes, decide
> rollback safely, and report change-failure analytics.
>
> Scope decision: full set of 7 capabilities (DI-1 … DI-7), integrated into the
> existing phases P2–P8 (no timeline change). Owner: Navin (design/AI-ML), with
> Gokul (pipeline/execution), Jegatheesan (APIs), Dhanush (UI).

---

## 1. Positioning

```text
AegisDeploy = Autonomous SRE Platform (A1–A12, B, C, D, E)
            + Deployment Intelligence tier (DI-1 … DI-7)   ← this document
```

The DI tier reuses the platform's existing machinery instead of adding a parallel
system:

| Platform machinery | Reused for DI |
|---|---|
| `deployment` events + envelope `deployment` field | every deploy is a first-class event (DI-1) |
| ML pipeline (`ml/`) | deployment risk scoring + bad-rollout detection (DI-2, DI-4) |
| RCA evidence set + `get_deployment_history` tool | change-incident correlation (DI-3) |
| Policy engine + executor (A6/A8) | rollback decisions, safe auto-rollback (DI-5) |
| Chaos lab `faulty-deployment` fault (A11) | training + validation data (DI-4/DI-7) |
| Evaluation framework (A12) | change failure rate as a headline metric (DI-7) |

## 2. Capabilities (DI-1 … DI-7)

| ID | Capability | Description | Owner | Phase |
|---|---|---|---|---|
| **DI-1** | Deployment tracking & registry | Every deploy/rollback/scale recorded with revision, version, trigger, status; deploy history API; **deploy timeline** per service | Jegatheesan (API) · Gokul (pipeline hook) | P2 |
| **DI-2** | Deployment risk scoring (ML) | Pre-deploy + post-deploy risk score from deploy attributes (size, blast radius, time, owner), service state, and historical outcome — *predict* risky deployments | Navin | P4 |
| **DI-3** | Change-incident correlation | RCA layer auto-attributes incidents to deployments: *"incident caused by deploy `abc1234`"* with evidence (timing overlap, metric shift after deploy, rollback history) | Navin | P4 |
| **DI-4** | Bad-rollout detection | Deploy-window anomaly evaluation: after each deploy, monitor error rate/latency/SLO-burn in the window; flag `rollout.bad` quickly (target < 3 min) | Navin + Gokul | P3 (base) → P4 |
| **DI-5** | Rollback intelligence | Recommend rollback (how far, to which revision) with impact summary; policy-gated: low-risk reversible rollbacks may auto-execute (L5), others require approval (L4); kill switch applies | Navin (design) · Gokul (executor) | P5 |
| **DI-6** | Canary / progressive delivery analysis | Compare canary vs stable metrics (traffic-split health comparison); used with a canary deployment in the demo | Gokul | P7 |
| **DI-7** | Change-failure analytics | Change failure rate (CFR) dashboards, deployment postmortems, and CFR as an evaluation metric (SRE metric, per proposal §9) | Navin + Gokul (dashboards) · Jegatheesan (backend) · Dhanush (UI) | P6 (dashboards) → P8 (evaluation) |

## 3. Data Model (additive to the envelope)

The envelope (`docs/architecture/telemetry-model.md`) gains **additive** fields
(schema v0.2, backward-compatible):

```json
{
  "type": "deployment",
  "deployment": {
    "revision": "abc1234",
    "version": "v2.3.1",
    "changed_at": "2026-08-31T10:14:00.000Z",
    "triggered_by": "github-actions",
    "status": "succeeded"
  },
  "payload": {
    "risk_score": 0.72,              // DI-2 (pre-deploy prediction)
    "risk_factors": ["large diff", "db-migration", "friday-17h"],
    "canary": { "enabled": true, "traffic_split": 0.1, "healthy": true },  // DI-6
    "rollout": { "status": "monitoring", "bad_after_s": null }             // DI-4
  }
}
```

New domain types (Postgres + event layer):

| Type | Produced by | Consumed by |
|---|---|---|
| `DeploymentRiskScore` | DI-2 model | dashboard, policy (pre-deploy gate), DI-4 |
| `ChangeCorrelation` | DI-3 | RCA hypotheses, incident page ("caused by deploy") |
| `RolloutHealth` | DI-4 | incident creation, DI-5 rollback trigger, DI-7 analytics |
| `RollbackRecord` | DI-5 | audit, CFR analytics |

## 4. Flow

```text
CI/CD push ──▶ DI-1 records deployment event
   │
   ├─▶ DI-2 risk scoring ──▶ (optional) pre-deploy gate / warning
   │
   ▼
Deploy executed → DI-4 monitor window (error · latency · SLO burn)
   │
   ├─ healthy → close deploy window → analytics (DI-7)
   │
   └─ rollout.bad ──▶ incident (A4)
                         │
                         ▼
              DI-3 correlation: which deploy? which revision? evidence
                         │
                         ▼
              DI-5 rollback recommendation (risk class)
                         ├─ low + reversible + policy → auto rollback (L5)
                         └─ else → human approval (L4)
                         │
                         ▼
              recovery verification (A9) → close / escalate → CFR analytics
```

## 5. Consistency with Existing Model

| Aspect | Rule |
|---|---|
| Autonomy | Rollback risk classes follow the autonomy model: auto only if policy-approved, reversible, low-risk (autonomy-model.md §2); kill switch applies |
| Tools | `get_deployment_history` already exists; DI adds `get_deploy_risk(service, revision)` (read-only) |
| Security | DI-5 rollback executes through the same scoped executor layer as A8 — never direct AI access |
| Statuses | Deployment lifecycle is **not** an incident status; incidents get an optional `change_correlation` reference |
| Demo | AegisShop `faulty-deployment` fault + a canary deployment are the two DI demo scenarios |

## 6. Evaluation (DI contribution to A12)

- **Change failure rate** = failed rollouts / total deployments, measured per experiment.
- **Correlation accuracy** = % of faulty-deploy faults where DI-3 names the correct revision.
- **Rollout detection latency** = fault → `rollout.bad` flag (target < 3 min).
- **Rollback success rate** = % of rollbacks that restore health (auto vs approved).

These join the existing metrics in [docs/operations/evaluation.md](../operations/evaluation.md).
