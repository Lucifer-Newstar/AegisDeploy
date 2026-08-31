# Component Diagram — AegisSRE Platform

> **Diagram 5 (UML 2.5 — Structural).** Deployable components of the platform with
> their **provided/required interfaces** (protocol + port), the external dependencies
> (Postgres, Redis, Prometheus, Loki, Tempo, Ollama, OTel collector), and AegisShop
> as the monitored external component. Colors match Diagrams 2a/4a. Decided 2026-08-31.

```mermaid
---
title: "Component Diagram — AegisSRE Platform"
---
flowchart TB
    %% ═══════════════════════════════════════════════════════
    %% PLATFORM COMPONENTS
    %% ═══════════════════════════════════════════════════════
    DASH["«component» Web Dashboard (Next.js)<br/>provides: browser UI<br/>requires: REST :8000"]

    GATEWAY["«component» API Gateway<br/>provides: REST :8000 · auth JWT<br/>requires: service REST APIs"]

    REGISTRY["«component» Service Registry<br/>provides: REST :8101 · health<br/>requires: SQL :5432 · HTTP health probes"]
    INCIDENTS["«component» Incident Manager<br/>provides: REST :8201<br/>requires: SQL :5432 · Streams :6379"]
    EVIDENCE["«component» Evidence Store<br/>provides: REST :8202<br/>requires: SQL :5432 (JSONB)"]
    REMEDIATION["«component» Remediation Planner<br/>provides: REST :8301<br/>requires: policy REST · executors"]
    POLICY["«component» Policy Engine<br/>provides: REST :8302<br/>requires: SQL :5432 (policies)"]
    AUDIT["«component» Audit Service<br/>provides: REST :8401<br/>requires: SQL :5432"]
    AUTONOMY["«component» Autonomy Controller<br/>provides: REST :8402<br/>requires: policy mode flag"]

    ML["«component» ML Service (detection)<br/>provides: REST :8501 · anomaly events<br/>requires: Streams :6379 · PromQL :9090"]

    AI["«component» AI Service (reasoning · RAG · tools · postmortem)<br/>provides: REST :8601<br/>requires: Streams :6379 · evidence REST · PromQL :9090 · LogQL :3100 · traces :3200 · LLM :11434 · SQL :5432 (pgvector)"]

    %% ═══════════════════════════════════════════════════════
    %% EXTERNAL COMPONENTS
    %% ═══════════════════════════════════════════════════════
    SHOP["«external» AegisShop (5 services)<br/>provides: OTLP :4317 · health HTTP :9000-9004"]
    OTEL["«infra» OTel Collector<br/>provides: OTLP :4317/4318"]
    PROM["«infra» Prometheus<br/>provides: PromQL :9090"]
    LOKI["«infra» Loki<br/>provides: LogQL :3100"]
    TEMPO["«infra» Tempo<br/>provides: trace API :3200"]
    PG["«external» PostgreSQL<br/>provides: SQL :5432 (+ pgvector)"]
    REDIS["«external» Redis<br/>provides: Streams/cache :6379"]
    OLLAMA["«external» Ollama (LLM)<br/>provides: OpenAI-compat API :11434"]

    %% ═══════════════════════════════════════════════════════
    %% CONNECTIONS (labeled with interface + port)
    %% ═══════════════════════════════════════════════════════
    DASH -->|REST :8000| GATEWAY

    GATEWAY -->|REST| REGISTRY
    GATEWAY -->|REST| INCIDENTS
    GATEWAY -->|REST| REMEDIATION
    GATEWAY -->|REST| EVIDENCE
    GATEWAY -->|REST| AUDIT
    GATEWAY -->|REST| AI

    REGISTRY -->|SQL :5432| PG
    REGISTRY -->|HTTP health| SHOP

    INCIDENTS -->|SQL :5432| PG
    INCIDENTS <-->|Streams :6379| REDIS

    EVIDENCE -->|SQL :5432| PG
    REMEDIATION -->|REST :8302| POLICY
    POLICY -->|SQL :5432| PG
    AUDIT -->|SQL :5432| PG
    AUTONOMY -->|mode flag| POLICY

    ML -->|Streams :6379 (sub metric / pub anomaly)| REDIS
    ML -->|PromQL :9090| PROM

    AI -->|Streams :6379| REDIS
    AI -->|REST :8202| EVIDENCE
    AI -->|PromQL :9090| PROM
    AI -->|LogQL :3100| LOKI
    AI -->|trace API :3200| TEMPO
    AI -->|LLM API :11434| OLLAMA
    AI -->|SQL :5432 (pgvector)| PG

    %% telemetry ingress
    SHOP -->|OTLP :4317| OTEL
    OTEL -->|remote write| PROM
    OTEL -->|push| LOKI
    OTEL -->|push| TEMPO

    %% ═══════════════════════════════════════════════════════
    %% COLOR CODING (consistent 5-layer palette)
    %% ═══════════════════════════════════════════════════════
    classDef domain fill:#ecfdf5,stroke:#059669,color:#064e3b;
    classDef ml fill:#ffedd5,stroke:#ea580c,color:#7c2d12;
    classDef ai fill:#fce7f3,stroke:#db2777,color:#831843;
    classDef telemetry fill:#dbeafe,stroke:#2563eb,color:#1e3a8a;
    classDef ext fill:#f3f4f6,stroke:#6b7280,color:#374151;
    class DASH,GATEWAY,REGISTRY,INCIDENTS,EVIDENCE,REMEDIATION,POLICY,AUDIT,AUTONOMY domain;
    class ML ml;
    class AI ai;
    class OTEL,PROM,LOKI,TEMPO telemetry;
    class SHOP,PG,REDIS,OLLAMA ext;
```

