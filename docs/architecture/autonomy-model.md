# Autonomous Remediation Model

AegisSRE implements five levels of autonomy. Every level above detection is gated by
policies; nothing executes outside the boundaries defined here.

## 1. The Five Levels

### Level 1 — Detection
```text
Anomaly detected
```
ML pipeline emits an `anomaly.score` event when a metric stream deviates from its
baseline. No diagnosis, no action.

### Level 2 — Diagnosis
```text
Anomaly
   ↓
Evidence collection
   ↓
Probable root cause
```
AI reasoning layer collects evidence (metrics, logs, traces, k8s events, deployment
history) and produces a *probable root cause* with cited evidence. Read-only tools only.

### Level 3 — Recommendation
```text
Root cause
   ↓
Recommended remediation
```
Remediation planner maps the root cause to concrete candidate actions
(restart / rollback / scale / replace instance / config change / escalate), each with a
risk classification.

### Level 4 — Human-Governed Automation
```text
Recommendation
      ↓
Engineer approval
      ↓
Remediation
```
The platform prepares the exact action and a dry-run impact summary; an engineer approves
via the dashboard; the scoped executor runs it. Approval, execution, and result are
audit-logged.

### Level 5 — Safe Autonomous Recovery
```text
Failure
 ↓
Known failure pattern
 ↓
Approved remediation policy
 ↓
Automatic action
 ↓
Health verification
 ↓
Success → close incident
Failure → escalate
```
Only **predefined, reversible, low-risk** operations can run automatically, and only when
a matching approved policy exists (see §3). Every automatic action is followed by recovery
verification; on failure the incident escalates to a human.

## 2. Policy Engine

The policy engine is the **only** component that decides whether an action may execute
and under what mode (auto vs. approval). Policies are declarative and versioned; examples:

```yaml
# infra/policies/remediation-policies.yaml (illustrative — formalized at M5)
policy:
  id: restart-unhealthy-workload
  actions: [workload.restart]
  risk_class: low
  reversible: true
  requires_approval: false          # Level 5 eligible
  max_blast_radius: 1               # replicas/instances affected
  cooldown: 15m                     # min between executions
  conditions:
    - anomaly.score >= 0.9
    - recovery.not_attempted_in(15m)
    - deployment.within(30m) == false   # never auto-restart right after a deploy

policy:
  id: rollback-deployment
  actions: [deployment.rollback]
  risk_class: high
  reversible: true
  requires_approval: true           # Level 4 only
  conditions:
    - incident.severity >= critical
```

### Risk classification (initial matrix — refined at M5)

| Risk class | Examples | Mode |
|---|---|---|
| Low | restart a single instance, scale up a replica, drain a canary | Level 5 (auto) if reversible + policy matches |
| Medium | scale down, restart workload (multi-replica) | Level 4 (approval) |
| High | rollback deployment, config mutation, data-affecting actions | Level 4 (approval) + escalation to on-call |
| Forbidden | schema changes, credential rotation, destructive deletes | Never executable by the platform |

## 3. Safety Boundaries

1. **Predefined tools only** — the AI can never invent new actions; tool list is
   compiled at build time.
2. **Least privilege** — executors hold scoped credentials; no admin access from the AI
   layer; the LLM never sees secrets.
3. **Reversibility** — auto-execution is limited to operations with a defined undo.
4. **Rate limits & cooldowns** — policies cap executions per incident and per time window.
5. **Audit trail** — every recommendation, approval, denial, execution, and verification
   is append-only logged.
6. **Verification gate** — an incident cannot close without recovery verification
   (health, error rate, latency, SLO checks).
7. **Kill switch** — `autonomy.mode` global flag: `observe` / `recommend` / `auto-safe`,
   controllable at runtime.

## 4. Autonomy State Machine (per incident)

```text
open ──▶ investigating ──▶ remediating ──▶ verifying ──▶ closed
  ▲          │                 │              │
  └──────────┴──── escalated ◀─┴──────────────┘   (verification failed → human on-call)
```

## 5. Human Overrides

- Approve / reject / defer any Level 4 recommendation.
- Cancel an in-flight auto action (if reversible).
- Downgrade global autonomy mode at any time.
- Annotate incidents with human context, which feeds back into the RAG knowledge base.
