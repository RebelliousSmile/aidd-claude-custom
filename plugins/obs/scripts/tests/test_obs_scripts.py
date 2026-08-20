#!/usr/bin/env python3
"""Invariants des scripts `obs` — ce qui ne doit jamais céder.

    python -m unittest discover -s scripts/tests -v

Chaque test monte une arborescence jetable, lance la commande réelle et
inspecte le disque. Rien n'est simulé : la garantie testée est celle que la
skill annonce.
"""

from __future__ import annotations

import io
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS))

import filler  # noqa: E402
import mail  # noqa: E402
import obslib  # noqa: E402
import project  # noqa: E402
import tree  # noqa: E402


def run(module, argv: list[str]) -> tuple[int, str]:
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        code = module.main(argv)
    return code, buffer.getvalue()


def snapshot(root: Path) -> dict[str, str]:
    """État complet du disque : chemin relatif → contenu (ou `<dir>`)."""
    out = {}
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        if path.is_dir():
            out[rel] = "<dir>"
        else:
            out[rel] = path.read_bytes().hex()
    return out


class Fixture(unittest.TestCase):
    """Ancre `Perso`/`Pro` jetable, reconstruite pour chaque test."""

    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="obs-test-"))
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.docs = self.tmp / "Documents"

    def write(self, relative: str, content: str = "contenu\n") -> Path:
        path = self.docs / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path


# --------------------------------------------------------------------------- #
# Garde-fous transversaux
# --------------------------------------------------------------------------- #


class TestGuards(Fixture):
    def test_credential_content_is_never_read(self) -> None:
        secret = self.write("Perso/Finance/banque/.env", "API_KEY=ne-doit-jamais-sortir\n")
        self.write("Perso/Finance/banque/note.md", "# Note\n\nDu texte.\n")
        _, out = run(filler, ["survey", str(secret.parent)])
        self.assertNotIn("ne-doit-jamais-sortir", out)
        self.assertIn(".env", out)

    def test_credential_inside_code_dir_is_silent(self) -> None:
        self.write("Pro/Projets/acme/_code/.env", "TOKEN=x\n")
        self.write("Pro/Projets/acme/_code/note.md", "# Note\n")
        _, out = run(filler, ["survey", str(self.docs / "Pro/Projets/acme/_code")])
        self.assertNotIn(".env", out)

    def test_media_are_never_read(self) -> None:
        binary = self.docs / "Perso/photos/vacances/photo.jpg"
        binary.parent.mkdir(parents=True, exist_ok=True)
        binary.write_bytes(b"\xff\xd8\xff\xe0 pas du texte")
        self.assertFalse(obslib.is_readable_content(binary))

    def test_dotfiles_never_move_alone(self) -> None:
        self.assertFalse(obslib.movable_standalone(self.docs / "Perso/x/.git"))
        self.assertFalse(obslib.movable_standalone(self.docs / "Perso/x/.gitignore"))
        self.assertTrue(obslib.movable_standalone(self.docs / "Perso/x/note.md"))


class TestDryRunIsTheDefault(Fixture):
    """Sept commandes sur sept : sans `--apply`, le disque est intact."""

    def test_no_command_writes_without_apply(self) -> None:
        self.write("Perso/Finance/banque/2026/06/note-une.md", "# Une\n\nTexte.\n")
        self.write("Perso/Finance/banque/2026/06/note-deux.md", "# Deux\n\nTexte.\n")
        self.write("Perso/Finance/banque/2026/06/Fichier Non Portable.md", "# Trois\n")
        target = str(self.docs / "Perso/Finance/banque/2026/06")
        before = snapshot(self.tmp)
        for module, argv in (
            (tree, ["index", target]),
            (tree, ["check", target]),
            (tree, ["fix", target]),
            (tree, ["destinations", target]),
            (filler, ["survey", target]),
            (filler, ["sort", target]),
            (filler, ["index", target]),
            (filler, ["merge", target]),
            (filler, ["clean", target, "--criteria", "empty"]),
        ):
            with self.subTest(command=argv[0]):
                run(module, argv)
                self.assertEqual(before, snapshot(self.tmp), f"{argv} a écrit sans --apply")


# --------------------------------------------------------------------------- #
# tree
# --------------------------------------------------------------------------- #


