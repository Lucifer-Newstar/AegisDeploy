# Gokul J — DevOps / Cloud Engineer

> **Member 3** — DevOps / Cloud track.

## Role

Build and operate everything that runs the platform and keeps it observable: the
infrastructure, the pipelines, and the failure laboratory. Works closely with the
Team Lead on SRE / monitoring / reliability.

## Primary responsibilities

- Docker (images, multi-stage builds) & container registry
- CI/CD (GitHub Actions)
- Kubernetes (kind cluster, Kustomize bases per ADR-0005)
- Infrastructure automation; supporting observability infrastructure
- Deployment of platform + AegisShop
- Chaos lab implementation (fault injection)
- Executors infrastructure for remediation actions (least privilege)

## Repo areas owned

- `infra/` (docker, k8s, observability configs), `iac/`, `.github/workflows/`
- `chaoslab/` (implementation)
- `docs/members/gokul-devops/` (this folder)

## Contracts I consume / provide

| Contract | Direction | Counterpart |
|---|---|---|
| Service Dockerfiles & ports | consume | Jega / Navin |
| Action catalog + policy definitions | consume | Navin (P5) |
| Compose + K8s configs (shared with all) | **provide** | everyone |
| Read-only query proxies (AI tool layer) | **provide** | Navin (P4) |
| Executors (restart/rollback/scale, scoped creds) | **provide** | A6/A8 (P5) |
| Chaoslab manifests + ground truth schema | **provide** | Navin (P7) |

## My commitments

- Every Compose service has a healthcheck; images are pinned and multi-stage.
- Configs in `infra/` are shared between Compose and K8s (ADR-0005) — no drift.
- Changes to shared stack land via PRs so nobody's local environment breaks.
