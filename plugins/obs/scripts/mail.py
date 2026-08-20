#!/usr/bin/env python3
"""
obs:mail — trie une arborescence d'emails Markdown selon `mail-config.yaml`,
sans appel LLM.

    python mail.py triage      <branche> [--config <chemin>] [--reprocess] [--apply]
    python mail.py init-config <branche> [--apply]

Le tri est un moteur de règles : ce que la configuration ne tranche pas reste
sur place et part au rapport. Aucune décision n'est inventée.

Rien n'est écrit sans `--apply`. Aucune suppression : ce que la configuration
condamne est déplacé dans `.archive/AAAA-MM-JJ/`, chemin relatif conservé.
Compatible Windows, Linux, macOS. Bibliothèque standard seulement.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from obslib import (  # noqa: E402
    AnchorNotFound,
    Plan,
    error,
    info,
    ok,
    parse_yaml,
    read_frontmatter,
    today,
    warn,
    write_text,
)

CONFIG_NAME = "mail-config.yaml"
ARCHIVE_DIR = ".archive"
EXCLUDED_DIRS = (ARCHIVE_DIR, "_drafts")
EXCLUDED_FILES = ("mail-sessions.log.md",)
EPOCH_MARKERS = ("1970-01-01", "")
EMAIL_RE = re.compile(r"[\w.+-]+@([\w-]+(?:\.[\w-]+)+)")

CONFIG_TEMPLATE = """\
# Emails et branches à conserver intacts (ne pas résumer, ne pas fusionner)
preserve:
  senders: []        # ex: - domain: gmail.com
  branches: []       # ex: - Banque/

# Emails et branches à écarter (spam, notifications sans valeur)
suppress:
  senders: []        # ex: - domain: klaviyo.com
  branches: []       # ex: - Publicités/Spam/

# Exceptions aux règles preserve/suppress
exceptions: []       # ex: - address: foo@bar.com
                     #      action: preserve

# Mise à l'écart automatique par âge (days: 0 = sans délai)
prune: []
# ex:
#   - branch: Publicités/Spam/
#     days: 0
#   - sender:
#       domain: jeveuxtravailler.com
#     days: 7

# Fusionner les threads par domaine racine plutôt que par adresse exacte
merge_by_domain: false

# Marques à surveiller pour la détection de hameçonnage
phishing_brands: []
"""


# --------------------------------------------------------------------------- #
# Scan
# --------------------------------------------------------------------------- #


class Mail:
    def __init__(self, path: Path, root: Path) -> None:
        self.path = path
        self.rel = path.relative_to(root)
        self.branch = self.rel.parent.as_posix() + "/" if self.rel.parent != Path(".") else ""
        self.frontmatter, _ = read_frontmatter(path)
        self.sender = str(self.frontmatter.get("from", "") or "")
        raw_date = self.frontmatter.get("date")
        self.date_text = raw_date.isoformat() if hasattr(raw_date, "isoformat") else str(raw_date or "")
        self.processed = str(self.frontmatter.get("processed", "")).lower() in ("true", "1", "yes")

    @property
    def domain(self) -> str:
        match = EMAIL_RE.search(self.sender)
        return match.group(1).lower() if match else ""

    @property
    def address(self) -> str:
        match = EMAIL_RE.search(self.sender)
        return match.group(0).lower() if match else ""

    @property
    def when(self) -> datetime | None:
        for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S"):
            try:
                return datetime.strptime(self.date_text[:len(fmt) + 2].strip(), fmt)
            except ValueError:
                continue
        return None

    @property
    def age_days(self) -> int | None:
        moment = self.when
        return None if moment is None else (datetime.now() - moment).days


def scan(root: Path, reprocess: bool) -> tuple[list[Mail], list[str]]:
    """Emails à traiter et rapport préliminaire. Aucun corps n'est lu."""
    mails: list[Mail] = []
    to_sort = epoch = 0
    for path in sorted(root.rglob("*.md")):
        rel = path.relative_to(root)
        if any(part in EXCLUDED_DIRS for part in rel.parts):
            continue
        if path.name in EXCLUDED_FILES or path.name == CONFIG_NAME:
            continue
        mail = Mail(path, root)
        if mail.processed and not reprocess:
            continue
        if "ATrier" in rel.parts:
            to_sort += 1
        if mail.date_text in EPOCH_MARKERS:
            epoch += 1
        mails.append(mail)

    report = []
    if to_sort:
        report.append(f"fichiers dans `ATrier/` : {to_sort} — arbitrage humain")
    if epoch:
        report.append(f"fichiers sans date exploitable : {epoch} — l'âge ne les concerne pas")
    return mails, report


