"""Structured logging for the catalog service (copied from the template)."""

from __future__ import annotations

import logging
import sys
from datetime import UTC, datetime

_EXTRA_FIELDS = ("service", "environment")


class KeyValueFormatter(logging.Formatter):
    """Format records as ``level service=... ts=... msg=...``."""

    def format(self, record: logging.LogRecord) -> str:
        parts = [record.levelname]
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
    """Configure the root logger once and return a service-scoped logger."""
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(KeyValueFormatter())
    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(level)
    base = logging.getLogger(service_name)
    base.setLevel(level)
    adapter = logging.LoggerAdapter(base, {"service": service_name, "environment": environment})
    return adapter
