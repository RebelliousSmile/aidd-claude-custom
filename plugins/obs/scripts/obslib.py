#!/usr/bin/env python3
"""
Socle commun des scripts `obs` : découverte de l'ancre, invariants de nommage,
garde-fous de sécurité, lecture YAML/frontmatter, plan dry-run.

Aucune dépendance hors bibliothèque standard. Compatible Windows, Linux, macOS.
"""

from __future__ import annotations

import os
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

# --------------------------------------------------------------------------- #
# Sortie terminal
# --------------------------------------------------------------------------- #


class Colors:
    """Codes ANSI, neutralisés quand la sortie n'est pas un terminal."""

    GREEN = "\033[92m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    DIM = "\033[2m"
    RESET = "\033[0m"

    @staticmethod
    def enabled() -> bool:
        if os.environ.get("NO_COLOR"):
            return False
        return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()


def _tag(color: str, tag: str, msg: str) -> str:
    if Colors.enabled():
        return f"{color}{tag}{Colors.RESET} {msg}"
    return f"{tag} {msg}"


def ok(msg: str) -> None:
    print(_tag(Colors.GREEN, "[OK]", msg))


def info(msg: str) -> None:
    print(_tag(Colors.CYAN, "[INFO]", msg))


def warn(msg: str) -> None:
    print(_tag(Colors.YELLOW, "[ATTENTION]", msg))


def error(msg: str) -> None:
    print(_tag(Colors.RED, "[ERREUR]", msg), file=sys.stderr)


def today() -> str:
    return date.today().isoformat()


# --------------------------------------------------------------------------- #
# Invariants de nommage (I1–I4 de references/tree-convention.md)
# --------------------------------------------------------------------------- #

YEAR_RE = re.compile(r"^\d{4}$")
MONTH_RE = re.compile(r"^(0[1-9]|1[0-2])$")
SLUG_RE = re.compile(r"^[a-z0-9]+(?:[-.][a-z0-9]+)*$")

ANCHOR_NAMES = ("Perso", "Pro")

#: Niveaux dont le nom est imposé : exemptés de l'invariant I3 (slug portable).
FORMAT_IMPOSED = set(ANCHOR_NAMES)


def is_working_dir(name: str) -> bool:
    """Répertoire de travail au sens I1 : préfixé `_`."""
    return name.startswith("_")


def is_dotfile(name: str) -> bool:
    return name.startswith(".")


def is_year(name: str) -> bool:
    return bool(YEAR_RE.match(name))


def is_month(name: str) -> bool:
    return bool(MONTH_RE.match(name))


def is_dated_level(name: str) -> bool:
    return is_year(name) or is_month(name)


def is_portable_slug(name: str) -> bool:
    """I3 : minuscules, chiffres, tirets. Ni espace, ni accent, ni majuscule."""
    return bool(SLUG_RE.match(name))


def slugify(name: str) -> str:
    """Rend un nom conforme à I3 sans perdre l'extension d'un fichier."""
    stem, dot, ext = name.partition(".")
    normalized = unicodedata.normalize("NFKD", stem)
    ascii_only = "".join(c for c in normalized if not unicodedata.combining(c))
    lowered = ascii_only.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", lowered).strip("-")
    slug = re.sub(r"-{2,}", "-", slug) or "sans-nom"
    return f"{slug}{dot}{ext.lower()}" if dot else slug


# --------------------------------------------------------------------------- #
# Garde-fous de sécurité — voir SKILL.md › Transversal rules
# --------------------------------------------------------------------------- #

#: Motifs de fichiers dont le contenu n'est JAMAIS lu, seulement signalé.
CREDENTIAL_PATTERNS = (
    r"^\.env$",
    r".*\.env$",
    r"^credentials\..*",
    r"^secrets\..*",
    r"^token\..*",
    r".*\.key$",
    r".*\.pem$",
    r".*\.p12$",
    r".*\.pfx$",
    r".*\.secret$",
    r".*password.*",
    r".*passwd.*",
    r".*apikey.*",
)
_CREDENTIAL_RE = re.compile("|".join(CREDENTIAL_PATTERNS), re.IGNORECASE)

#: Extensions dont le contenu n'est jamais lu ni jugé.
MEDIA_EXTENSIONS = frozenset(
    """.jpg .jpeg .png .gif .bmp .webp .heic .raw .psd .svg
       .mp3 .wav .flac .m4a .ogg .aac
       .mp4 .mov .avi .mkv .wmv .webm""".split()
)

#: Répertoires jamais parcourus par un scan.
SKIP_DIRS = frozenset({".git", ".svn", ".hg", "node_modules", "__pycache__", "_tree"})


def is_credential(path: Path) -> bool:
    """Vrai si le NOM du fichier trahit un secret. Le contenu reste non lu.

    Exception : sous un `_code/` à n'importe quelle profondeur, c'est de
    l'outillage de développement attendu — on passe sans signaler.
    """
    return bool(_CREDENTIAL_RE.match(path.name))


def in_code_dir(path: Path) -> bool:
    return "_code" in path.parts


def is_media(path: Path) -> bool:
    return path.suffix.lower() in MEDIA_EXTENSIONS


def is_readable_content(path: Path) -> bool:
    """Un fichier dont on s'autorise à ouvrir le contenu."""
    return not is_media(path) and not is_credential(path)


def movable_standalone(path: Path) -> bool:
    """Un `.git/` ou tout nom commençant par `.` ne voyage jamais seul."""
    return not is_dotfile(path.name)


def iter_entries(directory: Path, recursive: bool = False):
    """Parcourt un répertoire en sautant les répertoires interdits.

    Rend des `Path`. Les `SKIP_DIRS` ne sont ni rendus ni descendus.
    """
    try:
        entries = sorted(directory.iterdir(), key=lambda p: p.name)
    except (OSError, PermissionError):
        return
    for entry in entries:
        if entry.is_dir():
            if entry.name in SKIP_DIRS:
                continue
            yield entry
            if recursive:
                yield from iter_entries(entry, recursive=True)
        else:
            yield entry


# --------------------------------------------------------------------------- #
# Résolution de l'ancre (découverte, jamais hardcodée)
# --------------------------------------------------------------------------- #


def find_anchor(start: Path) -> Path | None:
    """Remonte les parents de `start` jusqu'à un segment `Perso` ou `Pro`."""
    current = start.resolve()
    if current.is_file():
        current = current.parent
    for candidate in (current, *current.parents):
        if candidate.name in ANCHOR_NAMES:
            return candidate
    return None


def resolve_anchor(target: Path, managed_root: bool = False) -> Path:
    """Ancre de `target`, ou `target` elle-même si `--managed-root` est passé.

    Sans ancre et sans `--managed-root`, on s'arrête : traiter un répertoire
    quelconque comme racine gérée y déposerait un `_tree/` non voulu.
    """
    anchor = find_anchor(target)
    if anchor is not None:
        return anchor
    if managed_root:
        return target.resolve()
    raise AnchorNotFound(target)


class AnchorNotFound(Exception):
    def __init__(self, target: Path):
        super().__init__(
            f"aucune ancre `Perso`/`Pro` en remontant depuis {target}. "
            "Relancer avec --managed-root pour traiter cette cible comme "
            "racine gérée (un `_tree/` y sera créé)."
        )
        self.target = target


# --------------------------------------------------------------------------- #
# YAML — sous-ensemble suffisant pour bank.yml, mail-config.yaml, frontmatter
# --------------------------------------------------------------------------- #

try:  # PyYAML quand il est là, notre lecteur restreint sinon.
    import yaml as _pyyaml
except ImportError:  # pragma: no cover - dépend de l'environnement
    _pyyaml = None


def _scalar(raw: str):
    text = raw.strip()
    if not text or text in {"~", "null"}:
        return None
    if text[0] in "\"'" and text[-1] == text[0] and len(text) >= 2:
        return text[1:-1]
    if text.startswith("[") and text.endswith("]"):
        inner = text[1:-1].strip()
        return [_scalar(part) for part in inner.split(",")] if inner else []
    low = text.lower()
    if low in {"true", "yes"}:
        return True
    if low in {"false", "no"}:
        return False
    if re.fullmatch(r"-?\d+", text):
        return int(text)
    if re.fullmatch(r"-?\d+\.\d+", text):
        return float(text)
    return text


def _parse_block(lines: list[tuple[int, str]], pos: int, indent: int):
    """Analyse récursive d'un bloc à l'indentation `indent`. Rend (valeur, pos)."""
    if pos >= len(lines):
        return None, pos
    first_indent, first_text = lines[pos]
    if first_indent < indent:
        return None, pos

    if first_text.startswith("- "):
        items = []
        while pos < len(lines):
            cur_indent, text = lines[pos]
            if cur_indent != first_indent or not text.startswith("- "):
                break
            rest = text[2:]
            pos += 1
            if ":" in rest and not rest.startswith("["):
                key, _, val = rest.partition(":")
                item = {key.strip(): _scalar(val)}
                if val.strip() == "":
                    nested, pos = _parse_block(lines, pos, cur_indent + 2)
                    item[key.strip()] = nested
                while pos < len(lines) and lines[pos][0] > cur_indent:
                    sub_indent, sub_text = lines[pos]
                    sub_key, _, sub_val = sub_text.partition(":")
                    pos += 1
                    if sub_val.strip() == "":
                        nested, pos = _parse_block(lines, pos, sub_indent + 1)
                        item[sub_key.strip()] = nested
                    else:
                        item[sub_key.strip()] = _scalar(sub_val)
                items.append(item)
            else:
                items.append(_scalar(rest))
        return items, pos

    # L'indentation du bloc est celle de sa première ligne : `indent` n'est
    # qu'un plancher. Comparer à `indent` ferait sortir dès la première clé
    # d'un sous-bloc plus indenté que son plancher.
    indent = first_indent
    mapping = {}
    while pos < len(lines):
        cur_indent, text = lines[pos]
        if cur_indent != indent or text.startswith("- "):
            break
        key, sep, val = text.partition(":")
        if not sep:
            pos += 1
            continue
        pos += 1
        if val.strip() == "":
            nested, pos = _parse_block(lines, pos, cur_indent + 1)
            mapping[key.strip()] = nested if nested is not None else {}
        else:
            mapping[key.strip()] = _scalar(val)
    return mapping, pos


def parse_yaml(text: str):
    """Lit le sous-ensemble YAML utilisé par ce plugin (pas d'ancres, pas de flow imbriqué)."""
    if _pyyaml is not None:
        try:
            return _pyyaml.safe_load(text) or {}
        except Exception:
            # Frontmatter réel non conforme — `from: "Nom" <a@b.c>` par exemple.
            # Le lecteur maison rend la valeur brute plutôt que de faire échouer
            # la lecture : un fichier mal formé reste un fichier à traiter.
            pass
    lines: list[tuple[int, str]] = []
    for raw in text.splitlines():
        without_comment = re.sub(r"(?<!\S)#.*$", "", raw).rstrip()
        if not without_comment.strip():
            continue
        if without_comment.strip() in {"---", "..."}:
            continue
        lines.append((len(without_comment) - len(without_comment.lstrip()),
                      without_comment.strip()))
    if not lines:
        return {}
    value, _ = _parse_block(lines, 0, lines[0][0])
    return value if value is not None else {}


def _dump_value(value, indent: int) -> list[str]:
    pad = " " * indent
    if isinstance(value, dict):
        out = []
        for key, val in value.items():
            if isinstance(val, (dict, list)) and val:
                out.append(f"{pad}{key}:")
                out.extend(_dump_value(val, indent + 2))
            elif isinstance(val, (dict, list)):
                out.append(f"{pad}{key}: {{}}" if isinstance(val, dict) else f"{pad}{key}: []")
            else:
                out.append(f"{pad}{key}: {_dump_scalar(val)}")
        return out
    if isinstance(value, list):
        out = []
        for item in value:
            if isinstance(item, dict):
                rendered = _dump_value(item, indent + 2)
                first = rendered[0].lstrip()
                out.append(f"{pad}- {first}")
                out.extend(rendered[1:])
            else:
                out.append(f"{pad}- {_dump_scalar(item)}")
        return out
    return [f"{pad}{_dump_scalar(value)}"]


def _dump_scalar(value) -> str:
    if value is None:
        return "~"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value)
    # Un tiret ou un deux-points interne ne gêne pas ; c'est en tête de scalaire,
    # ou suivi d'une espace, qu'ils changent le sens.
    needs_quotes = (
        text == ""
        or text != text.strip()
        or text[0] in "-?:,[]{}#&*!|>'\"%@`"
        or ": " in text
        or " #" in text
        or text.lower() in {"true", "false", "yes", "no", "null", "~"}
    )
    if needs_quotes:
        return '"' + text.replace('"', '\\"') + '"'
    return text


