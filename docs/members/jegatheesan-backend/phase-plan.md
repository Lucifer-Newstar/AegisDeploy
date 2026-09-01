# Jegatheesan — Phase Plan (Backend)

> My view of each phase: what I deliver, what I need, what I hand over, and when my
> track is "done". Mirrors [docs/planning/phases.md](../../planning/phases.md).

---

## Phase Overview

| Phase | My deliverables | Depends on | Integration output | Done when |
|---|---|---|---|---|
| **P2** | Backend service skeleton (API gateway, service registry, health); AegisShop v1 backend services (catalog, cart, order, payment + DB models); shared envelope lib; OpenAPI contracts committed; **DI-1 deploy tracker API** | Envelope v0.1 + event lib (Navin, P2 start) | AegisShop APIs run; registry lists services; OpenAPI published; **deploy events recorded** | Registry + health API pass acceptance (A2); AegisShop services healthy; DI-1 API live |
| **P3** | A4 incident manager (state machine, severity, timeline API); evidence store; incident APIs; fault hooks in AegisShop | Anomaly events (Navin) or test producer | Incident created from injected fault; timeline API live | Fault-to-incident integration demo passes |
| **P4** | Evidence collection APIs for AI tools; incident APIs for the reasoning layer; **deploy history API (DI-3 support)**; AegisShop hardening | — | RCA engine consumes my APIs; incident page data live; **correlation API live** | P4 checkpoint demo passes |
| **P5** | A6 remediation planner implementation; A7 approval workflow API; A9 verification API; audit logging | Policy design (Navin), executors (Gokul) | Approve → execute → verify → close works end-to-end | Full-loop demo passes |
| **P6** | API polish, OpenAPI client regeneration, integration fixes; authN/authZ baseline | — | Frontend fully live on my APIs | Product walkthrough passes |
| **P7** | Fault hooks finalization; backend manifests for K8s (with Gokul); DB migration hardening | Cluster (Gokul) | Backend + AegisShop run on kind | Cluster demo clean |
| **P8** | API documentation finalization; support evaluation runs | — | Docs complete; runs stable | Report + demo done |

## My Track's Key Risks

| Risk | Mitigation |
|---|---|
| Incident state machine complexity | Model on the envelope contract; unit tests per transition; timeline events append-only |
| API contract churn | Contracts-first + OpenAPI as artifact; breaking changes need lead sign-off |
| AegisShop scope creep | Only the 5 services in phases.md §7; faults defined by Navin's specs |
| DB schema changes late | Migrations versioned from P2; envelope JSONB for evidence |

## Definition of Done (per service/feature)

- [ ] OpenAPI contract committed before implementation of consumers
- [ ] Pydantic models reuse the envelope (no bespoke shapes)
- [ ] Health endpoint + OTel metrics/logs/traces
- [ ] Unit tests; CI green; code commented (rule 3)
- [ ] This file updated; features.md acceptance criteria met
