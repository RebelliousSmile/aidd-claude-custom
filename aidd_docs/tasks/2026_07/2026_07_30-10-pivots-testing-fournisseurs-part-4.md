---
type: plan
statut: livre
parent: 2026_07_30-10-pivots-testing-fournisseurs-master.md
part: 4
objective: "Ecrire le pivot testing de sc-rust et, ce faisant, mettre a l'epreuve les trois hypotheses du contrat que Rust contredit"
success_condition: "test -f plugins/sc-rust/skills/sniff/references/capabilities/tools/testing.md"
iteration: 0
created_at: 2026-07-30T13:30:51Z
depends_on: [2]
---

# Part 4 — Pivot `sc-rust`, et mise a l'epreuve du contrat

## Feature

`sc-rust` (0.4.5) porte 3 dossiers `capabilities/` et 7 fichiers, sans `testing.md`. Ce pivot n'a pas seulement une valeur de couverture : c'est le **premier cas qui contredit le contrat**, ecrit jusqu'ici sur des hypotheses JS.

**Trois hypotheses a l'epreuve.**

1. **`Test file glob` suppose que les tests vivent dans des fichiers dedies.** En Rust, les tests unitaires vivent dans le fichier source lui-meme, sous `#[cfg(test)] mod tests`. Un glob de fichiers ne les voit pas — et pire, il les compterait comme *fichier de production non teste*. Seuls les tests d'integration (`tests/*.rs`) et les doctests sont dans des fichiers dedies.
2. **`Coverage command` suppose un reporter fourni par l'outillage de test.** `cargo test` n'en produit aucun : la couverture passe par un outil **tiers** (`cargo-tarpaulin`, `cargo-llvm-cov`), qui peut ne pas etre installe. Le champ doit dire quoi faire quand l'outil est absent — ce qui n'est pas le meme cas que « champ absent ».
3. **`Anchor boundary` suppose un runtime navigateur.** Ce que le contrat donne en exemple (defaut de rendu qu'un vrai navigateur applique, mismatch d'hydratation) n'existe pas ici. La frontiere reelle d'un binaire Rust, c'est le processus lance, le socket ouvert, le fichier ecrit sur un vrai systeme de fichiers.

Le contrat prevoit qu'un champ introuvable soit **absent** avec son repli. Il ne prevoit pas qu'un champ soit **mal pose** pour une stack. C'est cette distinction que cette part doit trancher.

## Projection d'architecture

**Cree**
- `plugins/sc-rust/skills/sniff/references/capabilities/tools/testing.md`

**Modifie**
- `plugins/overcode/skills/control/references/pivot-contract.md` — **seulement si une hypothese est refutee** (amendement du champ concerne, pas reecriture)
- `plugins/overcode/docs/control.md` + ADR — si amendement, meme chaine que la part 1 (DEC-006)
- `plugins/sc-rust/CHANGELOG.md`, `.claude-plugin/marketplace.json` — `sc-rust` 0.4.5 → **0.5.0**
- `plugins/overcode/CHANGELOG.md` + bump si amendement du contrat

**Supprime** — rien.

## Traitement propose des trois hypotheses

Aucun n'est acquis : chacun est une **proposition a valider a l'ecriture**, pas une conclusion.

1. *Test file glob* → le champ rend **deux motifs de nature differente** : un glob de fichiers (`tests/**/*.rs`) et un motif intra-fichier (`#[cfg(test)]`). Si le contrat n'admet qu'un glob, il est amende pour admettre un motif de contenu. **Consequence a ne pas rater** : *Source glob & exclusions* et *Test file glob* deviennent **non disjoints** — un meme fichier est source et test. Le contrat suppose implicitement qu'ils le sont.
2. *Coverage command* → le champ nomme l'outil tiers, la commande qui produit un rapport machine-lisible par fichier, **et** la detection de son absence. Un outil absent n'est pas un champ absent : le champ existe et dit ce qui manque. Si le contrat ne distingue pas les deux, l'ajouter.
3. *Anchor boundary* → reecrit la frontiere en termes de processus, socket et systeme de fichiers reels. Nommer ce qui **n'ancre pas** malgre l'apparence : `#[tokio::test]` sur un runtime de test, un `TempDir`, un serveur monte in-process. Rappel contrat:24 : le champ **positionne** la frontiere, il ne dit **jamais** quelle preuve un cas merite.

