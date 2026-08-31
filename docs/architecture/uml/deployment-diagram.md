# Deployment Diagram — Kubernetes (kind) Runtime

> **Diagram 7 (UML 2.5 — Structural).** Physical deployment of the full system —
> platform + AegisShop + observability + data — onto the **kind** Kubernetes cluster
> (P7 target, ADR-0005: same images/configs as Compose). Nodes, artifacts, and
> protocol connections. Decided 2026-08-31.

```mermaid
---
title: "Deployment Diagram — kind cluster (P7)"
---
flowchart TB
    %% ═══════════════════════════════════════════════════════
    %% EXTERNAL NODES
    %% ═══════════════════════════════════════════════════════
    DEV["«device» Developer Workstation<br/>kubectl · docker · git<br/>«artifact» Kustomize overlays"]
    GH["«node» GitHub Actions<br/>«artifact» CI/CD workflows"]
    REG["«node» Container Registry<br/>«artifact» images: aegissre/* , aegisshop/*"]

    %% ═══════════════════════════════════════════════════════
    %% KIND CLUSTER
    %% ═══════════════════════════════════════════════════════
    subgraph KIND["«node» kind cluster — Kubernetes"]
        direction TB

        subgraph NS_PLAT["namespace: platform"]
            direction LR
            FE["frontend<br/>«artifact» aegissre/frontend:0.1"]
            GW["gateway<br/>«artifact» aegissre/gateway:0.1"]
            REGSVC["registry"]
            INC["incidents"]
            EV["evidence"]
            REM["remediation"]
            POL["policy"]
            AUD["audit"]
            AUT["autonomy"]
            ML["ml-service<br/>«artifact» aegissre/ml:0.1"]
            AI["ai-service<br/>«artifact» aegissre/ai:0.1"]
        end

        subgraph NS_SHOP["namespace: aegisshop"]
            direction LR
            SG["shop-gateway"]
            CA["catalog"]
            CT["cart"]
            OR["order"]
            PA["payment"]
        end

        subgraph NS_OBS["namespace: observability"]
            direction LR
            OTEL["otel-collector"]
            PROM["prometheus"]
            GRAF["grafana"]
            LOKI["loki"]
            TEMPO["tempo"]
        end

        subgraph NS_DATA["namespace: data"]
            direction LR
            PG["postgres (StatefulSet)<br/>«artifact» postgres:16 + pgvector"]
            REDIS["redis (StatefulSet)"]
        end
    end

    %% ═══════════════════════════════════════════════════════
    %% ARTIFACT & DEPLOY CONNECTIONS
    %% ═══════════════════════════════════════════════════════
    DEV -->|kubectl apply -k| KIND
    DEV -->|browser :8000| KIND
    GH -->|push images| REG
    KIND -->|pull images| REG
    GH -->|deploy workflow (P7)| KIND

    %% ── platform wiring ────────────────────────────────────
    FE -->|REST :8000| GW
    GW -->|REST| REGSVC
    GW -->|REST| INC
    GW -->|REST| REM
    GW -->|REST| EV
    GW -->|REST| AUD
    GW -->|REST| AI
    INC -->|SQL :5432| PG
    EV -->|SQL :5432| PG
    POL -->|SQL :5432| PG
    AUD -->|SQL :5432| PG
    AI -->|SQL :5432 pgvector| PG
    INC <-->|Streams :6379| REDIS
    ML <-->|Streams :6379| REDIS
    AI <-->|Streams :6379| REDIS
    ML -->|PromQL :9090| PROM
    AI -->|PromQL :9090| PROM
    AI -->|LogQL :3100| LOKI
    AI -->|trace API :3200| TEMPO
    AI -->|LLM :11434| OLLAMA

    %% ── shop → telemetry ───────────────────────────────────
    SG -->|OTLP :4317| OTEL
    CA -->|OTLP :4317| OTEL
    CT -->|OTLP :4317| OTEL
    OR -->|OTLP :4317| OTEL
    PA -->|OTLP :4317| OTEL
    OTEL -->|remote write| PROM
    OTEL -->|push| LOKI
    OTEL -->|push| TEMPO
    GRAF -->|queries| PROM
    GRAF -->|queries| LOKI
    GRAF -->|queries| TEMPO

    %% ── shop data ──────────────────────────────────────────
    CT -->|Redis :6379| REDIS
    OR -->|SQL :5432| PG

    %% ═══════════════════════════════════════════════════════
    %% COLOR CODING
    %% ═══════════════════════════════════════════════════════
    classDef domain fill:#ecfdf5,stroke:#059669,color:#064e3b;
    classDef ml fill:#ffedd5,stroke:#ea580c,color:#7c2d12;
    classDef ai fill:#fce7f3,stroke:#db2777,color:#831843;
    classDef shop fill:#dbeafe,stroke:#2563eb,color:#1e3a8a;
    classDef obs fill:#e0e7ff,stroke:#4f46e5,color:#312e81;
    classDef data fill:#f3f4f6,stroke:#6b7280,color:#374151;
    classDef node fill:#f8fafc,stroke:#475569,color:#1e293b;
    class FE,GW,REGSVC,INC,EV,REM,POL,AUD,AUT domain;
    class ML ml;
    class AI ai;
    class SG,CA,CT,OR,PA shop;
    class OTEL,PROM,GRAF,LOKI,TEMPO obs;
    class PG,REDIS data;
    class DEV,GH,REG,KIND node;
```

> Note: `OLLAMA` (LLM server) may run on the workstation or as a cluster pod —
> it is omitted from the cluster view for clarity; see composite structure diagram
> (Diagram 6) for its interface.

---

## 1. Nodes

| Node | Type | Runs |
|---|---|---|
| Developer Workstation | device | kubectl, docker, git, Kustomize overlays |
| GitHub Actions | node | CI/CD workflows (D5) |
| Container Registry | node | `aegissre/*`, `aegisshop/*` images |
| kind cluster | node (Kubernetes) | everything else, 4 namespaces |

## 2. Namespaces & Artifacts

| Namespace | Components | Artifacts (images) |
|---|---|---|
| `platform` | frontend, gateway, registry, incidents, evidence, remediation, policy, audit, autonomy, ml-service, ai-service | `aegissre/*:0.1` (P7 pins real versions) |
| `aegisshop` | shop-gateway, catalog, cart, order, payment | `aegisshop/*:0.1` |
| `observability` | otel-collector, prometheus, grafana, loki, tempo | pinned images (M1 versions) |
| `data` | postgres (StatefulSet + pgvector), redis (StatefulSet) | postgres:16-alpine, redis:7-alpine |

## 3. Key Connections

| Connection | Protocol | Purpose |
|---|---|---|
| workstation → cluster | kubectl | deploy via Kustomize (P7) |
| browser → gateway | HTTP :8000 | dashboard access (ingress) |
| shop services → collector | OTLP :4317 | telemetry ingress (A1) |
| collector → prometheus/loki/tempo | remote write / push | storage |
| ai-service → stores | PromQL/LogQL/traces | **read-only** tool access |
| platform + shop → data | SQL :5432 / Redis :6379 | persistence |

## 4. Deployment Parity (ADR-0005)

- The **same** config files under `infra/` are mounted here as in Docker Compose —
  dashboards, queries, and alert rules behave identically in dev and on the cluster.
- Every Compose service has a 1:1 Kustomize base (`infra/k8s/base/`); `kind` is the
  CI-friendly target (decision 2026-08-31).