def dump_yaml(value) -> str:
    """Sérialise en YAML lisible. Volontairement stable : même entrée, même sortie."""
    return "\n".join(_dump_value(value, 0)) + "\n"


FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?", re.DOTALL)


def read_frontmatter(path: Path) -> tuple[dict, str]:
    """Rend (frontmatter, corps). Frontmatter vide si absent ou illisible.

    Ne lit jamais un média ni un fichier à nom de credential : l'appelant doit
    filtrer en amont, mais on refuse une seconde fois ici par sécurité.
    """
    if not is_readable_content(path):
        return {}, ""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeDecodeError):
        return {}, ""
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
    parsed = parse_yaml(match.group(1))
    return (parsed if isinstance(parsed, dict) else {}), text[match.end():]


def first_heading(body: str) -> str:
    """Premier titre Markdown, sinon première ligne non vide, sinon ''."""
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip()
    for line in body.splitlines():
        if line.strip():
            return line.strip()[:120]
    return ""


def word_count(body: str) -> int:
    return len(body.split())


# --------------------------------------------------------------------------- #
# Plan dry-run — aucune écriture sans --apply
# --------------------------------------------------------------------------- #


class Operation:
    """Un déplacement ou renommage, jamais une suppression."""

    def __init__(self, src: Path, dst: Path, reason: str, optional: bool = False):
        self.src = src
        self.dst = dst
        self.reason = reason
        self.optional = optional
        self.status = "planned"
        self.detail = ""

    def __str__(self) -> str:
        return f"{self.src} → {self.dst}"


