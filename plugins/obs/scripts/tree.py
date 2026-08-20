#!/usr/bin/env python3
"""
obs:tree — maintient l'arborescence `Documents/` navigable, sans appel LLM.

    python tree.py index        [<cible>] [--managed-root] [--apply]
    python tree.py check        [<cible>] [--managed-root]
    python tree.py fix          [<cible>] [--managed-root] [--drift] [--apply]
    python tree.py sort         <items…> [--into <cible>] [--apply]
    python tree.py destinations [<cible>] [--out <chemin>] [--apply]

L'ancre (`Perso` ou `Pro`) est découverte en remontant depuis la cible ; aucun
chemin absolu n'est codé en dur. Le cache vit à `<ancre>/_tree/cache.json` et
reste régénérable : le disque fait foi.

Rien n'est écrit sans `--apply`. Aucune suppression, jamais.
Compatible Windows, Linux, macOS. Bibliothèque standard seulement.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from obslib import (  # noqa: E402
    AnchorNotFound,
    Plan,
    dump_yaml,
    error,
    first_heading,
    info,
    in_code_dir,
    is_credential,
    is_dotfile,
    is_media,
    is_month,
    is_portable_slug,
    is_working_dir,
    is_year,
    iter_entries,
    parse_yaml,
    read_frontmatter,
    resolve_anchor,
    slugify,
    today,
    warn,
    write_text,
)

CACHE_REL = Path("_tree") / "cache.json"
DEFAULT_PATTERN = "<category>/<subcategory>/<AAAA>/<MM>/<unité>"
DURABLE_HINTS = ("_univers", "_systeme", "_subsystems")

#: Seuls noms sur lesquels I1 est décidable sans jugement : ceux qu'un outil
#: produit ou consomme, y compris hérités d'outils retirés — le répertoire, lui,
#: est resté sur le disque. Un répertoire au nom libre reste du contenu.
KNOWN_WORKING_DIRS = frozenset(
    {
        "brief", "output", "research", "univers", "systeme", "subsystems",
        "code", "drafts", "trash", "archive", "tree", "corpus", "references",
    }
)

#: Catégories qui ne reçoivent jamais d'email : émises commentées par `destinations`.
NON_EMAIL_CATEGORIES = frozenset(
    {
        "photos", "photo", "images", "musique", "music", "video", "videos",
        "films", "movies", "jeux", "games", "dev", "tech", "library",
        "bibliotheque", "design", "medias", "media",
    }
)


# --------------------------------------------------------------------------- #
# Scan
# --------------------------------------------------------------------------- #


def is_pro_projet(anchor: Path, domain_rel: Path) -> bool:
    """`Pro/Projets/<projet>` a une convention connue, jamais inférée."""
    parts = domain_rel.parts
    return anchor.name == "Pro" and len(parts) >= 2 and parts[0].lower() == "projets"


def scan_domain(anchor: Path, domain_dir: Path) -> dict:
    """Décrit un domaine (niveau `category/subcategory`) tel qu'il est sur disque."""
    rel = domain_dir.relative_to(anchor)
    if is_pro_projet(anchor, rel):
        return scan_pro_projet(anchor, domain_dir)

    units: list[str] = []
    durable: list[str] = []
    dated = False
    for child in sorted(domain_dir.iterdir(), key=lambda p: p.name):
        if not child.is_dir() or is_dotfile(child.name) or child.name in {"_tree"}:
            continue
        if is_working_dir(child.name):
            durable.append(child.name)
            continue
        if is_year(child.name):
            dated = True
            for month in sorted(child.iterdir(), key=lambda p: p.name):
                if not month.is_dir():
                    continue
                if not is_month(month.name):
                    units.append(f"{child.name}/{month.name}")
                    continue
                leaves = [
                    leaf.name
                    for leaf in sorted(month.iterdir(), key=lambda p: p.name)
                    if leaf.is_dir() and not is_dotfile(leaf.name)
                ]
                if leaves:
                    units.extend(f"{child.name}/{month.name}/{leaf}" for leaf in leaves)
                else:
                    units.append(f"{child.name}/{month.name}")
        elif child.name.lower() in KNOWN_WORKING_DIRS:
            # Signalé en I1 par `collect_anomalies` — pas en double comme unité.
            continue
        else:
            units.append(child.name)

    convention = "<AAAA>/<MM>/<unité>" if dated else "plat (<unité>)"
    return {
        "path": rel.as_posix(),
        "dated": dated,
        "convention": convention,
        "units": units,
        "durable": durable,
        "notes": "convention effective apprise du contenu existant",
    }


