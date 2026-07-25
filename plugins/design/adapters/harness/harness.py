#!/usr/bin/env python3
"""
design:harness — standalone HTML maquette generator.

Produces a single auto-contained HTML file exposing window.setPage(key) /
window.setViewport(mode) and a .preview-bar toolbar. The file is driven by the
fidelity oracle (adapters/measure/measure.py) and the copycat fan-out.

Usage:
  python harness.py --out maquette.html
  python harness.py --out maquette.html --title "My Site" --pages "home:Accueil, contact:Contact"
  python harness.py --out maquette.html --title "My Site" --pages-json pages.json
  python harness.py --out maquette.html --contract <dir>   # inline the contract's tokens

Default (no --pages / --pages-json): single placeholder page "page-1" / "Page 1".

pages.json format — list of objects (or {"pages": [...]}):
  [{"key": "home", "label": "Accueil"}, {"key": "about", "label": "À propos", "group": "Info"}]

--contract (opt-in): inline the contract's already-generated stylesheet adapter — the
  policies.json § adapters[] entry whose consumer is "stylesheet" — into the maquette, so
  the reference speaks the same tokens the implementation is linted against. Nothing is
  derived or regenerated here (option C): the artifact is read as produced by generate.py.
  Exit codes under --contract: 0 ok (or no stylesheet adapter → one stderr warning, scaffold);
  3 the contract is 1.x (no release.json) — migrate it (tools/migrate-contract.py); 2 any
  required artifact is absent, unreadable, or structurally invalid. Never 1, never 4.
  Without --contract the scaffold path is unchanged and always exits 0.
"""

import argparse
import json
import sys
from pathlib import Path


# ─── Page parsing ────────────────────────────────────────────────────────────

def parse_pages_str(s):
    """Parse "key:Label, key2:Label 2" into list of {"key", "label"} dicts."""
    pages = []
    for item in s.split(","):
        item = item.strip()
        if not item:
            continue
        if ":" in item:
            key, _, label = item.partition(":")
            pages.append({"key": key.strip(), "label": label.strip()})
        else:
            pages.append({"key": item, "label": item})
    return pages


def key_to_fn(key):
    """Convert 'my-page-key' → 'pageMyPageKey'."""
    parts = key.replace("-", " ").replace("_", " ").split()
    return "page" + "".join(p.capitalize() for p in parts)


# ─── HTML fragment builders ──────────────────────────────────────────────────

def build_options(pages):
    """<option> / <optgroup> HTML for the page selector."""
    ungrouped = [p for p in pages if not p.get("group")]
    groups = {}
    for p in pages:
        g = p.get("group")
        if g:
            groups.setdefault(g, []).append(p)

    lines = []
    for p in ungrouped:
        lines.append(f'        <option value="{p["key"]}">{p["label"]}</option>')
    for g_name, g_pages in groups.items():
        lines.append(f'        <optgroup label="{g_name}">')
        for p in g_pages:
            lines.append(f'          <option value="{p["key"]}">{p["label"]}</option>')
        lines.append("        </optgroup>")
    return "\n".join(lines)


def build_functions(pages):
    """JS page function declarations (one per page, returning placeholder HTML)."""
    lines = []
    for p in pages:
        fn = key_to_fn(p["key"])
        k = p["key"].replace("'", "\\'")
        lbl = p["label"].replace("'", "\\'").replace("<", "&lt;").replace(">", "&gt;")
        lines.append(f"  function {fn}() {{ return placeholder('{k}', '{lbl}'); }}")
    return "\n".join(lines)


def build_registry(pages):
    """JS object literal entries for the pages const."""
    lines = []
    for p in pages:
        fn = key_to_fn(p["key"])
        k = p["key"].replace("'", "\\'")
        lines.append(f"    '{k}': {fn},")
    return "\n".join(lines)


# ─── Template ────────────────────────────────────────────────────────────────
# Uses %%PLACEHOLDER%% substitution — no .format() — so {} in HTML/CSS/JS are literal.

