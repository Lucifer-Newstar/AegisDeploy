# Kickoff Sync — Skeleton Demo Script (10 min)

> **Who:** Navin presents · **When:** first kickoff sync (item 1 of the
> agenda, [sync pack](p2-sync-pack.md)) · **Goal:** prove the foundation is
> real and hand each track its starting point. Run every command live —
> evidence beats slides.
> Prepped 2026-09-01.

## Before the demo (do this, not during)

```bash
cd AegisDeploy
make infra-up                      # stack + catalog-service
curl -s localhost:9001/health      # expect {"status":"healthy"}
```

## Step 1 — Repo tour (1 min)

Show the map (docs/README.md tree), then:
```bash
ls backend/libs backend/services demoapp docs/contracts
```
**Talking points:** libs = shared contracts (telemetry envelope v0.2, eventbus
ADR-0004) · `_template` = the pattern every service copies · `catalog-service`
= the first AegisShop slice · `docs/contracts/` = the API contracts we freeze
09-08.

## Step 2 — It's real (2 min)

```bash
docker compose ps                                   # all healthy
curl -s localhost:9001/products | head -c 200       # 5 products
```
**Talking points:** catalog API works end-to-end today; this is the reference
for cart/order/payment (Jega).

## Step 3 — Telemetry in Grafana (2 min)

```bash
for i in $(seq 1 20); do curl -s localhost:9001/products > /dev/null; done   # traffic
```
Open Grafana **localhost:3000** (`admin` / `aegis`) → dashboards →
**"AegisShop — Catalog Service"** → show QPS / p95 / 5xx / catalog-size panels.
Then Prometheus **localhost:9090/targets** → `aegisshop-catalog` = UP.

**Talking points:** metrics flow service → /metrics → Prometheus → Grafana;
this is the P2 gate pattern ("visible < 60 s"), just with one service today.

## Step 4 — Traces (1 min, if time)

Grafana → Explore → Tempo → trace a `/products` request (service:
`catalog-service`). If traces don't show, skip with one line: "tracing is
no-op when OTLP endpoint is unset — Gokul's A1 task wires it per service."

## Step 5 — CI + drift check (2 min)

Open `.github/workflows/ci.yml` → name the 5 jobs. Then run the guard live:
```bash
python3 scripts/check_contract_drift.py
```
**Talking points:** the drift check compares each built service's OpenAPI
against `docs/contracts/` — it already caught a real bug (catalog 404 wasn't
declared in the route decorator). Rule for everyone: **contracts change
first, code follows** (freeze 09-08, then contract PRs).

## Step 6 — Handoff (2 min)

| Track | Starts with |
|---|---|
| Jega | `_template` + contracts (registry :8101, deployments :8701, cart/order/payment 9002–9004) + libs |
| Gokul | compose + prometheus.yml + edge cases #7/#12 (DI-1 hook decision D5) |
| Dhanush | contracts → mock server (openapi-typescript + MSW, D3) + console scaffold |
| Navin | port register + edge-case register + weekly syncs |

Close with: **"One command shows every service in Grafana AND the console"**
— the gate (2026-10-31), rehearsal 2026-10-15.

## Troubleshooting (if something breaks on stage)

| Symptom | Fix |
|---|---|
| `docker compose ps` not healthy | Docker Desktop not running — start it, `make infra-up` again |
| Grafana panels empty | Prometheus → Targets: target down? Check `make infra-logs` |
| Port 9001 busy | `docker ps` → conflicting container; or demo still works without the traffic loop |
| Drift check prints "skipped" | Expected — unbuilt services are skipped by design (their contracts are the forward spec) |
