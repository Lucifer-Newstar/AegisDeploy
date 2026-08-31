# Navin — Phase Plan (Team Lead / SRE / AI-SRE)

> My view of each phase: what I deliver, what I need, what I hand over, and when my
> track is "done". Mirrors [docs/planning/phases.md](../../planning/phases.md).
> As Team Lead I also run the **gate review** for every phase (phases.md §6).

---

## Phase Overview

| Phase | My deliverables | Depends on | Integration output | Done when |
|---|---|---|---|---|
| **P1** | Repo, docs hub, ADRs, planning docs, CI foundation | — | ✅ passed 2026-08-31 | gate passed |
| **P2** | Telemetry envelope v0.1 (Pydantic); event layer design; **API contracts**; architecture refinement; integration protocol | — | Everyone builds against committed contracts | Contracts committed + P2 gate passed |
| **P3** | A3 anomaly detection (statistical baselines + Isolation Forest), feature pipeline, threshold tuning, validation mini-eval | Metric streams (Gokul) | `anomaly.score` events → incident manager | Detection precision/recall ≥ 0.85; gate passed |
| **P4** | A5 evidence collection + RCA engine (hypotheses w/ citations); B1 RAG (pgvector: runbooks, past incidents); B2 Ask Aegis engine (read-only tools) | Incident/evidence APIs (Jega), query proxies (Gokul) | AI reasoning APIs + engine for the UI | RCA accuracy ≥ 70%; gate passed |
| **P5** | A6 policy engine design + risk matrix; A8 safe-auto design + kill switch; A9 verification logic; autonomy docs | Action catalog (with Jega), executors (Gokul) | Policy engine + verification service | Safety violations = 0; gate passed |
| **P6** | SLO definitions (with Gokul); integration lead; autonomy mode documentation | — | SLO dashboards live; product walkthrough | Gate passed |
| **P7** | A11 fault specs + experiment manifests + ground-truth schema; evaluation protocol | Chaoslab impl (Gokul) | 10 injectable faults with labels | Cluster + chaos gate passed |
| **P8** | A12 evaluation lead (baseline vs platform, N≥10/fault); E2 comparison study; thesis report (results chapter) | All members' support | Evaluation report + thesis chapter | Report committed; gate passed |
| **Buffer** | B3 LoRA/QLoRA fine-tune experiment (gated); viva preparation | Core ahead of schedule | Optional MLOps add-on | — |

## My Track's Key Risks

| Risk | Mitigation |
|---|---|
| LLM behavior variance | Evidence-first design: hypotheses must cite telemetry; confidence scores; rule-based RCA fallback scaffolding |
| RAG corpus too small early | Seed with runbooks + fault specs from P2; grow with each incident (E1 dataset) |
| Policy/safety defects | Risk matrix frozen at P5 design; dry-run mode; audit-everything; kill switch |
| Lead bandwidth split (architecture + AI + coordination) | Contracts-first removes blocking; weekly sync keeps coordination cheap; delegate impl to members where sensible |

## Definition of Done (per deliverable)

- [ ] Contract/API documented and committed before consumers start
- [ ] AI outputs cite evidence; no unsupported claims
- [ ] Policies/ADRs reviewed; safety violations = 0
- [ ] Evaluation data reproducible (protocol in operations/evaluation.md)
- [ ] Docs updated (E4); decision log current; gate checklist complete
