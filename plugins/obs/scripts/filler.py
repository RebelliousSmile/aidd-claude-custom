#!/usr/bin/env python3
"""
obs:filler — inventorie, classe, indexe, fusionne et allège un répertoire de
contenu, sans appel LLM.

    python filler.py survey <répertoire> [--recursive]
    python filler.py sort   <répertoire> [--scheme entity|date|type|topic]
                                         [--owner <email>] [--apply]
    python filler.py index  <répertoire> [--group-by thread|sender|date|type]
                                         [--out <nom>] [--apply]
    python filler.py merge  <répertoire> [--glob <motif>] [--order date|alpha]
                                         [--out <nom>] [--apply]
    python filler.py clean  <répertoire> [--criteria empty,duplicate,old:AAAA-MM-JJ,orphan]
                                         [--delete] [--apply]

Portée non récursive par défaut : seuls les fichiers directement dans le
répertoire sont traités. Les fichiers et répertoires préfixés `_` sont du
matériel de travail, jamais de la matière première.

Les fichiers dérivés (`index`, `merge`, `_archive/`) sont déposés au niveau
`<Subcategory>` du tree quand il est reconnaissable, sinon dans le répertoire
cible lui-même.

Rien n'est écrit sans `--apply`. `clean` archive par défaut et ne supprime
qu'avec `--delete` : un script non interactif ne détruit pas sur inférence.
Compatible Windows, Linux, macOS. Bibliothèque standard seulement.
"""

from __future__ import annotations

import argparse
import fnmatch
import re
import sys
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from obslib import (  # noqa: E402
    MD_LINK_RE,
    WIKI_LINK_RE,
    AnchorNotFound,
    Plan,
    applied_moves,
    dangling_links,
    error,
    first_heading,
    in_code_dir,
    info,
    is_credential,
    is_dotfile,
    is_media,
    is_readable_content,
    ok,
    read_frontmatter,
    relink_moved,
    slugify,
    unique_destination,
    warn,
    word_count,
    workdir_root,
    write_text,
)

EMPTY_WORDS = 50           # seuil du critère `empty`, action 06
HOMOGENEOUS_MIN = 5        # taille minimale d'un groupe candidat au regroupement
QUOTE_RE = re.compile(r"^\s*(>|--+\s*$)")
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
DISPLAY_RE = re.compile(r"^\s*\"?([^\"<]+?)\"?\s*<")
CAMEL_RE = re.compile(r"[A-Z][a-z0-9]*|[a-z0-9]+")
NAME_TAG_RE = re.compile(r"_([A-Za-z][A-Za-z0-9]*)_")


# --------------------------------------------------------------------------- #
# Inventaire — une passe de lecture, toutes les commandes s'en servent
# --------------------------------------------------------------------------- #


