#!/usr/bin/env python3
"""config-gen — génère un config oracle (measure.py) depuis le contrat design system.

Lit design/components.json + design/tokens.json + design/oracle.json et produit un config JSON
exploitable directement par measure.py. Élimine la construction manuelle du selector mapping
pour les composants déclarés dans le manifeste.

Usage:
  python config-gen.py \\
    --components design/components.json \\
    --tokens design/tokens.json \\
    --reference-url http://localhost:8080 \\
    --implementation-url http://localhost:8888 \\
    --page accueil \\
    --out aidd_docs/qa/fidelity/accueil.config.json

Le config produit est un point de départ :
  - Sélecteurs implémentation : dérivés du manifeste (classes BEM canoniques) — déjà corrects.
  - Sélecteurs mockup         : identiques à l'implémentation par défaut. Surcharger si le mockup
    utilise des classes différentes. Inspecter les deux DOMs pour confirmer.
  - Props                     : dérivées des groupes de tokens présents dans tokens.json.
  - Breakpoints               : dérivés de tokens.breakpoint.* ou fallback mobile 375 + desktop 1440.
  - Hints oracle              : check_text et collections lus depuis oracle.json si présent.

Après génération :
  1. Vérifier que les sélecteurs résolvent sur les deux DOMs —
     measure.py signale les targets manquants en "missing".
  2. Surcharger le champ "mockup" des targets où le mockup diffère des classes DS.
  3. Ajouter coverage_ack si des sections sont délibérément non mesurées.
  4. Ajouter des targets manuels pour les éléments hors manifeste découverts via visual-diff.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

# Mapping groupe de tokens → propriétés CSS à mesurer.
# Ordre par valeur diagnostique décroissante ; chaque prop n'est ajoutée qu'une fois.
_GROUP_PROPS: list[tuple[str, list[str]]] = [
    ("font.size",        ["fontSize"]),
    ("font.weight",      ["fontWeight"]),
    ("font.lineHeight",  ["lineHeight"]),
    ("font.family",      ["fontFamily"]),
    ("color",            ["color", "backgroundColor"]),
    ("space",            ["paddingTop", "paddingBottom", "paddingLeft", "paddingRight",
                          "gap", "columnGap", "rowGap"]),
    ("radius",           ["borderRadius"]),
    ("shadow",           ["boxShadow"]),
    ("border.width",     ["borderWidth", "borderColor"]),
    ("motion.duration",  ["transitionDuration"]),
]

_DEFAULT_BREAKPOINTS = [
    {"name": "mobile",  "width": 375,  "height": 812,  "mockup_viewport": "mobile"},
    {"name": "desktop", "width": 1440, "height": 900,  "mockup_viewport": "desktop"},
]

# Heuristiques de nommage pour les tokens breakpoint.*
_BP_MAP: dict[str, tuple[str, int, int]] = {
    "mobile":  ("mobile",  375,  812),
    "sm":      ("mobile",  375,  812),
    "tablet":  ("tablet",  834,  1194),
    "md":      ("tablet",  834,  1194),
    "lg":      ("desktop", 1440, 900),
    "desktop": ("desktop", 1440, 900),
    "xl":      ("desktop", 1440, 900),
}

_BP_ORDER = {"mobile": 0, "tablet": 1, "desktop": 2}


def _flatten_prefixes(obj: dict, prefix: str = "") -> set[str]:
    """Retourne les préfixes de chemin des tokens (ex. 'font.size', 'color')."""
    prefixes: set[str] = set()
    for k, v in obj.items():
        path = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict) and "$type" not in v:
            prefixes.add(path)
            prefixes |= _flatten_prefixes(v, path)
        else:
            prefixes.add(path)
    return prefixes


def _derive_props(tokens: dict) -> list[str]:
    """Dérive la liste de props CSS depuis les groupes de tokens présents."""
    token_prefixes = _flatten_prefixes(tokens)
    props: list[str] = []
    seen: set[str] = set()
    for group, css_props in _GROUP_PROPS:
        if any(p == group or p.startswith(group + ".") for p in token_prefixes):
            for p in css_props:
                if p not in seen:
                    props.append(p)
                    seen.add(p)
    # Fallback si tokens.json est minimal
    return props or ["fontSize", "color", "backgroundColor", "padding", "gap"]


def _derive_breakpoints(tokens: dict) -> list[dict]:
    """Dérive les breakpoints depuis tokens.breakpoint.* ou fallback mobile+desktop.

    Invariant prouvé, non vérifié au runtime : `mockup_viewport ∈ {desktop, tablet, mobile}`.
    Toute clé `tokens.breakpoint.*` hors de `_BP_MAP` est ignorée (`:110-112`), le nom est
    pris dans `_BP_MAP` (`:121-122`), et le fallback est mobile+desktop (`:55-56`). L'ensemble
    est donc clos par construction — c'est exactement les trois échantillons device exposés
    par le harness (references/harness-contract.md § Accord measure / oracle)."""
    bp_group = tokens.get("breakpoint", {})
    if not bp_group:
        return _DEFAULT_BREAKPOINTS

    seen_names: set[str] = set()
    breakpoints: list[dict] = []
    for key, val in bp_group.items():
        hint = _BP_MAP.get(key)
        if not hint:
            continue
        name, default_w, default_h = hint
        if name in seen_names:
            continue
        raw = val.get("$value", "") if isinstance(val, dict) else str(val)
        try:
            w = int(str(raw).replace("px", "").strip())
        except ValueError:
            w = default_w
        breakpoints.append({"name": name, "width": w, "height": default_h,
                            "mockup_viewport": name})
        seen_names.add(name)

    if not breakpoints:
        return _DEFAULT_BREAKPOINTS
    breakpoints.sort(key=lambda b: _BP_ORDER.get(b["name"], 99))
    return breakpoints


def _dot_selector(cls: str) -> str:
    """Ajoute le préfixe '.' si absent."""
    return cls if cls.startswith(".") else f".{cls}"


def _derive_targets_and_collections(
    components: dict,
    oracle_hints: dict,
) -> tuple[list[dict], list[dict]]:
    """Dérive targets et collections depuis components.json + les hints de oracle.json."""
    targets: list[dict] = []
    collections: list[dict] = []

    for comp_name, comp in components.get("components", {}).items():
        base = comp.get("base", comp_name)
        oracle = oracle_hints.get(comp_name, {})
        oracle_elems = oracle.get("elements", {})

        # Target racine du composant (élément de layout — pas de check_text par défaut)
        root_sel = _dot_selector(base)
        targets.append({"name": comp_name, "mockup": root_sel, "implementation": root_sel})

        # Targets par élément BEM
        for elem_label, elem_class in comp.get("elements", {}).items():
            hint = oracle_elems.get(elem_label, {})
            sel = _dot_selector(elem_class)
            target: dict = {
                "name": f"{comp_name} · {elem_label}",
                "mockup": sel,
                "implementation": sel,
            }
            if hint.get("check_text"):
                target["check_text"] = True
            if hint.get("props"):
                target["props"] = hint["props"]
            targets.append(target)

        # Collections depuis oracle.collections
        for coll in oracle.get("collections", []):
            item_sel = _dot_selector(coll.get("item_selector", ""))
            entry: dict = {
                "name": coll.get("name", f"{comp_name} · items"),
                "mockup": item_sel,
                "implementation": item_sel,
            }
            if coll.get("ack"):
                entry["ack"] = coll["ack"]
            collections.append(entry)

    return targets, collections


def _css_rules(text: str):
    """Yield (selector, declaration-body), descending through media/layer/supports blocks."""
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    cursor = 0
    while cursor < len(text):
        opening = text.find("{", cursor)
        if opening < 0:
            return
        header = text[cursor:opening].strip()
        depth, closing = 1, opening + 1
        while closing < len(text) and depth:
            depth += (text[closing] == "{") - (text[closing] == "}")
            closing += 1
        if depth:
            return
        body = text[opening + 1:closing - 1]
        if header.startswith("@"):
            yield from _css_rules(body)
        elif header:
            yield header, body
        cursor = closing


def _declarations(body: str) -> list[str]:
    props = []
    for declaration in body.split(";"):
        name, separator, _ = declaration.partition(":")
        name = name.strip().lower()
        if separator and name and not name.startswith("--") and re.fullmatch(r"[a-z-]+", name):
            props.append(name)
    return props


def _camel_to_kebab(value: str) -> str:
    return re.sub(r"(?<!^)([A-Z])", r"-\1", value).lower()


def _derive_ownership_targets(components: dict, oracle_hints: dict,
                              stylesheets: list[str]) -> list[dict]:
    """Derive proof targets from declarations actually present in DS/platform binding sheets."""
    classes: dict[str, tuple[str, set[str]]] = {}
    for comp_name, comp in components.get("components", {}).items():
        base = comp.get("base", comp_name).lstrip(".")
        root_props = {_camel_to_kebab(p) for p in oracle_hints.get(comp_name, {}).get("props", [])}
        classes[base] = (comp_name, root_props)
        hints = oracle_hints.get(comp_name, {}).get("elements", {})
        for label, cls in comp.get("elements", {}).items():
            hinted = {_camel_to_kebab(p) for p in hints.get(label, {}).get("props", [])}
            classes[str(cls).lstrip(".")] = (f"{comp_name} · {label}", hinted)

    found: dict[tuple[str, str, str], dict] = {}
    seen_classes: set[str] = set()
    sources = [Path(path).name for path in stylesheets]
    for stylesheet in stylesheets:
        text = Path(stylesheet).read_text(encoding="utf-8")
        for selector_group, body in _css_rules(text):
            declared = _declarations(body)
            for selector in (part.strip() for part in selector_group.split(",")):
                for cls, (label, hinted) in classes.items():
                    if not re.search(rf"(?<![\w-])\.{re.escape(cls)}(?![\w-])", selector):
                        continue
                    seen_classes.add(cls)
                    props = [prop for prop in declared if not hinted or prop in hinted]
                    for prop in props:
                        key = (cls, selector, prop)
                        row = found.setdefault(key, {"name": label, "selector": selector,
                                                     "class": cls, "prop": prop, "sources": []})
                        source = Path(stylesheet).name
                        if source not in row["sources"]:
                            row["sources"].append(source)
    for cls, (label, _) in classes.items():
        if cls not in seen_classes:
            found[(cls, f".{cls}", "")] = {
                "name": label, "selector": f".{cls}", "class": cls, "prop": None,
                "sources": sources, "unrealized_reason": "DS class has no inspectable declaration",
            }
    return list(found.values())


def generate(
    components_path: str,
    tokens_path: str,
    reference_url: str,
    implementation_url: str,
    page: str | None = None,
    oracle_path: str | None = None,
    ownership_stylesheets: list[str] | None = None,
    editor_url: str | None = None,
) -> dict:
    components = json.loads(Path(components_path).read_text(encoding="utf-8"))
    tokens = json.loads(Path(tokens_path).read_text(encoding="utf-8"))

    # Les hints de mesure vivent dans oracle.json, artefact frère de components.json
    # (cf. references/contract-schema.md). Par défaut, le frère du manifeste ; absent,
    # les targets se dérivent de la seule anatomie, sans check_text ni collections.
    oracle_file = Path(oracle_path) if oracle_path else Path(components_path).with_name("oracle.json")
    oracle_hints: dict = {}
    if oracle_file.is_file():
        oracle_hints = json.loads(oracle_file.read_text(encoding="utf-8")).get("components", {})

    props = _derive_props(tokens)
    breakpoints = _derive_breakpoints(tokens)
    targets, collections = _derive_targets_and_collections(components, oracle_hints)

    cfg: dict = {
        "_generated_by": "config-gen.py — review selectors before use",
        "reference_url": reference_url,
        "implementation_url": implementation_url,
        "breakpoints": breakpoints,
        "props": props,
        "targets": targets,
        "headings_sel": {"mockup": "h1, h2, h3", "implementation": "h1, h2, h3"},
    }
    if page:
        cfg["reference_page"] = page
    if collections:
        cfg["collections"] = collections
    if ownership_stylesheets:
        cfg["ownership"] = {
            "surfaces": [
                {"name": "front", "url": implementation_url},
                {"name": "editor", "url": editor_url or implementation_url.rstrip("/") + "/wp-admin/site-editor.php",
                 "frame_selector": "iframe[name=editor-canvas]", "requires_auth": True,
                 "storage_state_env": "WP_EDITOR_STORAGE_STATE", "auth_hook_env": "WP_EDITOR_AUTH_HOOK"},
            ],
            "targets": _derive_ownership_targets(
                components, oracle_hints, ownership_stylesheets),
        }
    return cfg


def main():
    ap = argparse.ArgumentParser(
        description="Génère un config measure.py depuis le contrat design system (components.json + tokens.json + oracle.json)."
    )
    ap.add_argument("--components", required=True,
                    help="Chemin vers design/components.json")
    ap.add_argument("--tokens", required=True,
                    help="Chemin vers design/tokens.json")
    ap.add_argument("--oracle", default=None,
                    help="Chemin vers design/oracle.json (défaut : frère de --components)")
    # Deux rôles, jamais deux plateformes : la référence est ce qui fait foi, l'implémentation
    # est ce qui est mesuré contre elle.
    ap.add_argument("--reference-url", required=True, dest="reference_url",
                    help="URL de la référence qui fait foi (servie en HTTP)")
    ap.add_argument("--implementation-url", required=True, dest="implementation_url",
                    help="URL de l'implémentation mesurée contre la référence")
    ap.add_argument("--page", default=None,
                    help="Clé setPage pour les mockups SPA (window.setPage)")
    ap.add_argument("--ownership-stylesheet", action="append", default=[],
                    help="Feuille DS ou fse-bindings.css à inspecter (répétable); active la preuve front+éditeur")
    ap.add_argument("--editor-url", default=None,
                    help="URL de l’éditeur FSE (défaut: <implementation-url>/wp-admin/site-editor.php)")
    ap.add_argument("--out", required=True,
                    help="Chemin de sortie du config JSON (ex. aidd_docs/qa/fidelity/accueil.config.json)")
    args = ap.parse_args()

    cfg = generate(args.components, args.tokens,
                   args.reference_url, args.implementation_url, args.page, args.oracle,
                   args.ownership_stylesheet, args.editor_url)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")

    n_t = len(cfg["targets"])
    n_c = len(cfg.get("collections", []))
    n_b = len(cfg["breakpoints"])
    n_p = len(cfg["props"])
    print(f"Config -> {out}")
    print(f"  {n_t} target(s)  ·  {n_c} collection(s)  ·  {n_b} breakpoint(s)  ·  {n_p} prop(s)")
    print("  Vérifier : les sélecteurs résolvent sur les deux DOMs (measure.py -> 'missing' sinon)")
    print("  Surcharger le champ 'mockup' si le mockup utilise des classes différentes des classes DS")


if __name__ == "__main__":
    main()
