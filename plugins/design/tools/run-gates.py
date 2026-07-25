#!/usr/bin/env python3
"""run-gates.py - aggregation runner for the enforcement of one contract.

Routes, never evaluates. Every rule is realized by someone else: the markup rules by
`skills/enforce/adapters/lint-core.mjs`, the others by a `sc-<language>:design-bridge`
pivot that writes back a report. This runner reads the contract, invokes the realizers it
can invoke, collects the reports of those it cannot, and returns one exit code whatever the
call site. It reads no target file and matches no pattern of its own.

A rule with no realizer is not silently dropped: it is listed as unrealized, with its
reason, and it never changes the exit code. Declaring it is what stops it being read as
verified.

Registry of enforcement types:  references/enforcement-registry.md
Configuration:                  references/gate-config-schema.md

Prerequisite: Python 3.10+ to start this runner at all, Node.js 18+ for it to invoke the
portable linter. Both are stated in skills/enforce/references/gate-wiring.md.

The runner also opposes the contract's maturity: conformity may only be asserted at or
above `THRESHOLD` (references/maturity-status.md). Below it, the report still lists every
violation the linter and the pivots found, but the run cannot claim conformity — it names
the path that would raise the status and returns 4. The threshold has one executable source,
the `THRESHOLD` constant of `tools/status.py`, imported here rather than restated.

Usage:  python run-gates.py --config <file>
Exit:   0  no violation, and the contract is at or above the conformity threshold
        1  at least one violation, from the linter or from a pivot report
        2  invocation or environment error: unreadable configuration, unknown enforcement
           type, required runtime absent
        3  the contract is in 1.x format - migrate it first (tools/migrate-contract.py)
        4  the contract sits below the conformity threshold: conformity is not asserted, the
           violations are still reported, and the path that raises the status is named
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

# The status computation lives in one place. run-gates imports THRESHOLD and the compute
# path from it rather than repeating either the literal or the ladder logic.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from status import THRESHOLD, compute, meets_threshold, observe  # noqa: E402

POLICIES = "policies.json"
RELEASE = "release.json"

# Mirrors references/enforcement-registry.md. The value is who realizes the type; None is
# the marker itself. A type absent from this table is a decision the runner refuses to make.
REALIZER = {
    "markup": "lint-core",
    "stylesheet": "pivot",
    "source-graph": "pivot",
    "stored-content": "pivot",
    "platform-config": "pivot",
    "unrealized": None,
}


def fail(message: str) -> int:
    print(message, file=sys.stderr)
    return 2


def read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as exc:
        raise SystemExit(fail(f"{path}: invalid JSON - {exc}"))


def expand(base: Path, patterns) -> list[Path]:
    """Glob relative to the configuration file. A literal path is kept as written, so a
    missing target is reported by name instead of vanishing from an empty match."""
    found: list[Path] = []
    for pattern in patterns:
        if any(ch in pattern for ch in "*?["):
            found.extend(sorted(base.glob(pattern)))
        else:
            found.append(base / pattern)
    return found


def run(config_path: Path) -> int:
    config = read_json(config_path)
    if config is None:
        return fail(f"Configuration not found: {config_path}")
    if not isinstance(config, dict):
        return fail(f"{config_path}: expected an object at the root.")

    base = config_path.parent
    contract_dir = (base / config.get("contract", ".")).resolve()
    if not contract_dir.is_dir():
        return fail(f"{config_path}: contract directory not found: {contract_dir}")
    if not (contract_dir / RELEASE).is_file():
        print(f"CONTRACT {contract_dir}\n"
              f"  {RELEASE} absent - contract in 1.x format.\n"
              f"  Migrate it: python tools/migrate-contract.py --contract {contract_dir}",
              file=sys.stderr)
        return 3

    policies = read_json(contract_dir / POLICIES)
    if policies is None:
        return fail(f"{contract_dir / POLICIES}: not found, the contract declares it.")

    # Type every declared rule before invoking anything: an untyped rule makes the whole run
    # meaningless, and finding that out after half the targets were linted helps nobody.
    declared = (policies.get("usage") or {}).get("rules") or []
    typed: list[tuple[str, str]] = []
    for index, rule in enumerate(declared):
        rule_id = rule.get("id") or f"usage.rules[{index}]"
        kind = rule.get("enforcement")
        if kind not in REALIZER:
            return fail(f"{contract_dir / POLICIES}: rule \"{rule_id}\" declares "
                        f"enforcement {kind or 'nothing'}, outside the registry.\n"
                        f"  Allowed: {', '.join(sorted(REALIZER))}\n"
                        f"  See references/enforcement-registry.md")
        typed.append((rule_id, kind))

    targets = expand(base, config.get("targets") or [])
    missing = [t for t in targets if not t.is_file()]
    if missing:
        return fail(f"{config_path}: target(s) not found: "
                    + ", ".join(str(m) for m in missing))

    violations: list[str] = []
    realized_markup: set[str] = set()
    exit_code = 0

    if targets:
        linter = (base / config.get("linter", "")).resolve() if config.get("linter") else None
        if linter is None or not linter.is_file():
            return fail(f"{config_path}: `linter` must point at the portable linter; "
                        f"got {config.get('linter') or 'nothing'}.")
        if shutil.which("node") is None:
            return fail("Node.js not found on PATH. The runner invokes the portable linter "
                        "with it; without Node no markup rule can be realized.\n"
                        "  Install Node.js 18+, or remove the markup targets from "
                        f"{config_path}.")
        for target in targets:
            argv = ["node", str(linter), str(target), "--contract", str(contract_dir), "--json"]
            if config.get("strict"):
                argv.append("--strict")
            proc = subprocess.run(argv, capture_output=True, text=True, encoding="utf-8")
            if proc.returncode in (2, 3):
                sys.stderr.write(proc.stderr)
                return proc.returncode
            report = json.loads(proc.stdout) if proc.stdout.strip() else {}
            realized_markup.update(report.get("realized") or [])
            for message in report.get("errors") or []:
                violations.append(f"{target}: {message}")

    # A pivot is a skill and cannot be invoked from here, but the native linter it installs is
    # a process like any other. Declared with a `command`, it is re-run before its report is
    # read, so the report cannot be stale; declared as a bare path, the report is whatever the
    # last run left there. Its absence is what makes the rules unrealized at run time.
    reported: dict[str, str] = {}
    declined: dict[str, str] = {}
    report_paths: list[Path] = []
    for entry in config.get("pivotReports") or []:
        if isinstance(entry, str):
            report_paths.extend(expand(base, [entry]))
            continue
        if not isinstance(entry, dict) or not entry.get("path"):
            return fail(f"{config_path}: each pivotReports entry is a path, or an object "
                        f"carrying `path` and optionally `command`; got {entry!r}.")
        command = entry.get("command")
        if command:
            if not isinstance(command, list) or not all(isinstance(a, str) for a in command):
                return fail(f"{config_path}: `command` of {entry['path']} must be a list of "
                            "strings - no shell, so no quoting rule to get wrong.")
            try:
                # Its exit code says "violations found", which its report already carries in
                # full. Reading the report is what decides; the code here would only duplicate.
                subprocess.run(command, cwd=base, capture_output=True, text=True)
            except FileNotFoundError:
                return fail(f"{config_path}: realizer not found: {command[0]}\n"
                            f"  Declared to produce {entry['path']}. Install it, or drop the "
                            "`command` to read the report as it stands.")
        report_paths.append(base / entry["path"])

    for path in report_paths:
        payload = read_json(path)
        if payload is None:
            return fail(f"{config_path}: pivot report not found: {path}")
        realizer = payload.get("realizer") or str(path)
        for entry in payload.get("rules") or []:
            rule_id = entry.get("id")
            if not rule_id:
                return fail(f"{path}: a report entry declares no rule id.")
            status = entry.get("status")
            if status == "unrealized":
                # The pivot was assigned the rule and says it did not realize it. Louder than
                # silence, and the only case that tells apart "not run" from "cannot cover".
                declined[rule_id] = realizer
                continue
            reported[rule_id] = realizer
            if status == "fail":
                for message in entry.get("violations") or [rule_id]:
                    violations.append(f"{realizer}: {message}")

    print(f"CONTRACT {contract_dir}")
    print(f"TARGETS  {len(targets)} file(s), markup rules realized: "
          f"{', '.join(sorted(realized_markup)) or 'none'}")

    unrealized: list[str] = []
    for rule_id, kind in typed:
        if kind == "markup":
            print(f"  REALIZED   {rule_id} ({kind}) by lint-core")
        elif rule_id in reported:
            print(f"  REALIZED   {rule_id} ({kind}) by {reported[rule_id]}")
        elif rule_id in declined:
            unrealized.append(rule_id)
            print(f"  UNREALIZED {rule_id} ({kind}) - {declined[rule_id]} reports it unrealized")
        elif kind == "unrealized":
            unrealized.append(rule_id)
            print(f"  UNREALIZED {rule_id} - declared with no realizer")
        else:
            unrealized.append(rule_id)
            print(f"  UNREALIZED {rule_id} ({kind}) - no report from its realizer")

    for message in violations:
        print(f"  VIOLATION {message}")

    if unrealized:
        print(f"UNREALIZED {len(unrealized)} rule(s) - reported, never counted as verified, "
              "and never a violation.")

    if violations:
        print(f"FAIL {len(violations)} violation(s).")
        exit_code = 1

    # Oppose the maturity threshold last, once every violation is already on the report. Below
    # it, conformity cannot be asserted whatever the violation count - so exit 4 supersedes
    # both the 1 of a violation and the 0 of a clean run, and the report keeps the violations.
    status_value = compute(observe(contract_dir))
    if not meets_threshold(status_value):
        print(f"BELOW THRESHOLD status \"{status_value}\" is under \"{THRESHOLD}\"; "
              "conformity is not asserted.")
        print(f"  Raise it: python tools/status.py --contract {contract_dir} names the status; "
              "record the missing checks at adjust/02-freeze.md and lift the capping gaps.")
        print("  See references/maturity-status.md for the gap-to-cap table.")
        return 4

    if not violations:
        print("OK   no violation.")
    return exit_code


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="run-gates.py",
        description="Aggregate the enforcement of one contract into a single exit code.")
    parser.add_argument("--config", required=True,
                        help="gate configuration file; every path it holds is relative to it")
    args = parser.parse_args(argv)
    # Violation messages are contract text and carry whatever the contract is written in.
    # A gate must never die on the encoding of the console or of a redirection.
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")
    return run(Path(args.config))


if __name__ == "__main__":
    sys.exit(main())