class TestTree(Fixture):
    def test_check_reports_invariant_breaches(self) -> None:
        self.write("Perso/Finance/Relevés Banque/note.md")     # I3 : slug non portable
        self.write("Perso/Finance/_archive/_dedans/note.md")   # I2 : préfixe imbriqué
        self.write("Perso/Finance/banque/2026/13/note.md")     # I4 : mois hors bornes
        _, out = run(tree, ["check", str(self.docs / "Perso/Finance")])
        self.assertIn("I3", out)
        self.assertIn("I2", out)
        self.assertIn("I4", out)

    def test_fix_renames_without_deleting(self) -> None:
        self.write("Perso/Finance/Relevés Banque/note.md", "# Note\n")
        run(tree, ["fix", str(self.docs / "Perso/Finance"), "--apply"])
        self.assertFalse((self.docs / "Perso/Finance/Relevés Banque").exists())
        renamed = self.docs / "Perso/Finance/releves-banque/note.md"
        self.assertTrue(renamed.exists())
        self.assertEqual(renamed.read_text(encoding="utf-8"), "# Note\n")

    def test_fix_never_overwrites_an_existing_destination(self) -> None:
        self.write("Perso/Finance/Relevés Banque/a.md", "source\n")
        self.write("Perso/Finance/releves-banque/b.md", "déjà là\n")
        _, out = run(tree, ["fix", str(self.docs / "Perso/Finance"), "--apply"])
        self.assertTrue((self.docs / "Perso/Finance/Relevés Banque/a.md").exists())
        self.assertEqual(
            (self.docs / "Perso/Finance/releves-banque/b.md").read_text(encoding="utf-8"),
            "déjà là\n",
        )
        self.assertIn("collision", out.lower())

    def test_index_writes_only_derived_cache(self) -> None:
        self.write("Perso/Finance/banque/note.md", "# Note\n")
        run(tree, ["index", str(self.docs / "Perso/Finance"), "--apply"])
        self.assertTrue((self.docs / "Perso/_tree/cache.json").exists())
        self.assertEqual(
            (self.docs / "Perso/Finance/banque/note.md").read_text(encoding="utf-8"), "# Note\n"
        )

    def test_anchor_is_discovered_not_hardcoded(self) -> None:
        self.write("Perso/Finance/banque/2026/06/note.md")
        found = obslib.find_anchor(self.docs / "Perso/Finance/banque/2026/06")
        self.assertEqual(found, self.docs / "Perso")


# --------------------------------------------------------------------------- #
# filler
# --------------------------------------------------------------------------- #


class TestFiller(Fixture):
    def emails(self) -> Path:
        target = self.docs / "Perso/Communication/Emails/2026/06"
        self.write(
            "Perso/Communication/Emails/2026/06/email_2026-06-10_marie.md",
            "---\nfrom: \"Marie Dupont\" <marie@smartlockers.io>\ndate: 2026-06-10\n"
            "subject: Contrat\n---\n\n# Contrat\n\nVoir ![[schema.png]] et [[note-suivi]].\n",
        )
        self.write(
            "Perso/Communication/Emails/2026/06/email_2026-06-11_onet.md",
            "---\nfrom: alerte@onet.fr\ndate: 2026-06-11\nsubject: Badge\n---\n\n# Badge\n\nAlerte.\n",
        )
        self.write("Perso/Communication/Emails/2026/06/note-suivi.md", "# Suivi\n\nRAS.\n")
        (target / "schema.png").write_bytes(b"\x89PNG fake")
        return target

    def test_sort_groups_by_registrable_domain(self) -> None:
        target = self.emails()
        run(filler, ["sort", str(target), "--scheme", "entity", "--apply"])
        self.assertTrue((target / "smartlockers/email_2026-06-10_marie.md").exists())
        self.assertTrue((target / "onet/email_2026-06-11_onet.md").exists())

    def test_sort_co_moves_the_referenced_asset(self) -> None:
        target = self.emails()
        run(filler, ["sort", str(target), "--scheme", "entity", "--apply"])
        moved = target / "smartlockers/email_2026-06-10_marie.md"
        self.assertTrue((target / "smartlockers/schema.png").exists())
        self.assertIn("![[schema.png]]", moved.read_text(encoding="utf-8"))

    def test_sort_loses_no_file(self) -> None:
        target = self.emails()
        before = sorted(p.name for p in target.rglob("*") if p.is_file())
        run(filler, ["sort", str(target), "--scheme", "entity", "--apply"])
        after = sorted(p.name for p in target.rglob("*") if p.is_file())
        self.assertEqual(before, after)

    def test_merge_and_index_never_touch_the_sources(self) -> None:
        target = self.emails()
        before = snapshot(target)
        run(filler, ["merge", str(target), "--apply"])
        run(filler, ["index", str(target), "--apply"])
        for name, content in before.items():
            self.assertEqual(snapshot(target).get(name), content, f"{name} modifié")

    def test_clean_archives_instead_of_deleting(self) -> None:
        target = self.emails()
        self.write("Perso/Communication/Emails/2026/06/vide.md", "\n")
        run(filler, ["clean", str(target), "--criteria", "empty", "--apply"])
        self.assertFalse((target / "vide.md").exists())
        archived = list((self.docs / "Perso/Communication/Emails/_archive").rglob("vide.md"))
        self.assertEqual(len(archived), 1)

    def test_no_silent_overwrite_on_collision(self) -> None:
        target = self.emails()
        run(filler, ["merge", str(target), "--apply"])
        produced = sorted((self.docs / "Perso/Communication/Emails").glob("_merged*.md"))
        self.assertEqual(len(produced), 1)
        original = produced[0].read_text(encoding="utf-8")
        run(filler, ["merge", str(target), "--apply"])
        again = sorted((self.docs / "Perso/Communication/Emails").glob("_merged*.md"))
        self.assertEqual(len(again), 2, "la seconde fusion a écrasé la première")
        self.assertEqual(produced[0].read_text(encoding="utf-8"), original)

    def test_scope_is_not_recursive_by_default(self) -> None:
        target = self.emails()
        self.write("Perso/Communication/Emails/2026/06/sous/cachée.md", "# Cachée\n\nTexte.\n")
        _, out = run(filler, ["survey", str(target)])
        self.assertNotIn("cachée.md", out)
        _, recursive = run(filler, ["survey", str(target), "--recursive"])
        self.assertIn("cachée.md", recursive)

    def test_derived_files_land_at_subcategory_level(self) -> None:
        """`2026/06` est daté : on remonte jusqu'à `<Category>/<Subcategory>`."""
        target = self.emails()
        self.assertEqual(
            obslib.workdir_root(target), self.docs / "Perso/Communication/Emails"
        )

    def test_derived_files_stay_put_outside_a_recognizable_tree(self) -> None:
        loose = self.tmp / "Downloads/dump"
        loose.mkdir(parents=True)
        self.assertEqual(obslib.workdir_root(loose), loose)