class Plan:
    """Collecte les opérations, les affiche, puis les exécute sur `--apply`.

    Deux garde-fous non négociables : jamais d'écrasement d'une destination
    existante (collision signalée, opération sautée) et jamais de suppression.
    """

    def __init__(self, title: str, base: Path | None = None):
        self.title = title
        self.base = base
        self.operations: list[Operation] = []

    def show(self, path: Path) -> str:
        """Chemin relatif à la base quand c'est possible — un plan doit se lire."""
        if self.base is None:
            return str(path)
        try:
            return path.resolve().relative_to(self.base.resolve()).as_posix()
        except ValueError:
            return str(path)

    def line(self, op: "Operation") -> str:
        return f"{self.show(op.src)} → {self.show(op.dst)}"

    def add(self, src: Path, dst: Path, reason: str, optional: bool = False) -> Operation:
        op = Operation(src, dst, reason, optional)
        self.operations.append(op)
        return op

    def __len__(self) -> int:
        return len(self.operations)

    def render(self, include_optional: bool, apply: bool = False) -> None:
        suffix = "" if apply else " (dry-run)"
        print(f"\n## {self.title}{suffix}")
        shown = [op for op in self.operations if include_optional or not op.optional]
        if not shown:
            print("- rien à faire")
            return
        for op in shown:
            mark = " (opt-in)" if op.optional else ""
            print(f"- [{op.reason}]{mark} {self.line(op)}")

    def execute(self, include_optional: bool) -> tuple[int, int]:
        """Applique les opérations. Rend (appliquées, sautées)."""
        applied = skipped = 0
        for op in self.operations:
            if op.optional and not include_optional:
                op.status = "skipped"
                op.detail = "dérive non retenue"
                skipped += 1
                continue
            if not op.src.exists():
                op.status = "skipped"
                op.detail = "source disparue"
                skipped += 1
                continue
            if op.dst.exists():
                op.status = "skipped"
                op.detail = "destination déjà présente — collision"
                skipped += 1
                continue
            try:
                op.dst.parent.mkdir(parents=True, exist_ok=True)
                op.src.rename(op.dst)
            except OSError as exc:
                op.status = "skipped"
                op.detail = str(exc)
                skipped += 1
                continue
            op.status = "applied"
            applied += 1
        return applied, skipped

    def report(self) -> None:
        done = [op for op in self.operations if op.status == "applied"]
        missed = [op for op in self.operations if op.status == "skipped"]
        print("\n## Appliqué")
        for op in done:
            print(f"- {self.line(op)} ✓")
        if not done:
            print("- rien")
        if missed:
            print("\n## Sauté")
            for op in missed:
                print(f"- {self.line(op)} ⚠ {op.detail}")


