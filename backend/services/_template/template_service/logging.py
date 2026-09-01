"""Structured logging setup for AegisDeploy services.

Emits key=value lines to stdout so containers collect them naturally
(docker logs → Loki in P2). Kept dependency-free on purpose.
"""

from __future__ import annotations

import logging
import sys
from datetime import UTC, datetime

#: Extra fields always attached to every log record.
_EXTRA_FIELDS = ("service", "environment")


class KeyValueFormatter(logging.Formatter):
    """Format records as ``level service=... ts=... msg=...`` (log-friendly)."""

    def format(self, record: logging.LogRecord) -> str:
        parts = [record.levelname]
        # Attach service context fields if the logger provided them as extras.
        for field in _EXTRA_FIELDS:
            value = getattr(record, field, None)
            if value:
                parts.append(f"{field}={value}")
        ts = datetime.now(UTC).isoformat(timespec="seconds")
        parts.append(f"ts={ts}")
        parts.append(f"msg={record.getMessage()}")
        if record.exc_info:
            parts.append(f"exc={self.formatException(record.exc_info)}")
        return " ".join(parts)


def setup_logging(service_name: str, environment: str, level: int = logging.INFO) -> logging.LoggerAdapter[logging.Logger]:
    """Configure the root logger once and return a service-scoped logger.

    Args:
        service_name: value attached to every line (SERVICE_NAME).
        environment: value attached to every line (dev/staging/prod).
        level: minimum log level.
    """
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(KeyValueFormatter())
    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(level)
    base = logging.getLogger(service_name)
    base.setLevel(level)
    adapter = logging.LoggerAdapter(base, {"service": service_name, "environment": environment})
    return adapter