---

## 1. Component Map

| Component | Provides | Requires | Layer |
|---|---|---|---|
| Web Dashboard | browser UI | REST :8000 | Domain |
| API Gateway | REST :8000, JWT auth | service REST APIs | Domain |
| Service Registry | REST :8101, health | SQL, HTTP probes | Domain |
| Incident Manager | REST :8201 | SQL, Streams | Domain |
| Evidence Store | REST :8202 | SQL (JSONB) | Domain |
| Remediation Planner | REST :8301 | policy REST, executors | Domain |
| Policy Engine | REST :8302 | SQL (policies) | Domain |
| Audit Service | REST :8401 | SQL | Domain |
| Autonomy Controller | REST :8402 | policy mode flag | Domain |
| ML Service | REST :8501, anomaly events | Streams, PromQL | ML |
| AI Service | REST :8601 | Streams, evidence, PromQL/LogQL/traces, LLM, pgvector | AI |

## 2. Interface Inventory

| Interface | Protocol | Port | Used by |
|---|---|---|---|
| Public API | REST/JSON (OpenAPI) | 8000 | Dashboard |
| Service APIs | REST/JSON | 8101–8402 | Gateway |
| Event Bus | Redis Streams | 6379 | Incidents, ML, AI |
| Metrics query | PromQL | 9090 | ML, AI tools |
| Logs query | LogQL | 3100 | AI tools |
| Traces query | Tempo HTTP API | 3200 | AI tools |
| LLM | OpenAI-compatible | 11434 | AI reasoning, postmortem |
| Vector store | SQL + pgvector | 5432 | AI RAG |
| Telemetry ingress | OTLP gRPC/HTTP | 4317/4318 | AegisShop → Collector |

## 3. Security Boundaries (consistent with autonomy-model.md)

- **AI Service** holds **read-only** tool connections (PromQL/LogQL/traces/evidence/
  pgvector) — there is **no write interface** from the AI to any store.
- **Remediation Planner** is the *only* component that can request execution, and only
  through the Policy Engine — executors are infra-side (Diagram 4c) and never exposed
  to the AI.
- Dashboard talks to the platform **only** via the Gateway (no service is publicly
  exposed).

## 4. Runtime Notes

- All components run as containers (Compose in dev, Kustomize on kind from P7 —
  see Diagram 4c).
- The OTel Collector is the single telemetry ingress; components never push telemetry
  to Prometheus/Loki/Tempo directly.