## Fixture

**Aucune identifiee.** C'est l'objet de l'arbitrage A3 du master. Sans projet Rust reel, ce pivot est ecrit sur documentation et non sur mesure — et un pivot faux est pire qu'un pivot absent, puisque le contrat prevoit l'absence. Trois issues : fournir une fixture, marquer chaque champ non verifie comme tel, ou ne livrer que les champs verifiables.

## Terrain mesure (arbitrage A3 : `winfxstart`)

`C:\Users\fxgui\Documents\Perso\Projects\winfxstart\_code` — crate binaire natif Win32 (`tao` 0.26, `windows` 0.52, `image` 0.25), READ-ONLY, arbre `git status --porcelain` vide avant et apres mesure. Toolchain `cargo 1.93.0` / `rustc 1.93.0`. Compilation des tests hors depot (`CARGO_TARGET_DIR` pointe sur le scratchpad).

| Mesure | Valeur |
|---|---|
| Fichiers `src/**/*.rs` | 17 |
| Blocs `#[cfg(test)]` | 14, repartis sur **12 des 17** fichiers source |
| Fonctions `#[test]` | 122 |
| Repertoire `tests/` a la racine du crate | **absent** |
| Doctests (` ``` ` en `///`) | **0** |
| Cibles de test compilees | **une seule** — `unittests src\main.rs` |
| `cargo test -- --list` | `122 tests, 0 benchmarks` |
| `[dev-dependencies]` dans `Cargo.toml` | **aucune section** |
| `cargo-tarpaulin` / `cargo-llvm-cov` / `cargo-nextest` | **absents des trois** ; `cargo llvm-cov --version` → `error: no such command: llvm-cov` |

Second point de comparaison, mesure en part 1 : `choix-narratifs/_code/engine` — 64 fonctions `#[test]`, dont 18 en `#[cfg(test)]` intra-source, **plus** des `tests/*.rs`. Le cas mixte existe donc aussi ; `winfxstart` en est la forme pure.

## Phases

### Phase 1 — Confronter les trois hypotheses au contrat ✅

#### Hypothese 1 — `Test file glob` → **pivot + amendement**

Le champ lui-meme n'est pas mal pose : il reste repondable (`src/**/*.rs`, `tests/**/*.rs`), et `Test-count command` offre deja une sortie exacte que le glob n'a pas a fournir (`cargo test -- --list`, 122 sur le terrain). Ce qui est mal pose, c'est une hypothese **implicite et jamais ecrite** : que `Test file glob` et `Source glob & exclusions` designent des populations **disjointes**.

Mesure : sur `winfxstart`, tout fichier de test est un fichier source. Consequence sur le consommateur, localisee : `actions/04-strengthen.md:63` replie sur « un passage statique, **mappant les modules source aux fichiers de test via le glob du pivot** et signalant les modules qu'aucun test ne reference ». Sur cette stack le mapping est **degenere** — chaque module se reference lui-meme — et le classement produit est faux **en silence**, ce qui est exactement le mode de defaillance que le contrat combat ailleurs (« an under-enumeration reads exactly like a clean population », `pivot-contract.md:17`).

Amendement, formule pour toute stack ou le test cohabite avec la source dans un meme fichier (Rust `#[cfg(test)]`, doctests Python, tout equivalent) : la disjonction n'est pas garantie ; **quand elle ne tient pas, le pivot le declare et nomme l'unite reelle de separation** (ici un bloc annote a l'interieur du fichier, pas le fichier) ; le consommateur en tire que le mapping statique fichier-a-fichier perd son pouvoir discriminant sur cette stack et doit le dire plutot que de rendre un classement.

Retroactivite : **nulle**. La declaration n'est due que lorsque la disjonction ne tient pas ; `sc-js` (`**/*.{test,spec}.{js,ts}`) et `sc-python` (`test_*.py`, `tests/`) restent conformes sans etre touches.

#### Hypothese 2 — `Coverage command` → **pivot + amendement**

Le contrat traite l'absence du **champ** (`pivot-contract.md:37` : « When absent, the fallback is a static source-to-test mapping, stated as such »). Il ne traite pas l'absence de l'**outil** que le champ nomme. Cote consommateur le chemin existe deja a moitie — `04-strengthen.md:63` couvre « or none configured in the project », `05-stats.md:77` rend `not measurable - no coverage report, so no denominator` — mais rien ne dit qu'une commande qui echoue **faute d'outillage** n'est pas un echec du projet mesure.

Ce n'est pas propre a Rust : `pytest --cov` exige `pytest-cov`, `vitest --coverage` exige `@vitest/coverage-v8`. Rust ne fait que rendre le cas flagrant — `cargo test` n'embarque aucun reporter, et le terrain n'a ni les trois outils ni meme de section `[dev-dependencies]`.

Partage des roles, qui decide de la formulation : savoir si un outil est **installe** est une propriete de la machine, qu'un pivot ne peut pas connaitre ; savoir **de quel outil un champ depend et par quelle commande le constater** est une connaissance de stack, donc exactement son role. Amendement en deux moities :

- **Regle generale du contrat, valable pour tout champ dont la reponse est une commande** : un prerequis constate absent vaut **champ absent pour ce run** — le repli documente du champ s'applique, enonce comme tel, et l'echec de la commande n'est jamais rendu comme un defaut du projet.
- **Obligation du pivot** : quand la reponse d'un champ est une commande dependant d'un outil que la toolchain de base ne fournit pas, le pivot **nomme ce prerequis et la commande qui en constate la presence**.

Retroactivite : **reelle**. `sc-js:27` cite `@vitest/coverage-v8` dans une parenthese decrivant le projet mesure, `sc-python:45` nomme `pytest-cov` sans commande de constat — aucun des deux ne satisfait la seconde moitie. Les deux sont repris en phase 2 (une clause de detection chacun) et rebumpes ; le contrat ne fige pas avant.

#### Hypothese 3 — `Anchor boundary` → **pivot seul, aucun amendement**

L'hypothese telle que posee dans le plan est **infirmee** : le contrat ne suppose pas de runtime navigateur. Sa definition est deja stack-agnostique — « the product's real public boundary » contre « staying in process » (`pivot-contract.md:39`) — et le navigateur n'y figure qu'en exemple parenthetique. Cote consommateur, `references/decision-matrix.md:66` enonce **explicitement** l'inverse de l'hypothese : « **Anchored does not mean "in a browser."** The requirement is independence from the source of the error, not a specific tool — which is what lets the matrix apply to a stack with no e2e runner at all ». La table generique (`:59-64`) illustre quatre stacks (web, API, CLI, bibliotheque) sans pretendre les epuiser.

Un binaire natif a interface graphique n'y figure pas, et n'a pas a y figurer : le champ existe precisement pour que le pivot **positionne** la frontiere dans les termes concrets de sa stack. Le pivot la nomme donc — processus lance, fenetre et registre reels, systeme de fichiers reel — et nomme ce qui **n'ancre pas** malgre l'apparence. Aucune clause du contrat ne resiste a cet exercice, donc rien a amender.

- **Critere d'acceptation** : ✅ trois decisions ecrites avec leur motif, dont une qui infirme l'hypothese du plan.

### Phase 2 — Amendement du contrat ✅
- [x] `docs/control.md` § *Le pivot* — deux puces ajoutees (prerequis absent = champ absent ; source et test non garanties disjointes)
- [x] `pivot-contract.md` — clause de non-disjonction sur *Test file glob*, renvoi sur *Coverage command*, nouvelle section `## Prerequisites` avant `## Absence`, et l:3 rendue non perissable (elle nommait `sc-js`/`sc-python`, elle renvoie desormais a l'arbre)
- [x] ADR **DEC-009** — `aidd_docs/internal/decisions/009-what-a-pivot-field-assumes-silently.md`, antecedents DEC-006 et DEC-008, section *Compatibility* qui separe les deux regles par leur retroactivite
- [x] Consommateurs alignes : `04-strengthen.md:63` (la passe statique n'est pas executee quand elle ne discrimine pas) et `05-stats.md` (variante `density` nommant le prerequis absent)
- [x] Retroactivite : regle 1 nulle (declaration due seulement si la disjonction ne tient pas) ; regle 2 reelle → `sc-js` 0.15.1 et `sc-python` 0.6.1 repris **avant** que le contrat ne fige
- **Critere d'acceptation** : ✅ aucun pivot deja livre ne devient non conforme sans etre repris — les deux le sont dans ce lot.

### Phase 3 — Redaction du pivot ✅
- [x] 10 sections, titres anglais verbatim, corps francais ; **aucune table de correspondance due** (aucun titre ne diverge)
- [x] Frontmatter vide, comme les deux pivots livres — un `paths:` le ferait auto-charger a chaque edition `.rs`, or il decrit une suite, pas une famille de fichiers
- [x] Non verifie marque a l'endroit ou il apparait : commandes de couverture (aucun des trois outils installe), `tests/`, doctests, `#[tokio::test]`, `[features]`
- **Critere d'acceptation** : ✅ lisible seul ; les commandes de couverture portent leur marquage de non-execution.

### Phase 4 — Version ✅
- [x] `sc-rust` 0.4.5 → **0.5.0** · `overcode` 4.1.0 → **4.2.0** (le contrat a bouge, et 4.1.0 est deja commitee) · `sc-js` 0.15.0 → **0.15.1** · `sc-python` 0.6.0 → **0.6.1** · marketplace 3.8.0 → **3.9.0**
- [x] `plugin.json` + `marketplace.json` + CHANGELOG de chaque plugin + CHANGELOG racine, meme lot que le contenu
- **Critere d'acceptation** : arbre propre — a verifier au commit (non commite : la regle « ne pas committer sans demande » tient).

## Risques

| Risque | Mitigation |
|---|---|
| Pivot ecrit sans terrain | A3 ; a defaut, marquage explicite des champs non verifies |
| Amender le contrat sur un seul cas | Formuler l'amendement en termes de stack en general, pas « pour Rust » |
| L'amendement casse `sc-js`/`sc-python` deja livres | Phase 2 controle la retroactivite avant de figer |
| Source et test cessent d'etre disjoints, en silence | Enonce explicitement en phase 1, hypothese 1 |

## Log

| Date | Evenement |
|---|---|
| 2026-07-30 | Cree |
| 2026-07-30 | Terrain arbitre (A3) : `winfxstart`, crate binaire Win32, mesure READ-ONLY, arbre propre avant/apres |
| 2026-07-30 | Phase 1 — 3 hypotheses tranchees : H1 et H2 en pivot + amendement, **H3 infirmee** (le contrat traite deja le cas, `decision-matrix.md:66`) |
| 2026-07-30 | Phase 2 — DEC-009 ecrite, contrat + `docs/control.md` + 2 consommateurs amendes, `sc-js`/`sc-python` repris pour la regle retroactive |
| 2026-07-30 | Phase 3 — pivot `sc-rust` livre (10 champs, mesures reelles, non-verifie marque) + sections *Pivots* du README |
| 2026-07-30 | Phase 4 — 4 bumps de plugin + marketplace 3.9.0, CHANGELOGs ecrits. Livre, non commite. |
