# Development Timeline

> The 8–10 month development plan for AegisSRE (started **Aug 2026**; delivery window
> **Apr–Jun 2027**). Four members: Navin (lead), Gokul, Jegatheesan, Dhanush.
> Scope reference: [features.md](features.md). Milestone-level view: [docs/roadmap.md](../roadmap.md).

---

## 1. Planning Assumptions

- ~8 months of *effective* work (Oct–Mar core build), plus buffer for report/viva (Apr–Jun).
- Members work in parallel tracks; the **critical path** (A1→A9→A12) is protected.
- Interface contracts (API schemas, telemetry envelope) are written **first** so
  members never block each other.
- One weekly sync; demo checkpoint at the end of every phase.

---

## 2. Phase Plan

| Phase | Months | Focus | Members | Deliverable / Checkpoint |
|---|---|---|---|---|
| **M1 Foundation** | Aug–Sep | Repo, docs, ADRs, observability stack, CI | Navin | ✅ done (2026-08-31) |
| **M2 Observability + Backend** | Sep–Oct | A1 pipeline, A2 registry/health, demo app scaffold, event layer, envelope v0.1 | Gokul (A1), Jega (A2+demo app), Navin (envelope/event design), Dhanush (console scaffold) | **Checkpoint:** demo app metrics/logs/traces flow into Grafana/Loki/Tempo |
| **M3 Detection + Incidents** | Oct–Nov | A3 anomaly detection, A4 incident manager, demo app instrumented | Navin (A3), Jega (A4), Gokul (data plumbing), Dhanush (service page) | **Checkpoint:** injected fault → anomaly → incident on screen |
| **M4 RCA + AI** | Nov–Dec | A5 evidence+RCA, B1 RAG, B2 Ask Aegis engine | Navin (A5/B1/B2), Dhanush (Ask Aegis UI), Jega (evidence store) | **Checkpoint:** AI explains a fault with cited evidence; chat works |
| **M5 Remediation + Policy** | Dec–Jan | A6 planner+policy, A7 approvals, A8 safe-auto, A9 verification | Jega (A6/A7 impl), Navin (A6/A8/A9 design), Gokul (executors), Dhanush (approval UI) | **Checkpoint:** full approve→execute→verify cycle |
| **M6 Console Complete** | Nov–Jan (parallel) | C1 7 pages, C3 runbooks, C4 postmortem, C5 audit | Dhanush (all), with API support from Jega | **Checkpoint:** every page live from real APIs |
| **M7 K8s + Chaos Lab** | Jan–Feb | D1 Kubernetes, D5 CI/CD, D6 SLO dashboards, A11 chaoslab | Gokul (D1/D5/D6), Navin (A11 design), Jega (fault hooks) | **Checkpoint:** platform + demo app on cluster; 10 fault types injectable |
| **M8 Evaluation** | Feb–Mar | A12 evaluation runs (N≥10/fault), E2 comparison study | Navin (lead), all members run experiments | **Checkpoint:** evaluation report with MTTD/MTTR stats |
| **Report + Demo** | Mar–Apr | Thesis report, demo video, console polish | Navin (report), Dhanush (video), all (support) | **Checkpoint:** submission-ready demo + report |
| **Buffer / Stretch** | Apr–Jun | B3 fine-tune experiment (if approved), viva preparation, E1 dataset release (optional) | Navin (+ Gokul) | Final thesis defense |

---

## 3. Member Calendar

| Month | Navin (Lead / AI-SRE) | Gokul (DevOps) | Jegatheesan (Backend) | Dhanush (Frontend) |
|---|---|---|---|---|
| Sep–Oct | Envelope, event layer design, API contracts | A1 observability pipeline | A2 registry/health, demo app backend | Console scaffold, design system |
| Oct–Nov | A3 anomaly detection | Data plumbing, metrics wiring | A4 incident manager | Service detail page |
| Nov–Dec | A5 RCA, B1 RAG, B2 engine | Chaos hooks prep | Evidence store, incident APIs | Ask Aegis UI, incident page |
| Dec–Jan | A6/A8/A9 design + policy | Executors, safe-auto infra | A6/A7 implementation | Approval UI, runbooks |
| Jan–Feb | A11 fault specs, D6 alerts | D1 K8s, D5 CI/CD, A11 impl | Fault hooks, demo app hardening | Postmortem + audit pages, polish |
| Feb–Mar | A12 evaluation lead, E2 | Experiment runs | Experiment runs | Experiment runs, video support |
| Mar–Apr | Thesis report (results chapter) | Cluster finalization | API docs finalization | Demo video, UI final polish |
| Apr–Jun | B3 (if approved), viva prep | Stretch support | Stretch support | Stretch support |

---

## 4. Milestones (target dates, indicative)

| Milestone | Target | Definition of done |
|---|---|---|
| M1 Foundation | 2026-08-31 ✅ | done |
| M2 Observability + Backend | 2026-10-31 | checkpoint §M2 green |
| M3 Detection + Incidents | 2026-11-30 | checkpoint §M3 green |
| M4 RCA + AI | 2026-12-31 | checkpoint §M4 green |
| M5 Remediation + Policy | 2027-01-31 | checkpoint §M5 green |
| M6 Console Complete | 2027-01-31 | all 7 pages live |
| M7 K8s + Chaos Lab | 2027-02-28 | checkpoint §M7 green |
| M8 Evaluation | 2027-03-31 | report committed |
| Report + Demo | 2027-04-30 | submission-ready |
| Buffer / Viva | 2027-05–06 | defense-ready |

---

## 5. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| LLM/hardware constraints for AI features | Medium | Medium | Local open-weight via Ollama; RAG works with any model; fallback = rule-based RCA scaffolding |
| Integration friction between members | Medium | High | Contracts-first (envelope, API schemas); weekly sync; ADR gate |
| Scope creep during build | High | High | Locked feature list; re-opening requires lead decision (Decision Log) |
| Member availability dips (exams) | Medium | Medium | Parallel tracks; no member is on the critical path alone for >1 phase |
| Demo-app faults not triggering detection | Low | High | Chaoslab faults validated against detection thresholds during M3 |
| Evaluation statistics weak | Low | Medium | N ≥ 10 runs/fault; documented protocol (evaluation.md) |

---

## 6. Cadence

- **Weekly sync (30 min):** each member reports; lead tracks integration matrix.
- **Phase-end demo (60 min):** checkpoint criteria demonstrated, decisions logged.
- **Docs:** every phase ends with docs updated (E4) — no documentation debt carried.
