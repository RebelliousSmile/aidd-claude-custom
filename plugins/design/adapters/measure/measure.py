#!/usr/bin/env python3
"""Fidelity oracle — compares computed styles between a mockup and an implementation render,
per breakpoint, property by property. Deterministic: same inputs -> same numbers
(the numbers come from Chromium via Playwright, not from an LLM).

Two modes:
  B (default) — diff a mockup page against an implementation render (mockup<->implementation).
  A           — extract computed styles from a single side (seed a greenfield contract).

The mockup may be an SPA exposing window.setPage()/window.setViewport();
those hooks are called when present. Output is a per-breakpoint JSON report written
in UTF-8 (avoids console encoding loss); a short summary is printed to stdout.

--ledger-registry is REQUIRED — the oracle asserts conformity from the per-property comparison
alone, and every tolerated exception must resolve to an active entry of deviations.json carrying
an expected value. There is no unregistered tolerance: absent the registry the tool exits 2
instead of measuring, so a green run can never come from an unvouched sanction.

Usage:
  python measure.py --config <cfg> --ledger-registry <dir>/deviations.json \
                    --out <project>/<qa-dir>/fidelity/<page>-B.json
  python measure.py --config <cfg> --mode A --side mockup --ledger-registry <dir>/deviations.json \
                    --out <file>

--out is the CONSUMER's responsibility: always an absolute path into the consuming project's
QA/artifacts tree (gitignored), never plugin-relative. The script writes wherever it is told;
keeping reports out of the plugin is a caller convention (see the copycat agent / fidelity gate).

Config (JSON):
  {
    "reference_url": "...", "reference_page": "<setPage key|null>",   # the mockup side
    "implementation_url": "...",                                      # the implementation side
    # reference_url / implementation_url carrying a scheme (http://, file://) are used verbatim.
    # A value with no scheme is a path RELATIVE TO THE CONFIG FILE, resolved to a file:// URL —
    # so a self-contained fixture stays portable across machines (no baked absolute path).
    "breakpoints": [{"name":"desktop","width":1440,"height":900,"mockup_viewport":"desktop"}],
    "props": ["fontSize", ...],
    "targets": [{"name":"Hero · title","mockup":"<sel>","implementation":"<sel>"}],
    "headings_sel": {"mockup":"h1, h2","implementation":"h1, h2"},  # optional — completeness scope
    "coverage_ack": {"sections":["..."],"reason":"..."},  # optional — justify which sections
                                                          # are deliberately unmeasured (non-empty
                                                          # sections list required to disable guard)
    "check_text": true,                                       # optional — global default OR per-target:
                                                              # targets:[{"name":…,"check_text":true}]
                                                              # Compare textContent where label parity
                                                              # is meaningful (eyebrow, CTA, stat label).
                                                              # NEVER set globally on prose targets
                                                              # (body, testimonials) — those diverge
                                                              # legitimately from placeholder copy.
                                                              # Use per-target to avoid false diffs. (P11)
    "collections": [                                          # optional — sequence parity check
      {"name":"Stats hero","mockup":".stat-item","implementation":".stat-item",
       "ack":{"id":"DEV-004","reason":"..."}}               # P13 — sanction a deliberate divergence
      # Oracle enumerates ALL matching elements on both sides, normalises their text, diffs the
      # sequences → count diff, per-index label mismatch, missing/extra items, reordering.
      # ok:false with no ack contributes to OPEN verdict like missing_sections.
      # P13 — "ack":{"id":"DEV-xxx","reason":"..."} sanctions a deliberate content/structure
      # divergence (different business content). Acked ok:false entries are excluded from
      # collection_failures. Their id is validated via --ledger-registry like row-level ledger.
    ],
    "ledger": [                                           # deviation references
      {"id":"DEV-001","target":"Hero · title","prop":"fontSize","why":"..."}
      # id (DEV-xxx) is REQUIRED — unsigned entries are surfaced in ledger_ids for human review.
      # Each id is validated against --ledger-registry (deviations.json): an id that is not an
      # active entry carrying an expected value, or one past its expiry, forces verdict=OPEN.
    ]
  }

Report shape (per breakpoint):
  Mode B
    - diff row    : {"element","prop","mockup","implementation","match": bool}
                    if ledgered: adds "ledgered":true, "why":"...", "ledger_id":"DEV-xxx"
    - missing row : {"element",
                     "missing": {"mockup": "present"|"absent", "implementation": "present"|"absent"},
                     "searched": {"mockup": <sel>, "implementation": <sel>}}
      -> "present"|"absent" is explicit on purpose: do NOT infer presence from null.
  Mode A
    - value row   : {"element","values": {<prop>: <computed>}}
    - missing row : {"element","missing": true, "searched": {<side>: <sel>}}

Top-level (Mode B) — STRUCTURAL GATES, computed by the script, not claimed by the caller:
  "ledger_ids":   ["DEV-001", ...]   -> ids declared in config ledger (for human cross-check)
  "ledger_unused":[{"id","target","prop"}, ...]
      -> ledger entries that matched no actual diff (stale sanction or already-fixed delta).
         Non-blocking for verdict but signals ledger bloat.
  "completeness": {"mockup_headings":[...], "implementation_headings":[...],
                   "missing_in_implementation":[...], "extra_in_implementation":[...]}
      -> structure before pixels: a heading present in the mockup but absent in the
         implementation is a missing SECTION, the dominant delta. Defeats hero-only tunnel vision.
  "coverage": {"implementation_headings": N, "measured_targets": M, "ok": bool, "warning": "...",
               "ack_sections": [...]}
      -> fewer targets than headings => under-coverage (a hero-only config "passing" while
         the body is unmeasured). OPEN unless coverage_ack supplies a non-empty sections list.
  "collections": [{"name","mockup_count","implementation_count",
                   "diffs":[{"index","mockup","implementation","match":bool}],
                   "missing_in_implementation":[...], "extra_in_implementation":[...], "ok":bool,
                   "acked":bool, "ack_id":"DEV-xxx", "ack_reason":"..."}]  # P13 — when ack present
      -> sequence parity: count mismatch, per-index label diff, missing/extra items, reordering.
         Catches stat-block drift, card counts, nav items — structures invisible to getComputedStyle.
         ok:false with no ack contributes to OPEN verdict. ok:false with ack is excluded from
         collection_failures (ack_id validated via --ledger-registry). ack_unused:true when ok:true
         and ack is present (stale sanction). Measured once (content is layout-independent).
  "summary": {"verdict": "CLOSED"|"OPEN", "closed": bool, "reasons": [...],
              "total_diff": D, "total_missing": K, "missing_sections": S,
              "collection_failures": N,   # P13: only unacked failures
              "collection_acked": N,      # P13: present only if > 0 (acked sanctions applied)
              "ledger_ids": [...],        # P13: includes collection ack ids
              "ledger_unused_count": N}
      -> CLOSED iff D==0 AND K==0 AND no missing section AND coverage ok
         AND collection_failures==0 (unacked only) AND all ledger ids validated.
         The CALLER MUST cite summary.verdict — closure is asserted from THIS, never from
         inspecting one's own edit. "verified by grep of source" is not closure.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path

from playwright.sync_api import sync_playwright

# JS injected to read getComputedStyle for each target on the current page.
# When check_text is true, also captures __text (normalised textContent) for P7 text-parity.
_GRAB = """(args) => {
  const { targets, props, side, check_text } = args;
  const out = {};
  for (const t of targets) {
    const sel = t[side];
    const el = sel ? document.querySelector(sel) : null;
    if (!el) { out[t.name] = { __missing: sel || null }; continue; }
    const cs = getComputedStyle(el);
    const o = {};
    for (const p of props) o[p] = cs[p];
    const do_text = t.check_text !== undefined ? t.check_text : check_text;
    if (do_text) o['__text'] = (el.textContent || '').replace(/\\s+/g, ' ').trim();
    out[t.name] = o;
  }
  return out;
}"""

# JS injected to enumerate visible heading texts (structural completeness scan).
_HEADINGS = """(sel) => Array.from(document.querySelectorAll(sel))
  .map(e => (e.textContent || '').replace(/\\s+/g, ' ').trim())
  .filter(Boolean)"""

# JS injected to enumerate all items of a collection (P8 sequence parity).
_COLLECT = """(args) => {
  const { collections, side } = args;
  const out = {};
  for (const c of collections) {
    const sel = c[side];
    const els = sel ? Array.from(document.querySelectorAll(sel)) : [];
    out[c.name] = els.map(e => (e.textContent || '').replace(/\\s+/g, ' ').trim());
  }
  return out;
}"""

# JS injected to isolate the active .preview-frame by detaching non-active ones (P3).
# Each breakpoint opens a fresh page, so detaching is safe and permanent for this measurement.
_ISOLATE_FRAME = """(v) => {
  document.querySelectorAll('.preview-frame').forEach(f => {
    const isActive = v === 'desktop'
      ? !f.classList.contains('tablet') && !f.classList.contains('mobile')
      : f.classList.contains(v);
    if (!isActive && f.parentNode) f.parentNode.removeChild(f);
  });
}"""


def _prepare_mockup(page, page_key, mockup_viewport):
    """Drive the SPA mockup: set its viewport mode + page, hide preview chrome,
    then isolate the active .preview-frame so querySelector targets the right DOM."""
    if mockup_viewport:
        page.evaluate("(v) => window.setViewport && window.setViewport(v)", mockup_viewport)
    if page_key:
        page.evaluate("(k) => window.setPage && window.setPage(k)", page_key)
    page.evaluate("() => { const b = document.querySelector('.preview-bar'); if (b) b.style.display = 'none'; }")
    # Detach non-active frames so document.querySelector hits the right one (P3).
    page.evaluate(_ISOLATE_FRAME, mockup_viewport or "desktop")
    page.wait_for_timeout(400)


def _grab(page, targets, props, side, check_text=False):
    return page.evaluate(_GRAB, {"targets": targets, "props": props, "side": side,
                                 "check_text": check_text})


def _headings(page, sel):
    return page.evaluate(_HEADINGS, sel)


def _collect(page, collections, side):
    return page.evaluate(_COLLECT, {"collections": collections, "side": side})


def _diff_collections(mock_items: dict, impl_items: dict, collections: list) -> list:
    """Diff two sides of each named collection: count, LCS-aligned label diffs, missing/extra (P8+P12).

    P12 — uses SequenceMatcher (LCS) for per-item alignment so a single insertion at position 0
    does not cascade all subsequent items as false mismatches. The set-based missing/extra remain
    the authoritative verdict input; diffs[] is a human-readable trace.

    P13 — collection-level ack: {"id":"DEV-xxx","reason":"..."} on a config entry sanctions
    a deliberate content/structure divergence (mirrors row-level ledger). An acked ok:false entry
    does NOT contribute to collection_failures. ack_unused:true when ok:true and ack is present.
    """
    result = []
    for c in collections:
        name = c["name"]
        mock = [_norm(t) for t in mock_items.get(name, [])]
        impl = [_norm(t) for t in impl_items.get(name, [])]
        diffs: list = []
        sm = SequenceMatcher(None, mock, impl, autojunk=False)
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "equal":
                for k in range(i2 - i1):
                    diffs.append({"index": i1 + k, "mockup": mock[i1 + k],
                                  "implementation": impl[j1 + k], "match": True})
            else:  # replace / delete / insert
                mock_sl, impl_sl = mock[i1:i2], impl[j1:j2]
                for k in range(max(len(mock_sl), len(impl_sl))):
                    mv = mock_sl[k] if k < len(mock_sl) else None
                    iv = impl_sl[k] if k < len(impl_sl) else None
                    diffs.append({"index": i1 + k if k < len(mock_sl) else None,
                                  "mockup": mv, "implementation": iv, "match": False})
        mock_set, impl_set = set(mock), set(impl)
        ok = mock == impl
        entry: dict = {
            "name": name,
            "mockup_count": len(mock),
            "implementation_count": len(impl),
            "diffs": diffs,
            "missing_in_implementation": [t for t in mock if t not in impl_set],
            "extra_in_implementation": [t for t in impl if t not in mock_set],
            "ok": ok,
        }
        # P13 — propagate ack from config entry
        ack = c.get("ack")
        if ack:
            entry["ack_id"] = ack.get("id", "")
            entry["ack_reason"] = ack.get("reason", "")
            if not ok:
                entry["acked"] = True
            else:
                entry["ack_unused"] = True
        result.append(entry)
    return result


def _resolve_url(raw: str, base_dir: Path) -> str:
    """A config URL with a scheme is used verbatim; a bare path is resolved relative to the config
    file and turned into a file:// URL, so a committed fixture needs no machine-specific path."""
    if re.match(r"^[a-z][a-z0-9+.-]*://", raw, re.IGNORECASE):
        return raw
    return (base_dir / raw).resolve().as_uri()


