# Reference Service Template (`_template`)

> **Copy this folder to create a new AegisDeploy platform service.** It is the
> canonical pattern every backend service follows (working-rules rule 3: commented,
> consistent, easy to read). It is intentionally *not* a real service — the real
> services (gateway, registry, incidents, …) are built by copying this skeleton
> during P2/P3.

## What the template gives you

| Piece | File | Notes |
|---|---|---|
| App factory | `app/main.py` | FastAPI app with `/health`, `/ready`, `/metrics`, `/`; OTel tracing when configured |
| Settings | `app/config.py` | env-driven config via pydantic-settings (no hardcoded endpoints) |
| Logging | `app/logging.py` | structured key=value logs to stdout (container-friendly) |
| Tests | `tests/` | pytest + httpx health checks |
| Packaging | `pyproject.toml` | dist name + deps + dev extras |

## How to create a new service

```bash
cp -r backend/services/_template backend/services/<name>
# 1. rename the dist in pyproject.toml ("aegisdeploy-service-<name>")
# 2. set SERVICE_NAME + SERVICE_PORT in app/config.py defaults (or env)
# 3. add your routes to app/main.py (keep /health, /ready, /metrics)
# 4. write tests; run: pytest backend/services/<name>
```

## Conventions every service must follow

1. **Health endpoints** — `/health` (liveness, no deps), `/ready` (readiness,
   checks dependencies). Compose + K8s probes use these.
2. **Metrics** — `/metrics` exposes Prometheus-format metrics (prometheus-client);
   the scrape job in `infra/prometheus/prometheus.yml` targets the service.
3. **Tracing** — OTLP export to the OTel collector when
   `OTEL_EXPORTER_OTLP_ENDPOINT` is set; graceful no-op otherwise (runs offline).
4. **Config via env** — `app/config.py` reads env vars; no hardcoded endpoints
   (services must run identically in Compose and K8s — ADR-0005).
5. **Comments + types** — every module documents its purpose; functions have
   docstrings and type hints (ruff + mypy pass in CI).
6. **Envelope** — any emitted event uses `aegisdeploy-telemetry`
   (`backend/libs/telemetry`) — never a bespoke shape.

## Ports

Choose the next free port in the platform range (see component diagram):
registry 8101 · incidents 8201 · evidence 8202 · remediation 8301 · policy 8302 ·
audit 8401 · autonomy 8402 · ml 8501 · ai 8601 · **deployments 8701**.
