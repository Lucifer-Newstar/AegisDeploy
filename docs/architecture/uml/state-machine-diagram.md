# State Machine Diagram — Incident & RemediationAction Lifecycles

> **Diagram 10 (UML 2.5 — Behavioral).** Two state machines:
> (1) the **Incident** lifecycle — the canonical statuses used across this whole UML
> set (class diagram #2a, activity diagram #9, object diagram #3); (2) the
> **RemediationAction** lifecycle. Full transitions: `trigger [guard] / effect`;
> entry actions and initial/final states included. Decided 2026-08-31.

```mermaid
---
title: "State Machine — Incident"
---
stateDiagram-v2
    [*] --> OPEN : anomaly.score ≥ 0.9<br/>[no open incident for service]<br/>/ create incident · start MTTD timer
    OPEN --> INVESTIGATING : evidence collection started<br/>/ attach anomaly + timeline
    OPEN --> CLOSED : false positive<br/>[no root cause found]<br/>/ mark as false alarm · log audit
    INVESTIGATING --> REMEDIATING : remediation selected<br/>[approved or policy-auto]<br/>/ start execution · status REMEDIATING
    REMEDIATING --> VERIFYING : execution completed<br/>/ run recovery checks
    VERIFYING --> CLOSED : verification passed<br/>[health OK ∧ error rate ↓ ∧ latency ↓ ∧ SLO safe]<br/>/ compute MTTR · generate postmortem
    VERIFYING --> ESCALATED : verification failed<br/>[N attempts exhausted]<br/>/ notify on-call
    ESCALATED --> INVESTIGATING : human intervention<br/>[root cause identified]<br/>/ resume investigation
    ESCALATED --> CLOSED : human confirms resolution<br/>/ manual close · postmortem
    CLOSED --> [*]

    %% entry actions shown via state labels
    state "OPEN<br/>entry: start MTTD timer" as OPEN
    state "INVESTIGATING<br/>entry: attach evidence set" as INVESTIGATING
    state "REMEDIATING<br/>entry: record action audit" as REMEDIATING
    state "VERIFYING<br/>entry: run SLO/health checks" as VERIFYING
    state "CLOSED<br/>entry: compute MTTD/MTTR" as CLOSED
    state "ESCALATED<br/>entry: notify on-call" as ESCALATED
```

```mermaid
---
title: "State Machine — RemediationAction"
---
stateDiagram-v2
    [*] --> RECOMMENDED : created by planner<br/>[policy evaluated]<br/>/ attach risk class
    RECOMMENDED --> APPROVED : approve<br/>[requires_approval ∧ human approves]<br/>/ audit: actor + reason
    RECOMMENDED --> REJECTED : reject<br/>[human rejects]<br/>/ audit: actor + reason
    RECOMMENDED --> DEFERRED : defer<br/>[human defers]<br/>/ audit: actor + reason
    RECOMMENDED --> EXECUTED : auto-execute<br/>[low risk ∧ reversible ∧ SAFE_AUTO]<br/>/ audit: policy id
    DEFERRED --> APPROVED : approve later
    DEFERRED --> REJECTED : reject later
    APPROVED --> EXECUTED : executor runs<br/>/ audit: execution record
    APPROVED --> CANCELLED : kill switch<br/>[autonomy mode changed]<br/>/ audit: cancel
    EXECUTED --> [*] : success
    APPROVED --> FAILED : executor error<br/>/ audit: failure
    FAILED --> RECOMMENDED : retry<br/>[attempts < max]<br/>/ back to planner
    FAILED --> [*] : give up<br/>[attempts exhausted]<br/>/ escalate incident

    state "RECOMMENDED<br/>entry: send approval request" as RECOMMENDED
    state "APPROVED<br/>entry: notify executor" as APPROVED
    state "EXECUTED<br/>entry: attach execution record" as EXECUTED
```

---

## 1. Incident State Machine — Semantics

| Transition | Trigger | Guard | Effect |
|---|---|---|---|
| `[*] → OPEN` | anomaly event | score ≥ 0.9, no open incident for the service | create incident, start MTTD timer |
| `OPEN → INVESTIGATING` | evidence collection started | — | attach anomaly + timeline |
| `OPEN → CLOSED` | false positive | no root cause found | mark false alarm, audit |
| `INVESTIGATING → REMEDIATING` | remediation selected | approved or policy-auto | start execution |
| `REMEDIATING → VERIFYING` | execution completed | — | run recovery checks (A9) |
| `VERIFYING → CLOSED` | verification passed | health OK ∧ error ↓ ∧ latency ↓ ∧ SLO safe | compute MTTR, postmortem |
| `VERIFYING → ESCALATED` | verification failed | N attempts exhausted | notify on-call |
| `ESCALATED → INVESTIGATING` | human intervention | root cause identified | resume investigation |
| `ESCALATED → CLOSED` | human confirms | resolution | manual close |

## 2. RemediationAction State Machine — Semantics

| Transition | Meaning |
|---|---|
| `RECOMMENDED → APPROVED/REJECTED/DEFERRED` | The three human governance choices (A7) |
| `RECOMMENDED → EXECUTED` | The **Level 5** path: policy allows safe-auto execution |
| `APPROVED → CANCELLED` | Kill switch / autonomy-mode change mid-flight (A8) |
| `FAILED → RECOMMENDED` | Retry with backoff (attempts < max) |
| `FAILED → [*]` | Escalation: incident becomes ESCALATED |

## 3. Consistency Map

| Concept | Diagram 2a | Diagram 9 | Diagram 3 | This diagram |
|---|---|---|---|---|
| Statuses | `IncidentStatus` enum | statuses in activity states | `inc1.status = INVESTIGATING` | state names |
| Approval modes | `AutonomyMode` enum | L4/L5 branches | `ra1.mode = approval` | RECOMMENDED → APPROVED vs EXECUTED |
| Verification | `A9` class note | `DEC6` guard | — | VERIFYING → CLOSED/ESCALATED |

> One source of truth: if a status changes anywhere, it changes here first.