def measure(cfg: dict, mode: str, side: str, base_dir: Path) -> dict:
    report: dict = {"mode": mode, "mockup_page": cfg.get("reference_page"), "breakpoints": {}}
    props = cfg["props"]
    targets = cfg["targets"]
    check_text = cfg.get("check_text", False)
    collections = cfg.get("collections", [])
    hsel = cfg.get("headings_sel", {"mockup": "h1, h2", "implementation": "h1, h2"})
    mock_headings = impl_headings = None
    mock_coll = impl_coll = None  # collected once across breakpoints (content is layout-independent)

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        try:
            for bp in cfg["breakpoints"]:
                ctx = browser.new_context(viewport={"width": bp["width"], "height": bp["height"]})
                try:
                    mock = impl = None
                    if mode == "B" or side == "mockup":
                        m = ctx.new_page()
                        m.goto(_resolve_url(cfg["reference_url"], base_dir),
                               wait_until="networkidle", timeout=20000)
                        _prepare_mockup(m, cfg.get("reference_page"), bp.get("mockup_viewport"))
                        mock = _grab(m, targets, props, "mockup", check_text)
                        if mock_headings is None:
                            mock_headings = _headings(m, hsel.get("mockup", "h1, h2"))
                        if collections and mock_coll is None:
                            mock_coll = _collect(m, collections, "mockup")
                    if mode == "B" or side == "implementation":
                        w = ctx.new_page()
                        w.goto(_resolve_url(cfg["implementation_url"], base_dir),
                               wait_until="networkidle", timeout=20000)
                        w.wait_for_timeout(300)
                        impl = _grab(w, targets, props, "implementation", check_text)
                        if impl_headings is None:
                            impl_headings = _headings(w, hsel.get("implementation", "h1, h2"))
                        if collections and impl_coll is None:
                            impl_coll = _collect(w, collections, "implementation")
                finally:
                    ctx.close()

                rows = []
                for t in targets:
                    name = t["name"]
                    if mode == "A":
                        src = mock if side == "mockup" else impl
                        v = src[name]
                        rows.append({"element": name, "missing": True, "searched": {side: v["__missing"]}}
                                    if "__missing" in v
                                    else {"element": name, "values": v})
                        continue
                    m_v, i_v = mock[name], impl[name]
                    if "__missing" in m_v or "__missing" in i_v:
                        rows.append({"element": name,
                                     "missing": {"mockup": "absent" if "__missing" in m_v else "present",
                                                 "implementation": "absent" if "__missing" in i_v else "present"},
                                     "searched": {"mockup": t.get("mockup"),
                                                  "implementation": t.get("implementation")}})
                        continue
                    for p in props:
                        rows.append({"element": name, "prop": p,
                                     "mockup": m_v[p], "implementation": i_v[p], "match": m_v[p] == i_v[p]})
                    # P7+P11 — text parity: emit when JS captured __text (per-target or global)
                    if "__text" in m_v and "__text" in i_v:
                        mt, it = _norm(m_v["__text"]), _norm(i_v["__text"])
                        rows.append({"element": name, "prop": "text",
                                     "mockup": mt, "implementation": it, "match": mt == it})
                report["breakpoints"][bp["name"]] = rows
        finally:
            browser.close()

    if mode == "B":
        _apply_ledger(report, cfg.get("ledger", []))
        report["completeness"] = _completeness(mock_headings or [], impl_headings or [])
        report["coverage"] = _coverage(impl_headings or [], targets, cfg.get("coverage_ack"))
        # P8 — collection parity (evaluated once, content is layout-independent)
        if collections:
            report["collections"] = _diff_collections(mock_coll or {}, impl_coll or {}, collections)
            # P13 — merge collection ack ids into ledger_ids for --ledger-registry validation
            coll_ack_ids = [c["ack_id"] for c in report["collections"] if "ack_id" in c]
            if coll_ack_ids:
                report["ledger_ids"] = report.get("ledger_ids", []) + coll_ack_ids
        report["summary"] = _verdict(report)
    return report


