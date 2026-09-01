# Composite Structure Diagram — AI Reasoning Engine

> **Diagram 6 (UML 2.5 — Structural).** Internal structure of the **AI Service**
> component (Diagram 5): its parts, the ports on its boundary, and the connectors to
> the environment. Part names map 1:1 to classes in Diagram 2a. Decided 2026-08-31.

```mermaid
---
title: "Composite Structure — AI Service (Reasoning Engine)"
---
flowchart LR
    %% ═══════════════════════════════════════════════════════
    %% ENVIRONMENT (external to the component)
    %% ═══════════════════════════════════════════════════════
    GATEWAY["«external» API Gateway"]
    EVENTBUS["«external» Event Bus (Redis Streams)"]
    EVID_STORE["«external» Evidence Store"]
    PROM["«external» Prometheus"]
    LOKI["«external» Loki"]
    TEMPO["«external» Tempo"]
    OLLAMA["«external» Ollama (LLM)"]
    VECTOR["«external» PostgreSQL (pgvector)"]
    DEPLOY_TRK["«external» Deployment Tracker (REST :8701)"]

    %% ═══════════════════════════════════════════════════════
    %% COMPONENT BOUNDARY: AI SERVICE
    %% ═══════════════════════════════════════════════════════
    subgraph AI_SVC["«component» AI Service"]
        direction TB

        %% ── Ports (boundary) ──────────────────────────────
        P_REST["● REST :8601 (in)"]
        P_STREAMS["● Streams :6379 (in/out)"]
        P_EVID["● REST :8202 (out)"]
        P_PROMQL["● PromQL :9090 (out)"]
        P_LOGQL["● LogQL :3100 (out)"]
        P_TRACES["● traces :3200 (out)"]
        P_LLM["● LLM :11434 (out)"]
        P_VECTOR["● SQL :5432 pgvector (out)"]
        P_DEPLOY["● REST :8701 (out)"]

        %% ── Parts ─────────────────────────────────────────
        REASON["ReasoningEngine<br/>(orchestrator)"]
        COLLECTOR["EvidenceCollector"]
        LLMCLIENT["LLMClient"]
        RETRIEVER["RAGRetriever<br/>(embedder + vector)"]
        POSTMORTEM["PostmortemGenerator"]
        ASK["AskAegisService"]
        CORR["ChangeCorrelator<br/>(DI-3)"]

        subgraph TOOLS["ToolRegistry (read-only tools)"]
            T1["GetMetricsTool"]
            T2["GetLogsTool"]
            T3["GetTracesTool"]
            T4["GetServiceHealthTool"]
            T5["GetDeploymentHistoryTool"]
            T6["GetKubernetesEventsTool"]
            T7["GetRunbookTool"]
            T8["GetDeployRiskTool"]
        end

        %% ── Internal connectors ───────────────────────────
        REASON -->|invoke| TOOLS
        REASON -->|retrieve context| RETRIEVER
        REASON -->|reason via| LLMCLIENT
        REASON -->|collect| COLLECTOR
        REASON -->|generate| POSTMORTEM
        REASON -->|delegate correlation| CORR
        ASK -->|delegate| REASON

        %% ── Part → port wiring ────────────────────────────
        P_REST --- ASK
        P_STREAMS --- REASON
        P_EVID --- COLLECTOR
        P_PROMQL --- T1
        P_LOGQL --- T2
        P_TRACES --- T3
        P_LLM --- LLMCLIENT
        P_VECTOR --- RETRIEVER
        P_DEPLOY --- CORR
        P_DEPLOY --- T5
        P_DEPLOY --- T8
    end

    %% ═══════════════════════════════════════════════════════
    %% ENVIRONMENT CONNECTORS (port → external)
    %% ═══════════════════════════════════════════════════════
    GATEWAY -->|REST :8601| P_REST
    EVENTBUS <-->|incidents in · remediation out| P_STREAMS
    P_EVID -->|REST| EVID_STORE
    P_PROMQL -->|PromQL queries| PROM
    P_LOGQL -->|LogQL queries| LOKI
    P_TRACES -->|trace queries| TEMPO
    P_LLM -->|completions| OLLAMA
    P_VECTOR -->|embeddings + retrieval| VECTOR
    P_DEPLOY -->|deploy history & risk| DEPLOY_TRK

    %% ═══════════════════════════════════════════════════════
    %% COLOR CODING
    %% ═══════════════════════════════════════════════════════
    classDef ai fill:#fce7f3,stroke:#db2777,color:#831843;
    classDef tool fill:#fdf2f8,stroke:#f472b6,color:#9d174d;
    classDef port fill:#fff7ed,stroke:#f97316,color:#7c2d12;
    classDef ext fill:#f3f4f6,stroke:#6b7280,color:#374151;
    class REASON,COLLECTOR,LLMCLIENT,RETRIEVER,POSTMORTEM,ASK,CORR,TOOLS ai;
    class T1,T2,T3,T4,T5,T6,T7,T8 tool;
    class P_REST,P_STREAMS,P_EVID,P_PROMQL,P_LOGQL,P_TRACES,P_LLM,P_VECTOR,P_DEPLOY port;
    class GATEWAY,EVENTBUS,EVID_STORE,PROM,LOKI,TEMPO,OLLAMA,VECTOR,DEPLOY_TRK ext;
```

