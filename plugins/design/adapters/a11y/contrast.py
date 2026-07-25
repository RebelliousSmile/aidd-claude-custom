#!/usr/bin/env python3
"""contrast.py — WCAG contrast of a contract's semantic colors, per theme.

Computed from resolved token values only: no rendering, no browser, no markup. The same
`tokens.json` always yields the same verdict, so two runs produce byte-identical output — the
property the maturity status depends on (`references/maturity-status.md`).

What it pairs, stack-agnostically: under `color.semantic`, every foreground role
(`text`, `foreground`, `on-*`) against every surface role (`background`, `surface`, `base`).
Each pair is evaluated on the base tree (`default` theme) and on every `themes.<name>` overlay
(`references/token-schema.md § Modes / themes`), aliases resolved within the theme they belong
to. A project whose semantic vocabulary is wider extends the pairing from its own pivot.

Usage:  python contrast.py --contract <dir> [--json]
Exit:   0  computed (verdicts on stdout) · 2  unusable contract: no tokens.json, unparsable,
           dangling alias or alias cycle
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

TOKENS_FILE = "tokens.json"
AA = 4.5  # WCAG 2.x AA, normal text
DEFAULT_THEME = "default"

_FG_ROLE = re.compile(r"^(text|foreground|on[-A-Z])")
_SURFACE_ROLE = re.compile(r"^(background|surface|base)$")
_ALIAS = re.compile(r"^\{([^}]+)\}$")


def is_token(node) -> bool:
    return isinstance(node, dict) and "$value" in node


def deep_merge(base, overlay):
    """Overlay wins on `$value`; base keeps every path the overlay does not re-declare."""
    if is_token(base) or is_token(overlay):
        merged = dict(base) if isinstance(base, dict) else {}
        if isinstance(overlay, dict):
            merged.update(overlay)
        return merged
    result = {k: _copy(v) for k, v in base.items()}
    for key, value in (overlay or {}).items():
        result[key] = deep_merge(result[key], value) if key in result else _copy(value)
    return result


def _copy(node):
    return {k: _copy(v) for k, v in node.items()} if isinstance(node, dict) else node


def lookup(tree: dict, dotted: str):
    node = tree
    for part in dotted.split("."):
        if not isinstance(node, dict) or part not in node:
            raise KeyError(dotted)
        node = node[part]
    return node


def resolve(tree: dict, raw: str) -> str:
    """Follow `{a.b.c}` aliases within one theme's tree until a literal, guarding cycles."""
    seen: set[str] = set()
    value = raw
    while isinstance(value, str):
        match = _ALIAS.match(value.strip())
        if not match:
            return value
        ref = match.group(1)
        if ref in seen:
            raise ValueError(f"alias cycle at {{{ref}}}")
        seen.add(ref)
        value = lookup(tree, ref).get("$value")
    raise ValueError(f"alias resolves to a non-string value: {raw}")


def to_rgb(value: str) -> tuple[int, int, int]:
    hexstr = value.strip().lstrip("#")
    if len(hexstr) == 3:
        hexstr = "".join(ch * 2 for ch in hexstr)
    if len(hexstr) not in (6, 8) or any(c not in "0123456789abcdefABCDEF" for c in hexstr):
        raise ValueError(f"not a hex color: {value}")
    return tuple(int(hexstr[i:i + 2], 16) for i in (0, 2, 4))  # alpha, if any, ignored


def _linear(channel: int) -> float:
    c = channel / 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def luminance(rgb: tuple[int, int, int]) -> float:
    r, g, b = (_linear(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(fg: tuple[int, int, int], bg: tuple[int, int, int]) -> float:
    hi, lo = sorted((luminance(fg), luminance(bg)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def semantic_leaves(tree: dict) -> dict[str, dict]:
    node = (tree.get("color") or {}).get("semantic") or {}
    return {name: leaf for name, leaf in node.items() if is_token(leaf)}


def evaluate(tokens: dict) -> list[dict]:
    base = {k: v for k, v in tokens.items() if k != "themes"}
    themes = {DEFAULT_THEME: base}
    for name in sorted(tokens.get("themes") or {}):
        themes[name] = deep_merge(base, tokens["themes"][name])

    results: list[dict] = []
    for theme in sorted(themes):  # default sorts before named themes it never collides with
        tree = themes[theme]
        leaves = semantic_leaves(tree)
        foregrounds = sorted(n for n in leaves if _FG_ROLE.match(n))
        surfaces = sorted(n for n in leaves if _SURFACE_ROLE.match(n))
        for fg in foregrounds:
            fg_value = resolve(tree, leaves[fg]["$value"])
            for bg in surfaces:
                bg_value = resolve(tree, leaves[bg]["$value"])
                r = ratio(to_rgb(fg_value), to_rgb(bg_value))
                results.append({
                    "theme": theme,
                    "foreground": f"color.semantic.{fg}",
                    "background": f"color.semantic.{bg}",
                    "fgValue": fg_value,
                    "bgValue": bg_value,
                    "ratio": round(r, 2),
                    "pass": r >= AA,
                })
    return results


def run(contract: str) -> tuple[int, dict | None]:
    tokens_path = Path(contract) / TOKENS_FILE
    if not tokens_path.is_file():
        print(f"{tokens_path}: not found; a contract declares tokens.json.", file=sys.stderr)
        return 2, None
    try:
        tokens = json.loads(tokens_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"{tokens_path}: unreadable — {exc}", file=sys.stderr)
        return 2, None
    try:
        results = evaluate(tokens)
    except (KeyError, ValueError) as exc:
        print(f"{tokens_path}: {exc}", file=sys.stderr)
        return 2, None
    return 0, {"contract": contract, "aa": AA, "results": results}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="WCAG contrast of a contract, per theme.")
    parser.add_argument("--contract", required=True, metavar="DIR", help="contract directory")
    parser.add_argument("--json", action="store_true", help="emit the machine-readable report")
    args = parser.parse_args(argv)
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")

    code, report = run(args.contract)
    if report is None:
        return code
    if args.json:
        # sort_keys makes every dict key order fixed, results are already sorted: byte-identical.
        print(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=True))
    else:
        for r in report["results"]:
            verdict = "PASS" if r["pass"] else "FAIL"
            print(f"{verdict} {r['theme']:10} {r['foreground']} on {r['background']} "
                  f"= {r['ratio']} (AA {AA})")
        print(f"{sum(r['pass'] for r in report['results'])}/{len(report['results'])} pass")
    return code


if __name__ == "__main__":
    sys.exit(main())