def _apply_ledger(report: dict, ledger: list) -> None:
    """Tag diffs sanctioned by a deviation reference (target+prop+id).

    Each entry MUST carry an 'id' field (DEV-xxx). Entries without id are applied
    but flagged as unsigned (visible in report['ledger_ids'] as empty string).
    Unused entries — those that match no actual diff — are collected in
    report['ledger_unused'] to prevent silent ledger bloat (P2).
    """
    entry_map = {(e["target"], e["prop"]): (e.get("why", ""), e.get("id", ""))
                 for e in ledger}
    consumed: set = set()
    for rows in report["breakpoints"].values():
        for r in rows:
            k = (r.get("element", ""), r.get("prop", ""))
            if r.get("match") is False and k in entry_map:
                why, eid = entry_map[k]
                r["ledgered"] = True
                r["why"] = why
                if eid:
                    r["ledger_id"] = eid
                consumed.add(k)

    report["ledger_ids"] = [e.get("id", "") for e in ledger]
    report["ledger_unused"] = [
        {"id": e.get("id", ""), "target": e["target"], "prop": e["prop"]}
        for e in ledger if (e["target"], e["prop"]) not in consumed
    ]


def _load_deviations(registry_path: str) -> tuple[dict, list[str]]:
    """Load deviations.json and index its active entries by id.

    A structurally invalid registry is a validation error string, never a traceback: measure.py
    must not exit 1 (the violation code) on a malformed registry. Returns (active_by_id, errors).
    """
    try:
        raw = Path(registry_path).read_text(encoding="utf-8")
    except OSError as exc:
        return {}, [f"ledger-registry unreadable: {exc}"]
    try:
        data = json.loads(raw)
    except ValueError as exc:
        return {}, [f"ledger-registry is not valid JSON ({registry_path}): {exc}"]
    if not isinstance(data, dict):
        return {}, [f"ledger-registry must be a JSON object ({registry_path})"]
    active = data.get("active", [])
    if not isinstance(active, list):
        return {}, [f"ledger-registry .active must be an array ({registry_path})"]
    by_id: dict = {}
    for e in active:
        if isinstance(e, dict) and e.get("id"):
            by_id[e["id"]] = e
    return by_id, []


