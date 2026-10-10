# Gokul · Work log

> Dated record of DevOps / observability delivery. Keep newest entries at the bottom.

| Date | What I shipped | Notes |
|---|---|---|
| 2026-09-10 | Prometheus scrape jobs for P2 services | Replaced the `:8000` backend placeholder that could never come up. |
| 2026-09-16 | Grafana **AegisShop — Overview** dashboard | Request rate and p95 by `service` label. Catalog dashboard kept. |
| 2026-09-29 | Compose wiring for registry, deployments, cart, order, payment, console | Same env names as K8s (ADR-0005). |
| 2026-10-03 | Kustomize bases for P2 services + console | kubeconform + `kustomize build` cover the new manifests. |
| 2026-10-06 | CI container builds for catalog + registry | Frontend build job enabled separately. |
| 2026-10-10 | OTLP log export + Loki logs dashboard; console wired to live APIs in Compose | Completes A1 logs path for the P2 services. |
