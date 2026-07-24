#!/usr/bin/env python3
"""status.py — maturity status of a design-system contract.

The ONLY implementation of the status computation. No other code derives one; a tool
that needs a status calls `compute()` or this CLI and prints back what it returns.

The status is a ladder: the first unmet condition stops the climb. A contract with no
charter therefore caps at the first rung whatever else holds — the ladder caps, it never
skips a rung.

  rung 1  the artifacts exist
  rung 2  + the charter is present
  rung 3  + checks have been run (release.json declares them)
  rung 4  + contrast and declarative-state inputs — added by a later lot, never reached here

Usage:  python status.py --contract <dir>
Exit:   0 status printed on stdout · 2 unusable contract directory
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# The four literals live here and nowhere else.
LADDER = ["extracted", "normalized", "validated", "production-ready"]

DEFAULT_CHARTER = "design-system.md"
RELEASE_FILE = "release.json"

_VERSION_RE = re.compile(r"^version:\s*(\S+)\s*$", re.MULTILINE)


def read_release(contract_dir: Path) -> dict | None:
    """Parse release.json, or None when the contract has no release root (1.x)."""
    path = contract_dir / RELEASE_FILE
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def read_charter(contract_dir: Path, release: dict | None = None) -> dict:
    """Observe the charter document: path, presence, declared version.

    The path comes from the release root when there is one, so a contract that renamed
    its charter stays observable; otherwise the contract-wide default applies.
    """
    rel_path = DEFAULT_CHARTER
    if release:
        rel_path = (release.get("charter") or {}).get("path") or DEFAULT_CHARTER
    path = contract_dir / rel_path
    present = path.is_file()
    version = None
    if present:
        try:
            match = _VERSION_RE.search(path.read_text(encoding="utf-8"))
        except OSError:
            match = None
        if match:
            version = match.group(1)
    return {"path": rel_path, "present": present, "version": version}


def observe(contract_dir: Path) -> dict:
    """The facts a migration can establish by reading the contract directory."""
    release = read_release(contract_dir)
    charter = read_charter(contract_dir, release)
    return {
        "charter_present": charter["present"],
        "checks_run": bool(release and release.get("checks")),
    }


def compute(facts: dict) -> str:
    """Climb the ladder; return the last rung whose condition holds."""
    reached = LADDER[0]
    if not facts.get("charter_present"):
        return reached
    reached = LADDER[1]
    if not facts.get("checks_run"):
        return reached
    return LADDER[2]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Maturity status of a design-system contract.")
    parser.add_argument("--contract", required=True, metavar="DIR",
                        help="contract directory")
    args = parser.parse_args(argv)

    contract_dir = Path(args.contract)
    if not contract_dir.is_dir():
        print(f"Contract directory not found: {contract_dir}", file=sys.stderr)
        return 2
    print(compute(observe(contract_dir)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