def _expired(expires: str, today: date) -> bool:
    """A deviation past its declared expiry no longer sanctions. A malformed date is not treated
    as expired here — it is surfaced as its own reason — so the verdict never turns on a parse."""
    try:
        return date.fromisoformat(str(expires)) < today
    except ValueError:
        return False


def _validate_ledger_registry(report: dict, registry_path: str, today: date) -> list[str]:
    """Verify each ledger id the config references resolves to an ACTIVE deviation that carries an
    expected value and has not expired. Any failure is a reason string; the caller forces OPEN.

    deviations.json is the authority (references/deviations-schema.md): an id sanctions a delta
    only if it is in active[], carries a non-empty `expected`, and — if it declares `expires` —
    has not passed it against the run clock. Absence, no expected, or expiry each reopen the verdict.
    Returns a list of validation error strings (empty = every referenced id is a valid sanction).
    """
    by_id, errors = _load_deviations(registry_path)
    if errors:
        return errors
    for eid in report.get("ledger_ids", []):
        if not eid:
            continue  # unsigned entries are already surfaced via ledger_ids (empty strings)
        entry = by_id.get(eid)
        if entry is None:
            errors.append(f"ledger id {eid} absent des écarts actifs de {registry_path} — "
                          "exception qui référence un écart inexistant ou révolu")
            continue
        if not str(entry.get("expected", "")).strip():
            errors.append(f"ledger id {eid} sans valeur 'expected' dans {registry_path} — "
                          "rien à sanctionner")
        expires = entry.get("expires")
        if expires and _expired(expires, today):
            errors.append(f"ledger id {eid} expiré le {expires} — l'écart ne sanctionne plus")
        elif expires and not _valid_date(expires):
            errors.append(f"ledger id {eid} : date d'expiration illisible '{expires}' (ISO-8601 attendu)")
    return errors


