"""Redis Streams event bus — producer/consumer wrapper (ADR-0004).

Design
------
* ``publish(envelope)`` → ``XADD st:<type>`` with the envelope JSON as the
  message body. Streams are created on demand.
* Consumers use **consumer groups** (``XGROUP CREATE ... MKSTREAM``) for
  at-least-once delivery: each group sees every message once, and unacked
  messages stay in the pending list for retry.
* Consumers must be **idempotent on ``envelope.id``** — the same message can
  be redelivered after a crash (at-least-once semantics).
* Per-stream retention TTLs (``stream_ttls``) bound memory usage; business-
  critical events are also persisted to Postgres by their consumers.

References: ADR-0004, docs/architecture/telemetry-model.md §5.
"""

from __future__ import annotations

from redis import Redis
from telemetry import EventEnvelope


def stream_name(event_type: str) -> str:
    """Canonical Redis stream name for an event type (e.g. ``st:anomaly``)."""
    return f"st:{event_type}"


class EventBus:
    """Thin, typed wrapper over Redis Streams for AegisDeploy events.

    Args:
        redis_url: redis://[user]:[pass]@host:port/db connection URL.
        stream_ttls: optional mapping of stream name → retention seconds
            (e.g. ``{"st:metric": 3600}``). Applied with ``XTRIM MAXLEN``
            approximations on publish; a background trimmer can be added later.
    """

    def __init__(self, redis_url: str, stream_ttls: dict[str, int] | None = None) -> None:
        self._redis = Redis.from_url(redis_url, decode_responses=True)
        self._stream_ttls: dict[str, int] = stream_ttls or {}

    # ── Producer side ─────────────────────────────────────────────────────────

    def publish(self, envelope: EventEnvelope) -> str:
        """Append an event to its stream and return the stream message id.

        The envelope is serialized with ``model_dump_json`` so payloads keep
        their typed structure; consumers parse them back into envelopes.
        """
        stream = stream_name(envelope.type)
        raw_id = self._redis.xadd(stream, {"envelope": envelope.model_dump_json()})
        self._trim(stream)
        # decode_responses=True returns str; bytes possible in edge configs.
        return raw_id.decode() if isinstance(raw_id, bytes) else raw_id

    def _trim(self, stream: str) -> None:
        """Best-effort retention: keep recent messages when a TTL is configured."""
        ttl = self._stream_ttls.get(stream)
        if ttl:
            # Approximate trim by maxlen; a time-based trimmer can refine this.
            self._redis.xtrim(stream, maxlen=ttl, approximate=True)

    # ── Consumer side ─────────────────────────────────────────────────────────

    def ensure_group(self, event_type: str, group: str) -> None:
        """Create a consumer group for an event type (idempotent).

        ``MKSTREAM`` creates the stream if it does not exist yet, and
        ``BUSGROUP`` errors are swallowed so repeated calls are safe.
        """
        stream = stream_name(event_type)
        try:
            self._redis.xgroup_create(stream, group, id="0", mkstream=True)
        except Exception as exc:  # redis.exceptions.ResponseError: BUSGROUP/BUSYGROUP
            # Real Redis says "BUSGROUP", fakeredis says "BUSYGROUP" — cover both.
            if "BUSGROUP" not in str(exc) and "BUSYGROUP" not in str(exc):
                raise

    def read(self, event_type: str, group: str, consumer: str, count: int = 10, block_ms: int = 1000) -> list[tuple[str, EventEnvelope]]:
        """Read up to ``count`` pending messages for a group/consumer.

        Returns a list of ``(stream_message_id, envelope)``. Callers must
        ``ack`` each message after processing it (at-least-once semantics).
        """
        stream = stream_name(event_type)
        self.ensure_group(event_type, group)
        raw = self._redis.xreadgroup(group, consumer, {stream: ">"}, count=count, block=block_ms)
        messages: list[tuple[str, EventEnvelope]] = []
        if not raw:
            return messages
        # Defensive shape checks: redis-py's stub types are loose, and the
        # wire format is list[(stream, [(id, fields), ...]), ...].
        for item in raw:
            if not isinstance(item, (list, tuple)) or len(item) != 2:
                continue
            _stream, entries = item
            for entry in entries or []:
                if not isinstance(entry, (list, tuple)) or len(entry) != 2:
                    continue
                message_id, fields = entry
                envelope = EventEnvelope.model_validate_json(str(fields["envelope"]))
                messages.append((str(message_id), envelope))
        return messages

    def ack(self, event_type: str, group: str, message_id: str) -> None:
        """Acknowledge a processed message (removes it from the pending list)."""
        self._redis.xack(stream_name(event_type), group, message_id)

    # ── Diagnostics ───────────────────────────────────────────────────────────

    def stream_length(self, event_type: str) -> int:
        """Number of messages currently in a stream (useful for tests/debug)."""
        return int(self._redis.xlen(stream_name(event_type)))

    def pending_count(self, event_type: str, group: str) -> int:
        """Number of unacked messages for a group (redelivery backlog)."""
        stream = stream_name(event_type)
        if not self._redis.exists(stream):
            return 0
        info = self._redis.xpending(stream, group)
        return int(info.get("pending", 0)) if info else 0
