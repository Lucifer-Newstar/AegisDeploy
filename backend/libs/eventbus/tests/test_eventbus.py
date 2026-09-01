"""Tests for the Redis Streams event bus (ADR-0004 semantics).

Uses ``fakeredis`` so the tests run without a live Redis server — the fake
implements the XADD/XGROUP/XREADGROUP/XACK surface we rely on.
"""

# fakeredis exposes a redis-py-compatible client
from typing import Any

import fakeredis  # noqa: E402
import pytest
from eventbus import EventBus, stream_name
from telemetry import EventEnvelope, anomaly_payload


@pytest.fixture()
def bus(monkeypatch: pytest.MonkeyPatch) -> EventBus:
    """An EventBus wired to an in-memory fake Redis server."""
    fake = fakeredis.FakeRedis(decode_responses=True)
    monkeypatch.setattr("eventbus.eventbus.Redis.from_url", classmethod(lambda cls, *a, **k: fake))
    return EventBus("redis://localhost:6379/0")


def sample_envelope(**overrides: Any) -> EventEnvelope:
    """A minimal valid anomaly envelope for bus tests."""
    base: dict[str, Any] = {
        "id": "evt_01J8B1",
        "source": "ml",
        "type": "anomaly",
        "service": "catalog-service",
        "payload": anomaly_payload(
            metric="http_server_request_duration_seconds_p95",
            labels={"service": "catalog-service"},
            score=0.97,
            threshold=0.9,
            model="isolation-forest-v1",
            window={"start": "2026-09-01T10:10:00Z", "end": "2026-09-01T10:15:00Z"},
            baseline={"mean": 0.35, "std": 0.08},
        ),
    }
    base.update(overrides)
    return EventEnvelope(**base)


class TestPublish:
    """Producer semantics."""

    def test_publish_appends_to_typed_stream(self, bus: EventBus) -> None:
        """A publish lands on ``st:<type>`` (here: st:anomaly)."""
        env = sample_envelope()
        mid = bus.publish(env)
        assert mid is not None
        assert bus.stream_length("anomaly") == 1
        assert bus._redis.exists(stream_name("anomaly")) == 1

    def test_publish_roundtrip_preserves_payload(self, bus: EventBus) -> None:
        """The stored JSON deserializes back to an identical envelope."""
        env = sample_envelope()
        bus.publish(env)
        entries = bus._redis.xrange(stream_name("anomaly"))
        assert entries and entries[0][1] is not None  # (mypy: narrow Optional)
        stored = EventEnvelope.model_validate_json(str(entries[0][1]["envelope"]))
        assert stored.id == env.id
        assert stored.payload["score"] == 0.97  # typed payload survives the trip


class TestConsume:
    """Consumer-group semantics (at-least-once)."""

    def test_read_delivers_each_message_once_per_group(self, bus: EventBus) -> None:
        """Two publishes → one read with count=10 returns both, in order."""
        bus.publish(sample_envelope(id="evt_1"))
        bus.publish(sample_envelope(id="evt_2"))
        msgs = bus.read("anomaly", group="incident-manager", consumer="im-1", block_ms=100)
        assert [m[1].id for m in msgs] == ["evt_1", "evt_2"]

    def test_ack_removes_from_pending(self, bus: EventBus) -> None:
        """Acked messages leave the group's pending list (no redelivery)."""
        bus.publish(sample_envelope())
        msgs = bus.read("anomaly", group="incident-manager", consumer="im-1", block_ms=100)
        assert bus.pending_count("anomaly", "incident-manager") == 1
        for message_id, _ in msgs:
            bus.ack("anomaly", "incident-manager", message_id)
        assert bus.pending_count("anomaly", "incident-manager") == 0

    def test_unacked_messages_stay_pending(self, bus: EventBus) -> None:
        """Without ack, the message remains pending (retry on redelivery)."""
        bus.publish(sample_envelope())
        bus.read("anomaly", group="incident-manager", consumer="im-1", block_ms=100)
        assert bus.pending_count("anomaly", "incident-manager") == 1

    def test_ensure_group_is_idempotent(self, bus: EventBus) -> None:
        """Calling ensure_group twice must not raise (BUSGROUP swallowed)."""
        bus.ensure_group("anomaly", "incident-manager")
        bus.ensure_group("anomaly", "incident-manager")  # second call: no error