class Item:
    """Un fichier du répertoire, lu une fois."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.name = path.name
        self.suffix = path.suffix.lower()
        try:
            stat = path.stat()
            self.mtime = datetime.fromtimestamp(stat.st_mtime)
            self.size = stat.st_size
        except OSError:
            self.mtime = datetime.fromtimestamp(0)
            self.size = 0
        self.credential = is_credential(path)
        self.media = is_media(path)
        self.frontmatter: dict = {}
        self.body = ""
        if is_readable_content(path):
            self.frontmatter, self.body = read_frontmatter(path)
        self.flags: list[str] = []

    # -- champs dérivés ----------------------------------------------------- #

    @property
    def title(self) -> str:
        for key in ("title", "subject"):
            value = self.frontmatter.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
        heading = first_heading(self.body)
        return heading or self.path.stem

    @property
    def stem(self) -> str:
        return self.path.stem

    @property
    def words(self) -> int:
        return word_count(self.prose)

    @property
    def prose(self) -> str:
        """Corps hors citations et séparateurs — ce qui reste en propre."""
        kept = [ln for ln in self.body.splitlines() if not QUOTE_RE.match(ln)]
        return "\n".join(kept)

    @property
    def when(self) -> datetime:
        raw = self.frontmatter.get("date")
        if isinstance(raw, str):
            for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y/%m/%d"):
                try:
                    return datetime.strptime(raw[:len(fmt) + 2].strip(), fmt)
                except ValueError:
                    continue
        if isinstance(raw, date):
            return datetime(raw.year, raw.month, raw.day)
        return self.mtime

    @property
    def attachments(self) -> list:
        value = self.frontmatter.get("attachments")
        if isinstance(value, list):
            return [v for v in value if v]
        if isinstance(value, str) and value.strip():
            return [value.strip()]
        return []

    def first_paragraph(self) -> str:
        block: list[str] = []
        for line in self.prose.splitlines():
            if line.strip().startswith("#"):
                continue
            if not line.strip():
                if block:
                    break
                continue
            block.append(line.strip())
        return re.sub(r"\W+", " ", " ".join(block)).strip().lower()[:200]


def credentials_in(directory: Path, recursive: bool = False) -> list[Path]:
    """Fichiers à nom de credential, dotfiles compris — signalés, jamais lus.

    Exception : sous un `_code/`, un `.env` est de l'outillage de développeur
    attendu à cet endroit. Le signaler à chaque passage serait du bruit.
    """
    pattern = "**/*" if recursive else "*"
    return [
        p for p in sorted(directory.glob(pattern))
        if p.is_file() and is_credential(p) and not in_code_dir(p)
    ]


def inventory(directory: Path, recursive: bool = False) -> list[Item]:
    """Fichiers de matière première d'un répertoire, dans l'ordre du nom.

    Sont écartés : le matériel de travail (`_`), les dotfiles, et tout ce que
    les répertoires interdits contiennent.
    """
    items: list[Item] = []
    pattern = "**/*" if recursive else "*"
    for path in sorted(directory.glob(pattern)):
        if not path.is_file():
            continue
        parts = path.relative_to(directory).parts
        if any(p.startswith("_") or p.startswith(".") for p in parts[:-1]):
            continue
        if path.name.startswith("_") or is_dotfile(path.name):
            continue
        items.append(Item(path))
    return items


# --------------------------------------------------------------------------- #
# Entités — d'où vient un fichier
# --------------------------------------------------------------------------- #


GENERIC_DOMAINS = frozenset(
    """gmail googlemail outlook hotmail live msn yahoo icloud me free orange
       wanadoo sfr laposte proton protonmail gmx aol""".split()
)


def display_name(raw: str) -> str:
    """Premier mot du nom affiché : `ONET CDG <no@…>` → `onet`."""
    match = DISPLAY_RE.match(raw)
    words = match.group(1).split() if match else []
    return slugify(words[0]) if words else ""


def short_entity(raw: str) -> str:
    """Nom court et portable d'une entité.

    Le domaine passe avant le nom affiché : `"Marie Dupont" <marie@acme.io>`
    et `"Paul Martin" <paul@acme.io>` sont la même organisation, et c'est elle
    l'entité. Sur un domaine grand public le domaine ne dit rien : le nom
    affiché, puis la partie locale, reprennent la main.
    """
    address = EMAIL_RE.search(raw)
    if address:
        local, _, domain = address.group(0).partition("@")
        labels = [part for part in domain.split(".") if part]
        label = labels[-2] if len(labels) >= 2 else (labels[0] if labels else "")
        if label and label not in GENERIC_DOMAINS:
            return slugify(label)
        return display_name(raw) or slugify(local)
    name = display_name(raw)
    if name:
        return name
    token = raw.strip().split()[0] if raw.strip() else ""
    return slugify(token) if token else ""


def entity_of(item: Item, owner: str = "") -> str:
    """Entité significative d'un fichier, ou `divers` si indécidable.

    Un message envoyé par le propriétaire du vault porte son correspondant en
    `to:` — c'est lui l'entité, pas l'expéditeur.
    """
    sender = str(item.frontmatter.get("from", "") or "")
    recipient = str(item.frontmatter.get("to", "") or "")
    if owner and owner.lower() in sender.lower() and recipient:
        sender = recipient.split(",")[0]
    if sender:
        name = short_entity(sender)
        if name:
            return name
    tag = NAME_TAG_RE.search(item.stem)
    if tag:
        parts = CAMEL_RE.findall(tag.group(1))
        if parts:
            return slugify(parts[0])
    return "divers"


def owner_address(directory: Path, explicit: str) -> str:
    """Adresse du propriétaire : `--owner`, sinon `mail-config.yaml` du tree."""
    if explicit:
        return explicit
    config = workdir_root(directory) / "mail-config.yaml"
    if not config.exists():
        return ""
    from obslib import parse_yaml

    try:
        data = parse_yaml(config.read_text(encoding="utf-8"))
    except OSError:
        return ""
    if isinstance(data, dict):
        for key in ("owner", "self", "me", "address"):
            value = data.get(key)
            if isinstance(value, str) and "@" in value:
                return value
    return ""


# --------------------------------------------------------------------------- #
# Flags — ce qu'on peut établir sans jugement
# --------------------------------------------------------------------------- #

SECRET_RE = re.compile(
    r"\b(whsec_|sk-[A-Za-z0-9]{10,}|xox[baprs]-|AKIA[0-9A-Z]{16}|[0-9a-f]{32,})",
    re.IGNORECASE,
)
LINK_RE = re.compile(r"\[\[([^\]|#]+)")


def assess(items: list[Item], owner: str = "") -> None:
    """Pose les flags de chaque fichier. Idempotent."""
    by_signature: dict[tuple[str, str], list[Item]] = {}
    referenced: set[str] = set()
    for item in items:
        referenced.update(Path(ref.strip()).stem for ref in LINK_RE.findall(item.body))

    for item in items:
        item.flags = []
        if item.credential:
            item.flags.append("credential")
            continue
        if item.media:
            item.flags.append("media")
            continue
        if SECRET_RE.search(item.body):
            item.flags.append("secret")
        if item.words < EMPTY_WORDS and "secret" not in item.flags:
            item.flags.append("attachment-only" if item.attachments else "empty")
        para = item.first_paragraph()
        if para:
            # Le titre seul ne suffit pas : six notifications d'un même système
            # partagent leur sujet sans être des doublons.
            by_signature.setdefault((slugify(item.title), para), []).append(item)
        outgoing = bool(LINK_RE.search(item.body))
        heading = any(ln.lstrip().startswith("#") for ln in item.body.splitlines())
        if not item.frontmatter and not heading:
            if not outgoing and item.stem not in referenced:
                item.flags.append("orphan")

    for group in by_signature.values():
        if len(group) < 2:
            continue
        for duplicate in sorted(group, key=lambda i: (i.when, i.name))[1:]:
            if "duplicate" not in duplicate.flags:
                duplicate.flags.append("duplicate")


def homogeneous_groups(items: list[Item], owner: str = "") -> dict[str, list[Item]]:
    """Groupes assez nombreux et assez uniformes pour être traités en bloc."""
    groups: dict[str, list[Item]] = {}
    for item in items:
        if item.media or item.credential:
            continue
        groups.setdefault(f"{entity_of(item, owner)} ({item.suffix or 'sans ext'})", []).append(item)
    return {k: v for k, v in groups.items() if len(v) >= HOMOGENEOUS_MIN}


def triage(group: list[Item]) -> str:
    """Action recommandée pour un lot, d'après ce que les chiffres disent."""
    counts = sorted(i.words for i in group)
    median = counts[len(counts) // 2]
    spread = counts[-1] - counts[0]
    # L'homogénéité prime sur le flag `empty` : six notifications courtes du
    # même émetteur sont un lot à fusionner, pas six fichiers sans valeur.
    if len(group) >= HOMOGENEOUS_MIN and median < 200 and spread < 400:
        return "merge"
    if all("empty" in i.flags or "duplicate" in i.flags for i in group):
        return "clean"
    return "keep"


def plural(n: int, singular: str, plural_form: str = "") -> str:
    return f"{n} {singular if n < 2 else (plural_form or singular + 's')}"


def table(rows: list[list[str]], headers: list[str]) -> None:
    widths = [len(h) for h in headers]
    for row in rows:
        for n, cell in enumerate(row):
            widths[n] = max(widths[n], len(cell))
    line = "  ".join(h.ljust(widths[n]) for n, h in enumerate(headers))
    print(line)
    print("  ".join("-" * w for w in widths))
    for row in rows:
        print("  ".join(cell.ljust(widths[n]) for n, cell in enumerate(row)))


# --------------------------------------------------------------------------- #
# survey — console seulement, aucun fichier produit
# --------------------------------------------------------------------------- #


def cmd_survey(args: argparse.Namespace) -> int:
    directory = Path(args.path).expanduser()
    if not directory.is_dir():
        error(f"{directory} n'est pas un répertoire")
        return 2
    items = inventory(directory, args.recursive)
    if not items:
        info(f"{directory} : aucun fichier de matière première")
        return 0
    owner = owner_address(directory, args.owner)
    assess(items, owner)

    print(f"\n## Inventaire — {directory}")
    rows = [
        [
            item.path.relative_to(directory).as_posix(),
            item.suffix or "—",
            item.when.strftime("%Y-%m-%d"),
            str(item.words),
            ", ".join(item.flags) or "—",
        ]
        for item in items
    ]
    table(rows, ["fichier", "ext", "date", "mots", "flags"])

    extensions: dict[str, int] = {}
    for item in items:
        extensions[item.suffix or "—"] = extensions.get(item.suffix or "—", 0) + 1
    dates = sorted(item.when for item in items)
    flagged: dict[str, int] = {}
    for item in items:
        for flag in item.flags:
            flagged[flag] = flagged.get(flag, 0) + 1

    print("\n## Synthèse")
    print(f"- {len(items)} fichiers, {sum(i.words for i in items)} mots")
    print("- extensions : " + ", ".join(f"{k} ({v})" for k, v in sorted(extensions.items())))
    print(f"- période : {dates[0]:%Y-%m-%d} → {dates[-1]:%Y-%m-%d}")
    print("- flags : " + (", ".join(f"{k} ({v})" for k, v in sorted(flagged.items())) or "aucun"))

    groups = homogeneous_groups(items, owner)
    if groups:
        print("\n## Groupes homogènes")
        table(
            [[name, str(len(group)), triage(group)] for name, group in sorted(groups.items())],
            ["groupe", "n", "action"],
        )

    print("\n## Suite")
    for secret in credentials_in(directory, args.recursive):
        warn(f"{secret.relative_to(directory).as_posix()} : nom de credential — signalé, jamais lu")
    if flagged.get("duplicate", 0) or flagged.get("empty", 0):
        print("- `clean` : des fichiers vides ou en double occupent le répertoire")
    if len(groups) >= 2:
        print("- `sort entity` : plusieurs sources se mélangent dans le même répertoire")
    if not flagged and not groups:
        print("- rien à signaler")
    return 0


# --------------------------------------------------------------------------- #
# sort — regrouper en sous-répertoires
# --------------------------------------------------------------------------- #


def local_references(body: str) -> list[str]:
    """Références portant un chemin ou un nom de fichier, dans l'ordre du texte."""
    refs = [m.group(2) for m in MD_LINK_RE.finditer(body)]
    refs += [m.group(2) for m in WIKI_LINK_RE.finditer(body)]
    return [r.strip() for r in refs if not r.startswith(("http://", "https://", "#", "/"))]


def bucket_of(item: Item, scheme: str, owner: str) -> str:
    if scheme == "entity":
        return entity_of(item, owner)
    if scheme == "date":
        return f"{item.when:%Y}/{item.when:%m}"
    if scheme == "type":
        declared = item.frontmatter.get("type")
        if isinstance(declared, str) and declared.strip():
            return slugify(declared)
        return slugify(item.suffix.lstrip(".")) or "sans-extension"
    if scheme == "topic":
        tags = item.frontmatter.get("tags")
        if isinstance(tags, list) and tags:
            return slugify(str(tags[0]))
        if isinstance(tags, str) and tags.strip():
            return slugify(tags.split(",")[0])
        return "sans-topic"
    raise ValueError(scheme)


def cmd_sort(args: argparse.Namespace) -> int:
    directory = Path(args.path).expanduser()
    if not directory.is_dir():
        error(f"{directory} n'est pas un répertoire")
        return 2
    items = inventory(directory)
    if not items:
        info(f"{directory} : rien à classer")
        return 0
    owner = owner_address(directory, args.owner)
    assess(items, owner)

    plan = Plan(f"Classement `{args.scheme}` de {directory.name}", base=directory)
    buckets: dict[str, list[Item]] = {}
    assets: dict[str, set[str]] = {}
    for item in items:
        if item.credential:
            warn(f"{item.name} : nom de credential — signalé, jamais déplacé ni lu")
            continue
        if item.media:
            continue
        bucket = bucket_of(item, args.scheme, owner)
        buckets.setdefault(bucket, []).append(item)
        plan.add(item.path, directory / bucket / item.name, bucket)
        for ref in local_references(item.body):
            target = directory / ref
            if target.is_file() and is_media(target):
                assets.setdefault(target.name, set()).add(bucket)

    for item in items:
        if not item.media:
            continue
        owners = assets.get(item.name, set())
        if len(owners) == 1:
            plan.add(item.path, directory / next(iter(owners)) / item.name, "asset accompagnant")
        elif len(owners) > 1:
            warn(f"{item.name} : référencé depuis {len(owners)} entités — laissé sur place")
        else:
            info(f"{item.name} : média non référencé — laissé sur place")

    plan.render(include_optional=True, apply=args.apply)
    if not args.apply:
        info("relancer avec --apply pour exécuter")
    else:
        plan.execute(include_optional=True)
        plan.report()
        moves = applied_moves(plan)
        touched = relink_moved(moves, apply=True)
        if touched:
            ok(f"{touched} fichier(s) : liens relatifs recalculés")
        broken = dangling_links(directory)
        if broken:
            warn(f"{len(broken)} référence(s) pendante(s) après déplacement")
            for path, ref in broken[:10]:
                print(f"- {path.relative_to(directory).as_posix()} → {ref}")

    if args.scheme == "entity" and buckets:
        print("\n## Triage par entité")
        table(
            [
                [name, str(len(group)), str(sum(i.words for i in group)), triage(group)]
                for name, group in sorted(buckets.items())
            ],
            ["entité", "n", "mots", "action"],
        )
    return 0


# --------------------------------------------------------------------------- #
# index — navigation, jamais de contenu dupliqué
# --------------------------------------------------------------------------- #


def group_key(item: Item, mode: str) -> str:
    if mode == "thread":
        digest = item.frontmatter.get("subject_hash")
        if isinstance(digest, str) and digest.strip():
            return digest.strip()
        return re.sub(r"^\s*(re|fwd|tr|fw)\s*:\s*", "", item.title, flags=re.IGNORECASE).strip()
    if mode == "sender":
        return str(item.frontmatter.get("from", "") or "") or "sans expéditeur"
    if mode == "date":
        return f"{item.when:%Y-%m}"
    if mode == "type":
        declared = item.frontmatter.get("email_type") or item.frontmatter.get("type")
        if isinstance(declared, str) and declared.strip():
            return declared.strip()
        return item.suffix or "sans extension"
    raise ValueError(mode)


def heading_of(key: str, group: list[Item], mode: str) -> str:
    """En-tête lisible d'un groupe : un `subject_hash` ne dit rien à personne."""
    if mode == "thread" and group:
        return sorted(group, key=lambda i: (i.when, i.name))[0].title
    return key


def cmd_index(args: argparse.Namespace) -> int:
    directory = Path(args.path).expanduser()
    if not directory.is_dir():
        error(f"{directory} n'est pas un répertoire")
        return 2
    items = [i for i in inventory(directory) if not i.media and not i.credential]
    if not items:
        info(f"{directory} : rien à indexer")
        return 0

    mode = args.group_by
    if mode == "auto":
        mode = "thread" if any(i.frontmatter.get("subject_hash") for i in items) else "date"

    groups: dict[str, list[Item]] = {}
    for item in items:
        groups.setdefault(group_key(item, mode), []).append(item)

    lines = [
        "---",
        f"title: Index — {directory.name}",
        f"generated_by: obs:filler index --group-by {mode}",
        "---",
        "",
        f"# Index — {directory.name}",
        "",
        f"{plural(len(items), 'fichier')}, {plural(len(groups), 'groupe')}. "
        "Navigation seule : aucun contenu dupliqué.",
        "",
    ]
    for name, group in sorted(groups.items(), key=lambda kv: heading_of(kv[0], kv[1], mode)):
        lines.append(f"## {heading_of(name, group, mode)} ({len(group)})")
        lines.append("")
        for item in sorted(group, key=lambda i: (i.when, i.name)):
            hint = item.title if item.title != item.stem else f"{item.when:%Y-%m-%d}"
            lines.append(f"- [[{item.stem}]] — {hint}")
        lines.append("")

    target = workdir_root(directory) / (args.out or f"_index-{slugify(directory.name)}.md")
    target = unique_destination(target)
    write_text(target, "\n".join(lines), args.apply, label=str(target))
    print(f"\n## Rapport\n- {plural(len(groups), 'groupe')}, "
          f"{plural(len(items), 'fichier')} indexé{'s' if len(items) > 1 else ''}\n- sortie : {target}")
    return 0


# --------------------------------------------------------------------------- #
# merge — concaténation avec table des matières
# --------------------------------------------------------------------------- #


def cmd_merge(args: argparse.Namespace) -> int:
    directory = Path(args.path).expanduser()
    if not directory.is_dir():
        error(f"{directory} n'est pas un répertoire")
        return 2
    items = [
        i
        for i in inventory(directory)
        if not i.media and not i.credential and fnmatch.fnmatch(i.name, args.glob)
    ]
    if not items:
        info(f"{directory} : aucun fichier ne correspond à `{args.glob}`")
        return 0
    items.sort(key=(lambda i: i.name) if args.order == "alpha" else (lambda i: (i.when, i.name)))

    toc = [f"{n}. {item.title} — `{item.name}`" for n, item in enumerate(items, 1)]
    lines = [
        "---",
        f"title: {directory.name} — consolidé",
        f"generated_by: obs:filler merge --order {args.order}",
        f"sources: {len(items)}",
        "---",
        "",
        f"# {directory.name} — consolidé",
        "",
        "## Table des matières",
        "",
        *toc,
        "",
    ]
    for item in items:
        lines.extend(["---", "", f"## {item.title}", "", f"*source : `{item.name}`*", "", item.body.strip(), ""])

    target = unique_destination(workdir_root(directory) / (args.out or f"_merged-{slugify(directory.name)}.md"))
    content = "\n".join(lines)
    write_text(target, content, args.apply, label=str(target))
    total = sum(i.words for i in items)
    print("\n## Rapport")
    for n, item in enumerate(items, 1):
        print(f"{n}. {item.name}")
    print(f"- {total} mots de source, {word_count(content)} dans le consolidé")
    print(f"- sortie : {target}")
    print("- les sources ne sont pas touchées")
    return 0


# --------------------------------------------------------------------------- #
# clean — archiver par défaut, supprimer seulement si on le demande
# --------------------------------------------------------------------------- #


def referrers(scope: Path, stem: str) -> list[Path]:
    """Fichiers Markdown de `scope` qui référencent `stem`, lien valide compris.

    À calculer avant l'opération : après coup, un lien vers un fichier disparu
    ne se distingue plus d'un lien qui n'a jamais résolu.
    """
    hits: list[Path] = []
    for path in sorted(scope.rglob("*.md")):
        if path.stem == stem:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        refs = [m.group(2) for m in WIKI_LINK_RE.finditer(text)]
        refs += [m.group(2) for m in MD_LINK_RE.finditer(text)]
        if any(Path(ref.strip()).stem == stem for ref in refs):
            hits.append(path)
    return hits


def parse_criteria(raw: str) -> tuple[set[str], date | None]:
    wanted: set[str] = set()
    cutoff: date | None = None
    for token in raw.split(","):
        token = token.strip()
        if not token:
            continue
        if token.startswith("old:"):
            try:
                cutoff = datetime.strptime(token[4:], "%Y-%m-%d").date()
            except ValueError:
                raise SystemExit(f"critère `{token}` : date attendue au format AAAA-MM-JJ")
            wanted.add("old")
            continue
        if token not in ("empty", "duplicate", "orphan"):
            raise SystemExit(f"critère inconnu : `{token}`")
        wanted.add(token)
    return wanted, cutoff


def cmd_clean(args: argparse.Namespace) -> int:
    directory = Path(args.path).expanduser()
    if not directory.is_dir():
        error(f"{directory} n'est pas un répertoire")
        return 2
    wanted, cutoff = parse_criteria(args.criteria)
    items = inventory(directory)
    if not items:
        info(f"{directory} : rien à nettoyer")
        return 0
    assess(items, owner_address(directory, ""))

    candidates: list[tuple[Item, str]] = []
    for item in items:
        if item.credential or "secret" in item.flags:
            continue
        reasons = [f for f in item.flags if f in wanted]
        if "old" in wanted and cutoff and item.when.date() < cutoff:
            reasons.append(f"antérieur à {cutoff}")
        if reasons:
            candidates.append((item, ", ".join(reasons)))

    if not candidates:
        ok(f"{directory} : aucun fichier ne remplit les critères `{args.criteria}`")
        return 0

    scope = workdir_root(directory)
    cited = {item.stem: referrers(scope, item.stem) for item, _ in candidates}

    if args.delete:
        header = f"\n## Suppression ({plural(len(candidates), 'fichier')})"
        print(header + ("" if args.apply else " (dry-run)"))
        for item, reason in candidates:
            mark = f"  ⚠ cité par {plural(len(cited[item.stem]), 'fichier')}" if cited[item.stem] else ""
            print(f"- [{reason}] {item.path.relative_to(directory).as_posix()}{mark}")
        if not args.apply:
            info("relancer avec --apply pour supprimer, ou sans --delete pour archiver")
            return 0
        removed = 0
        for item, _ in candidates:
            try:
                item.path.unlink()
                removed += 1
            except OSError as exc:
                warn(f"{item.name} : {exc}")
                continue
            for source in cited[item.stem]:
                warn(f"{source.relative_to(scope).as_posix()} référençait {item.name} — lien à reprendre")
        print(f"\n## Rapport\n- {plural(removed, 'supprimé')}, "
              f"{plural(len(candidates) - removed, 'ignoré')}")
        return 0

    root = workdir_root(directory)
    archive = root / "_archive"
    plan = Plan(f"Archivage vers {archive.name}", base=root)
    for item, reason in candidates:
        plan.add(item.path, unique_destination(archive / item.name), reason)
    plan.render(include_optional=True, apply=args.apply)
    if not args.apply:
        info("relancer avec --apply pour archiver, ou ajouter --delete pour supprimer")
        return 0
    applied, skipped = plan.execute(include_optional=True)
    plan.report()
    relink_moved(applied_moves(plan), apply=True)
    for item, _ in candidates:
        for source in cited[item.stem]:
            if source.exists():
                warn(f"{source.relative_to(scope).as_posix()} pointe vers {item.name}, archivé")
    print(f"\n## Rapport\n- {plural(applied, 'archivé')}, {plural(skipped, 'ignoré')}, 0 supprimé")
    return 0


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="filler.py",
        description="Inventorie, classe, indexe, fusionne et allège un répertoire de contenu.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    survey = sub.add_parser("survey", help="inventorier le répertoire (console seule)")
    survey.add_argument("path")
    survey.add_argument("--recursive", action="store_true", help="descendre dans les sous-répertoires")
    survey.add_argument("--owner", default="", help="adresse du propriétaire du vault")
    survey.set_defaults(func=cmd_survey)

    sort = sub.add_parser("sort", help="regrouper les fichiers en sous-répertoires")
    sort.add_argument("path")
    sort.add_argument("--scheme", choices=("entity", "date", "type", "topic"), default="entity")
    sort.add_argument("--owner", default="", help="adresse du propriétaire du vault")
    sort.add_argument("--apply", action="store_true")
    sort.set_defaults(func=cmd_sort)

    index = sub.add_parser("index", help="écrire un index de navigation en wikilinks")
    index.add_argument("path")
    index.add_argument("--group-by", choices=("auto", "thread", "sender", "date", "type"), default="auto")
    index.add_argument("--out", default="", help="nom du fichier d'index")
    index.add_argument("--apply", action="store_true")
    index.set_defaults(func=cmd_index)

    merge = sub.add_parser("merge", help="concaténer les fichiers en un document avec TOC")
    merge.add_argument("path")
    merge.add_argument("--glob", default="*.md", help="filtre de nom (défaut : *.md)")
    merge.add_argument("--order", choices=("date", "alpha"), default="date")
    merge.add_argument("--out", default="", help="nom du fichier consolidé")
    merge.add_argument("--apply", action="store_true")
    merge.set_defaults(func=cmd_merge)

    clean = sub.add_parser("clean", help="archiver ou supprimer les fichiers sans valeur")
    clean.add_argument("path")
    clean.add_argument(
        "--criteria",
        default="empty,duplicate",
        help="empty, duplicate, orphan, old:AAAA-MM-JJ (séparés par des virgules)",
    )
    clean.add_argument("--delete", action="store_true", help="supprimer au lieu d'archiver")
    clean.add_argument("--apply", action="store_true")
    clean.set_defaults(func=cmd_clean)

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
