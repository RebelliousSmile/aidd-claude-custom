#!/usr/bin/env python3
"""Classify and inventory author HTML without modifying it."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path


class InventoryParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tags: list[str] = []
        self.styles = 0
        self.scripts = 0
        self.resources: list[dict] = []
        self.external: list[str] = []
        self.units: list[str] = []
        self.unit_candidates: list[str] = []
        self.states: list[str] = []
        self.annotations = 0
        self.ambiguous = False
        self.hidden_interactions: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        self.tags.append(tag)
        if tag == "style": self.styles += 1
        if tag == "script": self.scripts += 1
        if values.get("data-wireframe-unit"): self.units.append(values["data-wireframe-unit"] or "")
        if values.get("data-wireframe-unit-candidate"): self.unit_candidates.append(values["data-wireframe-unit-candidate"] or "")
        if values.get("data-wireframe-state"): self.states.append(values["data-wireframe-state"] or "")
        if "data-wireframe-annotation" in values: self.annotations += 1
        if "data-wireframe-ambiguous" in values or "data-wireframe-unit-candidate" in values and values.get("data-wireframe-unit-candidate") == "ambiguous":
            self.ambiguous = True
        if "hidden" in values or "display:none" in (values.get("style") or "").replace(" ", "").lower():
            self.hidden_interactions.append(tag)
        resource_fields = {"link": "href", "script": "src", "img": "src", "video": "src", "audio": "src", "source": "src"}
        field = resource_fields.get(tag)
        if field and values.get(field):
            value = values[field] or ""
            self.resources.append({"tag": tag, "attribute": field, "value": value})
            if re.match(r"^(?:https?:)?//", value) or value.startswith("/"):
                self.external.append(value)


def atomic_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
        os.replace(temporary, path)
    except Exception:
        try: os.unlink(temporary)
        except OSError: pass
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    source, output = Path(args.source).resolve(), Path(args.out).resolve()
    if source == output:
        print("Error: inventory output must differ from source", file=sys.stderr); return 2
    try:
        raw = source.read_bytes()
        text = raw.decode("utf-8")
    except (OSError, UnicodeError) as exc:
        print(f"Error: cannot read source: {exc}", file=sys.stderr); return 2
    probe = InventoryParser()
    try: probe.feed(text)
    except Exception as exc:
        print(f"Error: cannot parse source HTML: {exc}", file=sys.stderr); return 2
    if re.search(r"(?:classList\.(?:add|remove|toggle)|\.hidden\s*=|style\.display\s*=)", text):
        probe.hidden_interactions.append("script-driven-visibility")
    canonical = bool(re.search(r'<script[^>]+id=["\']wireframe-manifest["\']', text, re.I) and probe.units)
    if probe.ambiguous:
        classification = "ambiguous"
    elif canonical:
        classification = "canonical-wireframe"
    elif re.search(r"<!doctype\s+html|<html(?:\s|>)", text, re.I):
        classification = "html-document"
    else:
        classification = "html-fragment"
    blocks = []
    for kind, count in (("markup", len(probe.tags)), ("style", probe.styles), ("script", probe.scripts), ("annotation", probe.annotations)):
        if count:
            blocks.append({"id": kind, "count": count, "disposition": "unresolved" if classification == "ambiguous" else "pending-review"})
    decisions = []
    if classification == "ambiguous": decisions.append("unit-and-state-mapping")
    if probe.resources: decisions.append("resource-dependency-omission")
    if probe.hidden_interactions: decisions.append("hidden-content-interaction")
    result = {
        "schemaVersion": 1,
        "source": {"path": str(source), "sha256": hashlib.sha256(raw).hexdigest()},
        "classification": classification,
        "inventory": {"blocks": blocks, "resources": probe.resources, "externalDependencies": sorted(set(probe.external)), "unitCandidates": sorted(set(probe.units + probe.unit_candidates)), "states": sorted(set(probe.states)), "annotations": probe.annotations, "hiddenContentInteractions": probe.hidden_interactions},
        "decisions": decisions,
        "canNormalize": classification != "ambiguous"
    }
    try: atomic_json(output, result)
    except OSError as exc:
        print(f"Error: cannot write inventory: {exc}", file=sys.stderr); return 2
    print(output)
    return 1 if classification == "ambiguous" else 0


if __name__ == "__main__":
    raise SystemExit(main())