def scan_pro_projet(anchor: Path, project_dir: Path) -> dict:
    """`Pro/Projets/<projet>` : `_code/` + `<AAAA>/<MM>/`, pas d'INDEX.md attendu."""
    travaux: list[str] = []
    unknown: list[str] = []
    code_dir = None
    for child in sorted(project_dir.iterdir(), key=lambda p: p.name):
        if not child.is_dir() or is_dotfile(child.name):
            continue
        if child.name == "_code":
            code_dir = "_code"
            continue
        if is_year(child.name):
            for month in sorted(child.iterdir(), key=lambda p: p.name):
                if month.is_dir() and is_month(month.name):
                    travaux.append(f"{child.name}/{month.name}")
                elif month.is_dir():
                    unknown.append(f"{child.name}/{month.name}")
            continue
        unknown.append(child.name)

    travaux.sort()
    return {
        "path": project_dir.relative_to(anchor).as_posix(),
        "kind": "pro-projet",
        "dated": True,
        "convention": "_code + AAAA/MM (travaux)",
        "code_dir": code_dir or "_code",
        "travaux": travaux,
        "entry": travaux[-1] if travaux else None,
        "unknown": unknown,
        "notes": "Pro/Projets — entrée courante : mois le plus récent",
    }


def discover_domains(anchor: Path) -> list[Path]:
    """Domaines = niveau `category/subcategory` sous l'ancre.

    Sous `Pro/Projets`, chaque projet est lui-même un domaine à convention
    connue : on descend d'un cran de plus.
    """
    domains: list[Path] = []
    for category in sorted(anchor.iterdir(), key=lambda p: p.name):
        if not category.is_dir() or is_dotfile(category.name) or is_working_dir(category.name):
            continue
        for sub in sorted(category.iterdir(), key=lambda p: p.name):
            if not sub.is_dir() or is_dotfile(sub.name) or is_working_dir(sub.name):
                continue
            if anchor.name == "Pro" and category.name.lower() == "projets":
                domains.append(sub)
            else:
                domains.append(sub)
    return domains


def collect_anomalies(anchor: Path) -> list[str]:
    """Violations I1–I4, formulées « chemin — In: motif → suggestion »."""
    anomalies: list[str] = []
    for path in iter_entries(anchor, recursive=True):
        rel = path.relative_to(anchor)
        name = path.name
        if is_dotfile(name):
            continue
        if in_code_dir(rel):
            # `_code/` suit les conventions du dépôt de code : I2–I3 non jugés.
            continue
        depth = len(rel.parts)
        parent_name = rel.parts[-2] if depth >= 2 else ""

        if path.is_dir() and depth == 1:
            # Niveau `category` : bucket sémantique nommé par l'auteur
            # (`RPG`, `Finance`, `Projets`) — format imposé, hors I3.
            continue
        if path.is_dir() and not is_working_dir(name) and name.lower() in KNOWN_WORKING_DIRS:
            anomalies.append(
                f"{rel.as_posix()} — I1: répertoire de travail sans préfixe `_` "
                f"→ suggestion `_{name.lower()}`"
            )
            continue
        if is_working_dir(parent_name) and is_working_dir(name):
            anomalies.append(
                f"{rel.as_posix()} — I2: contenu préfixé dans un répertoire de "
                f"travail → suggestion `{name.lstrip('_')}`"
            )
            continue
        if is_working_dir(name) or is_year(name) or is_month(name):
            continue
        if is_year(parent_name) and not is_month(name) and path.is_dir():
            anomalies.append(
                f"{rel.as_posix()} — I4: mois mal formé sous une année → "
                f"suggestion `{name.zfill(2) if name.isdigit() else '01–12'}`"
            )
            continue
        if not is_portable_slug(name):
            anomalies.append(
                f"{rel.as_posix()} — I3: slug non portable → suggestion "
                f"`{slugify(name)}`"
            )
    return anomalies


