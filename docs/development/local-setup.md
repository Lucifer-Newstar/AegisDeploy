# Local Development Setup (AegisDeploy)

> **For every member:** one-time machine setup to run the repo, the local
> stack, and the Python packages. Written from the P2 kickoff; extend as new
> components land.
> Last verified against: walking-skeleton commits (2026-09-01) + P2 kickoff.

---

## 1. Prerequisites (one-time, per machine)

| Tool | Version | Needed for | Install |
|---|---|---|---|
| Git | ≥ 2.40 | everything (clone, branches, commits) | [git-scm.com](https://git-scm.com) |
| Python | **3.12.x** | all backend/ML/AI packages (target `py312` in ruff/mypy) | pyenv or [python.org](https://python.org) |
| uv (recommended) | latest | fast venv + editable installs | `pip install uv` or [astral.sh/uv](https://docs.astral.sh/uv/) |
| Docker Desktop | latest (Compose v2) | `make infra-up` local stack | [docker.com](https://www.docker.com/products/docker-desktop/) |
| Make | — | task runner (`make infra-up`, `make lint`) | built into macOS/Linux; WSL/choco on Windows |
| Node.js | **22 LTS** | frontend toolchain (Dhanush's track; optional for others) | [nodejs.org](https://nodejs.org) |

> Windows note: use **WSL2 + Ubuntu** — Docker Desktop integrates with WSL2 and
> `make` works natively. Everything below assumes a POSIX shell.

---

## 2. GitHub prep (Team Lead / Navin only)

```bash
# 1. One-time identity (matches your GitHub account)
git config --global user.name  "Navin Jairam"
git config --global user.email "navin.jairam@gmail.com"

# 2. Auth for push: SSH key (recommended) or fine-grained PAT
#    SSH:  ssh-keygen -t ed25519 -C "navin.jairam@gmail.com"  → add pubkey at
#          github.com/settings/ssh/new

# 3. Rename the GitHub repo: Settings → General → Repository name
#        AegisSRE  →  AegisDeploy   (do this BEFORE pushing the rename commits)

# 4. Clone (or pull if you already have the old clone)
git clone git@github.com:Lucifer-Newstar/AegisDeploy.git
cd AegisDeploy
git push origin main          # after rename — pushes all local commits
```

> Team members: fork-and-PR or branch-per-feature against this repo (see
> [contributing.md](contributing.md) for the full workflow).

---

## 3. Python environment (all members)

The repo is a **monorepo of editable packages** — no global installs, one venv.

```bash
cd AegisDeploy

# Option A — uv (fast, recommended)
uv venv .venv --python 3.12
source .venv/bin/activate
uv pip install -e "backend/libs/telemetry[dev]" \
                -e "backend/libs/eventbus[dev]" \
                -e "backend/services/_template[dev]" \
                -e "demoapp/aegisshop/catalog-service[dev]"

# Option B — classic venv + pip
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e "backend/libs/telemetry[dev]" \
             -e "backend/libs/eventbus[dev]" \
             -e "backend/services/_template[dev]" \
             -e "demoapp/aegisshop/catalog-service[dev]"
```

> **Why editable?** The libs (`telemetry`, `eventbus`) are shared contracts —
> services import them live, so changes apply immediately without reinstalls.
> New packages (cart, order, registry, …) get added to this list as they land.

### Verify the toolchain (all green = ready)

```bash
ruff check backend demoapp            # lint          → All checks passed!
mypy backend/libs/telemetry backend/libs/eventbus \
     backend/services/_template demoapp/aegisshop/catalog-service   # → Success
pytest backend/libs/telemetry backend/libs/eventbus \
       backend/services/_template demoapp/aegisshop/catalog-service # → 27 passed
make lint                             # YAML validation
```

---

## 4. Environment variables — the full list

### 4a. The `.env` file (Docker Compose stack)

Copy once from the template — **Compose only** (the Python services do not read
this file; they get their vars from compose directly):

```bash
cp .env.example .env    # then edit passwords if you want non-defaults
```

| Variable | Default | Required? | Used by | Notes |
|---|---|---|---|---|
| `POSTGRES_USER` | `aegis` | optional | postgres container | superuser for the dev DB |
| `POSTGRES_PASSWORD` | `aegis` | optional | postgres container | dev-only credential |
| `POSTGRES_DB` | `aegisdeploy` | optional | postgres container | main platform DB |
| `GRAFANA_ADMIN_USER` | `admin` | optional | grafana container | login user |
| `GRAFANA_ADMIN_PASSWORD` | `aegis` | optional | grafana container | login password (login: `admin`/`aegis`) |

### 4b. Service-level variables (Python services — set by compose, or in your shell when running a service manually)

Defaults live in each service's `config.py`; environment variables **always
win** (ADR-0005: same container in Compose and K8s).

| Variable | Default | Set to (compose/K8s) | Used by | Notes |
|---|---|---|---|---|
| `SERVICE_NAME` | per-service | e.g. `catalog-service` | all services | metric labels, log lines, OTel resource |
| `SERVICE_PORT` | per-service | e.g. `9001` | all services | uvicorn bind port (template says copy per service) |
| `ENVIRONMENT` | `dev` | `dev` (compose) / `prod` (cluster) | all services | OTel resource + structured logs |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | *(empty)* | `http://otel-collector:4317` | all services | **empty = tracing no-op** (safe offline dev); set it to send traces to the collector |

### 4c. GitHub auth (not env vars — but part of setup)

| Item | Where | Notes |
|---|---|---|
| SSH key | `~/.ssh/id_ed25519` + github.com settings | for `git push` |
| PAT (alternative) | github.com → Settings → Developer settings | only if you don't use SSH |

> **No cloud API keys are needed** for local development — the stack is fully
> self-contained (Postgres/Redis/Prometheus/Grafana/Loki/Tempo/OTel in Docker).
> Keys/tokens appear only in P5+ (executors, least-privilege credentials) and
> will be documented then.

---

## 5. Run the local stack

```bash
make infra-up           # docker compose up -d --wait (stack + catalog-service)
docker compose ps       # all services healthy
```

| Service | URL | Login |
|---|---|---|
| Grafana | http://localhost:3000 | `admin` / `aegis` (from `.env`) |
| Prometheus | http://localhost:9090 | — |
| Loki | http://localhost:3100 | — |
| Tempo | http://localhost:3200 | — |
| Catalog API | http://localhost:9001/products | — |

**First-run verification (5 minutes):**
1. `curl localhost:9001/health` → `{"status":"healthy"}`
2. Grafana → dashboards → **"AegisShop — Catalog Service"** → panels populate
   (hit `/products` a few times first: `for i in $(seq 1 20); do curl -s localhost:9001/products > /dev/null; done`)
3. Prometheus → Status → Targets → `aegisshop-catalog` = **UP**
4. Grafana → Explore → Tempo → trace a `/products` request (service: `catalog-service`)
5. `make infra-down` when done (removes volumes too)

---

## 6. Day-to-day loop

```bash
git checkout -b feat/<member>-<area>-<topic>   # e.g. feat/navin-contracts-openapi
# …work…
ruff check backend demoapp && pytest           # quick pre-commit loop
git add -A && git commit -m "feat(...): ..."   # Conventional Commits
git push -u origin feat/…                      # then open a PR into main
```

Full rules: [contributing.md](contributing.md) · [working-rules.md](../team/working-rules.md)

---

## 7. Troubleshooting

| Symptom | Fix |
|---|---|
| `docker compose` errors on start | Docker Desktop not running → start it; `docker info` first |
| Port already in use (3000/9001/…) | `docker ps` → stop the conflicting container, or change the mapped port in `docker-compose.yml` |
| Stack stuck after config change | `make infra-down && make infra-up` (down removes volumes — data resets) |
| `ModuleNotFoundError: telemetry/eventbus` | venv not activated, or re-run the editable installs (§3) |
| `mypy`/`ruff` not found | deps are in the `[dev]` extras — reinstall with `[dev]` |
| Grafana panels empty | Prometheus target down → check `make infra-logs` for the collector/catalog |
| Traces not showing | `OTEL_EXPORTER_OTLP_ENDPOINT` unset in your manual run — tracing is then a no-op by design |
