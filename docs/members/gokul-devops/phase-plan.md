# Gokul — Phase Plan (DevOps / Cloud)

> My view of each phase: what I deliver, what I need, what I hand over, and when my
> track is "done". Mirrors [docs/planning/phases.md](../../planning/phases.md).

---

## Phase Overview

| Phase | My deliverables | Depends on | Integration output | Done when |
|---|---|---|---|---|
| **P2** | A1 observability pipeline: OTel configs, Prometheus/Loki/Tempo wiring, Grafana dashboards; compose additions for AegisShop; Dockerfiles for services | — (stack exists) | AegisShop telemetry visible in Grafana/Loki/Tempo | P2 gate: telemetry in Grafana < 60 s |
| **P3** | Metrics plumbing for the anomaly pipeline; alert/health wiring; mini-fault validation runs | Detector API (Navin) | Anomaly pipeline receives clean metric streams | Fault → anomaly validation passes |
| **P4** | Read-only query proxies for AI tools (metrics/logs/traces/k8s with least privilege); Grafana evidence dashboards | — | RCA engine tools operational | P4 checkpoint demo passes |
| **P5** | Executors infra (restart/**rollback**/scale with scoped credentials, dry-run mode); autonomy-mode support; **DI-5 rollback execution** | Action catalog + policies (Navin) | Safe execution path works end-to-end; **safe auto-rollback works** | Full-loop demo passes |
| **P6** | D5 CI/CD full pipeline (test, lint, build, images); D6 SLO dashboards + burn-rate alerts (with Navin); **DI-7 CFR dashboards** | Services | CI green on every PR; SLO + CFR panels live | Product walkthrough passes |
| **P7** | D1 kind cluster + Kustomize bases for every service; A11 chaoslab implementation + experiment manifests; **DI-6 canary deployment + analysis** | Fault specs (Navin), fault hooks (Jega) | Whole platform + AegisShop on kind; 10 faults injectable; **canary analyzed** | Cluster + chaos checkpoint passes |
| **P8** | Cluster stability for evaluation runs; support experiment execution | — | N≥10 runs per fault complete | Evaluation report done |

## My Track's Key Risks

| Risk | Mitigation |
|---|---|
| Cluster/CI flakiness eats time | kind is fast + reproducible; CI jobs timeboxed; k3s fallback |
| Config drift Compose vs K8s | Shared `infra/` configs; kubeconform lint in CI; ADR-0005 discipline |
| Executor safety (least privilege) | Scoped credentials only; dry-run mode; audit logging mandatory (A8) |
| Chaoslab nondeterminism | Experiment manifests with fixed durations + automatic state restore |

## Definition of Done (per deliverable)

- [ ] Configs live in `infra/` and are mounted by the runtime (Compose/K8s)
- [ ] Images pinned + healthchecked; compose validated by CI
- [ ] Executors logged to audit store; no admin credentials in AI layer
- [ ] Docs updated (runbooks/ops notes) + this file updated
- [ ] CI green; code/comments per rule 3