def collect_unsorted(anchor: Path, domains: list[Path]) -> list[str]:
    """Items hors de tout domaine reconnu — candidats à `sort`."""
    known = {d.relative_to(anchor).parts[0] for d in domains}
    unsorted: list[str] = []
    for entry in sorted(anchor.iterdir(), key=lambda p: p.name):
        if is_dotfile(entry.name) or is_working_dir(entry.name):
            continue
        if entry.is_file():
            unsorted.append(entry.name)
        elif entry.name not in known:
            unsorted.append(entry.name + "/")
    for category in sorted(anchor.iterdir(), key=lambda p: p.name):
        if not category.is_dir() or is_dotfile(category.name) or is_working_dir(category.name):
            continue
        for entry in sorted(category.iterdir(), key=lambda p: p.name):
            if entry.is_file() and not is_dotfile(entry.name):
                unsorted.append(entry.relative_to(anchor).as_posix())
    return unsorted


def build_cache(anchor: Path) -> dict:
    domains = discover_domains(anchor)
    return {
        "root": str(anchor),
        "scanned_at": today(),
        "default_pattern": DEFAULT_PATTERN,
        "domains": [scan_domain(anchor, d) for d in domains],
        "anomalies": collect_anomalies(anchor),
        "unsorted": collect_unsorted(anchor, domains),
    }


