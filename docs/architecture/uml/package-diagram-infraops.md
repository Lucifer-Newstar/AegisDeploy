# Package Diagram — Infra / Ops

> **Diagram 4c (UML 2.5 — Structural).** Module organization of the **infrastructure
> and operations** side: observability stack, orchestration, CI/CD, IaC, and the
> chaos lab. Labeled dependency arrows; neutral palette (infra = gray, chaos =
> amber). Decided 2026-08-31.

```mermaid
---
title: "Package Diagram — Infra / Ops"
---
flowchart TB
    %% ═══════════════════════════════════════════════════════
    %% INFRA / OPS PACKAGES
    %% ═══════════════════════════════════════════════════════
    subgraph OBS["infra.observability"]
        direction TB
        OTEL["otel-collector"]
        PROM["prometheus (metrics)"]
        LOKI["loki (logs)"]
        TEMPO["tempo (traces)"]
        GRAFANA["grafana (visualization)"]
    end

    subgraph ORCH["infra.orchestration"]
        direction TB
        COMPOSE["docker-compose (dev)"]
        K8S["kubernetes / kustomize (prod-ish)"]
    end

    subgraph CI["infra.ci"]
        GH["github-actions workflows"]
    end

    subgraph IAC["iac"]
        TF["terraform (future)"]
    end

    subgraph CHAOS["chaoslab"]
        EXP["experiment-manifests"]
        RUNNER["fault-runner"]
    end

    subgraph OPS["ops"]
        SCRIPTS["scripts"]
        POLICIES["remediation-policies"]
    end

    %% ═══════════════════════════════════════════════════════
    %% DEPENDENCIES
    %% ═══════════════════════════════════════════════════════
    OTEL -->|feeds metrics| PROM
    OTEL -->|feeds logs| LOKI
    OTEL -->|feeds traces| TEMPO
    GRAFANA -->|queries| PROM
    GRAFANA -->|queries| LOKI
    GRAFANA -->|queries| TEMPO

    COMPOSE -->|runs| OTEL
    COMPOSE -->|runs| PROM
    COMPOSE -->|runs| GRAFANA
    K8S -->|runs same images as| COMPOSE
    K8S -->|mounts same configs as| COMPOSE

    GH -->|validates + builds| COMPOSE
    GH -->|lints| K8S
    GH -->|deploys (P7)| K8S

    TF -.->|provisions (future)| K8S

    RUNNER -->|executes manifests| EXP
    EXP -->|injects faults into| K8S
    POLICIES -->|referenced by| RUNNER
    SCRIPTS -->|helpers for| GH

    %% ═══════════════════════════════════════════════════════
    %% COLOR CODING
    %% ═══════════════════════════════════════════════════════
    classDef obs fill:#e0e7ff,stroke:#4f46e5,color:#312e81;
    classDef orch fill:#f3f4f6,stroke:#6b7280,color:#374151;
    classDef ops fill:#f3f4f6,stroke:#6b7280,color:#374151;
    classDef chaos fill:#fef3c7,stroke:#d97706,color:#78350f;
    class OTEL,PROM,LOKI,TEMPO,GRAFANA obs;
    class COMPOSE,K8S orch;
    class GH,TF,SCRIPTS,POLICIES ops;
    class EXP,RUNNER chaos;
```

---

## 1. Package Map

| Package | Contents | Owned by |
|---|---|---|
| `infra.observability.*` | OTel collector, Prometheus, Loki, Tempo, Grafana configs | Gokul (design: Navin) |
| `infra.orchestration.compose` | Local dev stack (docker-compose.yml) | Gokul |
| `infra.orchestration.k8s` | Kustomize bases (ADR-0005: 1:1 with Compose) | Gokul |
| `infra.ci.github-actions` | CI/CD workflows | Gokul |
| `iac.terraform` | Cloud IaC (reserved, M7/M8) | Gokul |
| `chaoslab.*` | Fault manifests + runner (ground truth) | Gokul + Navin |
| `ops.policies` | Declarative remediation policies (A6) | Navin |

## 2. Key Dependency Rules

- **Config parity:** `k8s` mounts the *same* config files as `compose` — no drift
  (ADR-0005).
- **CI lints K8s** (kubeconform) even before the cluster exists — manifests stay green
  from day one.
- **Chaos lab targets the cluster** (or compose in dev) via the AegisShop `fault-hooks`
  interface (Diagram 4b) — the single injection point.
- **Remediation policies** are data, not code — the policy engine loads them at
  runtime (A6), so policy changes never require a deploy.

## 3. Cross-Diagram Integration

| This package | Connects to (Diagram 4a) | How |
|---|---|---|
| `infra.observability` | `ai.tools` | read-only queries (metrics/logs/traces) |
| `infra.observability` | `ml.detection.feature-pipeline` | metric streams via event bus |
| `chaoslab` | `demoapp.libs.fault-hooks` (4b) | fault injection |
| `ops.policies` | `backend.services.policy` | policy evaluation |
