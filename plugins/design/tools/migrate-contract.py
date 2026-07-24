#!/usr/bin/env python3
"""migrate-contract.py — turn a 1.x monolithic contract into the four 2.0 artifacts.

One idempotent, replayable pass. The redistribution applied is the table of
`references/contract-schema.md § Redistribution depuis un contrat 1.x`; nothing is invented
and nothing is dropped — a key the table does not name is carried verbatim and reported as
an anomaly, never discarded.

The maturity status is not computed here: `status.py` is the only implementation, and this
script prints back what it returns.

Usage:
  python migrate-contract.py --contract <dir> [--dry-run] [--mode bem|utility-first]
                             [--now <ISO-8601>]

`status.py` travels with this script: both are copied side by side into a consuming project.
Its absence is an environment error (exit 2), never a traceback — an uncaught ImportError exits
1, which the exit-code space reserves for a violation.

Exit:
  0  migrated, or already 2.0 (no-op)
  2  invocation error, missing runtime dependency, a structurally invalid artifact, or a
     decision the tool refuses to guess (undeclared mode)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import status
except ImportError:
    print(
        "status.py not found next to %s.\n"
        "  It is the only implementation of the maturity status and this script prints back\n"
        "  what it returns. Copy it from the design plugin's tools/ directory, or run the\n"
        "  migration from there." % Path(__file__).resolve().parent,
        file=sys.stderr,
    )
    sys.exit(2)

BACKUP_DIR = ".contract-1x"
SCHEMA = "design/references/contract-schema"
FORMAT = "2.0"
MODES = ("bem", "utility-first")

TOKENS, COMPONENTS, POLICIES, ORACLE, RELEASE = (
    "tokens.json", "components.json", "policies.json", "oracle.json", "release.json")
ARTIFACTS = (TOKENS, COMPONENTS, POLICIES, ORACLE)

# The 1.x keys the redistribution table names. Anything else is carried verbatim and reported.
KNOWN_TOP = {"$schema", "$version", "mode", "$utilityPrefixes", "components", "usage", "oracle"}
KNOWN_COMPONENT = {"base", "elements", "modifiers", "backgrounds", "a11y", "oracle"}

# Adapter consumer by extension - a role, never a platform.
CONSUMER_BY_SUFFIX = {
    ".css": "stylesheet",
    ".scss": "stylesheet source",
    ".sass": "stylesheet source",
    ".less": "stylesheet source",
    ".json": "platform token file",
    ".js": "build configuration",
    ".mjs": "build configuration",
    ".cjs": "build configuration",
    ".ts": "build configuration",
}
UNKNOWN_CONSUMER = "unknown"


def fail(message: str) -> int:
    print(message, file=sys.stderr)
    return 2


def shape_of(value) -> str:
    if value is None:
        return "null"
    return {dict: "an object", list: "an array", str: "a string",
            bool: "a boolean", int: "a number", float: "a number"}.get(
        type(value), f"a {type(value).__name__}")


def fail_shape(path: Path, field: str, expected: str, got) -> int:
    """A structurally invalid artifact is an environment error, never a traceback.

    Left unguarded these sites raise AttributeError, which exits 1 — the code the exit-code
    space reserves for a violation — and prints a stack trace instead of naming the field.
    """
    seen = json.dumps(got, ensure_ascii=False)
    if len(seen) > 120:
        seen = seen[:117] + "..."
    # Resolved, unlike the sibling fail() calls in this file: this message is meant to be
    # pasted as evidence, and a relative path is unciteable outside the shell that produced it.
    return fail(f"{path.name} {field} is {shape_of(got)}, expected {expected}: {path.resolve()}\n"
                f"  Got: {seen}\n"
                "  The redistribution reads this field. Read as is, the migration would crash, or\n"
                "  write an artifact the linter cannot derive its rules from.")


def check_shape(manifest, path: Path) -> int | None:
    """Refuse a manifest the redistribution cannot walk. Returns an exit code, or None."""
    if not isinstance(manifest, dict):
        return fail_shape(path, "$", "an object", manifest)
    components = manifest.get("components")
    if components is None:
        return None
    if not isinstance(components, dict):
        return fail_shape(path, "$.components", "an object", components)
    for name, comp in components.items():
        if not isinstance(comp, dict):
            return fail_shape(path, f"$.components.{name}", "an object", comp)
    return None


def sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def dump(obj: dict) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False) + "\n"


def adapter_table(contract_dir: Path) -> tuple[list[dict], list[str]]:
    """One entry per adapter actually present, each carrying its consumer role."""
    entries: list[dict] = []
    anomalies: list[str] = []
    root = contract_dir / "adapters"
    if not root.is_dir():
        return entries, anomalies
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        consumer = CONSUMER_BY_SUFFIX.get(path.suffix.lower(), UNKNOWN_CONSUMER)
        rel = path.relative_to(contract_dir).as_posix()
        entries.append({"artifact": rel, "consumer": consumer})
        if consumer == UNKNOWN_CONSUMER:
            anomalies.append(f"adapter {rel}: consumer not derivable from the extension, complete it by hand")
    return entries, anomalies


def split(manifest: dict, mode: str) -> tuple[dict, list[tuple[str, str]], list[str]]:
    """Redistribute the 1.x manifest into the three derived artifact payloads."""
    mapping: list[tuple[str, str]] = []
    anomalies: list[str] = []

    components: dict = {}
    oracle_components: dict = {}
    for name, comp in (manifest.get("components") or {}).items():
        anatomy: dict = {}
        for key, value in comp.items():
            if key == "oracle":
                continue
            anatomy[key] = value
            if key not in KNOWN_COMPONENT:
                anomalies.append(
                    f"$.components.{name}.{key}: outside the redistribution table, kept in {COMPONENTS}")
        components[name] = anatomy
        if comp.get("oracle"):
            oracle_components[name] = comp["oracle"]
    if components:
        mapping.append(("$.components.*.<anatomy>", f"{COMPONENTS}.components"))
    if oracle_components:
        mapping.append(("$.components.*.oracle", f"{ORACLE}.components.*"))

    policies: dict = {"$schema": f"{SCHEMA}#policies", "mode": mode}
    mapping.append(("$.mode" if "mode" in manifest else "--mode", f"{POLICIES}.mode"))
    if "$utilityPrefixes" in manifest:
        policies["$utilityPrefixes"] = manifest["$utilityPrefixes"]
        mapping.append(("$.$utilityPrefixes", f"{POLICIES}.$utilityPrefixes"))
    if "usage" in manifest:
        policies["usage"] = manifest["usage"]
        mapping.append(("$.usage", f"{POLICIES}.usage"))

    oracle: dict = {"$schema": f"{SCHEMA}#oracle", "components": oracle_components}
    if manifest.get("oracle"):
        oracle["contract"] = manifest["oracle"]
        mapping.append(("$.oracle", f"{ORACLE}.contract"))
        anomalies.append(
            f"$.oracle: contract-level hints, kept in {ORACLE}.contract; only the per-component form has a reader")

    for key, value in manifest.items():
        if key in KNOWN_TOP:
            continue
        policies[key] = value
        mapping.append((f"$.{key}", f"{POLICIES}.{key}"))
        anomalies.append(f"$.{key}: outside the redistribution table, kept in {POLICIES}")

    payload = {COMPONENTS: {"$schema": f"{SCHEMA}#components", "components": components},
               POLICIES: policies}
    # An empty oracle.json is not written, and not declared: a contract without measure
    # targets has no oracle side. Its only reader is the measure adapter, never the linter.
    if oracle_components or oracle.get("contract"):
        payload[ORACLE] = oracle
    return payload, mapping, anomalies


def migrate(contract_dir: Path, mode_arg: str | None, dry_run: bool, now: str) -> int:
    if not contract_dir.is_dir():
        return fail(f"Contract directory not found: {contract_dir}")

    if (contract_dir / RELEASE).is_file():
        print(f"CONTRACT {contract_dir}\n"
              f"NO-OP    {RELEASE} present - already 2.0, nothing to migrate.")
        return 0

    manifest_path = contract_dir / COMPONENTS
    tokens_path = contract_dir / TOKENS
    for path in (tokens_path, manifest_path):
        if not path.is_file():
            return fail(f"Not a 1.x contract: {path.name} missing in {contract_dir}")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except ValueError as exc:
        return fail(f"Unreadable {COMPONENTS}: {exc}")

    # Before any field is read, including in the dry-run path: a dry run that crashes is not a
    # dry run, and the shape is what every read below takes on faith.
    bad_shape = check_shape(manifest, manifest_path)
    if bad_shape is not None:
        return bad_shape

    declared_mode = manifest.get("mode")
    if declared_mode and mode_arg and declared_mode != mode_arg:
        return fail(f'Mode conflict: {COMPONENTS} declares "{declared_mode}", --mode says "{mode_arg}". '
                    "Drop --mode, or fix the contract. The tool does not pick between them.")
    if declared_mode and declared_mode not in MODES:
        return fail(f'Unknown mode "{declared_mode}" in {manifest_path}. Expected one of: {", ".join(MODES)}.')
    mode = declared_mode or mode_arg
    if not mode:
        return fail(f"Undeclared mode in {manifest_path}. Pass --mode {'|'.join(MODES)}. "
                    "The tool refuses to guess it: the wrong mode leaves the vocabulary rules inert "
                    "and turns a green run into a verdict about nothing.")

    payload, mapping, anomalies = split(manifest, mode)
    adapters, adapter_anomalies = adapter_table(contract_dir)
    anomalies += adapter_anomalies
    if adapters:
        payload[POLICIES]["adapters"] = adapters
        mapping.append(("adapters/*", f"{POLICIES}.adapters"))

    charter = status.read_charter(contract_dir)
    version = manifest.get("$version")
    if not version:
        version = charter["version"] or "0.0.0"
        anomalies.append(f'$.$version absent - {RELEASE} declares "{version}", read from the charter or defaulted')
    if not charter["present"]:
        anomalies.append(f"charter {charter['path']} absent - recorded in {RELEASE}.charter, and the status is capped by it")
    elif charter["version"] and charter["version"] != version:
        anomalies.append(f'declared versions differ - {COMPONENTS} "{version}", charter "{charter["version"]}"; '
                         f"both are recorded in {RELEASE}, neither is a violation")

    manifest_hash = sha256(manifest_path)
    source_hash = {TOKENS: sha256(tokens_path)}
    release = {
        "$schema": f"{SCHEMA}#release",
        "$format": FORMAT,
        "designSystem": {"version": version},
        "artifacts": {name: {"version": version, "sourceHash": source_hash.get(name, manifest_hash)}
                      for name in ARTIFACTS if name == TOKENS or name in payload},
        "charter": {"present": charter["present"], "path": charter["path"], "version": charter["version"]},
        "provenance": {"producedBy": Path(__file__).name, "producedAt": now, "from": "1.x contract"},
        "checks": None,
        "status": status.compute(status.observe(contract_dir)),
    }

    mapping = ([(TOKENS, f"{TOKENS} (unchanged)"),
                ("$.$version", f"{RELEASE}.designSystem.version, artifacts.*.version")]
               + mapping
               + [(charter["path"], f"{RELEASE}.charter")])

    width = max(len(src) for src, _ in mapping)
    lines = [f"CONTRACT {contract_dir}",
             f"MODE     {mode} ({'declared' if declared_mode else '--mode'})",
             f"STATUS   {release['status']}",
             "MAPPING"]
    lines += [f"  {src.ljust(width)}  ->  {dst}" for src, dst in mapping]
    lines.append("ADAPTERS")
    lines += [f"  {e['artifact']}  ->  {e['consumer']}" for e in adapters] or ["  (none)"]
    lines.append("ANOMALIES")
    lines += [f"  {a}" for a in anomalies] or ["  (none)"]

    if dry_run:
        lines.append("DRY RUN  nothing written")
        print("\n".join(lines))
        return 0

    backup = contract_dir / BACKUP_DIR
    backup.mkdir(exist_ok=True)
    for name in (COMPONENTS, TOKENS, charter["path"]):
        src = contract_dir / name
        if src.is_file():
            shutil.copy2(src, backup / Path(name).name)

    for name, obj in payload.items():
        (contract_dir / name).write_text(dump(obj), encoding="utf-8")
    (contract_dir / RELEASE).write_text(dump(release), encoding="utf-8")

    lines.append(f"WRITTEN  {', '.join(list(payload) + [RELEASE])}")
    lines.append(f"BACKUP   {BACKUP_DIR}/")
    print("\n".join(lines))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Migrate a 1.x design-system contract to the 2.0 artifacts.")
    parser.add_argument("--contract", required=True, metavar="DIR", help="contract directory")
    parser.add_argument("--dry-run", action="store_true", help="report only, write nothing")
    parser.add_argument("--mode", choices=MODES, help="vocabulary mode, when the contract declares none")
    parser.add_argument("--now", metavar="ISO-8601",
                        help="pin provenance.producedAt, so a migration is byte-reproducible")
    args = parser.parse_args(argv)
    now = args.now or datetime.now(timezone.utc).isoformat(timespec="seconds")
    return migrate(Path(args.contract), args.mode, args.dry_run, now)


if __name__ == "__main__":
    sys.exit(main())