# --------------------------------------------------------------------------- #
# Moteur de règles
# --------------------------------------------------------------------------- #


def as_list(value) -> list:
    if isinstance(value, list):
        return value
    return [] if value in (None, "", {}) else [value]


def sender_matches(mail: Mail, rule) -> bool:
    if isinstance(rule, str):
        needle = rule.lower().lstrip("@")
        return needle in (mail.address or mail.sender.lower())
    if isinstance(rule, dict):
        domain = str(rule.get("domain", "") or "").lower().lstrip("@")
        address = str(rule.get("address", "") or "").lower()
        if domain and (mail.domain == domain or mail.domain.endswith("." + domain)):
            return True
        if address and mail.address == address:
            return True
    return False


def branch_matches(mail: Mail, rule) -> bool:
    prefix = str(rule or "").strip().strip("/")
    if not prefix:
        return False
    return mail.branch.startswith(prefix + "/")


def side_matches(mail: Mail, side: dict) -> bool:
    if not isinstance(side, dict):
        return False
    if any(sender_matches(mail, r) for r in as_list(side.get("senders"))):
        return True
    return any(branch_matches(mail, r) for r in as_list(side.get("branches")))


def prune_matches(mail: Mail, rule: dict) -> bool:
    """Une règle d'âge ne mord que sur un email dont la date est lisible."""
    if not isinstance(rule, dict):
        return False
    scoped = False
    if "branch" in rule:
        scoped = branch_matches(mail, rule.get("branch"))
    if not scoped and "sender" in rule:
        scoped = sender_matches(mail, rule.get("sender"))
    if not scoped:
        return False
    age = mail.age_days
    if age is None:
        return False
    try:
        days = int(rule.get("days", 0))
    except (TypeError, ValueError):
        days = 0
    return age >= days


def decide(mail: Mail, config: dict) -> tuple[str, str]:
    """Rend (décision, motif). `arbitrer` quand la configuration ne dit rien."""
    for rule in as_list(config.get("exceptions")):
        if isinstance(rule, dict) and sender_matches(mail, rule):
            action = str(rule.get("action", "preserve"))
            return ("intact" if action == "preserve" else "écarter"), "exception"
    if side_matches(mail, config.get("preserve") or {}):
        return "intact", "preserve"
    if side_matches(mail, config.get("suppress") or {}):
        return "écarter", "suppress"
    for rule in as_list(config.get("prune")):
        if prune_matches(mail, rule):
            return "écarter", f"prune ({mail.age_days} j)"
    return "arbitrer", "aucune règle"


def flatten(text: str) -> str:
    """Forme comparable : `Ma Banque` et `ma-banque` désignent la même marque."""
    return re.sub(r"[^a-z0-9]", "", str(text).lower())


def phishing_suspects(mails: list[Mail], config: dict) -> list[tuple[Mail, str]]:
    """Marque connue dans le nom affiché, domaine étranger à cette marque.

    La comparaison porte sur le domaine enregistrable et exige l'égalité :
    `ma-banque-verif.tk` contient `ma-banque` sans en être. Signalement
    seulement — rien n'est déplacé sur cette seule base.
    """
    brands = [(str(b), flatten(b)) for b in as_list(config.get("phishing_brands")) if b]
    suspects = []
    for mail in mails:
        display = flatten(mail.sender.split("<")[0])
        labels = mail.domain.split(".")
        registrable = flatten(labels[-2]) if len(labels) >= 2 else flatten(mail.domain)
        for label, brand in brands:
            if brand and brand in display and registrable != brand:
                suspects.append((mail, label))
                break
    return suspects


# --------------------------------------------------------------------------- #
# Écritures
# --------------------------------------------------------------------------- #


def mark_processed(path: Path, apply: bool) -> None:
    """Pose `processed: true`, en créant un frontmatter minimal si besoin."""
    if not apply or not path.exists():
        return
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return
    if re.match(r"^---\s*\n", text):
        if re.search(r"^processed\s*:", text, re.MULTILINE):
            updated = re.sub(r"^processed\s*:.*$", "processed: true", text, count=1, flags=re.MULTILINE)
        else:
            updated = re.sub(r"^---\s*\n", "---\nprocessed: true\n", text, count=1)
    else:
        updated = "---\nprocessed: true\n---\n\n" + text
    path.write_text(updated, encoding="utf-8", newline="\n")


