# Development Timeline

> The 8–10 month development calendar for AegisSRE (started **Aug 2026**; delivery window
> **Apr–Jun 2027**). Four members: Navin (lead), Gokul, Jegatheesan, Dhanush.
> Phase definitions, gates & integration checkpoints: [phases.md](phases.md).
> Scope reference: [features.md](features.md). Milestone-level view:
> [docs/project/roadmap.md](../project/roadmap.md).

---

## 1. Planning Assumptions

- ~8 months of *effective* work (Oct–Mar core build), plus buffer for report/viva (Apr–Jun).
- Members work in parallel tracks; the **critical path** (A1→A9→A12) is protected.
- **Phase gates** — a phase ends only when its working increment + integration checkpoint
  pass (see [phases.md](phases.md) §1, §6).
- Interface contracts (API schemas, telemetry envelope) are written **first** so members
  never block each other.
- One weekly sync; integration demo at the end of every phase.

---

## 2. Phase Calendar

| Phase | Months | Focus | Lead member(s) | Checkpoint (end of phase) |
|---|---|---|---|---|
| **P1 Foundation** | Aug–Sep | Repo, docs, ADRs, observability stack, CI | Navin | ✅ done (2026-08-31) |
| **P2 Observability + Demo App v1** | Sep–Oct | A1 pipeline, AegisShop v1, A2 registry, console scaffold | Gokul (A1), Jega (app+registry), Dhanush (scaffold), Navin (contracts) | AegisShop telemetry in Grafana; console + registry live |
| **P3 Detection + Incidents** | Oct–Nov | A3 anomaly detection, A4 incident manager | Navin (A3), Jega (A4) | fault → anomaly → incident demo |
| **P4 AI Reasoning** | Nov–Dec | A5 RCA, B1 RAG, B2 Ask Aegis | Navin (engine), Dhanush (UI), Jega (APIs) | AI explains fault w/ cited evidence; chat works |
| **P5 Remediation + Autonomy** | Dec–Jan | A6 planner/policy, A7 approvals, A8 safe-auto, A9 verification | Jega (impl), Navin (design), Gokul (executors) | approve → execute → verify → close cycle |
| **P6 Console Complete** | Nov–Jan (parallel) | C1 7 pages, C3/C4/C5, D5 CI/CD, D6 SLO dashboards | Dhanush (UI), Gokul (CI/SLO), Jega (API polish) | every page live from real APIs |
| **P7 K8s + Chaos Lab** | Jan–Feb | D1 Kubernetes (kind), A11 chaoslab | Gokul (K8s/chaos), Navin (fault specs) | platform + app on cluster; 10 faults injectable |
| **P8 Evaluation** | Feb–Mar | A12 evaluation runs (N≥10/fault), E2 study | Navin (lead), all members | evaluation report committed |
| **Report + Demo** | Mar–Apr | Thesis report, demo video, polish | Navin (report), Dhanush (video) | submission-ready demo + report |
| **Buffer / Stretch** | Apr–Jun | B3 fine-tune (if approved), viva prep | Navin (+ Gokul) | defense-ready |

---

## 3. Member Calendar

| Month | Navin (Lead / AI-SRE) | Gokul (DevOps) | Jegatheesan (Backend) | Dhanush (Frontend) |
|---|---|---|---|---|
| Sep–Oct | Envelope, event layer design, API contracts | A1 observability pipeline | A2 registry/health, AegisShop backend | Console scaffold, design system |
| Oct–Nov | A3 anomaly detection | Data plumbing, metrics wiring | A4 incident manager | Service detail page |
| Nov–Dec | A5 RCA, B1 RAG, B2 engine | Read-only query proxies | Evidence store, incident APIs | Ask Aegis UI, incident page |
| Dec–Jan | A6/A8/A9 design + policy | Executors, safe-auto infra | A6/A7 implementation | Approval UI, runbooks |
| Jan–Feb | A11 fault specs, D6 alerts | D1 K8s, D5 CI/CD, A11 impl | Fault hooks, app hardening | Postmortem + audit pages, polish |
| Feb–Mar | A12 evaluation lead, E2 | Experiment runs | Experiment runs | Experiment runs, video support |
| Mar–Apr | Thesis report (results chapter) | Cluster finalization | API docs finalization | Demo video, UI final polish |
| Apr–Jun | B3 (if approved), viva prep | Stretch support | Stretch support | Stretch support |

---

## 4. Phase Targets (dates are indicative; gates are hard)

| Phase | Target | Definition of done (gate) |
|---|---|---|
| P1 Foundation | 2026-08-31 ✅ | passed |
| P2 Observability + Demo App v1 | 2026-10-31 | checkpoint §P2 green |
| P3 Detection + Incidents | 2026-11-30 | checkpoint §P3 green |
| P4 AI Reasoning | 2026-12-31 | checkpoint §P4 green |
| P5 Remediation + Autonomy | 2027-01-31 | checkpoint §P5 green |
| P6 Console Complete | 2027-01-31 | all 7 pages live |
| P7 K8s + Chaos Lab | 2027-02-28 | checkpoint §P7 green |
| P8 Evaluation | 2027-03-31 | report committed |
| Report + Demo | 2027-04-30 | submission-ready |
| Buffer / Viva | 2027-05–06 | defense-ready |

---

## 5. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Phase gate slips (feature not ready) | Medium | High | Contracts-first; smallest vertical slice per gate; scope freeze during integration window |
| LLM/hardware constraints for AI features | Medium | Medium | Local open-weight via Ollama; RAG works with any model; fallback = rule-based RCA scaffolding |
| Integration friction between members | Medium | High | Contracts-first; weekly sync; ADR gate; integration protocol (§5 of phases.md) |
| Scope creep during build | High | High | Locked feature list; re-opening requires lead decision (Decision Log) |
| Member availability dips (exams) | Medium | Medium | Parallel tracks; no member is on the critical path alone for >1 phase |
| Demo-app faults not triggering detection | Low | High | Chaoslab faults validated against detection thresholds during P3 |
| Evaluation statistics weak | Low | Medium | N ≥ 10 runs/fault; documented protocol (operations/evaluation.md) |

---

## 6. Cadence

- **Weekly sync (30 min):** each member reports; lead tracks the integration matrix.
- **Phase-end integration demo (60 min):** gate criteria demonstrated; decisions logged.
- **Docs:** every phase ends with docs updated (E4) — no documentation debt carried.
