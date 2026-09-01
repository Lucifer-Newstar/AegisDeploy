"""AegisDeploy event layer (Redis Streams — ADR-0004).

One stream per event type (``st:<type>``), consumer groups per logical
consumer, at-least-once delivery with explicit acks. Semantics are defined
in docs/architecture/telemetry-model.md §5.
"""

from eventbus.eventbus import EventBus, stream_name

__all__ = ["EventBus", "stream_name"]
