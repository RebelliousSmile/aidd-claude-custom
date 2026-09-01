#!/usr/bin/env python3
"""Create or revoke a detached wireframe review receipt."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


def digest(path: Path) -> dict:
    return {"path": str(path.resolve()), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def atomic_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True); handle.write("\n")
        os.replace(temporary, path)
    except Exception:
        try: os.unlink(temporary)
        except OSError: pass
        raise


def green(static: dict, rendered: dict) -> bool:
    return static.get("summary", {}).get("valid") is True and rendered.get("static", {}).get("status") == "passed" and rendered.get("rendered", {}).get("status") == "passed" and rendered.get("summary", {}).get("validCandidate") is True


def targets_artifact(report: dict, artifact: Path) -> bool:
    try: return Path(report["file"]).resolve() == artifact.resolve()
    except (KeyError, TypeError): return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    accept = sub.add_parser("accept")
    for flag in ("artifact", "static-report", "rendered-report", "reviewer", "out"):
        accept.add_argument(f"--{flag}", required=True)
    revoke = sub.add_parser("revoke")
    revoke.add_argument("--receipt", required=True); revoke.add_argument("--out", required=True)
    args = parser.parse_args()
    try:
        if args.command == "accept":
            paths = [Path(args.artifact), Path(args.static_report), Path(args.rendered_report)]
            static, rendered = json.loads(paths[1].read_text(encoding="utf-8")), json.loads(paths[2].read_text(encoding="utf-8"))
            if not args.reviewer.strip(): raise ValueError("reviewer must be explicit")
            if not green(static, rendered): raise ValueError("static and rendered reports must both be green")
            if not targets_artifact(static, paths[0]) or not targets_artifact(rendered, paths[0]): raise ValueError("reports must target the exact artifact")
            receipt = {"schemaVersion": 1, "status": "accepted", "reviewer": args.reviewer.strip(), "reviewedAt": datetime.now(timezone.utc).isoformat(), "artifact": digest(paths[0]), "staticReport": digest(paths[1]), "renderedReport": digest(paths[2])}
            output = Path(args.out).resolve()
            if output in {p.resolve() for p in paths}: raise ValueError("receipt output must be distinct")
        else:
            receipt_path, output = Path(args.receipt).resolve(), Path(args.out).resolve()
            if receipt_path == output: raise ValueError("revocation output must be distinct from receipt")
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            if receipt.get("status") != "accepted": raise ValueError("only an accepted receipt can be revoked")
            receipt["status"] = "revoked"
        atomic_json(output, receipt); print(output); return 0
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr); return 2


if __name__ == "__main__":
    raise SystemExit(main())
