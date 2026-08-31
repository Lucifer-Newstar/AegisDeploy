# Class Diagram — AegisShop (Demo Application)

> **Diagram 2b (UML 2.5 — Structural).** Static structure of the **AegisShop** demo
> microservices application — the monitored subject. Full detail with multiplicity,
> inheritance, composition, and the chaos fault-hook interface. Decided 2026-08-31.

```mermaid
classDiagram
    direction LR

    %% ═══════════════════════════════════════════════════════
    %% SERVICE LAYER
    %% ═══════════════════════════════════════════════════════
    class ShopService {
        <<abstract>>
        +str name
        +str version
        +str health
        +health_check() dict
        +expose_metrics() dict
    }
    class ApiGateway {
        +route(path) Response
        +authenticate(token) bool
        +rate_limit(client) bool
    }
    class CatalogService {
        -list~Product~ products
        +search(query) list~Product~
        +get_product(id) Product
        +add_product(product) void
        +update_product(product) void
    }
    class CartService {
        -RedisClient redis
        +add_item(cart_id, item) Cart
        +update_item(cart_id, item) void
        +get_cart(cart_id) Cart
    }
    class OrderService {
        -PostgresClient db
        +place_order(cart) Order
        +get_order(id) Order
        +update_status(id, status) void
    }
    class PaymentService {
        -PaymentGateway gateway
        +process_payment(order) Payment
        +refund(payment) void
    }

    %% ═══════════════════════════════════════════════════════
    %% DOMAIN ENTITIES
    %% ═══════════════════════════════════════════════════════
    class Product {
        +str id
        +str name
        +float price
        +int stock
        +str category
    }
    class Cart {
        +str id
        +list~CartItem~ items
        +add(item) void
        +update(item) void
        +total() float
    }
    class CartItem {
        +str product_id
        +int quantity
        +float price
    }
    class Order {
        +str id
        +str status
        +list~OrderItem~ items
        +float total
        +datetime created_at
    }
    class OrderItem {
        +str product_id
        +int quantity
        +float price
    }
    class Payment {
        +str id
        +str order_id
        +str status
        +float amount
        +datetime processed_at
    }

    %% ═══════════════════════════════════════════════════════
    %% EXTERNAL & CHAOS INTERFACES
    %% ═══════════════════════════════════════════════════════
    class PaymentGateway {
        <<external>>
        +charge(amount) Receipt
    }
    class FaultHook {
        <<interface>>
        +inject(fault_type) void
        +restore() void
    }

    %% ── Inheritance ────────────────────────────────────────
    ApiGateway <|-- ShopService
    CatalogService <|-- ShopService
    CartService <|-- ShopService
    OrderService <|-- ShopService
    PaymentService <|-- ShopService

    %% ── Realization (chaos readiness) ──────────────────────
    CatalogService ..|> FaultHook
    CartService ..|> FaultHook
    OrderService ..|> FaultHook
    PaymentService ..|> FaultHook
    ApiGateway ..|> FaultHook

    %% ── Composition / association ──────────────────────────
    CatalogService "1" *-- "0..*" Product
    Cart "1" *-- "1..*" CartItem
    Order "1" *-- "1..*" OrderItem
    Order "1" --> "0..1" Payment
    PaymentService "1" --> "1" PaymentGateway
    OrderService "1" --> "1" PostgresClient
    CartService "1" --> "1" RedisClient

    %% ═══════════════════════════════════════════════════════
    %% COLOR CODING
    %% ═══════════════════════════════════════════════════════
    classDef svc fill:#dbeafe,stroke:#2563eb,color:#1e3a8a;
    classDef entity fill:#ecfdf5,stroke:#059669,color:#064e3b;
    classDef ext fill:#f3f4f6,stroke:#6b7280,color:#374151;
    classDef chaos fill:#fef3c7,stroke:#d97706,color:#78350f;
    class ApiGateway,CatalogService,CartService,OrderService,PaymentService,ShopService svc;
    class Product,Cart,CartItem,Order,OrderItem,Payment entity;
    class PaymentGateway ext;
    class FaultHook chaos;
```

---

## 1. Purpose

Static model of the demo application: five FastAPI microservices (see
[phases.md](../../planning/phases.md) §7), their domain entities, external dependency
(payment gateway), and the **FaultHook** interface that makes every service
chaos-ready (A11).

## 2. Service Map (v1)

| Service | Base class | Persistence | Chaos targets |
|---|---|---|---|
| `ApiGateway` | ShopService | — | 5xx injection, traffic spike, latency |
| `CatalogService` | ShopService | in-memory (P2) → Postgres | CPU saturation |
| `CartService` | ShopService | Redis | Redis unavailable |
| `OrderService` | ShopService | Postgres | DB unavailable, faulty deployment |
| `PaymentService` | ShopService | in-memory | container crash, latency |

## 3. Key Relationships

| Relationship | Meaning |
|---|---|
| `ShopService <|-- <service>` | Shared base: name/version/health + telemetry exposure |
| `..|> FaultHook` | Every service implements fault injection + restore (chaos-ready) |
| `Order "1" --> "0..1" Payment` | An order may have zero or one payment (payment optional at demo level) |
| `CatalogService *-- Product` | Composition: catalog owns its products |

## 4. Notes for Implementers

- Services are **OTel-instrumented** — `expose_metrics()` emits the envelope-compliant
  telemetry consumed by A1 (Gokul's pipeline).
- `FaultHook.inject()` is called by the chaos lab only; it is a **demo-only** interface
  and must never be reachable from the public API in a real deployment.
- Postgres/Redis clients are injected (dependency injection) so fault hooks can
  simulate outages of the real dependencies.
