# Use Case Diagram — AegisShop (Demo Application)

> **Diagram 1b (UML 2.5 — Behavioral).** Use cases of the **AegisShop** demo
> microservices application — the monitored subject of the platform. The AegisDeploy
> platform appears as an **external system** (it observes the app; it does not
> participate in shop functionality). Medium detail (~11 use cases).

```mermaid
---
title: "Use Case Diagram — AegisShop Demo Application"
---
flowchart LR
    %% ═══ ACTORS ═══════════════════════════════════════════
    CUST["🛒 Customer"]                %% primary actor — end user
    STAFF["🧑‍💼 Shop Staff / Admin"]    %% manages catalog & orders
    PG["💳 Payment Gateway"]           %% external payment processor
    AEGIS["🛰️ AegisDeploy Platform"]      %% external system — observes the app

    %% ═══ SYSTEM BOUNDARY ══════════════════════════════════
    subgraph SHOP["AegisShop"]
        direction TB
        AS1("Browse product catalog")
        AS2("Search products")
        AS3("View product details")
        AS4("Add item to cart")
        AS5("Update cart")
        AS6("Place order")
        AS7("Make payment")
        AS8("Track order status")
        AS9("Manage product catalog")
        AS10("Manage orders")
        AS11("Serve telemetry & health")

        %% helper use cases
        VALIDATE("Validate cart")
        PROC("Process payment")
        AUTH("Authenticate")
    end

    %% ═══ ACTOR → USE CASE ASSOCIATIONS ═══════════════════
    CUST --- AS1 & AS2 & AS3 & AS4 & AS5 & AS6 & AS7 & AS8
    STAFF --- AS9 & AS10
    PG -.->|processes| AS7
    AEGIS -.->|consumes| AS11

    %% ═══ INCLUDE / EXTEND RELATIONSHIPS ══════════════════
    AS6 -.->|«include»| VALIDATE
    AS7 -.->|«include»| PROC
    AS9 -.->|«include»| AUTH
    AS10 -.->|«include»| AUTH

    %% ═══ STYLING ═════════════════════════════════════════
    classDef actor fill:#dbeafe,stroke:#2563eb,stroke-width:1.5px,color:#1e3a8a;
    classDef uc fill:#ecfdf5,stroke:#059669,stroke-width:1px,color:#064e3b;
    classDef helper fill:#fef3c7,stroke:#d97706,stroke-width:1px,color:#78350f;
    class CUST,STAFF,PG,AEGIS actor;
    class AS1,AS2,AS3,AS4,AS5,AS6,AS7,AS8,AS9,AS10,AS11 uc;
    class VALIDATE,PROC,AUTH helper;
```

---

## 1. Purpose

Documents the functional requirements of the **demo application** that the platform
monitors and protects. AegisShop exists to be the *test subject* — its fault hooks
(see [phases.md](../../planning/phases.md) §7) make it chaos-ready.

## 2. Actors

| Actor | Type | Description |
|---|---|---|
| **Customer** | Primary | End user of the shop: browses, carts, orders, pays |
| **Shop Staff / Admin** | Secondary | Manages the product catalog and orders |
| **Payment Gateway** | External system | Simulated payment processing (no real money) |
| **AegisDeploy Platform** | External system | Consumes the shop's telemetry/health for monitoring (A1) |

## 3. Use Cases (summary)

| # | Use case | Primary actor | Service (v1) | Chaos relevance |
|---|---|---|---|---|
| 1 | Browse product catalog | Customer | `catalog-service` | — |
| 2 | Search products | Customer | `catalog-service` | CPU saturation target |
| 3 | View product details | Customer | `catalog-service` | latency target |
| 4 | Add item to cart | Customer | `cart-service` | — |
| 5 | Update cart | Customer | `cart-service` | Redis-down target |
| 6 | Place order | Customer | `order-service` | DB-down, faulty-deploy target |
| 7 | Make payment | Customer | `payment-service` | crash, 5xx target |
| 8 | Track order status | Customer | `order-service` | — |
| 9 | Manage product catalog | Staff | `catalog-service` | — |
| 10 | Manage orders | Staff | `order-service` | — |
| 11 | Serve telemetry & health | AegisDeploy | all services | the monitoring contract |

## 4. Include Semantics

| Relationship | Meaning |
|---|---|
| `«include» Validate cart` | Placing an order validates cart contents first |
| `«include» Process payment` | Payment always delegates to the payment gateway |
| `«include» Authenticate` | Staff use cases require authentication (demo-level) |

> AegisShop's fault hooks are the bridge to the chaos lab (A11): each service's
> fault targets are listed in `docs/planning/phases.md` §7.