---

## 1. Parts (map to Diagram 2a classes)

| Part | Class in Diagram 2a | Responsibility |
|---|---|---|
| `ReasoningEngine` | ReasoningEngine | Orchestrates RCA: collect evidence → retrieve context → reason → hypothesize → recommend |
| `EvidenceCollector` | ReasoningEngine.collect_evidence | Fetches evidence via the Evidence Store API |
| `LLMClient` | ReasoningEngine.llm | Talks to the local LLM (Ollama) |
| `RAGRetriever` | RAGRetriever | Embeds + retrieves runbooks/past incidents from pgvector |
| `ToolRegistry` | list~Tool~ | Holds the eight compiled-in read-only tools |
| `GetMetricsTool` … `GetRunbookTool`, `GetDeployRiskTool` | the eight Tool realizations | Queries Prometheus/Loki/Tempo/registry/runbooks/**deploy risk** |
| `PostmortemGenerator` | PostmortemGenerator | Writes the incident postmortem on close |
| `AskAegisService` | AskAegisService | Chat front-end of the same engine (read-only) |

## 2. Ports & Environment Connectors

| Port | Direction | Connects to | Protocol |
|---|---|---|---|
| `REST :8601` | in | API Gateway | HTTP/JSON (RCA, ask, postmortem) |
| `Streams :6379` | in/out | Event Bus | Redis Streams (incident events in, remediation recommendations out) |
| `REST :8202` | out | Evidence Store | HTTP/JSON |
| `PromQL :9090` | out | Prometheus | HTTP (read-only) |
| `LogQL :3100` | out | Loki | HTTP (read-only) |
| `traces :3200` | out | Tempo | HTTP (read-only) |
| `LLM :11434` | out | Ollama | OpenAI-compatible API |
| `SQL :5432` | out | PostgreSQL (pgvector) | SQL (embeddings/retrieval) |
| `REST :8701` | out | Deployment Tracker | HTTP/JSON (deploy history, risk — DI-1/DI-2/DI-3) |

## 3. Design Invariants

- **All eight out-ports are read-only** — there is no write path from any part to any
  store (autonomy-model.md §3; component diagram §3).
- **ToolRegistry is compiled-in** — the AI cannot register new tools at runtime; the
  **eight** tools (seven telemetry/ops + `GetDeployRiskTool`) are the complete tool
  surface (security boundary).
- **AskAegisService and ReasoningEngine share the same engine** — a chat question and
  an incident RCA use identical evidence/grounding paths, so answers are equally
  citable.
