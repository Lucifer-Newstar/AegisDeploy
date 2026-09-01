# Use Case Diagram — AegisDeploy Platform

> **Diagram 1a (UML 2.5 — Behavioral).** Shows what the AegisDeploy platform does *for
> whom*. The AegisShop demo application is an **external system** (the monitored
> subject), not part of the platform. Medium detail (~18 use cases) with
> include/extend relationships. Decided 2026-08-31.

```mermaid
---
title: "Use Case Diagram — AegisDeploy Platform"
---
flowchart LR
    %% ═══ ACTORS ═══════════════════════════════════════════
    SRE["🧑‍💻 SRE Engineer"]            %% primary actor
    ADMIN["🛡️ Admin / Team Lead"]       %% governance actor
    DEVOPS["🔧 DevOps Engineer"]        %% platform operations actor
    SHOP["🏪 AegisShop (monitored app)"] %% external system under monitoring
    K8S["☸️ Kubernetes Cluster"]        %% external system that executes actions
    NOTIF["🔔 Notification Service"]    %% external system receiving alerts

    %% ═══ SYSTEM BOUNDARY ══════════════════════════════════
    subgraph AEGIS["AegisDeploy Platform"]
        direction TB

        %% ── SRE-facing use cases ─────────────────────────
        UC1("Monitor service health")
        UC2("View live telemetry")
        UC3("View incident timeline")
        UC4("Review AI root-cause analysis")
        UC5("Approve remediation action")
        UC6("Reject / defer remediation")
        UC7("Chat with Ask Aegis")
        UC8("View & generate postmortem")
        UC9("Manage runbooks")
        UC10("View audit log")

        %% ── Admin-facing use cases ───────────────────────
        UC11("Manage users & roles")
        UC12("Configure autonomy mode")
        UC13("Define remediation policies")

        %% ── DevOps-facing use cases ──────────────────────
        UC14("Register & manage services")
        UC15("Configure SLOs")
        UC16("Trigger chaos experiment")

        %% ── System-driven use cases ──────────────────────
        UC17("Execute safe autonomous action")
        UC18("Notify on incident")

        %% ── Included / extended helper use cases ─────────
        AUTH("Authenticate")
        EVID("Collect evidence")
        IMPACT("Review impact summary")
        VERIFY("Verify recovery")
    end

    %% ═══ ACTOR → USE CASE ASSOCIATIONS ═══════════════════
    SRE --- UC1 & UC2 & UC3 & UC4 & UC5 & UC6 & UC7 & UC8 & UC9 & UC10
    ADMIN --- UC10 & UC11 & UC12 & UC13
    DEVOPS --- UC14 & UC15 & UC16
    SHOP -.->|observes| UC1
    SHOP -.->|telemetry| UC2
    K8S -.->|executes on| UC16
    K8S -.->|executes on| UC17
    NOTIF --- UC18

    %% ═══ INCLUDE / EXTEND RELATIONSHIPS ══════════════════
    UC4 -.->|«include»| EVID
    UC7 -.->|«include»| EVID
    UC5 -.->|«include»| IMPACT
    UC5 -.->|«extend»| VERIFY
    UC17 -.->|«extend»| VERIFY
    UC11 -.->|«include»| AUTH
    UC12 -.->|«include»| AUTH
    UC13 -.->|«include»| AUTH

    %% ═══ STYLING ═════════════════════════════════════════
    classDef actor fill:#dbeafe,stroke:#2563eb,stroke-width:1.5px,color:#1e3a8a;
    classDef uc fill:#ecfdf5,stroke:#059669,stroke-width:1px,color:#064e3b;
    classDef helper fill:#fef3c7,stroke:#d97706,stroke-width:1px,color:#78350f;
    class SRE,ADMIN,DEVOPS,SHOP,K8S,NOTIF actor;
    class UC1,UC2,UC3,UC4,UC5,UC6,UC7,UC8,UC9,UC10,UC11,UC12,UC13,UC14,UC15,UC16,UC17,UC18 uc;
    class AUTH,EVID,IMPACT,VERIFY helper;
```

---

## 1. Purpose

Documents the **functional requirements** of the AegisDeploy platform from the user's
perspective: who interacts with the system and which capabilities each actor uses.
This is the requirements-level contract that the class diagram (Diagram 2) and the
phase plan (P2–P8) refine.

## 2. Actors

| Actor | Type | Description |
|---|---|---|
| **SRE Engineer** | Primary | Day-to-day user: monitors services, investigates incidents, reviews AI analysis, approves/rejects remediations, uses Ask Aegis, manages runbooks |
| **Admin / Team Lead** | Primary | Governance: user/role management, autonomy mode, remediation policies, audit visibility |
| **DevOps Engineer** | Primary | Platform operations: service registration, SLO configuration, chaos experiments |
| **AegisShop** | External system | The monitored application (demo subject) — source of telemetry |
| **Kubernetes Cluster** | External system | Executes chaos experiments and remediation actions (restart/rollback/scale) |
| **Notification Service** | External system | Receives incident notifications (P2 stretch: webhook/email) |

## 3. Use Cases (summary)

| # | Use case | Primary actor | Phase | Notes |
|---|---|---|---|---|
| 1 | Monitor service health | SRE | P2 | live health grid (A2) |
| 2 | View live telemetry | SRE | P2 | metrics/logs/traces (A1) |
| 3 | View incident timeline | SRE | P3 | full lifecycle timeline (A4) |
| 4 | Review AI root-cause analysis | SRE | P4 | evidence-cited hypotheses (A5) |
| 5 | Approve remediation action | SRE | P5 | Level 4 governance (A7) |
| 6 | Reject / defer remediation | SRE | P5 | with reason (A7) |
| 7 | Chat with Ask Aegis | SRE | P4 | read-only tools + citations (B2) |
| 8 | View & generate postmortem | SRE | P4 | AI-generated on close (A5) |
| 9 | Manage runbooks | SRE | P4 | markdown corpus (B1/C3) |
| 10 | View audit log | SRE, Admin | P5 | append-only trail (C5) |
| 11 | Manage users & roles | Admin | P6 | authN/authZ baseline |
| 12 | Configure autonomy mode | Admin | P5 | kill switch: observe/recommend/approval/safe-auto (A8) |
| 13 | Define remediation policies | Admin | P5 | risk classes, approval matrix (A6) |
| 14 | Register & manage services | DevOps | P2 | service registry (A2) |
| 15 | Configure SLOs | DevOps | P6 | SLO + burn rate (D6) |
| 16 | Trigger chaos experiment | DevOps | P7 | fault injection (A11) |
| 17 | Execute safe autonomous action | System | P5 | Level 5 low-risk actions (A8) |
| 18 | Notify on incident | System | P2+ | notification hook (C6 cut — optional) |

## 4. Include / Extend Semantics

| Relationship | Meaning |
|---|---|
| `«include» Authenticate` | Admin use cases always require authentication |
| `«include» Collect evidence` | RCA review and Ask Aegis both fetch telemetry evidence |
| `«include» Review impact summary` | Approving requires an impact summary |
| `«extend» Verify recovery` | After an approval-driven or autonomous action, recovery is verified (A9) |
