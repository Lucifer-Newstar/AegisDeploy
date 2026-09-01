# Sequence Diagram — Incident Lifecycle (db-down scenario)

> **Diagram 11 (UML 2.5 — Behavioral).** The time-ordered interaction for the
> full incident lifecycle — the same `db-down` demo scenario as the object diagram
> (#3). Solid arrows = synchronous calls, dashed arrows = async events/returns;
> `alt`/`opt`/`loop` fragments show decision structure. Decided 2026-08-31.

```mermaid
---
title: "Sequence Diagram — db-down incident lifecycle"
---
sequenceDiagram
    autonumber
    participant SRE as 🧑‍💻 SRE Engineer
    participant DASH as 🖥️ Dashboard
    participant GW as 🚪 API Gateway
    participant SHOP as 🏪 AegisShop
    participant OTEL as 📡 OTel / Stores
    participant ML as 🧠 ML Detection
    participant IM as 📋 Incident Manager
    participant ES as 🗄️ Evidence Store
    participant AI as 🤖 AI Reasoning
    participant RAG as 📚 RAG (pgvector)
    participant LLM as 🎛️ Ollama (LLM)
    participant POL as ⚖️ Policy Engine
    participant EXEC as ⚙️ Executor

    %% ── steady state telemetry ─────────────────────────────
    loop continuous
        SHOP->>OTEL: OTLP :4317 (metrics · logs · traces)
    end
    loop every evaluation window
        OTEL-->>ML: metric streams (event bus)
        ML->>ML: score streams (isolation forest)
    end

    %% ── detection (L1) ─────────────────────────────────────
    ML-->>IM: anomaly event (score 0.97 ≥ 0.9)
    IM->>IM: create incident (OPEN) · start MTTD
    IM-->>DASH: incident.created
    DASH-->>SRE: 🔴 sev1 alert

    %% ── investigation (L2) ─────────────────────────────────
    IM-->>AI: incident.created (event)
    AI->>ES: collect evidence: metric window
    ES-->>AI: evidence (p95 1.42s)
    AI->>ES: collect evidence: log excerpt
    ES-->>AI: evidence (12× timeout)
    AI->>ES: collect evidence: failing trace
    ES-->>AI: evidence (trace 4bf92f35)
    AI->>RAG: retrieve (runbooks · past incidents)
    RAG-->>AI: rb-004 · similar incident
    AI->>LLM: reason (hypothesis prompt)
    LLM-->>AI: hypothesis (conf 0.84)
    AI-->>IM: root-cause hypothesis (cited)

    %% ── recommendation (L3) ────────────────────────────────
    AI->>POL: evaluate (restart · LOW risk)
    POL-->>AI: decision: approval required
    AI-->>IM: remediation recommended
    IM-->>DASH: timeline updated
    DASH-->>SRE: 📋 action pending approval

    %% ── execution (L4 / L5) ────────────────────────────────
    alt human approval (L4)
        SRE->>DASH: approve (impact summary reviewed)
        DASH-->>IM: approval granted
        IM-->>EXEC: execute (restart order-service)
        EXEC->>EXEC: kubectl rollout restart
        EXEC-->>IM: execution result (ok)
    else safe auto (L5 — low risk · reversible · policy)
        IM-->>EXEC: auto-execute (policy match)
        EXEC-->>IM: execution result (ok)
    end

    %% ── verification (A9) ──────────────────────────────────
    IM->>IM: verify recovery (health · errors · latency · SLO)
    opt not recovered after N attempts
        IM-->>SRE: 🔔 escalated to on-call
    end
    IM-->>AI: incident.closed
    AI->>AI: generate postmortem
    AI-->>DASH: postmortem ready
    DASH-->>SRE: ✅ resolved · MTTD 69s · MTTR < 5m
```

---

## 1. Interaction Summary

| Stage | Messages | Autonomy |
|---|---|---|
| Telemetry | shop → stores (loop) | — |
| Detection | ML scores → anomaly event | L1 |
| Investigation | AI collects 3 evidence items → RAG → LLM → hypothesis | L2 |
| Recommendation | policy decision → remediation recommended | L3 |
| Execution | **alt: human approve (L4) / policy auto (L5)** | L4/L5 |
| Verification | recovery checks → close or escalate (opt) | gate |
| Postmortem | AI generates report → dashboard | — |

## 2. Sync vs Async Convention

| Arrow | Meaning | Used for |
|---|---|---|
| `->>` solid | synchronous call (request/response) | REST APIs (gateway, evidence store, policy, executor) |
| `-->>` dashed | async event or return | event bus messages, notifications, returns |
| `->>` self | internal computation | scoring, incident creation, verification, postmortem |

## 3. Consistency Map

| Element | Same as |
|---|---|
| Scenario + timestamps | Object diagram (#3) snapshot 10:17:02Z |
| Statuses | State machine (#10) — OPEN → … → CLOSED |
| Participants | Activity swimlanes (#9) + component interfaces (#5) |
| Policy decision | Policy engine = only decision point (autonomy-model.md §2) |
| Guard values | anomaly ≥ 0.9 (A3), confidence ≥ 0.7 (A5), N attempts (A9) |

---

## 4. Deployment Incident Sequence (DI — the second demo story)

The same lifecycle as the first block, but driven by a **faulty deployment** (DI-4/DI-5):
the deployment incident scenario from the product vision (§5.2).

```mermaid
---
title: "Sequence Diagram — deployment incident (faulty deploy — DI)"
---
sequenceDiagram
    autonumber
    participant CI as 🚀 CI/CD
    participant TRK as 🗂️ Deployment Tracker (DI-1)
    participant ML2 as 🧠 ML (risk + window DI-2/DI-4)
    participant IM2 as 📋 Incident Manager
    participant AI2 as 🤖 AI (correlation DI-3)
    participant POL2 as ⚖️ Policy Engine
    participant EXEC2 as ⚙️ Executor (rollback DI-5)
    participant CFR as 📊 Analytics (DI-7)
    participant SRE2 as 🧑‍💻 SRE Engineer

    CI->>TRK: deployment event (order-service v2.4.0)
    TRK->>ML2: score risk (DI-2)
    ML2-->>TRK: risk 0.72 (factors: large diff, db-migration)
    TRK->>TRK: start deploy window (DI-4)
    loop window (60 s)
        TRK->>ML2: stream metrics
    end
    ML2-->>TRK: rollout.bad (error rate ↑ after 60 s)
    TRK-->>IM2: incident event (sev2 · change-caused)
    IM2-->>AI2: incident.created
    AI2->>TRK: get_deployment_history (DI-3)
    TRK-->>AI2: revision abc1234 at 10:14
    AI2-->>IM2: correlated: caused by deploy abc1234 (conf 0.9)
    AI2->>POL2: evaluate rollback (DI-5)
    POL2-->>AI2: decision: low risk · reversible · SAFE_AUTO
    alt auto rollback (L5)
        IM2-->>EXEC2: auto rollback to v2.3.1
    else approval (L4)
        IM2-->>SRE2: rollback approval requested
        SRE2-->>IM2: approve
        IM2-->>EXEC2: rollback to v2.3.1
    end
    EXEC2-->>IM2: result ok
    IM2->>IM2: verify recovery (A9)
    IM2-->>CFR: deployment outcome (DI-7)
    CFR-->>SRE2: CFR updated · incident closed · postmortem
```

### DI Interaction Summary

| Stage | Messages | Feature |
|---|---|---|
| Deploy recorded | CI → Tracker | DI-1 |
| Risk scored | Tracker → ML | DI-2 |
| Window monitoring | Tracker ⇄ ML | DI-4 |
| Bad rollout flagged | ML → Tracker → Incident | DI-4 |
| Correlation | AI → Tracker (history) | DI-3 |
| Rollback decision | AI → Policy → Executor | DI-5 |
| Outcome analytics | Tracker/IM → CFR | DI-7 |
