# ADR-0004: Redis Streams as Initial Event Layer

- **Status:** Accepted
- **Date:** 2026-08-31
- **Deciders:** Navin Jairam, Arena Agent

## Context

Producers (telemetry, deployments, chaoslab, ML) must publish events consumed by
multiple consumers (incident manager, anomaly pipeline, AI reasoning, audit). The
event layer must support at-least-once delivery, consumer groups, and replay of
business events. It should add zero new infrastructure during development.

## Decision

**Redis Streams** is the initial event layer, with one stream per event type
(`st:metric`, `st:anomaly`, `st:incident`, ...), consumer groups per logical consumer,
and per-stream retention TTLs. See `docs/architecture/telemetry-model.md` §5 for semantics.

Re-evaluate when one of the following triggers is hit:

1. sustained throughput exceeding Redis Streams capacity, or
2. need for long-term replay/retention beyond Postgres-archived business events, or
3. multi-node durability requirements.

At that point, revisit **NATS JetStream** (low ops, similar semantics) or **Kafka**
(heaviest, most mature). This decision is revisited in an ADR, not silently.

## Consequences

### Positive

- Zero extra infrastructure in dev (Redis already required).
- Consumer groups + pending-entry lists give at-least-once delivery and simple
  ack/retry semantics.
- Streams are observable and debuggable with `redis-cli XRANGE`.

### Negative / Trade-offs

- Redis is an in-memory store: retention is bounded and durability is weaker than
  Kafka/NATS. Mitigation: business-critical events (incidents, remediations, audit)
  are also persisted to Postgres; streams only need to be fast and short-lived.
- No native partitioning; fine at this scale.
