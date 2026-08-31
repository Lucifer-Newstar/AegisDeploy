# Roadmap

Milestone plan for AegisSRE. Each milestone ends with a commit-able, demonstrable
increment on `main`. Dates are indicative.

## M1 — Foundation (current)
- [x] Repository layout + `.gitignore` + editorconfig
- [x] Project docs: proposal, architecture, tech stack, autonomy model, telemetry model, evaluation
- [x] ADRs 0001–0005 (+ template)
- [x] Docker Compose stack: Postgres, Redis, Prometheus, Grafana, Loki, Tempo, OTel Collector
- [x] Observability configs (Prometheus, Loki, Tempo, OTel, Grafana provisioning)
- [x] GitHub Actions CI: compose validation, YAML lint, docs build
- [ ] Kustomize base skeletons under `infra/k8s/base/` (CI-linted)
- [ ] Terraform skeleton under `iac/terraform/`

## M2 — Observability & Backend
- [ ] FastAPI service skeleton: API gateway, service registry, telemetry ingestion
- [ ] Telemetry envelope v0.1 (Pydantic models) shared across services
- [ ] Event layer (Redis Streams) producer/consumer scaffolding
- [ ] Deployment tracker (records deploys as first-class events)
- [ ] AuthN/AuthZ baseline + audit logging
- [ ] Compose services wired into the stack; health endpoints

## M3 — Anomaly Detection
- [ ] Metric feature engineering pipeline (rolling windows, rates, residuals)
- [ ] Statistical baseline detectors (z-score, EWMA)
- [ ] Isolation Forest detector + threshold tuning
- [ ] Anomaly score events → event layer
- [ ] MLflow experiment tracking
- [ ] Precision/recall/F1 evaluation on chaoslab-generated data (first pass)

## M4 — Incidents & Root-Cause Analysis
- [ ] Incident manager: state machine, severity, correlation of anomalies
- [ ] Evidence store + attachment of telemetry to incidents
- [ ] AI reasoning service: read-only tools (metrics/logs/traces/k8s/deployments)
- [ ] RAG pipeline: runbooks + past incidents → pgvector, retrieval
- [ ] Root-cause hypothesis generation with evidence citations
- [ ] Incident timeline API for the dashboard

## M5 — Remediation & Policy Engine
- [ ] Remediation planner (root cause → candidate actions)
- [ ] Policy engine: declarative policies, risk classes, approval matrix
- [ ] Human approval workflow (API + UI)
- [ ] Safe autonomous execution for low-risk reversible actions
- [ ] Recovery verifier (health/error/latency/SLO checks)
- [ ] Audit trail completeness; autonomy kill-switch

## M6 — Dashboard
- [ ] Next.js app: service health, telemetry views, incident list/detail
- [ ] Incident timeline with AI reasoning trail and evidence
- [ ] Approval UI (approve/reject/defer), autonomy-mode control
- [ ] MTTD/MTTR panels; postmortem view

## M7 — Chaos Lab & K8s
- [ ] Chaoslab: fault injection manifests (CPU, memory, crash, DB down, latency, 5xx, bad deploy, traffic spike)
- [ ] Kubernetes as primary runtime; Kustomize bases promoted to deployed state
- [ ] Objective evaluation runs (N≥5 per fault type) vs. baseline workflow
- [ ] SRE telemetry/incident dataset export (project contribution #2)

## M8 — Evaluation & Final Demo
- [ ] Full pipeline demo: inject failure → detect → investigate → RCA → remediate → verify → close → postmortem
- [ ] Metrics report (MTTD/MTTR reduction, RCA accuracy, autonomy success rates)
- [ ] Postmortem generation polish; final documentation pass
- [ ] Presentation materials