TEMPLATE = r"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%%TITLE%% — maquette de référence</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
%%TOKENS_STYLE%%
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body { height: 100%; }
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #fff; color: #1F2A37; overflow: hidden; }

  /* ===== Preview chrome — HIDDEN by the fidelity oracle before measuring ===== */
  .preview-bar {
    position: fixed; top: 0; left: 0; right: 0; height: 56px; z-index: 9999;
    display: flex; align-items: center; justify-content: space-between; padding: 0 24px;
    background: #1F2A37; color: #fff; border-bottom: 1px solid rgba(255,255,255,.1);
  }
  .preview-bar__brand { font-size: 18px; font-weight: 600; display: flex; align-items: center; gap: 12px; }
  .preview-bar__brand small { font-size: 12px; font-weight: 400; color: rgba(255,255,255,.5); letter-spacing: .04em; text-transform: uppercase; }
  .preview-bar__controls { display: flex; gap: 12px; align-items: center; }
  .page-select {
    background: rgba(255,255,255,.08); color: #fff; border: 1px solid rgba(255,255,255,.15);
    padding: 8px 32px 8px 14px; font-size: 13px; font-weight: 500; border-radius: 8px; cursor: pointer;
    appearance: none; -webkit-appearance: none; min-width: 220px;
    background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%23FFFFFF' stroke-width='2'><polyline points='6 9 12 15 18 9'/></svg>");
    background-repeat: no-repeat; background-position: right 10px center;
  }
  .page-select option { background: #1F2A37; }
  .page-select optgroup { font-weight: 600; }
  .viewport-toggle { display: flex; gap: 4px; padding: 4px; background: rgba(255,255,255,.08); border-radius: 8px; }
  .viewport-btn {
    background: transparent; border: none; color: rgba(255,255,255,.7); padding: 6px 12px;
    font-size: 13px; font-weight: 500; border-radius: 6px; cursor: pointer;
    display: flex; align-items: center; gap: 6px; transition: all .2s;
  }
  .viewport-btn svg { width: 14px; height: 14px; }
  .viewport-btn:hover { color: #fff; }
  .viewport-btn.active { background: #fff; color: #1F2A37; }

  /* ===== Stage + device frame ===== */
  .preview-stage { position: fixed; top: 56px; left: 0; right: 0; bottom: 0; overflow-y: auto; background: #f0f0f0; }
  .preview-frame {
    width: 100%; max-width: 100%; margin: 0 auto; position: relative; overflow-x: hidden;
    background: #fff; transition: max-width .4s cubic-bezier(.22,1,.36,1);
  }
  .preview-frame.tablet { max-width: 834px; border-radius: 24px; border: 10px solid #1F2A37; box-shadow: 0 30px 80px rgba(0,0,0,.25); margin: 24px auto; overflow: hidden; }
  .preview-frame.mobile { max-width: 390px; border-radius: 32px; border: 8px solid #1F2A37; box-shadow: 0 30px 80px rgba(0,0,0,.3); margin: 32px auto; overflow: hidden; }
  /* 834 / 390 are fixed device samples, not contract breakpoints — see the RESPONSIVE note. */
  #page-container { display: block; width: 100%; }

  /* Placeholder until a page function is filled in. */
  .ph { padding: 80px 32px; text-align: center; color: #6B7280; }
  .ph h2 { font-size: 28px; color: #1F2A37; margin-bottom: 12px; font-weight: 600; }
  .ph p { font-size: 14px; line-height: 1.6; }
  .ph code { background: #F4F4F4; padding: 2px 6px; border-radius: 4px; font-size: 13px; }

  /* Author responsive overrides: `.preview-frame.mobile <sel>` / `.preview-frame.tablet <sel>`
     They fire both in manual preview (frame class) AND under the fidelity oracle, which
     toggles the same class via window.setViewport. Class-based only — no media queries.
     The three frames are device samples (desktop fluid · tablet 834 · mobile 390),
     not contract breakpoints: nothing here is derived from tokens.json § breakpoint.*. */
</style>
</head>
<body>
<!--
  ============================================================================
  MAQUETTE DE RÉFÉRENCE · %%TITLE%%
  Généré par : design:harness (adapters/harness/harness.py)
  ============================================================================
  À QUOI SERT CE FICHIER
    Formaliser une maquette pour le plugin `design` : piloté par l'oracle de
    fidélité (adapters/measure/measure.py) et par le fan-out `copycat`.
    Contrat : window.setPage(key) · window.setViewport(mode) · barre .preview-bar.

  COMMENT LE REMPLIR (1 page = 1 fonction)
    1. Dans le 1er <script>, chaque page est une fonction `pageXxx()` qui RETOURNE
       le HTML de la page (template literal). Remplace le corps :
           function pageHome() { return placeholder('home', 'Accueil'); }
       devient :
           function pageHome() { return `
             <header class="site-header">...</header>
             <main>...</main>
             <footer class="site-footer">...</footer>
           `; }
    2. Le HTML retourné est injecté dans #page-container : PAS de
       <html>/<head>/<body> ni de <style> global dans la fonction.
       Les styles vont dans le <style> du <head>.
    3. La clé de page doit correspondre à la valeur de l'<option> ET
       au champ "maquette_page" du config measure.

  RÈGLES ORACLE (fidélité mesurée)
    • Sélecteurs STABLES et sémantiques (BEM : .hero__title, .card__price).
    • Un seul h1 par page ; hiérarchie de titres réelle (h2/h3 par section).
    • NE PAS modifier .preview-bar ni les <script> de contrôle.
    • URLs absolues ou data: pour images / fonts (fichier servi en statique).

  RESPONSIVE
    Écrire les variations device en CLASSE dans le <style> du <head> :
        .preview-frame.mobile .hero__title { font-size: 28px; }
        .preview-frame.tablet .hero__inner { grid-template-columns: 1fr; }
    JAMAIS de media query : la classe bascule à l'aperçu manuel ET sous l'oracle
    (qui appelle window.setViewport). Les trois cadres sont des ÉCHANTILLONS
    device — desktop (fluide) · tablet 834 · mobile 390 — pas des breakpoints
    du contrat : rien ici ne dérive de tokens.json § breakpoint.*.

  ============================================================================
  PROMPT LLM (à copier pour faire remplir une page depuis un visuel/brief)
  ============================================================================
    « Voici une maquette de référence "%%TITLE%%" (harness HTML auto-contenu avec
      .preview-bar, registre `pages` de fonctions, responsive par classe
      .preview-frame.mobile|tablet). À partir du visuel/brief que je te donne
      pour la page "<CLÉ>", remplis UNIQUEMENT le corps de la fonction `pageXxx()` :
      retourne le HTML (sans <html>/<head>/<body>), classes STABLES BEM,
      hiérarchie de titres (un seul h1), styles dans le <style> du <head> —
      variations device en .preview-frame.mobile / .preview-frame.tablet,
      jamais de media query. Ne modifie pas .preview-bar ni les scripts. »%%TOKENS_NOTE_HEADER%%
  ============================================================================
-->
  <div class="preview-bar">
    <div class="preview-bar__brand">
      %%TITLE%% <small>maquette</small>
    </div>
    <div class="preview-bar__controls">
      <select class="page-select" id="page-select">
%%PAGE_OPTIONS%%
      </select>
      <div class="viewport-toggle" role="group" aria-label="Device">
        <button class="viewport-btn active" data-viewport="desktop" type="button"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg> Desktop</button>
        <button class="viewport-btn" data-viewport="tablet" type="button"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="4" y="2" width="16" height="20" rx="2"/><circle cx="12" cy="18" r="1" fill="currentColor" stroke="none"/></svg> Tablette</button>
        <button class="viewport-btn" data-viewport="mobile" type="button"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="5" y="2" width="14" height="20" rx="2"/><circle cx="12" cy="18" r="1" fill="currentColor" stroke="none"/></svg> Mobile</button>
      </div>
    </div>
  </div>

  <div class="preview-stage">
    <div class="preview-frame" id="preview-frame">
      <div id="page-container" class="site"></div>
    </div>
  </div>

  <script>
    // ===== Page registry — one function per page, returning the page HTML string. =====
    // FILL EACH PAGE: replace `placeholder(...)` body with the page markup:
    //   function pageHome() { return `<header class="site-header">…</header><main>…</main>`; }
    // Rules:
    //   • return ONLY the page content (no <html>/<head>/<body>); global styles go in <head>.
    //   • stable, semantic class names (BEM) — the fidelity oracle measures by CSS selector.
    //   • device variations as `.preview-frame.mobile|tablet <sel>` in <head>, no media queries.
    //   • never edit .preview-bar or the control scripts below.%%TOKENS_NOTE_RULES%%
    function placeholder(key, label) {
      return '<div class="ph"><h2>' + label + '</h2>'
        + '<p>Page <code>' + key + '</code> — remplacez le corps de la fonction '
        + 'dans le registre <code>pages</code> ci-dessous.</p></div>';
    }

%%PAGE_FUNCTIONS%%

    const pages = {
%%PAGE_REGISTRY%%
    };
  </script>

  <script>
    let currentPage = '%%FIRST_PAGE_KEY%%';
    let currentViewport = 'desktop';
    const container = document.getElementById('page-container');
    const frame = document.getElementById('preview-frame');
    const select = document.getElementById('page-select');

    function render() {
      const fn = pages[currentPage];
      container.innerHTML = fn ? fn() : '<div class="ph"><h2>Page introuvable</h2></div>';
      const stage = document.querySelector('.preview-stage');
      if (stage) stage.scrollTop = 0;
    }
    function setPage(page) {
      currentPage = page;
      if (select && select.value !== page) select.value = page;
      try { history.replaceState(null, '', '#' + encodeURIComponent(page)); } catch (e) {}
      render();
    }
    function setViewport(vp) {
      currentViewport = vp;
      frame.classList.remove('tablet', 'mobile');
      if (vp === 'tablet' || vp === 'mobile') frame.classList.add(vp);
      document.querySelectorAll('.viewport-btn').forEach(
        b => b.classList.toggle('active', b.dataset.viewport === vp)
      );
    }

    window.setPage = setPage;
    window.setViewport = setViewport;

    select.addEventListener('change', e => setPage(e.target.value));
    document.querySelectorAll('.viewport-btn').forEach(
      b => b.addEventListener('click', () => setViewport(b.dataset.viewport))
    );

    (function init() {
      const hash = decodeURIComponent((location.hash || '').slice(1));
      if (hash && pages[hash]) { currentPage = hash; if (select) select.value = hash; }
      setViewport('desktop');
      render();
    })();
  </script>
</body>
</html>
"""


# ─── Contract resolution (opt-in --contract) ─────────────────────────────────
# Option C: inline the ALREADY-generated stylesheet adapter. Nothing is derived or
# regenerated here — the harness reads what generate.py produced. Exit-code space is
# 0 / 2 / 3, never 1, never 4 (master § Exit-code space; references/harness-contract.md).

RELEASE = "release.json"
POLICIES = "policies.json"

TOKENS_NOTE_HEADER = (
    "\n\n  CONTRAT INLINE (--contract)\n"
    "    La feuille de tokens du contrat est inline dans le <head>, avant le chrome.\n"
    "    Consomme ces tokens via var(--…) ; ne code jamais en dur couleur/espacement/typo."
)
TOKENS_NOTE_RULES = (
    "\n    //   • when the contract stylesheet is inlined, consume its tokens via "
    "var(--…); never hardcode color/spacing/type values."
)


def _fail(message):
    """Print to stderr and return the invocation/invalid-artifact code (2)."""
    print(message, file=sys.stderr)
    return 2


def resolve_tokens_style(contract):
    """Resolve the contract's stylesheet adapter into an inline <style> block.

    Returns (style, code). code is None on success; style is the <style> block, or ""
    when the contract declares no stylesheet adapter (scaffold, one stderr warning).
    A non-None code (3 = 1.x contract, 2 = missing/unreadable/invalid artifact) means
    the caller stops with that code — the file is not written.
    """
    cdir = Path(contract)
    release = cdir / RELEASE
    if not release.is_file():
        # Absence alone means 1.x — the only branch that yields 3.
        print(f"1.x contract: no {RELEASE} in {cdir.resolve()}\n"
              f"  Migrate it first: python tools/migrate-contract.py --contract {contract}",
              file=sys.stderr)
        return None, 3
    try:
        json.loads(release.read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        # Present but corrupt is a broken contract, not a 1.x one: exit 2, not 3.
        return None, _fail(f"Unreadable {RELEASE}: {exc}\n  {release.resolve()}\n"
                           "  A present but invalid release.json is a broken contract, "
                           "not 1.x — fix the artifact or re-freeze the contract.")

    policies_path = cdir / POLICIES
    if not policies_path.is_file():
        return None, _fail(f"Missing artifact: {policies_path.resolve()}")
    try:
        policies = json.loads(policies_path.read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        return None, _fail(f"Unreadable {POLICIES}: {exc}\n  {policies_path.resolve()}")
    if not isinstance(policies, dict):
        return None, _fail(f"{POLICIES} is not an object: {policies_path.resolve()}")

    adapters = policies.get("adapters")
    entry = None
    if isinstance(adapters, list):
        for candidate in adapters:
            if isinstance(candidate, dict) and candidate.get("consumer") == "stylesheet":
                entry = candidate
                break
    if entry is None:
        print(f"Warning: no adapters[] entry declares consumer \"stylesheet\" in {POLICIES}; "
              "continuing in scaffold mode (no tokens inlined).", file=sys.stderr)
        return "", None

    artifact = entry.get("artifact")
    if not isinstance(artifact, str) or not artifact:
        return None, _fail(f"{POLICIES} adapters[].artifact is not a non-empty string: "
                           f"{policies_path.resolve()}")
    css_path = cdir / artifact
    try:
        css = css_path.read_text(encoding="utf-8")
    except (OSError, ValueError):
        # Option C: the harness never derives the stylesheet — generate.py owns it.
        return None, _fail(f"Declared stylesheet adapter is absent or unreadable: "
                           f"{css_path.resolve()}\n"
                           f"  Generate it first: python tools/generate.py --contract {contract}")
    style = "<style>\n" + css.rstrip("\n") + "\n</style>"
    return style, None


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description="design:harness — HTML maquette generator")
    ap.add_argument("--out", required=True, help="Output HTML file path")
    ap.add_argument("--title", default="Maquette", help='Project title (default: "Maquette")')
    ap.add_argument("--pages", default=None,
                    help='Pages as "key:Label, key2:Label 2" (default: page-1:Page 1)')
    ap.add_argument("--pages-json", default=None,
                    help="Path to JSON file — list [{key, label, group?}] or {pages: [...]}")
    ap.add_argument("--contract", default=None,
                    help="Contract dir — inline its generated stylesheet adapter (opt-in)")
    args = ap.parse_args()

    # Opt-in contract coupling. Absent, style stays "" and the scaffold path is unchanged.
    style = ""
    if args.contract is not None:
        style, code = resolve_tokens_style(args.contract)
        if code is not None:
            return code

    if args.pages_json:
        data = json.loads(Path(args.pages_json).read_text("utf-8"))
        pages = data if isinstance(data, list) else data.get("pages", [])
    elif args.pages:
        pages = parse_pages_str(args.pages)
    else:
        pages = [{"key": "page-1", "label": "Page 1"}]

    if not pages:
        # An invocation error, not a violation (1) — 1 is not in the harness code space.
        print("Error: no pages defined.", file=sys.stderr)
        return 2

    note_header = TOKENS_NOTE_HEADER if style else ""
    note_rules = TOKENS_NOTE_RULES if style else ""

    html = (TEMPLATE
            .replace("%%TOKENS_STYLE%%\n", (style + "\n") if style else "")
            .replace("%%TOKENS_NOTE_HEADER%%", note_header)
            .replace("%%TOKENS_NOTE_RULES%%", note_rules)
            .replace("%%TITLE%%", args.title)
            .replace("%%PAGE_OPTIONS%%", build_options(pages))
            .replace("%%PAGE_FUNCTIONS%%", build_functions(pages))
            .replace("%%PAGE_REGISTRY%%", build_registry(pages))
            .replace("%%FIRST_PAGE_KEY%%", pages[0]["key"]))

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"Harness written -> {out}  ({len(pages)} page(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