def _valid_date(value: str) -> bool:
    try:
        date.fromisoformat(str(value))
        return True
    except ValueError:
        return False


def _norm(s: str) -> str:
    """Normalize typographic punctuation so a curly-quote target (wptexturize) and a
    straight-quote mockup compare equal — a section is missing by STRUCTURE, not by
    the renderer's smart-quotes."""
    return (s.replace("’", "'").replace("‘", "'")
             .replace("”", '"').replace("“", '"')
             .replace("–", "-").replace("—", "-").replace(" ", " "))


def _completeness(mock_headings: list, impl_headings: list) -> dict:
    """Structure before pixels: which section headings exist on each side (quote-normalized)."""
    mock_n, impl_n = {_norm(h) for h in mock_headings}, {_norm(h) for h in impl_headings}
    return {"mockup_headings": mock_headings, "implementation_headings": impl_headings,
            "missing_in_implementation": [h for h in mock_headings if _norm(h) not in impl_n],
            "extra_in_implementation": [h for h in impl_headings if _norm(h) not in mock_n]}


def _coverage(impl_headings: list, targets: list, ack) -> dict:
    """Fewer measured targets than headings => the body is likely unmeasured (tunnel vision).

    coverage_ack must be a structured dict {"sections": [...], "reason": "..."}
    with a non-empty sections list to disable the guard. A bare boolean true is
    accepted for backward compatibility but triggers a migration warning.
    """
    cov = {"implementation_headings": len(impl_headings), "measured_targets": len(targets)}

    # Parse coverage_ack
    ack_sections: list = []
    ack_legacy = False
    if isinstance(ack, dict):
        ack_sections = ack.get("sections") or []
        if ack_sections:
            cov["ack_sections"] = ack_sections
            cov["ack_reason"] = ack.get("reason", "")
    elif ack is True:
        ack_legacy = True

    under = len(targets) < len(impl_headings)
    if not under or ack_sections:
        cov["ok"] = True
        if ack_legacy:
            cov["ok"] = True
            cov["warning"] = ("coverage_ack: upgrade to structured form "
                              '{"sections":[...],"reason":"..."} — bare true accepted but opaque')
    else:
        cov["ok"] = False
        if ack_legacy:
            cov["warning"] = (f"under-coverage: {len(targets)} targets for {len(impl_headings)} headings — "
                              "coverage_ack:true accepted but opaque; upgrade to "
                              '{"sections":[...],"reason":"..."} listing the sections deliberately skipped')
        else:
            cov["warning"] = (f"under-coverage: {len(targets)} targets for {len(impl_headings)} headings — "
                              'set coverage_ack:{"sections":[...],"reason":"..."} listing sections '
                              "deliberately not measured (non-empty list required)")
    return cov


