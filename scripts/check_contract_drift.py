#!/usr/bin/env python3
"""Contract-drift check (integration edge case #8).

Compares each built service's *live* OpenAPI (FastAPI ``app.openapi()`` —
no server needed) against its contract file in ``docs/contracts/``, using
the mapping in ``docs/contracts/manifest.json``.

Drift rule (contracts-first, additive-only):
  * every contract path+method must exist in the live API
  * contract response codes must be a subset of the live codes
  * request-body ``required`` fields must match exactly
  (additive live endpoints are allowed — contracts change via contract PRs
  first, then implementations follow; the check fails only when the live
  API falls behind or contradicts the agreed surface)

Usage:
    python3 scripts/check_contract_drift.py [manifest.json]

Exit codes: 0 = clean, 1 = drift found, 2 = tooling error.
Services listed in the manifest that are not built yet are skipped with a
note (their contracts are the spec the track implements against).
"""

from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required (pip install pyyaml)", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MANIFEST = ROOT / "docs" / "contracts" / "manifest.json"

METHODS = ("get", "post", "put", "patch", "delete")


def _resolve(schema: dict[str, Any], spec: dict[str, Any], depth: int = 0) -> dict[str, Any]:
    """Resolve a single-level local ``$ref`` (components.schemas.*)."""
    if depth > 3 or "$ref" not in schema:
        return schema
    ref = schema["$ref"]
    if not ref.startswith("#/components/schemas/"):
        return schema
    name = ref.rsplit("/", 1)[-1]
    resolved = spec.get("components", {}).get("schemas", {}).get(name)
    if not isinstance(resolved, dict):
        return schema
    return _resolve(resolved, spec, depth + 1)


def _surface(spec: dict[str, Any]) -> dict[tuple[str, str], tuple[list[str], list[str]]]:
    """Reduce an OpenAPI doc to (path, method) → (sorted codes, sorted required)."""
    surface: dict[tuple[str, str], tuple[list[str], list[str]]] = {}
    for path, path_item in spec.get("paths", {}).items():
        for method in METHODS:
            op = path_item.get(method)
            if not isinstance(op, dict):
                continue
            codes = sorted(str(code) for code in op.get("responses", {}))
            required: list[str] = []
            body = op.get("requestBody")
            if isinstance(body, dict):
                schema = body.get("content", {}).get("application/json", {}).get("schema", {})
                if isinstance(schema, dict):
                    required = sorted(_resolve(schema, spec).get("required", []))
            surface[(path, method)] = (codes, required)
    return surface


def _load_contract(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text())


def _live_spec(module_name: str) -> dict[str, Any]:
    module = importlib.import_module(module_name)
    app = module.app  # FastAPI instance per template convention
    spec = app.openapi()
    if not isinstance(spec, dict):
        raise TypeError(f"{module_name}.app.openapi() returned {type(spec).__name__}")
    return spec


def check_service(entry: dict[str, Any], contracts_dir: Path) -> tuple[bool, list[str], list[str]]:
    """Return (ok, drift_messages, notes)."""
    service_id = entry["id"]
    module = entry["module"]
    contract_file = contracts_dir / entry["contract"]
    if not contract_file.exists():
        return False, [f"{service_id}: contract file missing: {contract_file}"], []

    try:
        live = _live_spec(module)
    except ModuleNotFoundError:
        # Service not built yet — contract is the forward spec. Not drift.
        return True, [], [f"{service_id}: skipped (module {module!r} not built yet)"]
    except Exception as exc:  # any import/runtime failure is a real signal
        return False, [f"{service_id}: could not load live spec: {exc}"], []

    contract = _load_contract(contract_file)
    live_surface = _surface(live)
    contract_surface = _surface(contract)

    drift: list[str] = []
    extra_ok: list[str] = []
    for (path, method), (codes, required) in sorted(contract_surface.items()):
        if (path, method) not in live_surface:
            drift.append(f"{service_id}: contract has {method.upper()} {path} but live API does not")
            continue
        live_codes, live_required = live_surface[(path, method)]
        missing_codes = [c for c in codes if c not in live_codes]
        if missing_codes:
            drift.append(f"{service_id}: {method.upper()} {path} contract responses {missing_codes} missing in live API")
        if required != live_required:
            drift.append(
                f"{service_id}: {method.upper()} {path} required body fields differ "
                f"(contract={required or None}, live={live_required or None})"
            )
    for (path, method) in sorted(set(live_surface) - set(contract_surface)):
        extra_ok.append(f"{service_id}: live has extra (allowed, additive) {method.upper()} {path}")

    return not drift, drift, extra_ok


def main(manifest_path: Path = DEFAULT_MANIFEST) -> int:
    if not manifest_path.exists():
        print(f"ERROR: manifest not found: {manifest_path}", file=sys.stderr)
        return 2
    manifest = json.loads(manifest_path.read_text())
    entries = manifest.get("services", [])
    if not entries:
        print("ERROR: manifest has no services", file=sys.stderr)
        return 2

    failures: list[str] = []
    contracts_dir = manifest_path.parent
    for entry in entries:
        ok, drift, notes = check_service(entry, contracts_dir)
        for note in notes:
            print(f"  · {note}")
        for line in drift:
            failures.append(line)
            print(f"  ✗ {line}")

    if failures:
        print(f"\nContract drift detected ({len(failures)} issue(s)) — contract-first: update docs/contracts/ in a contract PR, then align the service.")
        return 1
    print(f"\nContract drift: clean ({len(entries)} service(s) in manifest)")
    return 0


if __name__ == "__main__":
    arg = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_MANIFEST
    sys.exit(main(arg))
