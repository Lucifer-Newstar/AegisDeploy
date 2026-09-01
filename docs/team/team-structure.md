# Team Structure

> AegisDeploy is a **four-member final-year team project**. This document defines each
> member's role, primary responsibilities, and repository ownership so that everyone
> knows their lane — and the integration points between lanes.
>
> Maintainer: Member 4 (Team Lead). Updated whenever responsibilities shift.

---

## 1. Members and Roles

> Each member has a **designated planning folder** — see
> [docs/members/](../members/) for per-member phase plans and deliverables.

| # | Member | Role | Primary responsibilities |
|---|--------|------|--------------------------|
| 1 | **Dhanush Kumar S** | Frontend Developer | Frontend application, dashboard, UI/UX, system visualization, incident visualization, AI interaction interfaces |
| 2 | **Jegatheesan K** | Backend Developer | Backend services, APIs, database, authentication/authorization, application business logic, backend integrations |
| 3 | **Gokul J** | DevOps / Cloud Engineer | Docker, CI/CD, cloud infrastructure, Kubernetes, infrastructure automation, deployment, supporting observability infrastructure — works closely with the Team Lead on SRE/monitoring |
| 4 | **Navin Jairam M** | **Team Lead** — SRE / DevOps / Architecture | See §2 below |

---

## 2. Team Lead (Navin Jairam M — Member 4) — Expanded Role

**Primary technical focus:**

- SRE (reliability engineering, incident management, SLOs)
- DevOps & cloud architecture
- System architecture & infrastructure architecture
- Kubernetes
- Observability
- AI-SRE integration & MLOps
- Autonomous remediation
- System integration
- Reliability testing & chaos/failure engineering

**Coordination responsibilities:**

- Owns the overall technical architecture and its documentation
  (`docs/architecture/`, `docs/architecture/adr/`)
- Coordinates technical decisions between the four members (frontend ↔ backend ↔
  DevOps ↔ AI/ML) so components integrate cleanly
- Reviews architecture-impacting changes (ADRs) before merge
- Owns the cross-cutting AI/ML track of the platform (anomaly detection, AI
  reasoning, RAG, autonomous remediation policy)

**Personal learning goal:** build strong practical knowledge in
**SRE + DevOps + Cloud + Architecture**, while also working deeply with the AI/ML
side of the platform.

---

## 3. Repository Ownership

Ownership = primary author/maintainer. "Review" = must approve changes before merge.

| Area | Owner | Reviewer |
|---|---|---|
| `frontend/` | Member 1 | Member 4 |
| `backend/` | Member 2 | Member 4 |
| `infra/` (docker, k8s), `iac/`, `.github/workflows/` | Member 3 | Member 4 |
| `ml/`, `ai/`, `chaoslab/` | Member 4 | Member 2 (integration) |
| `docs/architecture/`, `docs/architecture/adr/` | Member 4 | All (by area) |
| `docs/team/` | Member 4 (maintainer) | All |
| `README.md`, root configs | Member 4 | All |

> Observability configs (`infra/prometheus`, `grafana`, `loki`, `tempo`, `otel`) are a
> **shared area**: Member 3 implements and operates them; Member 4 designs and reviews
> them (they are the core evidence sources for the AI-SRE track).

---

## 4. Coordination Model

1. **Branches & PRs** — every member works on a feature branch
   (`feat/<member>-<area>-<topic>`) and merges via pull request; `main` stays
   always-deployable. See `working-rules.md` §3.
2. **Architecture gate** — any change touching system architecture, interfaces, or the
   tech stack requires an ADR reviewed by the Team Lead (Member 4).
3. **Interface contracts first** — cross-member work starts from the shared contracts
   (API schemas, telemetry envelope in `docs/architecture/telemetry-model.md`), so
   members can build in parallel.
4. **Weekly sync areas** — each member reports on their lane; the lead tracks the
   integration matrix (frontend ↔ API ↔ observability ↔ AI).
