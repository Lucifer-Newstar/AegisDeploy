# Evaluation

How the platform's effectiveness is measured, objectively, using the controlled failure
laboratory (chaoslab) — not just demonstrations.

## 1. Reliability Metrics

| Metric | Definition | Target direction |
|---|---|---|
| **MTTD** | Time from failure injection to incident creation (detection) | ↓ |
| **MTTR** | Time from failure injection to verified recovery | ↓ |
| **MTTA** | Time from incident creation to first acknowledgment (human or automated) | ↓ |
| Incident frequency | Incidents per experiment window | baseline |
| Recovery success rate | % of incidents reaching `closed` with verified recovery | ↑ |
| Change failure rate | % of deployments requiring rollback/remediation | ↓ |
| False alarm rate | % of incidents created with no true fault | ↓ |

**Primary research question target:** MTTD/MTTR reduction of the AI-assisted workflow
vs. conventional monitoring/response workflow on the *same* injected failures.

## 2. ML Metrics (Anomaly Detection)

| Metric | Definition |
|---|---|
| Precision | anomalies flagged / true anomalies (of flagged) |
| Recall | true anomalies flagged / all true anomalies |
| F1 | harmonic mean of precision & recall |
| False-positive rate | normal points flagged / normal points |
| Detection latency | time from anomaly onset to first flag (per experiment) |

Ground truth comes from chaoslab experiment manifests: we know exactly when and what was
injected, so every window is labelable. Thresholds (e.g., `score ≥ 0.9`) are tuned on a
held-out experiment set, never on the evaluation set.

## 3. RCA & AI Metrics

| Metric | Definition |
|---|---|
| Root-cause identification accuracy | % of incidents where the top-1 hypothesis names the injected fault |
| Root-cause ranking accuracy | % where true cause is in top-3 hypotheses |
| Remediation recommendation accuracy | % of incidents where the recommended action would have resolved the fault |
| Evidence citation correctness | % of cited evidence actually relevant to the fault (human review) |
| Postmortem quality | human rubric: completeness, accuracy, actionability |

## 4. Automation Metrics

| Metric | Definition |
|---|---|
| Autonomous remediation success rate | % of auto-executed actions that pass recovery verification |
| Human intervention rate | % of incidents requiring human action (approval, manual fix) |
| Failed remediation rate | % of executed remediations that did not restore health |
| Recovery verification accuracy | % of `closed` verdicts correct (vs. ground truth) |
| Safety violations | % of actions violating policy boundaries (must be 0) |

## 5. Evaluation Protocol

1. **Experiment definition** — chaoslab manifest declares the fault, target service,
   duration, and expected impact (see chaoslab/).
2. **Baseline run** — conventional monitoring + human response workflow on the same
   failure; measure MTTD/MTTR and correctness manually.
3. **Platform runs** — same failures with AegisDeploy at increasing autonomy levels
   (observe → recommend → approval → safe-auto).
4. **Repetition** — N ≥ 5 runs per fault type for statistical stability; report mean ± std.
5. **Fairness** — identical telemetry, identical environment, same fault manifests;
   only the *response layer* differs.
6. **Reporting** — results table per fault type + aggregate summary committed to
   `docs/evaluation-results/` as each milestone completes.

## 6. Experiment Matrix (initial; refined at M7)

| Fault type | Target | Expected signals |
|---|---|---|
| CPU saturation | workload | CPU%, latency p95 ↑ |
| Memory exhaustion | workload | OOMKilled, memory ↑, restarts |
| Container crash / CrashLoop | workload | k8s_event, restart count ↑, 5xx ↑ |
| Database unavailability | postgres | connection errors, 5xx, latency ↑ |
| Network latency | workload → db | latency ↑, timeouts |
| HTTP 5xx injection | workload | error rate ↑, SLO burn |
| Dependency failure | downstream svc | cascading errors, trace failures |
| Configuration error | workload | crash on start, rollout failure |
| Faulty deployment | rollout of bad revision | error rate after deploy |
| Traffic spike | workload | load ↑, saturation |

## 7. Deployment Intelligence (DI) Metrics

> Added 2026-09-01 with the DI tier (DI-1…DI-7 — see
> `docs/architecture/deployment-intelligence.md` §6). These join the metrics above
> and are evaluated on the **faulty-deployment** and **canary** chaos faults (A11).

| Metric | Definition | Target |
|---|---|---|
| **Change failure rate (CFR)** | failed rollouts (bad / rolled back) ÷ total deployments | ↓ (measured per experiment set) |
| **Correlation accuracy** | % of faulty-deploy faults where DI-3 names the correct revision (top-1) | ≥ 0.8 |
| **Rollout detection latency** | deploy start → `rollout.bad` flag (DI-4) | < 3 min |
| **Rollback success rate** | % of rollbacks restoring health (DI-5) | ≥ 0.8 |
| **Risk-score prediction recall** | % of faulty deploys scored high-risk before/at deploy (DI-2) | ≥ 0.7 |
| **Auto-rollback safety** | % of auto-executed rollbacks policy-compliant (safety violations) | 100% (0 violations) |

The baseline-vs-platform protocol (§5) applies to the deployment scenario exactly as
to the runtime scenario: the **same** faulty-deploy manifests are run with a manual
response workflow (baseline) and with AegisDeploy at increasing autonomy levels.
