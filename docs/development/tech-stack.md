# Technology Stack

Selected stack for AegisDeploy (Milestone 1 decision). Selections follow the evaluation
criteria in the proposal (§7): resource requirements, compatibility, cost, and project
complexity. Changes to this table must be recorded as ADRs.

## 1. Selected Stack

| Layer | Choice | Rationale | Alternatives considered |
|---|---|---|---|
| Frontend | **Next.js + TypeScript** | Mature React framework, SSR, typed end-to-end, huge ecosystem; aligns with proposal. | React+Vite, Angular |
| Frontend charts | **Recharts / ECharts (assess at M6)** | Lightweight time-series + topology rendering. | Grafana-embed, D3 |
| Backend | **Python 3.12 + FastAPI** | Async, OpenAPI-first, Pydantic v2 for the telemetry contract; single language across backend/ML/AI. | Go, Node.js, Spring |
| Primary DB | **PostgreSQL 16** | Relational core for services/incidents/deployments; **pgvector** doubles as the RAG vector store — one dependency. | MySQL, MongoDB, Qdrant |
| Cache / queue | **Redis 7** | Cache + Redis Streams as the initial Event Layer; one dependency. | NATS, Kafka, RabbitMQ |
| Event Layer | **Redis Streams (initial)** | Zero-extra-dependency dev loop; consumer groups map well to microservices. NATS/Kafka re-evaluated when scale/durability demands (ADR-0004). | NATS JetStream, Kafka |
| Observability | **OpenTelemetry + Prometheus + Grafana + Loki + Tempo** | CNCF standard, works identically in Compose and K8s, proposal-aligned. | ELK, Datadog (proprietary) |
| ML | **scikit-learn, numpy, pandas** | Isolation Forest + statistical baselines for v1 detection; zero GPU needs. | PyTorch (reserved for LoRA experiments) |
| LLM runtime | **Open-weight models via Ollama** (e.g., Qwen/Llama 3 small) | Local, free, reproducible for experiments; fine-tuning with LoRA/QLoRA is an optional later track (hardware permitting). | Cloud API LLMs (cost, data egress) |
| Embeddings / RAG | **sentence-transformers + pgvector** | Local embeddings; vector store inside Postgres. | OpenAI embeddings, Qdrant |
| MLOps | **MLflow** | Experiment tracking + model registry for the anomaly pipeline. | None (keep light) |
| Orchestration | **Docker Compose (dev) → Kubernetes (prod-ready)** | "Compose now, K8s-ready" posture; manifests under `infra/k8s/`. | Docker Swarm |
| IaC | **Terraform** | Cloud provisioning later (e.g., GKE/EKS); structure reserved in `iac/terraform/`. | Pulumi |
| CI/CD | **GitHub Actions** | Repository-native, free for public repos. The CD workflow records **deployment events** to the Deployment Tracker (DI-1) and runs canary releases (DI-6, P7). | GitLab CI, ArgoCD (later) |
| Containerization | **Docker** (multi-stage builds per service) | Standard. | Buildpacks |

## 2. Key Version Pins (as of foundation milestone)

| Component | Version | Notes |
|---|---|---|
| Python | 3.12 | Backend runtime target |
| FastAPI | 0.115.x | |
| PostgreSQL | 16-alpine | + `pgvector` extension when RAG lands |
| Redis | 7-alpine | |
| Prometheus | v2.53.x | |
| Grafana | 11.3.x | |
| Loki | 3.3.x | |
| Tempo | 2.6.x | |
| OTel Collector | 0.109.x (contrib) | |
| Node | 22 LTS | Frontend toolchain |

> Versions are bumped deliberately via PRs, not ad hoc. Compose pins are in
> `docker-compose.yml`; container image tags stay explicit so local and K8s runs match.

## 3. Deferred Decisions (recorded when they arrive)

- **Kubernetes distribution** for evaluation clusters (kind/k3s/minikube) — M7.
- **LLM final model + quantization** — after benchmark of small open-weight models on
  SRE tasks — M4/M5.
- **Terraform cloud provider** — depends on final demo hosting — M7.
- **MLflow deployment mode** — M3.
- **NATS vs Kafka for the Event Layer** at scale — when Redis Streams limits are hit.
- **Canary tooling** (Argo Rollouts vs manual traffic-split analysis) — DI-6, decided at P7; default is a lightweight traffic-split comparison without extra tooling.
