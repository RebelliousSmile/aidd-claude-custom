#!/usr/bin/env python3
"""
obs:project — crée et tient à jour les notes de projet de `Pro/Projets/`, sans
appel LLM.

    python project.py create     <nom> --type commercial|open-source|personnel [--apply]
    python project.py invoice    <nom> --objet <texte> --montant <HT>
                                       [--date AAAA-MM-JJ] [--statut …] [--apply]
    python project.py export-rag <nom> [--out <chemin>] [--apply]

L'ancre `Pro` est découverte en remontant depuis `--anchor` (défaut : le
répertoire courant) ; aucun chemin absolu n'est codé en dur. Les gabarits
voyagent avec le plugin, jamais dans le vault.

Rien n'est écrit sans `--apply`. Aucune suppression, jamais.
Compatible Windows, Linux, macOS. Bibliothèque standard seulement.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from obslib import (  # noqa: E402
    AnchorNotFound,
    error,
    find_anchor,
    info,
    ok,
    today,
    warn,
    write_text,
)

TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "skills" / "project" / "references" / "projet-template"

FILES_BY_TYPE = {
    "commercial": ("projet.md", "memory.md", "backlog.md", "commercial.md"),
    "open-source": ("projet.md", "memory.md", "backlog.md", "communication.md"),
    "personnel": ("projet.md", "memory.md", "backlog.md", "objectifs.md"),
}

STATUSES = ("émise", "payée", "en attente", "annulée")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
# Une ligne de tableau qui porte encore un `<champ>` ou une date-gabarit est un
# exemple, pas une donnée : la première vraie ligne prend sa place.
PLACEHOLDER_ROW_RE = re.compile(r"^\|.*(<[^>|]+>|YYYY-MM-DD|AAAA-MM-JJ)")

EMPTY_MARK = "> ⚠️ Section vide — à compléter"


# --------------------------------------------------------------------------- #
# Localisation
# --------------------------------------------------------------------------- #


def projects_root(start: Path) -> Path:
    """`Pro/Projets/`, découvert en remontant depuis `start`."""
    anchor = find_anchor(start)
    if anchor is None or anchor.name != "Pro":
        raise AnchorNotFound(start)
    return anchor / "Projets"


def project_dir(start: Path, name: str) -> Path:
    return projects_root(start) / name


def section(text: str, title: str) -> str:
    """Corps d'une section Markdown, sans son titre. Vide si absente."""
    pattern = re.compile(
        rf"^(#{{1,6}})\s*{re.escape(title)}\s*$(.*?)(?=^#{{1,6}}\s|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    return match.group(2).strip() if match else ""


def normalize(text: str) -> str:
    """Forme comparable : dates et espacement neutralisés."""
    without_dates = re.sub(r"\d{4}-\d{2}-\d{2}|YYYY-MM-DD|AAAA-MM-JJ", "D", text)
    return re.sub(r"\s+", " ", without_dates).strip()


def is_filled(body: str, template: str = "") -> bool:
    """Une section remplie, par opposition à un gabarit resté en l'état.

    Le gabarit fait référence : une section identique au modèle livré n'a rien
    à dire, quels que soient les mots qu'elle contient. Sans modèle, il suffit
    qu'il reste du texte une fois les marques de gabarit retirées.
    """
    if template and normalize(body) == normalize(template):
        return False
    stripped = re.sub(r"<[^>]*>|<!--.*?-->|\[ \]|\[x\]|[-|\s]", "", body, flags=re.DOTALL)
    stripped = re.sub(r"YYYY-MM-DD|AAAA-MM-JJ", "", stripped)
    return bool(stripped.strip())


def template_section(filename: str, title: str) -> str:
    return section(read(TEMPLATE_DIR / filename), title)


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


# --------------------------------------------------------------------------- #
# create
# --------------------------------------------------------------------------- #


def cmd_create(args: argparse.Namespace) -> int:
    target = project_dir(Path(args.anchor).expanduser(), args.name)
    if target.exists():
        error(f"{target} existe déjà — un projet ne s'écrase pas")
        return 1

    written = 0
    for filename in FILES_BY_TYPE[args.type]:
        template = TEMPLATE_DIR / filename
        body = read(template)
        if not body.strip():
            warn(f"gabarit {filename} vide ou illisible — fichier non écrit")
            continue
        body = body.replace("[Projet]", args.name)
        body = body.replace("YYYY-MM-DD", today()).replace("AAAA-MM-JJ", today())
        if write_text(target / filename, body, args.apply, label=f"{args.name}/{filename}"):
            written += 1

    expected = len(FILES_BY_TYPE[args.type])
    print(f"\n## Rapport\n- projet `{args.name}` ({args.type}) dans {target}")
    if args.apply:
        print(f"- {written} fichier(s) écrit(s) sur {expected}")
    else:
        print(f"- {expected} fichier(s) à écrire")
    if args.apply:
        info("`projet.md` attend un résumé de contexte en trois lignes")
    else:
        info("relancer avec --apply pour écrire")
    return 0


# --------------------------------------------------------------------------- #
# invoice
# --------------------------------------------------------------------------- #


def insert_row(text: str, row: str) -> str:
    """Ajoute une ligne au tableau `## Devis`, en évacuant la ligne d'exemple."""
    lines = text.splitlines()
    start = next((n for n, ln in enumerate(lines) if re.match(r"^#{1,6}\s*Devis\s*$", ln)), None)
    if start is None:
        raise SystemExit("`commercial.md` n'a pas de section `## Devis`")
    end = start + 1
    last_row = None
    while end < len(lines) and not re.match(r"^#{1,6}\s", lines[end]):
        if lines[end].strip().startswith("|"):
            last_row = end
        end += 1
    if last_row is None:
        raise SystemExit("la section `## Devis` ne contient pas de tableau")
    if PLACEHOLDER_ROW_RE.match(lines[last_row].strip()):
        lines[last_row] = row
    else:
        lines.insert(last_row + 1, row)
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def update_billing(text: str, when: str, statut: str) -> str:
    """`Dernière facture` suit la dernière pièce réellement émise ou payée."""
    if statut not in ("émise", "payée"):
        return text
    return re.sub(
        r"^(-\s*Dernière facture\s*:).*$",
        rf"\1 {when}",
        text,
        count=1,
        flags=re.MULTILINE,
    )


def cmd_invoice(args: argparse.Namespace) -> int:
    when = args.date or today()
    if not DATE_RE.match(when):
        error(f"date `{when}` : format attendu AAAA-MM-JJ")
        return 2
    target = project_dir(Path(args.anchor).expanduser(), args.name) / "commercial.md"
    text = read(target)
    if not text:
        error(f"{target} absent ou illisible — `create --type commercial` d'abord")
        return 1

    montant = args.montant.replace(",", ".").strip()
    row = f"| {when} | {args.objet} | {montant} | {args.statut} |"
    updated = update_billing(insert_row(text, row), when, args.statut)

    print(f"\n## Ligne ajoutée\n{row}")
    if not write_text(target, updated, args.apply, label=str(target)):
        info("relancer avec --apply pour écrire")
    return 0


# --------------------------------------------------------------------------- #
# export-rag
# --------------------------------------------------------------------------- #


def build_rag(directory: Path, name: str) -> tuple[str, list[str]]:
    """Assemble le contexte RAG. Rend (contenu, sections restées vides).

    Le découpage est mécanique : chaque section de sortie a une source fixe.
    Aucun résumé n'est produit — ce qui est recopié l'est tel quel.
    """
    projet = read(directory / "projet.md")
    backlog = read(directory / "backlog.md")
    snippets = read(directory / "snippets.md")

    etat = "\n\n".join(
        f"### {titre}\n{section(backlog, titre)}"
        for titre in ("En cours", "En attente", "Livré")
        if is_filled(section(backlog, titre), template_section("backlog.md", titre))
    )
    attention = "\n\n".join(
        f"### {titre}\n{section(projet, titre)}"
        for titre in ("En cours", "Accès")
        if is_filled(section(projet, titre), template_section("projet.md", titre))
    )

    blocks = {
        "Contexte": (section(projet, "Contexte"), template_section("projet.md", "Contexte")),
        "Stack & architecture": (
            section(projet, "Décisions techniques"),
            template_section("projet.md", "Décisions techniques"),
        ),
        "État du projet": (etat, ""),
        "Points d'attention": (attention, ""),
        "Snippets de référence": (snippets.strip(), ""),
    }

    empty = [title for title, (body, model) in blocks.items() if not is_filled(body, model)]
    lines = [
        "---",
        "name: project-notes",
        "description: Contexte projet issu des notes Obsidian — généré par obs:project export-rag",
        f"source: Pro/Projets/{name}/",
        f"date: {today()}",
        "---",
        "",
        f"# Contexte projet — {name}",
        "",
    ]
    for title, (body, _) in blocks.items():
        lines.append(f"## {title}")
        lines.append("")
        lines.append(EMPTY_MARK if title in empty else body.strip())
        lines.append("")
    return "\n".join(lines), empty


def cmd_export_rag(args: argparse.Namespace) -> int:
    directory = project_dir(Path(args.anchor).expanduser(), args.name)
    if not directory.is_dir():
        error(f"{directory} n'existe pas")
        return 1
    content, empty = build_rag(directory, args.name)
    target = Path(args.out).expanduser() if args.out else directory / "project-notes.md"

    if not args.apply:
        print(content)
    write_text(target, content, args.apply, label=str(target))
    print(f"\n## Rapport\n- sortie : {target}")
    if empty:
        warn("sections vides : " + ", ".join(empty))
    else:
        ok("les cinq sections sont remplies")
    if not args.apply:
        info("relancer avec --apply pour écrire")
    return 0


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="project.py",
        description="Crée et tient à jour les notes de projet de `Pro/Projets/`.",
    )
    parser.add_argument(
        "--anchor",
        default=".",
        help="point de départ de la recherche de l'ancre `Pro` (défaut : répertoire courant)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    create = sub.add_parser("create", help="créer le dossier projet et ses fichiers")
    create.add_argument("name")
    create.add_argument("--type", choices=tuple(FILES_BY_TYPE), required=True)
    create.add_argument("--anchor", default=argparse.SUPPRESS)
    create.add_argument("--apply", action="store_true")
    create.set_defaults(func=cmd_create)

    invoice = sub.add_parser("invoice", help="ajouter une ligne de devis ou facture")
    invoice.add_argument("name")
    invoice.add_argument("--objet", required=True)
    invoice.add_argument("--montant", required=True, help="montant HT")
    invoice.add_argument("--date", default="", help="AAAA-MM-JJ (défaut : aujourd'hui)")
    invoice.add_argument("--statut", choices=STATUSES, default="émise")
    invoice.add_argument("--anchor", default=argparse.SUPPRESS)
    invoice.add_argument("--apply", action="store_true")
    invoice.set_defaults(func=cmd_invoice)

    rag = sub.add_parser("export-rag", help="assembler le contexte RAG du projet")
    rag.add_argument("name")
    rag.add_argument("--out", default="", help="chemin de sortie (défaut : project-notes.md)")
    rag.add_argument("--anchor", default=argparse.SUPPRESS)
    rag.add_argument("--apply", action="store_true")
    rag.set_defaults(func=cmd_export_rag)

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
