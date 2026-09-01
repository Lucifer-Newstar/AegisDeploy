# catalog-service (AegisShop) — vertical slice

> The **base-layer vertical slice**: the first AegisShop service that proves the
> whole observability flow end-to-end — service emits metrics + traces → OTel
> collector → Prometheus/Tempo → visible in Grafana (A1, P2 gate).
>
> It is intentionally **minimal**: in-memory catalog data (no Postgres yet),
> health/metrics/tracing from the service template conventions, and a stub of the
> FaultHook interface (chaos readiness — A11 comes later in the plan).

## Run it locally (dev)

```bash
pip install -e .[dev]
uvicorn catalog_service.main:app --port 9001 --reload
# → http://localhost:9001        metadata
# → http://localhost:9001/health liveness
# → http://localhost:9001/products   the catalog API
# → http://localhost:9001/metrics    Prometheus metrics
```

## Run it in the stack (compose)

```bash
make infra-up          # starts the observability stack + catalog-service
# Grafana → http://localhost:3000 → dashboards → AegisShop Catalog
# Prometheus target check → http://localhost:9090/targets → aegisshop-catalog
```

## What this slice proves (P2 gate inputs)

| Claim | Proof |
|---|---|
| FastAPI service runs in compose | `docker compose ps` → catalog-service healthy |
| Prometheus scrapes it | `/targets` shows `aegisshop-catalog` UP |
| Metrics reach Grafana | dashboard panels render request rate / latency / error rate |
| Traces reach Tempo | a request traced in Grafana Explore (Tempo datasource) |
| The envelope contract holds | future events use `backend/libs/telemetry` (lib added in the same sprint) |

## Deliberately NOT in this slice (P2 full / later phases)

- Postgres persistence (v1 uses in-memory data)
- Real FaultHook implementation (interface stub only)
- Deployment tracker integration (DI-1 lands in P2)
- Loki log scraping (logs go to stdout for now)
