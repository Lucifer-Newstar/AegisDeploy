# ADR-0005: Compose Now, Kubernetes-Ready

- **Status:** Accepted
- **Date:** 2026-08-31
- **Deciders:** Navin Jairam, Arena Agent

## Context

The platform must be developed and tested quickly on a laptop, but the proposal
requires Kubernetes orchestration and a controlled failure laboratory (chaoslab) that
will eventually run workloads in a cluster. Running a full cluster locally from day one
slows iteration; developing without any K8s story invites a painful migration later.

## Decision

Adopt a **"Compose now, Kubernetes-ready"** posture:

1. Local development runs on **Docker Compose** (`docker-compose.yml` at repo root).
2. Every service/config in Compose has a **1:1 Kustomize base** in `infra/k8s/base/`
   (same image tags, same env names, same ports/probes) so cluster deployment is
   mechanical, not a rewrite.
3. Shared configuration lives in `infra/` and is mounted by both runtimes
   (Prometheus/Loki/Tempo/OTel configs; future: policies, dashboards).
4. Kubernetes becomes the primary runtime in the chaos-lab milestone (M7); until then
   K8s manifests stay green via CI linting (kubeconform) even if not deployed.
5. Container images must be **architecture-independent and size-conscious** from the
   start (multi-stage builds), since they will run on a cluster later.

## Consequences

### Positive

- Fast local loop with Compose; no cluster expertise required for daily work.
- K8s migration risk is minimized because the manifests are exercised from the start.
- Observability configs are identical in both runtimes — dashboards, alerts, and
  queries behave the same.

### Negative / Trade-offs

- Some duplication between Compose and Kustomize manifests; mitigated by shared
  config files and by keeping compose files thin.
- Compose and K8s differ in networking/service discovery; services must use env-driven
  endpoints (no hardcoded `localhost`) from day one — enforced by CI linting.

## Alternatives Considered

| Option | Why rejected |
|---|---|
| Full Kubernetes from day one (kind/k3s on laptop) | Slower iteration; heavier toolchain; not needed until chaoslab workloads. |
| Compose only, "deal with K8s later" | Migration becomes a rewrite; config drift between runtimes. |