def unique_destination(path: Path) -> Path:
    """Suffixe numérique déterministe plutôt qu'un écrasement silencieux."""
    if not path.exists():
        return path
    stem, suffix = path.stem, path.suffix
    for n in range(2, 1000):
        candidate = path.with_name(f"{stem}-{n}{suffix}")
        if not candidate.exists():
            return candidate
    raise RuntimeError(f"impossible de dériver un nom libre pour {path}")


def write_text(path: Path, content: str, apply: bool, label: str = "") -> bool:
    """Écrit un fichier dérivé. Sans `--apply`, annonce et n'écrit rien."""
    name = label or str(path)
    if not apply:
        info(f"[dry-run] écrirait {name} ({len(content.splitlines())} lignes)")
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    ok(f"écrit {name}")
    return True


# --------------------------------------------------------------------------- #
# Répertoire de travail dérivé et intégrité des liens
# --------------------------------------------------------------------------- #


def workdir_root(path: Path) -> Path:
    """Niveau `<Subcategory>` où déposer un fichier dérivé.

    Les niveaux datés (`AAAA`, `MM`) sont remontés ; hors d'un tree reconnu,
    le fichier reste dans `path` — mieux vaut un dérivé au mauvais endroit
    qu'un dérivé déposé dans une arborescence qu'on n'a pas comprise.
    """
    current = path.resolve()
    if current.is_file():
        current = current.parent
    while is_dated_level(current.name):
        current = current.parent
    anchor = find_anchor(current)
    if anchor is None:
        return current
    rel = current.relative_to(anchor).parts
    if len(rel) >= 2:
        return anchor.joinpath(*rel[:2])
    return current


