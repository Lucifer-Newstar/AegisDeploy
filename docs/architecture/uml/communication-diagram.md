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
