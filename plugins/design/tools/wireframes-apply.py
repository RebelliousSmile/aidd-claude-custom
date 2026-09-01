#!/usr/bin/env python3
"""Apply reviewed author payload to an untouched generated wireframe shell."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from pathlib import Path


class ApplyError(ValueError):
    pass


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise ApplyError(f"cannot read {path}: {exc}") from exc


def load_payload(path: Path) -> dict:
    try:
        value = json.loads(read(path))
    except json.JSONDecodeError as exc:
        raise ApplyError(f"invalid payload JSON: {exc}") from exc
    if not isinstance(value, dict) or not isinstance(value.get("states"), dict):
        raise ApplyError("payload must be an object with a states object")
    if set(value) - {"states", "styles", "interactions"}:
        raise ApplyError("payload contains unknown fields")
    return value


def reject_breakouts(value: str, label: str) -> None:
    lowered = value.lower()
    forbidden = ["</script", "</style", "<!-- author state", "<!-- end author state"]
    if any(token in lowered for token in forbidden):
        raise ApplyError(f"{label} crosses a governed boundary")


def replace_once(source: str, pattern: str, replacement: str, label: str) -> str:
    matches = list(re.finditer(pattern, source, flags=re.S))
    if len(matches) != 1:
        raise ApplyError(f"{label}: expected one untouched generated placeholder, found {len(matches)}")
    return source[: matches[0].start()] + replacement + source[matches[0].end() :]


def apply(shell: str, payload: dict) -> str:
    output = shell
    expected = re.findall(r"<!-- AUTHOR STATE ([a-z0-9-]+) ([a-z0-9-]+) ([a-z0-9-]+) -->", shell)
    if not expected:
        raise ApplyError("input has no generated author-state placeholders")
    expected_pairs = {(u, s) for u, s, _ in expected}
    supplied_pairs = {(u, s) for u, states in payload["states"].items() for s in states}
    if supplied_pairs != expected_pairs:
        missing = sorted(expected_pairs - supplied_pairs)
        extra = sorted(supplied_pairs - expected_pairs)
        raise ApplyError(f"payload state mismatch; missing={missing}, extra={extra}")
    for unit, state, viewport in expected:
        markup = payload["states"][unit][state]
        if not isinstance(markup, str) or not markup.strip():
            raise ApplyError(f"state {unit}/{state} must be non-empty HTML")
        reject_breakouts(markup, f"state {unit}/{state}")
        start = f"<!-- AUTHOR STATE {unit} {state} {viewport} -->"
        end = f"<!-- END AUTHOR STATE {unit} {state} {viewport} -->"
        pattern = re.escape(start) + r"[\s\S]*?" + re.escape(end)
        output = replace_once(output, pattern, f"{start}{markup}{end}", f"state {unit}/{state}/{viewport}")
    styles = payload.get("styles", "")
    interactions = payload.get("interactions", "")
    if not isinstance(styles, str) or not isinstance(interactions, str):
        raise ApplyError("styles and interactions must be strings")
    reject_breakouts(styles, "styles")
    reject_breakouts(interactions, "interactions")
    output = replace_once(
        output,
        re.escape("/* ===== AUTHOR STYLES — LLM MAY EDIT BETWEEN THESE MARKERS ===== */") + r"[\s\S]*?" + re.escape("/* ===== END AUTHOR STYLES ===== */"),
        "/* ===== AUTHOR STYLES — LLM MAY EDIT BETWEEN THESE MARKERS ===== */\n" + styles + "\n    /* ===== END AUTHOR STYLES ===== */",
        "author styles",
    )
    output = replace_once(
        output,
        re.escape("/* ===== AUTHOR INTERACTIONS — OPTIONAL HELPERS ONLY ===== */") + r"[\s\S]*?" + re.escape("/* ===== END AUTHOR INTERACTIONS ===== */"),
        "/* ===== AUTHOR INTERACTIONS — OPTIONAL HELPERS ONLY ===== */\n" + interactions + "\n    /* ===== END AUTHOR INTERACTIONS ===== */",
        "author interactions",
    )
    return output


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
        os.replace(tmp, path)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply author content to a generated wireframe")
    parser.add_argument("--shell", required=True)
    parser.add_argument("--payload", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    try:
        shell = Path(args.shell).resolve()
        payload = Path(args.payload).resolve()
        out = Path(args.out).resolve()
        if out in {shell, payload}:
            raise ApplyError("output must differ from shell and payload")
        atomic_write(out, apply(read(shell), load_payload(payload)))
        print(out)
        return 0
    except (ApplyError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
