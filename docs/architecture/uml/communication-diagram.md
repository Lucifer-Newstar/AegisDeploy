# Communication Diagram — Incident Lifecycle (db-down scenario)

> **Diagram 12 (UML 2.5 — Behavioral).** The same `db-down` incident lifecycle as the
> sequence diagram (#11), shown as a **communication (collaboration) diagram**:
> objects as nodes, **hierarchically numbered messages** on the links — structure and
> order in one view. Message names match Diagram 11 exactly (renumbered for nesting).
> Decided 2026-08-31.

```mermaid
---
title: "Communication Diagram — db-down incident lifecycle"
---
flowchart LR
    %% ═══════════════════════════════════════════════════════
    %% OBJECTS (same set as sequence diagram #11)
    %% ═══════════════════════════════════════════════════════
    SRE["🧑‍💻 SRE Engineer"]
    DASH["🖥️ Dashboard"]
    GW["🚪 API Gateway"]
    SHOP["🏪 AegisShop"]
    OTEL["📡 OTel / Stores"]
    ML["🧠 ML Detection"]
    IM["📋 Incident Manager"]
    ES["🗄️ Evidence Store"]
    AI["🤖 AI Reasoning"]
    RAG["📚 RAG (pgvector)"]
    LLM["🎛️ Ollama (LLM)"]
    POL["⚖️ Policy Engine"]
    EXEC["⚙️ Executor"]

    %% ═══════════════════════════════════════════════════════
    %% NUMBERED MESSAGES (hierarchical)
    %% ═══════════════════════════════════════════════════════
    SHOP -->|"1 · OTLP telemetry (continuous)"| OTEL
    OTEL -->|"2 · metric streams (async)"| ML
    ML -->|"3 · anomaly event (0.97 ≥ 0.9)"| IM
    IM -->|"4 · incident.created"| DASH
    DASH -->|"4.1 · 🔴 sev1 alert"| SRE
    IM -->|"5 · incident.created (event)"| AI
    AI -->|"6 · collect evidence: metric window"| ES
    ES -->|"6.1 · evidence (p95 1.42s)"| AI
    AI -->|"7 · collect evidence: log excerpt"| ES
    ES -->|"7.1 · evidence (12× timeout)"| AI
    AI -->|"8 · collect evidence: failing trace"| ES
    ES -->|"8.1 · evidence (trace 4bf92f35)"| AI
    AI -->|"9 · retrieve (runbooks · past incidents)"| RAG
    RAG -->|"9.1 · rb-004 · similar incident"| AI
    AI -->|"10 · reason (hypothesis prompt)"| LLM
    LLM -->|"10.1 · hypothesis (conf 0.84)"| AI
    AI -->|"11 · root-cause hypothesis (cited)"| IM
    AI -->|"12 · evaluate (restart · LOW risk)"| POL
    POL -->|"12.1 · decision: approval required"| AI
    AI -->|"13 · remediation recommended"| IM
    IM -->|"14 · 📋 action pending approval"| DASH
    DASH -->|"14.1 · approval requested"| SRE
    SRE -->|"15 · approve"| DASH
    DASH -->|"15.1 · approval granted"| GW
    GW -->|"15.2 · execute approval"| IM
    IM -->|"16 · execute (restart order-service)"| EXEC
    EXEC -->|"16.1 · result ok"| IM
    IM -->|"17 · verify recovery (self)"| IM
    IM -->|"18 · escalate (opt: not recovered)"| SRE
    IM -->|"19 · incident.closed"| AI
    AI -->|"20 · generate postmortem (self)"| AI
    AI -->|"21 · postmortem ready"| DASH
    DASH -->|"22 · ✅ resolved · MTTD 69s · MTTR < 5m"| SRE

    %% ═══════════════════════════════════════════════════════
    %% COLOR CODING (same palette as the set)
    %% ═══════════════════════════════════════════════════════
    classDef ml fill:#ffedd5,stroke:#ea580c,color:#7c2d12;
    classDef domain fill:#ecfdf5,stroke:#059669,color:#064e3b;
    classDef ai fill:#fce7f3,stroke:#db2777,color:#831843;
    classDef tele fill:#dbeafe,stroke:#2563eb,color:#1e3a8a;
    classDef hum fill:#fef9c3,stroke:#ca8a04,color:#713f12;
    class ML ml;
    class IM,ES,POL,EXEC,GW domain;
    class AI,RAG,LLM ai;
    class SHOP,OTEL tele;
    class SRE,DASH hum;
```

---

## 1. Message Numbering (hierarchy explained)

| Number | Message | Nested under |
|---|---|---|
| 1–3 | telemetry → detection → incident | top-level flow |
| 4 / 4.1 | incident created → dashboard → alert | notification |
| 5–11 | investigation: evidence ×3, RAG, LLM, hypothesis | investigation (L2) |
| 12 / 12.1 | policy evaluation | recommendation (L3) |
| 13–14.1 | remediation recommended → approval request | recommendation |
| 15–15.2 | approval via gateway | governance (L4) |
| 16–16.1 | execution + result | execution |
| 17–18 | verification + optional escalation | verification (A9) |
| 19–22 | close → postmortem → resolution | closure |

## 2. Relationship to Sequence Diagram (#11)

| Aspect | Sequence (#11) | Communication (#12) |
|---|---|---|
| Focus | **Time order** (vertical lifelines) | **Structure** (objects + links) |
| Messages | same set, in time | same set, numbered by nesting |
| Participants | 13 lifelines | same 13 objects |
| Scenario | db-down incident | db-down incident |

> Rule of thumb: use #11 to see *when*, use #12 to see *who talks to whom* — the
> message names are identical by design, so the two diagrams can be cross-checked.

---

## 4. Deployment Incident Communication (DI)

The faulty-deploy scenario as a communication diagram — numbered messages show the
call structure of the DI flow.

```mermaid
---
title: "Communication Diagram — deployment incident (DI)"
---
flowchart LR
    CI["🚀 CI/CD"] -->|"1 · deployment event (order-service v2.4.0)"| TRK["🗂️ Deployment Tracker"]
    TRK -->|"2 · score risk (DI-2)"| ML2["🧠 ML Risk/Window"]
    ML2 -->|"2.1 · risk 0.72"| TRK
    TRK -->|"3 · start deploy window (DI-4)"| ML2
    ML2 -->|"4 · rollout.bad (error rate ↑)"| TRK
    TRK -->|"5 · incident event (sev2)"| IM2["📋 Incident Manager"]
    IM2 -->|"6 · incident.created"| AI2["🤖 AI Correlation"]
    AI2 -->|"7 · get_deployment_history (DI-3)"| TRK
    TRK -->|"7.1 · revision abc1234"| AI2
    AI2 -->|"8 · correlated: deploy abc1234 (conf 0.9)"| IM2
    AI2 -->|"9 · evaluate rollback (DI-5)"| POL2["⚖️ Policy Engine"]
    POL2 -->|"9.1 · SAFE_AUTO decision"| AI2
    IM2 -->|"10 · auto rollback (L5) / approval (L4)"| EXEC2["⚙️ Executor"]
    EXEC2 -->|"10.1 · result ok"| IM2
    IM2 -->|"11 · verify recovery (A9)"| IM2
    IM2 -->|"12 · deployment outcome (DI-7)"| CFR["📊 Analytics"]
    CFR -->|"13 · CFR updated · incident closed"| SRE2["🧑‍💻 SRE Engineer"]

    classDef trk fill:#ffedd5,stroke:#ea580c,color:#7c2d12;
    classDef inc fill:#ecfdf5,stroke:#059669,color:#064e3b;
    classDef ai fill:#fce7f3,stroke:#db2777,color:#831843;
    classDef pol fill:#ede9fe,stroke:#7c3aed,color:#4c1d95;
    classDef ana fill:#d1fae5,stroke:#0d9488,color:#115e59;
    classDef hum fill:#fef9c3,stroke:#ca8a04,color:#713f12;
    class TRK,ML2 trk;
    class IM2,EXEC2 inc;
    class AI2 ai;
    class POL2 pol;
    class CFR ana;
    class CI,SRE2 hum;
```

### Message Hierarchy

| Number | Message | Feature |
|---|---|---|
| 1 | deployment event | DI-1 |
| 2 / 2.1 | risk scoring | DI-2 |
| 3–4 | window monitoring → bad | DI-4 |
| 5–8 | incident → correlation | DI-3 |
| 9 / 9.1 | rollback evaluation | DI-5 |
| 10 / 10.1 | execution | DI-5 |
| 11–13 | verification → CFR | A9, DI-7 |