def _verdict(report: dict) -> dict:
    total_diff = total_missing = ledgered = 0
    for rows in report["breakpoints"].values():
        for r in rows:
            if r.get("match") is False:
                if r.get("ledgered"):
                    ledgered += 1
                else:
                    total_diff += 1
        total_missing += sum(1 for r in rows if "missing" in r)
    missing_sections = report.get("completeness", {}).get("missing_in_implementation", [])
    cov = report.get("coverage", {})
    ledger_ids = report.get("ledger_ids", [])
    ledger_unused = report.get("ledger_unused", [])
    # P13 — separate acked from non-acked collection failures
    all_collections = report.get("collections", [])
    failed_collections = [c for c in all_collections if not c.get("ok") and not c.get("acked")]
    acked_collections = [c for c in all_collections if c.get("acked")]
    unused_ack_collections = [c for c in all_collections if c.get("ack_unused")]

    reasons = []
    if total_diff:
        reasons.append(f"{total_diff} unledgered style diff(s)")
    if total_missing:
        reasons.append(f"{total_missing} missing target(s) — stale selector or absent element")
    if missing_sections:
        reasons.append(f"{len(missing_sections)} section(s) missing in implementation: {missing_sections}")
    if not cov.get("ok", True):
        reasons.append(cov.get("warning", "under-coverage"))
    for fc in failed_collections:
        reasons.append(f"collection '{fc['name']}': {fc['mockup_count']} mockup vs "
                       f"{fc['implementation_count']} implementation"
                       + (f", missing: {fc['missing_in_implementation']}" if fc["missing_in_implementation"] else "")
                       + (f", extra: {fc['extra_in_implementation']}" if fc["extra_in_implementation"] else ""))
    # Unsigned ledger entries (no id) — includes unsigned collection acks: surfaced but not alone blocking
    unsigned = [eid for eid in ledger_ids if not eid]
    if unsigned:
        reasons.append(f"{len(unsigned)} unsigned ledger entry(ies) — add 'id' (DEV-xxx) and "
                       "register it in deviations.json § active")

    closed = not reasons
    summary: dict = {"verdict": "CLOSED" if closed else "OPEN", "closed": closed, "reasons": reasons,
                     "total_diff": total_diff, "ledgered_diff": ledgered, "total_missing": total_missing,
                     "missing_sections": len(missing_sections),
                     "collection_failures": len(failed_collections),
                     "ledger_ids": ledger_ids,
                     "ledger_unused_count": len(ledger_unused)}
    if acked_collections:
        summary["collection_acked"] = len(acked_collections)
    if unused_ack_collections:
        summary["collection_ack_unused"] = [{"name": c["name"], "ack_id": c.get("ack_id", "")}
                                            for c in unused_ack_collections]
    return summary


