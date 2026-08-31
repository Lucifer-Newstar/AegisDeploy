# Profile Diagram — AegisSRE UML Extension

> **Diagram 8 (UML 2.5 — Structural).** The **profile** (stereotype extension) used
> across this UML set: every stereotype applied in Diagrams 2–7, with its base UML
> metaclass, tagged values, and constraints. This is the project's own modeling
> convention, kept consistent so the whole set reads as one language. Decided 2026-08-31.

```mermaid
---
title: "Profile — Stereotypes used in the AegisSRE UML set"
---
classDiagram
    direction LR

    %% ═══════════════════════════════════════════════════════
    %% BASE UML METACLASSES
    %% ═══════════════════════════════════════════════════════
    class CompMC {
        <<metaclass>>
        Component
    }
    class NodeMC {
        <<metaclass>>
        Node
    }
    class ClassMC {
        <<metaclass>>
        Class
    }
    class ArtMC {
        <<metaclass>>
        Artifact
    }
    class DevMC {
        <<metaclass>>
        Device
    }
    class EnumMC {
        <<metaclass>>
        Enumeration
    }
    class IfMC {
        <<metaclass>>
        Interface
    }

    %% ═══════════════════════════════════════════════════════
    %% STEREOTYPES (extends base metaclasses)
    %% ═══════════════════════════════════════════════════════
    class CompS {
        <<stereotype>>
        +str layer
        +int port
        +int replicas
    }
    class ExtS {
        <<stereotype>>
        +str system
    }
    class InfraS {
        <<stereotype>>
    }
    class DevS {
        <<stereotype>>
        +str os
    }
    class NodeS {
        <<stereotype>>
        +int replicas
        +str resources
    }
    class ArtS {
        <<stereotype>>
        +str version
        +str registry
    }
    class EnumS {
        <<stereotype>>
        +list~str~ values
    }
    class IfS {
        <<stereotype>>
        +str protocol
        +int port
    }
    class AbsS {
        <<stereotype>>
    }
    class MetaS {
        <<stereotype>>
    }
    class SterS {
        <<stereotype>>
        +str base
        +list~str~ tagged_values
    }

    %% ═══════════════════════════════════════════════════════
    %% «extend» RELATIONSHIPS (stereotype → metaclass)
    %% ═══════════════════════════════════════════════════════
    CompS ..>|«extend»| CompMC
    ExtS ..>|«extend»| CompMC
    InfraS ..>|«extend»| CompMC
    DevS ..>|«extend»| DevMC
    NodeS ..>|«extend»| NodeMC
    ArtS ..>|«extend»| ArtMC
    EnumS ..>|«extend»| EnumMC
    IfS ..>|«extend»| IfMC
    AbsS ..>|«extend»| ClassMC
    MetaS ..>|«extend»| ClassMC
    SterS ..>|«extend»| ClassMC

    %% ═══════════════════════════════════════════════════════
    %% CONSTRAINTS (notes)
    %% ═══════════════════════════════════════════════════════
    note for CompS "constraint: 1 component = 1 Kustomize base (ADR-0005)"
    note for ExtS "constraint: read-only — never holds write tools (AI boundary)"
    note for ArtS "constraint: image tags are always pinned"
    note for EnumS "constraint: values are DB-checked at ingestion"

    %% ═══════════════════════════════════════════════════════
    %% COLOR CODING
    %% ═══════════════════════════════════════════════════════
    classDef meta fill:#f3f4f6,stroke:#6b7280,color:#374151;
    classDef stereo fill:#ede9fe,stroke:#7c3aed,color:#4c1d95;
    class CompMC,NodeMC,ClassMC,ArtMC,DevMC,EnumMC,IfMC meta;
    class CompS,ExtS,InfraS,DevS,NodeS,ArtS,EnumS,IfS,AbsS,MetaS,SterS stereo;
```

---

## 1. Stereotype Inventory

| Stereotype | Base metaclass | Tagged values | Used in diagrams |
|---|---|---|---|
| `«component»` | Component | `layer`, `port`, `replicas` | 5, 6, 7 |
| `«external»` | Component | `system` | 1a, 1b, 5, 6, 7 |
| `«infra»` | Component | — | 5, 7 |
| `«device»` | Device | `os` | 7 |
| `«node»` | Node | `replicas`, `resources` | 7 |
| `«artifact»` | Artifact | `version`, `registry` | 7 |
| `«enum»` | Enumeration | `values` | 2a, 2b |
| `«interface»` | Interface | `protocol`, `port` | 5, 6 |
| `«abstract»` | Class | — | 2a, 2b |
| `«metaclass»` | Class | — | this profile |
| `«stereotype»` | Class | `base`, `tagged_values` | this profile |

## 2. Constraints (enforced by convention)

| Constraint | Meaning |
|---|---|
| `1 component = 1 Kustomize base` | Compose/K8s parity (ADR-0005) — every `«component»` appears in `infra/k8s/base/` |
| **read-only externals** | `«external»` systems that the AI touches are **read-only**; no write tools (autonomy-model.md §3) |
| **pinned artifacts** | `«artifact»` image tags are pinned in compose/K8s — no `latest` |
| **DB-checked enums** | `«enum»` values validated at telemetry ingestion (envelope contract) |

## 3. Application Rule

When modeling in this project: **prefer these stereotypes over ad-hoc labels**. If a
new stereotype is needed (e.g., `«runbook»`), it must be added to this profile first
and referenced in the diagram that uses it.