# --------------------------------------------------------------------------- #
# project
# --------------------------------------------------------------------------- #


class TestProject(Fixture):
    def create(self, name: str = "acme", kind: str = "commercial") -> Path:
        (self.docs / "Pro/Projets").mkdir(parents=True, exist_ok=True)
        run(project, ["create", name, "--type", kind,
                      "--anchor", str(self.docs / "Pro/Projets"), "--apply"])
        return self.docs / "Pro/Projets" / name

    def test_create_writes_the_template_files(self) -> None:
        folder = self.create()
        for name in ("projet.md", "memory.md", "backlog.md", "commercial.md"):
            self.assertTrue((folder / name).exists(), name)

    def test_create_never_overwrites_an_existing_project(self) -> None:
        folder = self.create()
        (folder / "projet.md").write_text("# Mon contenu\n", encoding="utf-8")
        code, _ = run(project, ["create", "acme", "--type", "commercial",
                                "--anchor", str(self.docs / "Pro/Projets"), "--apply"])
        self.assertNotEqual(code, 0)
        self.assertEqual((folder / "projet.md").read_text(encoding="utf-8"), "# Mon contenu\n")

    def test_invoice_replaces_the_example_row_then_appends(self) -> None:
        folder = self.create()
        run(project, ["invoice", "acme", "--objet", "Audit", "--montant", "1200",
                      "--date", "2026-08-01", "--anchor", str(self.docs / "Pro/Projets"), "--apply"])
        body = (folder / "commercial.md").read_text(encoding="utf-8")
        self.assertIn("Audit", body)
        self.assertNotIn("<objet>", body)
        run(project, ["invoice", "acme", "--objet", "Maintenance", "--montant", "300",
                      "--date", "2026-08-15", "--anchor", str(self.docs / "Pro/Projets"), "--apply"])
        body = (folder / "commercial.md").read_text(encoding="utf-8")
        self.assertIn("Audit", body)
        self.assertIn("Maintenance", body)

    def test_export_rag_flags_template_sections_as_empty(self) -> None:
        self.create()
        _, out = run(project, ["export-rag", "acme",
                               "--anchor", str(self.docs / "Pro/Projets")])
        self.assertIn("vide", out.lower())

    def test_no_credential_is_written_to_markdown(self) -> None:
        folder = self.create()
        body = (folder / "projet.md").read_text(encoding="utf-8")
        self.assertIn("BW:", body)
        for leak in ("password", "api_key", "token:"):
            self.assertNotIn(leak, body.lower())