def _summarize(report: dict) -> str:
    lines = []
    for bp, rows in report["breakpoints"].items():
        diffs = sum(1 for r in rows if r.get("match") is False and not r.get("ledgered"))
        led = sum(1 for r in rows if r.get("ledgered"))
        oks = sum(1 for r in rows if r.get("match") is True)
        missing = sum(1 for r in rows if "missing" in r)
        lines.append(f"  {bp:8s} : {oks} match · {diffs} diff · {led} ledgered · {missing} missing")
    comp = report.get("completeness")
    if comp and comp["missing_in_implementation"]:
        lines.append(f"  ! sections missing in implementation : {comp['missing_in_implementation']}")
    cov = report.get("coverage")
    if cov and not cov.get("ok", True):
        lines.append(f"  ! {cov['warning']}")
    for fc in report.get("collections", []):
        if not fc.get("ok"):
            head = f"collection '{fc['name']}': {fc['mockup_count']} mockup vs {fc['implementation_count']} implementation"
            miss = f"  missing={fc['missing_in_implementation']}" if fc["missing_in_implementation"] else ""
            extra = f"  extra={fc['extra_in_implementation']}" if fc["extra_in_implementation"] else ""
            if fc.get("acked"):
                lines.append(f"  ~ {head} [ACKED {fc.get('ack_id') or 'unsigned'}]{miss}{extra}")
            else:
                lines.append(f"  ! {head}{miss}{extra}")
        elif fc.get("ack_unused"):
            lines.append(f"  ~ collection '{fc['name']}': ok but ack {fc.get('ack_id') or 'unsigned'} unused")
    unused = report.get("ledger_unused", [])
    if unused:
        ids = [e.get("id") or "(unsigned)" for e in unused]
        lines.append(f"  ! ledger_unused ({len(unused)}) — no matching diff: {ids}")
    s = report.get("summary")
    if s:
        lines.append(f"  VERDICT  : {s['verdict']}" + ("" if s["closed"] else f" — {'; '.join(s['reasons'])}"))
    return "\n".join(lines)


def main():
    # P10 — fix UnicodeEncodeError on Windows (cp1252 stdout) when _summarize emits →/★/·
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="Fidelity oracle (computed-style diff, per breakpoint).")
    ap.add_argument("--config", required=True, help="Path to the JSON config.")
    ap.add_argument("--out", required=True, help="Path to write the JSON report (UTF-8).")
    ap.add_argument("--mode", choices=["A", "B"], default="B",
                    help="A=extract one side, B=diff mockup<->implementation.")
    ap.add_argument("--side", choices=["mockup", "implementation"], default="implementation",
                    help="Mode A only: which side to extract.")
    ap.add_argument("--ledger-registry", required=True,
                    help="Path to deviations.json. REQUIRED: every tolerated exception must resolve "
                         "to an active entry carrying an expected value. Each ledger id in the config "
                         "is validated against this file; an id that is not an active, unexpired entry "
                         "with an expected value forces verdict=OPEN.")
    args = ap.parse_args()

    cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
    base_dir = Path(args.config).resolve().parent
    report = measure(cfg, args.mode, args.side, base_dir)

    # P1 — validate ledger ids against deviations.json (the authority) in mode B
    if args.mode == "B":
        today = datetime.now(timezone.utc).date()
        registry_errors = _validate_ledger_registry(report, args.ledger_registry, today)
        if registry_errors:
            s = report.get("summary", {})
            s["reasons"] = registry_errors + s.get("reasons", [])
            s["verdict"] = "OPEN"
            s["closed"] = False
            report["summary"] = s

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Report -> {out}")
    print(_summarize(report))


if __name__ == "__main__":
    main()