MD_LINK_RE = re.compile(r"(!?\[[^\]]*\]\()([^)\s]+)(\))")
WIKI_LINK_RE = re.compile(r"(!?\[\[)([^\]|#]+)([^\]]*\]\])")
_EXTERNAL_RE = re.compile(r"^(?:[a-z][a-z0-9+.-]*:|//|#)", re.IGNORECASE)


def _retarget(ref: str, old_dir: Path, new_dir: Path, add_md: bool) -> str | None:
    """Chemin relatif équivalent depuis `new_dir`, ou None si rien à changer."""
    if _EXTERNAL_RE.match(ref) or ref.startswith("/"):
        return None
    probe = ref + ".md" if add_md and not ref.endswith(".md") else ref
    target = (old_dir / probe).resolve()
    if not target.exists():
        return None
    try:
        rebuilt = os.path.relpath(target, new_dir)
    except ValueError:
        return None
    rebuilt = Path(rebuilt).as_posix()
    if add_md and rebuilt.endswith(".md"):
        rebuilt = rebuilt[:-3]
    return rebuilt if rebuilt != ref else None


def relink_moved(moves: list[tuple[Path, Path]], apply: bool) -> int:
    """Réécrit les liens relatifs sortants des fichiers Markdown déplacés.

    Les wikilinks sans chemin (`[[note]]`) ne sont pas touchés : Obsidian les
    résout par nom, un déplacement ne les casse pas. Seules les références
    portant un chemin — liens Markdown et wikilinks contenant un `/` — sont
    recalculées depuis la nouvelle position.
    """
    touched = 0
    for src, dst in moves:
        if dst.suffix.lower() != ".md" or not dst.exists():
            continue
        try:
            text = dst.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        old_dir, new_dir = src.parent, dst.parent
        if old_dir.resolve() == new_dir.resolve():
            continue

        def fix_md(match: re.Match) -> str:
            new_ref = _retarget(match.group(2), old_dir, new_dir, add_md=False)
            return match.group(0) if new_ref is None else f"{match.group(1)}{new_ref}{match.group(3)}"

        def fix_wiki(match: re.Match) -> str:
            ref = match.group(2)
            if "/" not in ref:
                return match.group(0)
            new_ref = _retarget(ref, old_dir, new_dir, add_md=True)
            return match.group(0) if new_ref is None else f"{match.group(1)}{new_ref}{match.group(3)}"

        rewritten = WIKI_LINK_RE.sub(fix_wiki, MD_LINK_RE.sub(fix_md, text))
        if rewritten == text:
            continue
        touched += 1
        if apply:
            dst.write_text(rewritten, encoding="utf-8", newline="\n")
    return touched


def applied_moves(plan: "Plan") -> list[tuple[Path, Path]]:
    return [(op.src, op.dst) for op in plan.operations if op.status == "applied"]


def dangling_links(directory: Path) -> list[tuple[Path, str]]:
    """Références portant un chemin qui ne résolvent plus, sous `directory`."""
    broken: list[tuple[Path, str]] = []
    for entry in iter_entries(directory, recursive=True):
        if entry.is_dir() or entry.suffix.lower() != ".md":
            continue
        try:
            text = entry.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        refs = [m.group(2) for m in MD_LINK_RE.finditer(text)]
        refs += [m.group(2) for m in WIKI_LINK_RE.finditer(text) if "/" in m.group(2)]
        for ref in refs:
            if _EXTERNAL_RE.match(ref) or ref.startswith("/"):
                continue
            probe = ref if Path(ref).suffix else ref + ".md"
            if not (entry.parent / probe).exists():
                broken.append((entry, ref))
    return broken