def load_config(root: Path, explicit: str) -> tuple[dict, Path]:
    path = Path(explicit).expanduser() if explicit else root / CONFIG_NAME
    if not path.exists():
        return {}, path
    try:
        data = parse_yaml(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise SystemExit(f"{path} illisible : {exc}")
    return (data if isinstance(data, dict) else {}), path


# --------------------------------------------------------------------------- #
# Commandes
# --------------------------------------------------------------------------- #


def cmd_init_config(args: argparse.Namespace) -> int:
    root = Path(args.scope).expanduser()
    if not root.is_dir():
        error(f"{root} n'est pas un répertoire")
        return 2
    target = root / CONFIG_NAME
    if target.exists():
        error(f"{target} existe déjà — édition manuelle")
        return 1
    write_text(target, CONFIG_TEMPLATE, args.apply, label=str(target))
    if not args.apply:
        info("relancer avec --apply pour écrire")
    return 0


def cmd_triage(args: argparse.Namespace) -> int:
    root = Path(args.scope).expanduser()
    if not root.is_dir():
        error(f"{root} n'est pas un répertoire")
        return 2
    config, config_path = load_config(root, args.config)
    if not config:
        error(f"{config_path} absent ou vide — `init-config` d'abord")
        return 1

    mails, prelim = scan(root, args.reprocess)
    if not mails:
        ok(f"{root} : rien à trier")
        return 0
    if prelim:
        print("\n## Rapport préliminaire")
        for line in prelim:
            print(f"- {line}")

    decisions = [(mail, *decide(mail, config)) for mail in mails]
    archive = root / ARCHIVE_DIR / today()
    plan = Plan(f"Mise à l'écart vers {ARCHIVE_DIR}/{today()}", base=root)
    for mail, verdict, reason in decisions:
        if verdict == "écarter":
            plan.add(mail.path, archive / mail.rel, reason)

    plan.render(include_optional=True, apply=args.apply)
    archived = 0
    if args.apply and len(plan):
        archived, skipped = plan.execute(include_optional=True)
        plan.report()
        for op in plan.operations:
            if op.status == "applied":
                mark_processed(op.dst, apply=True)
    elif not args.apply:
        info("relancer avec --apply pour exécuter")

    intact = [m for m, v, _ in decisions if v == "intact"]
    pending = [(m, r) for m, v, r in decisions if v == "arbitrer"]
    if pending:
        print("\n## À arbitrer")
        for mail, reason in pending[:50]:
            print(f"- {mail.rel.as_posix()} — {mail.domain or 'expéditeur inconnu'} ({reason})")
        if len(pending) > 50:
            print(f"- … {len(pending) - 50} autres")

    suspects = phishing_suspects(mails, config)
    if suspects:
        print("\n## Hameçonnage possible")
        for mail, brand in suspects:
            warn(f"{mail.rel.as_posix()} : se présente comme `{brand}` depuis `{mail.domain}`")

    print("\n## Rapport")
    print(f"- {len(mails)} emails dans la portée, config : {config_path}")
    suffix = f", {archived} archivé{'s' if archived > 1 else ''}" if args.apply else " (dry-run)"
    print(f"- {len(plan)} à écarter{suffix}")
    print(f"- {len(intact)} conservés intacts, {len(pending)} à arbitrer")
    if len(plan):
        print("- aucune suppression : les originaux sont dans l'archive")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mail.py",
        description="Trie une arborescence d'emails Markdown selon mail-config.yaml.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    triage = sub.add_parser("triage", help="appliquer les règles de tri à une branche")
    triage.add_argument("scope")
    triage.add_argument("--config", default="", help=f"chemin du {CONFIG_NAME}")
    triage.add_argument("--reprocess", action="store_true", help="reprendre les fichiers déjà traités")
    triage.add_argument("--apply", action="store_true")
    triage.set_defaults(func=cmd_triage)

    init = sub.add_parser("init-config", help=f"écrire un {CONFIG_NAME} vierge")
    init.add_argument("scope")
    init.add_argument("--apply", action="store_true")
    init.set_defaults(func=cmd_init_config)

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
