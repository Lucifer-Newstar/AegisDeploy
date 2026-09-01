# Interaction Overview Diagram — Incident Lifecycle

> **Diagram 14 (UML 2.5 — Behavioral).** The **map of interactions**: an
> activity-style overview whose nodes are **interaction frames** referencing the
> detailed behavioral diagrams (#9 activity, #10 state machine, #11 sequence,
> #12 communication). Decision guards match the activity diagram exactly. This is
> the final diagram of the 14-diagram set. Decided 2026-08-31.

```mermaid
---
title: "Interaction Overview — incident lifecycle (frames → diagrams 9-13)"
---
flowchart TB
    START((start)) --> F1

    %% ═══════════════════════════════════════════════════════
    %% INTERACTION FRAMES (each expands to a detailed diagram)
    %% ═══════════════════════════════════════════════════════
    F1["«interaction» Telemetry → Detection (L1)<br/>ref: sequence #11 · activity #9<br/>AegisShop → OTel → ML scoring → anomaly event"]
    D1{"anomaly score<br/>≥ 0.9 ?"}

    F2["«interaction» Investigation & RCA (L2)<br/>ref: sequence #11 · object #3<br/>evidence collection → RAG → LLM → hypothesis"]
    D2{"confidence<br/>≥ 0.7 ?"}

    F3["«interaction» Recommendation & Policy (L3)<br/>ref: communication #12 · state machine #10<br/>remediation recommended → policy evaluated"]

    F4["«interaction» Approval / Auto-execution (L4/L5)<br/>ref: sequence #11 · state machine #10<br/>human approval or policy-safe auto action → execute"]

    D3{"recovered ?"}

    F5["«interaction» Closure & Postmortem<br/>ref: communication #12 · timing #13<br/>verification passed → close → postmortem → metrics"]

    F6["«interaction» Escalation<br/>ref: state machine #10<br/>ESCALATED → on-call"]

    %% ═══════════════════════════════════════════════════════
    %% FLOW
    %% ═══════════════════════════════════════════════════════
    F1 --> D1
    D1 -->|"no (normal)"| F1
    D1 -->|"yes"| F2
    F2 --> D2
    D2 -->|"no"| F3
    F2 -->|"low confidence path"| F3
    D2 -->|"yes"| F3
    F3 --> F4
    F4 --> D3
    D3 -->|"no"| F6
    F6 --> END((end))
    D3 -->|"yes"| F5
    F5 --> END((end))

    %% ═══════════════════════════════════════════════════════
    %% COLOR CODING (frame tinted by layer)
    %% ═══════════════════════════════════════════════════════
    classDef tele fill:#dbeafe,stroke:#2563eb,color:#1e3a8a;
    classDef ml fill:#ffedd5,stroke:#ea580c,color:#7c2d12;
    classDef ai fill:#fce7f3,stroke:#db2777,color:#831843;
    classDef inc fill:#ecfdf5,stroke:#059669,color:#064e3b;
    classDef hum fill:#fef9c3,stroke:#ca8a04,color:#713f12;
    class F1 tele;
    class D1 ml;
    class F2 ai;
    class D2 ai;
    class F3 inc;
    class F4 inc;
    class D3 inc;
    class F5 inc;
    class F6 hum;
```

---

## 1. Frame → Diagram Mapping

| Frame | Expands to | Stage / Autonomy |
|---|---|---|
| F1 Telemetry → Detection | sequence #11 (first block), activity #9 (lanes 1–2) | L1 Detection |
| F2 Investigation & RCA | sequence #11 (evidence→RAG→LLM), object #3 | L2 Diagnosis |
| F3 Recommendation & Policy | communication #12 (msgs 12–14), state machine #10 | L3 Recommendation |
| F4 Approval / Auto-execution | sequence #11 (alt block), state machine #10 | L4 / L5 |
| F5 Closure & Postmortem | communication #12 (msgs 19–22), timing #13 | closure |
| F6 Escalation | state machine #10 (ESCALATED) | on-call |

## 2. How This Diagram Ties the Behavioral Set Together

```text
activity #9      → the workflow (swimlanes + guards)
state machine #10 → the states (incident + action)
sequence #11      → the time (lifelines)
communication #12 → the structure (numbered messages)
timing #13        → the clock (MTTD/MTTR)
interaction overview #14 → THE MAP (this diagram)
```

> Reading order for the behavioral set: **14 → 9 → 10 → 11/12 → 13** — start at the
> map, drill into the workflow, then the states, then the two interaction views, and
> finally the timing evidence.

---

## 4. Interaction Overview — Deployment Intelligence (DI)

The map of DI interactions: frames reference the DI blocks added to the behavioral
diagrams (activity #9, sequence #11, communication #12, timing #13, state machine #10).

```mermaid
---
title: "Interaction Overview — Deployment Intelligence (DI)"
---
flowchart TB
    START2((start)) --> G1

    G1["«interaction» Deploy & Track (DI-1)<br/>ref: activity #9 (DI) · sequence #11 (DI)"]
    G2["«interaction» Risk Scoring (DI-2)<br/>ref: class #2a (DeployRiskModel)"]
    DG1{"risk ≥ 0.8 ?"}
    G3["«interaction» Deploy-Window Monitoring (DI-4)<br/>ref: timing #13 (DI) · state machine #10 (rollout)"]
    DG2{"rollout.bad ?"}
    G4["«interaction» Change Correlation (DI-3)<br/>ref: sequence #11 (DI) · communication #12 (DI)"]
    G5["«interaction» Rollback (DI-5)<br/>ref: state machine #10 (rollout) · sequence #11 (DI)"]
    DG3{"recovered ?"}
    G6["«interaction» CFR Analytics & Postmortem (DI-7)<br/>ref: timing #13 (DI)"]
    END2((end))

    START2 --> G1
    G1 --> G2
    G2 --> DG1
    DG1 -->|"no"| G3
    DG1 -->|"yes (warn/gate)"| G3
    G3 --> DG2
    DG2 -->|"no (healthy)"| G6
    DG2 -->|"yes"| G4
    G4 --> G5
    G5 --> DG3
    DG3 -->|"yes"| G6
    DG3 -->|"no"| END2
    G6 --> END2

    classDef di fill:#d1fae5,stroke:#0d9488,color:#115e59;
    class G1,G2,G3,G4,G5,G6 di;
```

### Frame → Diagram Mapping (DI)

| Frame | Expands to | Feature |
|---|---|---|
| G1 Deploy & Track | activity #9 (DI block), sequence #11 (DI block) | DI-1 |
| G2 Risk Scoring | class #2a (`DeployRiskModel`) | DI-2 |
| G3 Window Monitoring | timing #13 (DI), state machine #10 (rollout) | DI-4 |
| G4 Change Correlation | sequence #11 (DI), communication #12 (DI) | DI-3 |
| G5 Rollback | state machine #10 (rollout), sequence #11 (DI) | DI-5 |
| G6 CFR & Postmortem | timing #13 (DI) | DI-7 |

> The full set now covers **both** evaluation scenarios: the runtime incident
> (Sections 1–3 above) and the deployment incident (this section).
