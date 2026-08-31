#!/usr/bin/env python3
"""Validate all YAML files in the repository.

- Strict parse of every *.yml / *.yaml (catches bad indentation/syntax).
- Extra checks for docker-compose.yml (file existence of mounted configs).

Usage:
    python3 scripts/validate_yaml.py          # scan repo
    python3 scripts/validate_yaml.py <file>   # scan one file
"""

from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    print("ERROR: PyYAML is required. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", "node_modules", ".next", ".venv", "venv", "data"}

COMPOSE_FILE = ROOT / "docker-compose.yml"
# Paths inside the repo that compose mounts (validated to exist)
COMPOSE_MOUNTS = [
    "infra/prometheus/prometheus.yml",
    "infra/grafana/provisioning",
    "infra/loki/loki-config.yaml",
    "infra/tempo/tempo.yaml",
    "infra/otel/otel-collector.yaml",
]


def iter_yaml_files(start: Path, single: Path | None = None):
    if single is not None:
        yield single
        return
    for path in sorted(start.rglob("*")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix in {".yml", ".yaml"}:
            yield path


def check_compose_mounts() -> list[str]:
    """Check that every repo-relative path mounted in compose exists."""
    errors: list[str] = []
    text = COMPOSE_FILE.read_text(encoding="utf-8")
    for mount in COMPOSE_MOUNTS:
        if f"./{mount}" in text and not (ROOT / mount).exists():
            errors.append(f"compose mount missing: {mount}")
    return errors


def main() -> int:
    single = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if single and not single.exists():
        print(f"ERROR: file not found: {single}", file=sys.stderr)
        return 2

    files = list(iter_yaml_files(ROOT, single))
    errors: list[str] = []

    for path in files:
        try:
            yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:  # noqa: PERF203
            errors.append(f"{path.relative_to(ROOT)}: {exc}")

    if COMPOSE_FILE.exists():
        errors.extend(check_compose_mounts())

    if errors:
        print("YAML validation FAILED:")
        for err in errors:
            print(f"  ✗ {err}")
        return 1

    print(f"YAML validation OK ({len(files)} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
