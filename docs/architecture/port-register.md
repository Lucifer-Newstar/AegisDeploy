# Port & Naming Register

> **Single source of truth** for service identities: ids, DNS names, ports,
> metric/label conventions, and env-var names. Every P2+ service must get a
> row here **in the same PR that creates it** (PR template checklist).
> Owner: Navin (Team Lead) — reviewed at weekly syncs.

## 1. Naming rules (binding)

| Thing | Rule | Example |
|---|---|---|
| Service id | **kebab-case**, equals the compose service name **and** the K8s Service name (ADR-0005 1:1) | `catalog-service` |
| DNS name | = service id (compose + K8s resolve it) | `catalog-service:9001` |
| Python package | snake_case of the id (`<id>-service` → `<id>_service`) — never `app` | `catalog_service` |
| Contract file | `<id>.yaml` in `docs/contracts/` + row in `manifest.json` | `catalog-service.yaml` |
| Docker image | `<part-of>/<id>:<version>` | `aegisshop/catalog-service:0.1.0` |
| OTel resource | `service.name=<id>` · `deployment.environment=<ENVIRONMENT>` | — |

## 2. Platform services (control plane, 8xxx)

| Service | Port | DNS | Contract | Feature | Phase | Status |
|---|---|---|---|---|---|---|
| registry | **8101** | registry-service | [registry-service.yaml](../contracts/registry-service.yaml) | A2 registry + health | P2 | pending (Jega) |
| incidents | 8201 | incidents-service | — | A4 incident manager | P3 | planned |
| evidence | 8202 | evidence-service | — | A5 evidence store | P3/P4 | planned |
| remediation | 8301 | remediation-service | — | A6/A7 planner + approvals | P5 | planned |
| policy | 8302 | policy-service | — | A6/A8 policy + risk matrix | P5 | planned |
| audit | 8401 | audit-service | — | C5 audit log | P5/P6 | planned |
| autonomy | 8402 | autonomy-service | — | A8 autonomy modes + kill switch | P5 | planned |
| ml | 8501 | ml-service | — | A3 detectors / DI-2 / DI-3 | P3/P4 | planned |
| ai | 8601 | ai-service | — | B1 RAG / B2 Ask Aegis / RCA | P4 | planned |
| deployments | **8701** | deployments-service | [deployments-service.yaml](../contracts/deployments-service.yaml) | DI-1 deploy tracker | P2 | pending (Jega) |

## 3. AegisShop demo workload (9xxx)

| Service | Port | DNS | Contract | Status |
|---|---|---|---|---|
| catalog | **9001** | catalog-service | [catalog-service.yaml](../contracts/catalog-service.yaml) | **LIVE** (slice) |
| cart | 9002 | cart-service | [cart-service.yaml](../contracts/cart-service.yaml) | pending (P2, Jega) |
| order | 9003 | order-service | [order-service.yaml](../contracts/order-service.yaml) | pending (P2, Jega) |
| payment | 9004 | payment-service | [payment-service.yaml](../contracts/payment-service.yaml) | pending (P2, Jega) |

Ports **locked 2026-09-01** (lead pre-approval, decision D1) — recorded at
the kickoff sync; team confirmation is a formality.

## 4. Infrastructure (compose, fixed)

| Component | Port | Notes |
|---|---|---|
| Postgres | 5432 | platform DB |
| Redis | 6379 | eventbus streams (ADR-0004) |
| Prometheus | 9090 | scrape + remote-write |
| Grafana | 3000 | console-in-a-pinch, dashboards |
| Loki | 3100 | logs |
| Tempo | 3200 | traces API; OTLP receivers are internal to the Compose network |
| OTel collector | 4317 (gRPC) / 4318 (HTTP) | host-published OTLP ingress for apps; forwards traces to Tempo internally |

**Port-range policy:** 3xxx–6xxx infra · 8xxx platform control plane ·
9xxx demo workload (AegisShop). New service = next free port in its range;
never reuse.

## 5. Metric & label conventions (binding)

| Metric | Labels | Owner of the name |
|---|---|---|
| `http_server_requests_total` | `service`, `method`, `path`, `status` | shared (template) |
| `http_server_request_duration_seconds` | `service`, `method`, `path` | shared (template) |
| domain metrics (e.g. `catalog_products_total`) | `service` (+ domain labels) | owning track |

Rules (edge case #5):
- Shared names keep the **exact** label set above — a label added/removed in
  one service silently drops series in Prometheus.
- Each service registers metrics on its **own CollectorRegistry**
  (template default) so combined test runs don't collide.
- New metric names: review by Navin; catalogued in the same PR.

## 6. Environment variables (naming standard)

| Variable | Used by | Notes |
|---|---|---|
| `SERVICE_NAME` | all services | = service id (metric labels, logs, OTel resource) |
| `SERVICE_PORT` | all services | bind port (matches this register) |
| `ENVIRONMENT` | all services | dev / staging / prod |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | all services | empty = tracing no-op; compose sets `http://otel-collector:4317` |
| `SERVICE_REGISTRY_URL` | P2 services (planned) | how services find the registry (A2) — added with registry PR |

Rule: env names come from `config.py` defaults per service; compose and K8s
bases set the **same** names (ADR-0005 parity).

## 7. Event streams

One stream per event type: `st:<event_type>` — see the event catalogue
([telemetry-model.md §3.5](../architecture/telemetry-model.md)).

## 8. Adding a service (checklist)

1. Reserve the next free port here (this doc) — same PR as the service.
2. Contract file in `docs/contracts/` + row in `manifest.json`.
3. Compose service + K8s base (ADR-0005) + CI `python-quality` install line.
4. Env vars per §6; metrics per §5; events per §7.
5. PR template checklist covers all of the above — Navin reviews against
   this register.