# --------------------------------------------------------------------------- #
# mail
# --------------------------------------------------------------------------- #


CONFIG = """\
preserve:
  senders:
    - domain: smartlockers.io
  branches:
    - Banque/
suppress:
  senders:
    - domain: klaviyo.com
exceptions:
  - address: news@klaviyo.com
    action: preserve
prune:
  - branch: Publicites/Spam/
    days: 30
phishing_brands:
  - ma-banque
"""


class TestMail(Fixture):
    def branch(self) -> Path:
        root = self.docs / "Pro/Emails"
        files = {
            "Banque/garde.md": "---\nfrom: alerte@ma-banque.fr\ndate: 2026-08-01\n---\n\nVirement.\n",
            "Publicites/Spam/vieux.md": "---\nfrom: bulk@promo.net\ndate: 2025-01-15\n---\n\nSoldes.\n",
            "Publicites/Spam/klaviyo.md": "---\nfrom: promo@klaviyo.com\ndate: 2026-07-02\n---\n\nPromo.\n",
            "Publicites/Spam/exception.md": "---\nfrom: news@klaviyo.com\ndate: 2026-08-19\n---\n\nNews.\n",
            "Clients/phish.md": "---\nfrom: \"Ma Banque\" <secure@ma-banque-verif.tk>\ndate: 2026-08-05\n---\n\nCliquez.\n",
            "Clients/traite.md": "---\nfrom: x@y.fr\ndate: 2026-08-01\nprocessed: true\n---\n\nDéjà vu.\n",
            "_drafts/brouillon.md": "brouillon\n",
            ".archive/2026-01-01/vieux.md": "archivé\n",
            "mail-sessions.log.md": "log\n",
        }
        for rel, body in files.items():
            path = root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(body, encoding="utf-8")
        (root / "mail-config.yaml").write_text(CONFIG, encoding="utf-8")
        return root

    def test_scope_excludes_archive_drafts_log_and_processed(self) -> None:
        root = self.branch()
        _, out = run(mail, ["triage", str(root)])
        self.assertIn("5 emails dans la portée", out)

    def test_suppress_archives_and_preserve_leaves_intact(self) -> None:
        root = self.branch()
        run(mail, ["triage", str(root), "--apply"])
        self.assertFalse((root / "Publicites/Spam/klaviyo.md").exists())
        self.assertTrue(list((root / ".archive").rglob("klaviyo.md")))
        self.assertNotIn("processed", (root / "Banque/garde.md").read_text(encoding="utf-8"))

    def test_exception_overrides_suppress(self) -> None:
        root = self.branch()
        run(mail, ["triage", str(root), "--apply"])
        self.assertTrue((root / "Publicites/Spam/exception.md").exists())

    def test_prune_uses_age_and_spares_the_recent(self) -> None:
        root = self.branch()
        run(mail, ["triage", str(root), "--apply"])
        self.assertFalse((root / "Publicites/Spam/vieux.md").exists())

    def test_archived_copy_is_marked_processed(self) -> None:
        root = self.branch()
        run(mail, ["triage", str(root), "--apply"])
        archived = next(iter((root / ".archive").rglob("klaviyo.md")))
        self.assertIn("processed: true", archived.read_text(encoding="utf-8"))

    def test_nothing_is_deleted(self) -> None:
        root = self.branch()
        before = sorted(p.name for p in root.rglob("*.md"))
        run(mail, ["triage", str(root), "--apply"])
        after = sorted(p.name for p in root.rglob("*.md"))
        self.assertEqual(before, after)

    def test_phishing_is_signalled_not_moved(self) -> None:
        root = self.branch()
        _, out = run(mail, ["triage", str(root), "--apply"])
        self.assertIn("ma-banque", out)
        self.assertTrue((root / "Clients/phish.md").exists())

    def test_unruled_mail_stays_and_goes_to_arbitration(self) -> None:
        root = self.branch()
        _, out = run(mail, ["triage", str(root), "--apply"])
        self.assertIn("Clients/phish.md", out)
        self.assertTrue((root / "Clients/phish.md").exists())

    def test_triage_is_idempotent(self) -> None:
        root = self.branch()
        run(mail, ["triage", str(root), "--apply"])
        state = snapshot(root)
        run(mail, ["triage", str(root), "--apply"])
        self.assertEqual(state, snapshot(root))


if __name__ == "__main__":
    unittest.main(verbosity=2)
