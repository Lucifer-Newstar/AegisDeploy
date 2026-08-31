# Kubernetes deployment (K8s-ready posture)

Per **ADR-0005**, the platform is developed with Docker Compose but structured to be
Kubernetes-ready: every service has (or will have) a 1:1 Kustomize base in `base/`,
using the same image tags, environment variable names, and config mounts as Compose.

## Current state (M1)

- `base/kustomization.yaml` is the anchor; manifests land incrementally as services
  are implemented (M2+).
- CI lints every manifest in this directory with kubeconform.

## Conventions

- One manifest per workload/statefulset + matching Service.
- Config maps mount the exact files under `infra/` (same content as Compose mounts).
- Environment comes from env vars / secrets — never hardcoded endpoints
  (service discovery differs from Compose DNS).
- Overlays (e.g., `overlays/dev/`, `overlays/prod/`) add per-environment patches.

## Preview of mapping (as components land)

| Compose service | K8s resource |
|---|---|
| postgres | StatefulSet + Service `postgres` |
| redis | StatefulSet + Service `redis` |
| prometheus | Deployment/StatefulSet + Service `prometheus` |
| grafana | Deployment + Service `grafana` |
| loki | StatefulSet + Service `loki` |
| tempo | StatefulSet + Service `tempo` |
| otel-collector | Deployment + Service `otel-collector` |