def load_cache(anchor: Path) -> dict | None:
    cache_file = anchor / CACHE_REL
    if not cache_file.exists():
        return None
    try:
        return json.loads(cache_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        warn(f"cache illisible ({cache_file}) — rescan")
        return None


def cache_or_scan(anchor: Path, refresh: bool = False) -> tuple[dict, str]:
    """Rend (cache, état) où état ∈ {fresh, refreshed, missing → indexed}."""
    cached = None if refresh else load_cache(anchor)
    if cached is None:
        return build_cache(anchor), "missing → indexed"
    if cached.get("scanned_at") != today():
        return build_cache(anchor), "refreshed"
    return cached, "fresh"


# --------------------------------------------------------------------------- #
# bank.yml — cache des ressources durables d'un domaine
# --------------------------------------------------------------------------- #

KIND_BY_DIR = {"_univers": "lore", "_systeme": "rules", "_subsystems": "rules"}


def bank_entries(domain_dir: Path) -> list[dict]:
    entries: list[dict] = []
    for hint in DURABLE_HINTS:
        durable = domain_dir / hint
        if not durable.is_dir():
            continue
        for path in iter_entries(durable, recursive=True):
            if not path.is_file() or path.suffix.lower() != ".md":
                continue
            if is_credential(path):
                warn(f"credential ignoré (jamais lu) : {path}")
                continue
            if is_media(path):
                continue
            _, body = read_frontmatter(path)
            entries.append(
                {
                    "id": slugify(path.stem),
                    "kind": KIND_BY_DIR.get(hint, "reference"),
                    "path": path.relative_to(domain_dir).as_posix(),
                    "summary": first_heading(body) or path.stem,
                }
            )
    return entries


def refresh_bank(domain_dir: Path, apply: bool) -> str | None:
    """Fusion non destructive : un `summary` curé n'est jamais écrasé."""
    if not any((domain_dir / hint).is_dir() for hint in DURABLE_HINTS):
        return None

    bank_file = domain_dir / "bank.yml"
    existing = {}
    domain_slug = slugify(domain_dir.name)
    if bank_file.exists():
        parsed = parse_yaml(bank_file.read_text(encoding="utf-8", errors="replace"))
        if isinstance(parsed, dict):
            domain_slug = parsed.get("domain") or domain_slug
            for res in parsed.get("resources") or []:
                if isinstance(res, dict) and res.get("path"):
                    existing[res["path"]] = res

    merged = []
    for entry in bank_entries(domain_dir):
        prior = existing.pop(entry["path"], None)
        if prior:
            # Le summary curé prime sur le titre déduit du scan.
            entry = {**entry, **{k: v for k, v in prior.items() if v}}
        merged.append(entry)
    for orphan in existing.values():
        orphan = dict(orphan)
        orphan["missing"] = True
        merged.append(orphan)
        warn(f"{bank_file.name}: ressource disparue du disque — {orphan.get('path')}")

    content = (
        "# R/bank.yml — ressources globales de ce domaine.\n"
        "# Cache régénérable, maintenu par obs:tree. Les summary curés sont préservés.\n"
        + dump_yaml({"domain": domain_slug, "resources": merged})
    )
    write_text(bank_file, content, apply, label=str(bank_file))
    return str(bank_file)


# --------------------------------------------------------------------------- #
# Commandes
# --------------------------------------------------------------------------- #


def cmd_index(args) -> int:
    anchor = resolve_anchor(Path(args.target), args.managed_root)
    cache = build_cache(anchor)
    cache_file = anchor / CACHE_REL
    write_text(cache_file, json.dumps(cache, indent=2, ensure_ascii=False) + "\n",
               args.apply, label=str(cache_file))

    banks = []
    for domain in discover_domains(anchor):
        result = refresh_bank(domain, args.apply)
        if result:
            banks.append(result)

    print(f"\n# Tree Index — {anchor}")
    print(f"- domaines : {len(cache['domains'])}")
    print(f"- unités : {sum(len(d.get('units') or d.get('travaux') or []) for d in cache['domains'])}")
    print(f"- anomalies : {len(cache['anomalies'])}")
    print(f"- non classés : {len(cache['unsorted'])}")
    print(f"- bank.yml rafraîchis : {len(banks)}")
    if not args.apply:
        info("dry-run — relancer avec --apply pour écrire le cache")
    return 0


def within(target: Path, anchor: Path, rel_path: str) -> bool:
    """La portée est stricte : seul ce qui est sous `target` est rapporté."""
    absolute = (anchor / rel_path.split(" — ")[0].rstrip("/")).resolve()
    try:
        absolute.relative_to(target.resolve())
        return True
    except ValueError:
        return False


def drift_for(domain: dict) -> list[str]:
    """Dérive souple, jugée contre la convention apprise du domaine."""
    drift = []
    if domain.get("kind") == "pro-projet":
        for name in domain.get("unknown") or []:
            drift.append(
                f"{domain['path']}/{name} — structure inconnue (ni `_code/` ni "
                f"`<AAAA>/<MM>/`) (convention apprise : {domain['convention']})"
            )
        return drift
    if domain.get("dated"):
        for unit in domain.get("units") or []:
            head = unit.split("/")[0]
            if not is_year(head):
                drift.append(
                    f"{domain['path']}/{unit} — unité hors de l'axe daté "
                    f"(convention apprise : {domain['convention']})"
                )
    return drift


def gather_report(anchor: Path, target: Path, refresh: bool):
    cache, state = cache_or_scan(anchor, refresh)
    anomalies = [a for a in cache["anomalies"] if within(target, anchor, a)]
    drift = []
    for domain in cache["domains"]:
        for item in drift_for(domain):
            if within(target, anchor, item):
                drift.append(item)
    unsorted = [u for u in cache["unsorted"] if within(target, anchor, u)]
    return cache, state, anomalies, drift, unsorted


def cmd_check(args) -> int:
    target = Path(args.target).resolve()
    anchor = resolve_anchor(target, args.managed_root)
    _, state, anomalies, drift, unsorted = gather_report(anchor, target, args.refresh)

    print(f"# Tree Check — {anchor}\n")
    print(f"**Date :** {today()}   **Cache :** [{state}]\n")
    print("## Anomalies d'invariant (dures)")
    print("\n".join(f"- {a}" for a in anomalies) if anomalies else "✓ aucune")
    print("\n## Dérive de convention (souple)")
    print("\n".join(f"- {d}" for d in drift) if drift else "✓ aligné")
    print("\n## Non classés")
    print("\n".join(f"- {u} — aucun domaine ne correspond → `tree sort`" for u in unsorted)
          if unsorted else "✓ aucun")
    print("\n## Verdict")
    if anomalies:
        print(f"ANOMALIES ({len(anomalies)} dures) — lancer `tree fix`")
        return 1
    if drift:
        print(f"DRIFT ({len(drift)} souples) — `tree fix --drift` pour les proposer")
        return 0
    print("CLEAN")
    return 0


def plan_from_anomaly(anchor: Path, anomaly: str) -> tuple[Path, Path] | None:
    """« chemin — In: motif → suggestion `x` » devient une opération de renommage."""
    path_part, _, rest = anomaly.partition(" — ")
    if "suggestion `" not in rest:
        return None
    suggestion = rest.split("suggestion `", 1)[1].split("`", 1)[0]
    if not suggestion or "–" in suggestion:  # « 01–12 » n'est pas un nom
        return None
    src = anchor / path_part
    return src, src.with_name(suggestion)


def cmd_fix(args) -> int:
    target = Path(args.target).resolve()
    anchor = resolve_anchor(target, args.managed_root)
    _, _, anomalies, drift, _ = gather_report(anchor, target, args.refresh)

    plan = Plan(f"Tree Fix — {anchor}", base=anchor)
    for anomaly in anomalies:
        op = plan_from_anomaly(anchor, anomaly)
        if op is None:
            warn(f"anomalie sans correction automatique : {anomaly}")
            continue
        src, dst = op
        if is_dotfile(src.name):
            # Un dotfile ne voyage jamais seul.
            continue
        plan.add(src, dst, "invariant")
    for item in drift:
        # La dérive n'a pas de correction mécanique sûre : on la liste sans agir.
        warn(f"dérive laissée en l'état (arbitrage humain requis) : {item}")

    plan.render(include_optional=args.drift, apply=args.apply)
    if not args.apply:
        info("dry-run — relancer avec --apply pour exécuter le plan")
        return 0
    plan.execute(include_optional=args.drift)
    plan.report()
    info("relancer `tree index --apply` pour rafraîchir le cache")
    return 0


def cmd_sort(args) -> int:
    """Ne place que ce qui a une destination certaine ; le reste est signalé.

    L'arbitrage d'un cas ambigu demande un jugement : ce script ne devine pas,
    il laisse l'item où il est en disant pourquoi.
    """
    into = Path(args.into).resolve() if args.into else Path.cwd()
    anchor = resolve_anchor(into, args.managed_root)
    cache, _ = cache_or_scan(anchor, args.refresh)

    items = [Path(item).resolve() for item in args.items] or [
        (anchor / rel.rstrip("/")) for rel in cache["unsorted"]
    ]

    plan = Plan(f"Tree Sort — {anchor}", base=anchor)
    left: list[tuple[Path, str]] = []
    for item in items:
        if not item.exists():
            left.append((item, "introuvable"))
            continue
        if is_dotfile(item.name):
            left.append((item, "dotfile — ne voyage jamais seul"))
            continue
        if is_credential(item):
            left.append((item, "nom de credential — signalé, jamais déplacé ni lu"))
            continue
        candidates = match_domains(cache, item)
        if not candidates:
            left.append((item, "aucun domaine ne correspond"))
            continue
        if len(candidates) > 1:
            names = ", ".join(c["path"] for c in candidates[:4])
            left.append((item, f"ambigu ({len(candidates)} domaines : {names}) — arbitrage humain"))
            continue
        destination = destination_for(anchor, candidates[0], item)
        if destination is None:
            left.append((item, "domaine trouvé mais destination indéterminée"))
            continue
        plan.add(item, destination, "placement certain")

    plan.render(include_optional=True, apply=args.apply)
    print("\n## Laissés non classés")
    if left:
        for item, reason in left:
            print(f"- {item.name} — {reason}")
    else:
        print("- aucun")

    if not args.apply:
        info("dry-run — relancer avec --apply pour déplacer")
        return 0
    plan.execute(include_optional=True)
    plan.report()
    return 0


def match_domains(cache: dict, item: Path) -> list[dict]:
    """Un domaine correspond si son slug apparaît dans le nom de l'item."""
    stem = slugify(item.stem)
    tokens = {t for t in stem.split("-") if len(t) > 3}
    matches = []
    for domain in cache["domains"]:
        slug = domain["path"].split("/")[-1].lower()
        if slug in stem or slug in tokens:
            matches.append(domain)
    return matches


def destination_for(anchor: Path, domain: dict, item: Path) -> Path | None:
    """Place un item dans le domaine, en respectant sa convention apprise."""
    base = anchor / domain["path"]
    name = slugify(item.name)
    if domain.get("kind") == "pro-projet":
        entry = domain.get("entry")
        if not entry:
            return None
        return base / entry / name
    if domain.get("dated"):
        entry = sorted(domain.get("units") or [])
        if not entry:
            return None
        head = "/".join(entry[-1].split("/")[:2])
        return base / head / name
    return base / name


def cmd_destinations(args) -> int:
    target = Path(args.target).resolve()
    anchor = resolve_anchor(target, args.managed_root)
    cache, state = cache_or_scan(anchor, args.refresh)

    grouped: dict[str, list[str]] = {}
    for domain in cache["domains"]:
        parts = domain["path"].split("/")
        if len(parts) < 2:
            continue
        category, subcategory = parts[0], parts[1]
        grouped.setdefault(category, [])
        line = f"{anchor.name}/{category}/{subcategory}"
        if line not in grouped[category]:
            grouped[category].append(line)

    lines = [
        "# destinations.txt — carte de routage du second cerveau",
        f"# Générée depuis {anchor} le {today()} (convention obs:tree).",
        "# Format : <chemin>  [ | <attr>, <attr>… ] — chemin relatif à notes_dir,",
        "#   /<Année>/<Mois> ajouté automatiquement. Priorité = ordre du fichier.",
        "",
    ]
    active = commented = 0
    for category in sorted(grouped):
        is_non_email = category.lower() in NON_EMAIL_CATEGORIES
        lines.append(f"# ── {category} " + "─" * max(0, 60 - len(category)))
        for entry in sorted(grouped[category]):
            if is_non_email:
                lines.append(f"# {entry}")
                commented += 1
            else:
                lines.append(entry)
                active += 1
        lines.append("")
    lines.append(f"# {anchor.name}/Communication/Emails  | default")
    content = "\n".join(lines) + "\n"

    print(f"# Tree Destinations — {anchor}\n")
    print(f"**Date :** {today()}   **Cache :** [{state}]")
    print(f"**Destinations :** {active}   **Commentées (hors email) :** {commented}\n")
    print("```text")
    print(content.rstrip())
    print("```")
    print("\n## Étapes suivantes")
    print(f"- notes_dir = {anchor.parent}")
    print("- Ajouter les règles domain:/from:/subject: — seul l'utilisateur connaît ses correspondants.")

    if args.out:
        out = Path(args.out)
        if out.exists():
            warn(f"{out} existe déjà — fichier curé à la main, jamais réécrit "
                 f"automatiquement. Comparer puis remplacer manuellement.")
            return 1
        write_text(out, content, args.apply, label=str(out))
    return 0


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tree.py",
        description="Maintient l'arborescence Documents/ — index, check, fix, sort, destinations.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    def common(p, target=True):
        if target:
            p.add_argument("target", nargs="?", default=".", help="cible (défaut : CWD)")
        p.add_argument("--managed-root", action="store_true",
                       help="traiter la cible comme racine gérée si aucune ancre Perso/Pro")
        p.add_argument("--refresh", action="store_true", help="forcer un rescan du cache")

    p_index = sub.add_parser("index", help="scanner l'arbo et écrire le cache")
    common(p_index)
    p_index.add_argument("--apply", action="store_true", help="écrire cache.json et bank.yml")
    p_index.set_defaults(func=cmd_index)

    p_check = sub.add_parser("check", help="vérifier invariants et dérive (lecture seule)")
    common(p_check)
    p_check.set_defaults(func=cmd_check)

    p_fix = sub.add_parser("fix", help="corriger les anomalies d'invariant")
    common(p_fix)
    p_fix.add_argument("--drift", action="store_true", help="inclure les corrections de dérive")
    p_fix.add_argument("--apply", action="store_true", help="exécuter le plan")
    p_fix.set_defaults(func=cmd_fix)

    p_sort = sub.add_parser("sort", help="placer les items dont la destination est certaine")
    p_sort.add_argument("items", nargs="*", help="fichiers/dossiers (défaut : unsorted du cache)")
    p_sort.add_argument("--into", help="restreindre le placement à ce sous-arbre")
    p_sort.add_argument("--managed-root", action="store_true")
    p_sort.add_argument("--refresh", action="store_true")
    p_sort.add_argument("--apply", action="store_true", help="déplacer réellement")
    p_sort.set_defaults(func=cmd_sort)

    p_dest = sub.add_parser("destinations", help="exporter la carte de routage email")
    common(p_dest)
    p_dest.add_argument("--out", help="écrire le destinations.txt à ce chemin")
    p_dest.add_argument("--apply", action="store_true", help="écrire le fichier --out")
    p_dest.set_defaults(func=cmd_destinations)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except AnchorNotFound as exc:
        error(str(exc))
        return 2
    except KeyboardInterrupt:
        error("interrompu")
        return 130


if __name__ == "__main__":
    sys.exit(main())
