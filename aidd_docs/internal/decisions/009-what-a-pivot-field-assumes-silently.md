# Decision: ce qu'un champ de pivot suppose sans le dire — disjonction source/test, et outil présent

| Field   | Value |
|---------|-------|
| ID      | DEC-009 |
| Date    | 2026-07-30 |
| Feature | `overcode:control` — contrat de pivot `testing`, hypothèses implicites des champs |
| Status  | Accepted |
| Antécédents | **DEC-006** — l'autorité d'un pivot se donne champ par champ ; la présente décision n'en étend aucune, elle rend explicites deux suppositions que des champs faisaient en silence. **DEC-008** — le pivot suit le fichier ; la non-disjonction ci-dessous est une seconde façon dont une population de tests échappe à un glob, la première étant l'appartenance à une autre stack |

## Context

Le contrat a été écrit sur deux stacks qui se ressemblent. `sc-js` et `sc-python` séparent tous deux les tests dans des fichiers dédiés (`**/*.spec.ts`, `test_*.py`) et exposent tous deux un reporter de couverture par un paquet d'usage courant. Rien dans les champs ne dépendait de ces deux propriétés — mais rien ne les énonçait non plus, et deux consommateurs s'appuyaient dessus.

Terrain de mesure : `winfxstart/_code`, crate binaire Win32, en lecture seule, `cargo 1.93.0` / `rustc 1.93.0`.

| Mesure | Valeur |
|---|---|
| Fichiers `src/**/*.rs` | 17 |
| Fonctions `#[test]` | **122**, dans 14 blocs `#[cfg(test)]`, sur **12 des 17** fichiers source |
| Répertoire `tests/`, doctests | **aucun des deux** |
| Cibles de test compilées | une seule — `unittests src\main.rs` |
| `cargo test -- --list` | `122 tests, 0 benchmarks` |
| `cargo-tarpaulin` / `cargo-llvm-cov` / `cargo-nextest` | absents des trois ; `cargo llvm-cov --version` → `error: no such command: llvm-cov` |
| `[dev-dependencies]` | section absente du `Cargo.toml` |

Ce n'est pas un cas limite : c'est la forme la plus courante d'un crate Rust. Le second terrain mesuré, `choix-narratifs/_code/engine`, en est la forme mixte — 64 `#[test]`, dont 18 intra-source, **plus** des `tests/*.rs`.

**Ce que ces mesures cassent.** Un glob de fichiers de test rend, sur ce dépôt, **zéro test et 17 fichiers de production non testés**, sur un crate qui en porte 122. Et le repli documenté du champ *Coverage command* — « a static source-to-test mapping » (`04-strengthen.md:63`, « mapping source modules to test files via the pivot glob ») — devient dégénéré : chaque module se référence lui-même, donc le passage statique signale soit rien, soit tout.

## Decision

Deux règles, formulées pour toute stack, aucune ne parlant de Rust.

### 1. Les populations *source* et *test* ne sont pas garanties disjointes

Le contrat ne l'a jamais énoncé, et deux clauses le supposaient. **Quand la disjonction ne tient pas, le pivot le déclare sous *Test file glob* et nomme l'unité réelle de séparation** — le construit intra-fichier dans lequel un test vit réellement, le fichier ayant cessé d'être cette unité.

Côté consommateur : le repli statique fichier-à-fichier **ne discrimine pas** sur une telle stack et n'est pas exécuté à la place. La stack est rapportée comme non classable par mapping statique, l'unité déclarée nommée, et les autres stacks classées normalement. Un classement grossier reste un classement ; un classement dégénéré est une fabrication.

### 2. Un prérequis constaté absent vaut champ absent pour ce run

Un champ dont la réponse est une **commande** porte une dépendance que le pivot ne peut pas résoudre : qu'un outil soit installé est une propriété de la machine, pas de la stack. Le partage suit cette frontière :

- **Le pivot** nomme le prérequis et la commande qui en constate la présence, quand le champ dépend d'un outil que la toolchain de base ne fournit pas. Savoir *de quoi* un champ dépend est du savoir de stack.
- **Le consommateur** applique le repli documenté du champ, en le disant, et ne rapporte **jamais** l'échec de la commande comme un défaut du projet mesuré.

La règle vaut pour tout champ répondu par une commande, pas seulement pour la couverture.

## Rationale

**Pourquoi pas « le champ est mal posé pour cette stack ».** C'était l'issue que la part 4 gardait ouverte. Elle est écartée sur les deux champs : *Test file glob* reste répondable en Rust, et `Test-count command` y donne même une réponse **exacte** que le glob n'a jamais promise (`cargo test -- --list`, 122). *Coverage command* reste répondable aussi — la commande existe, elle nomme un outil tiers. Aucun des deux champs ne demande à être reformulé ; ce qui manquait était l'énoncé de ce qu'ils supposaient. Un champ mal posé se retire ou se réécrit ; une supposition tacite s'écrit.

**Pourquoi le pivot porte la moitié « prérequis ».** L'alternative était de laisser le consommateur déduire l'absence de l'échec de la commande. Un `error: no such command` et un échec de compilation sortent tous deux en non-zéro ; distinguer les deux par le texte de l'erreur, c'est faire du consommateur un parseur des messages de chaque outillage. Le pivot connaît déjà l'outil, il connaît donc la commande qui le constate — le coût est d'une ligne par pivot et il tombe du bon côté.

**Pourquoi une distinction plutôt qu'un simple repli.** Le repli existait déjà et se déclenchait au bon moment ; ce qui manquait est le **motif rendu**. `05-stats` routait toute densité non mesurable vers `03-configure`, c'est-à-dire vers le câblage du projet. Sur une machine sans outil de couverture, ce projet n'a rien à câbler, et la ligne envoyait corriger ce qui n'était pas cassé.

### Ce que la décision ne fait pas

Elle ne donne aucune autorité nouvelle à un pivot : les deux clauses ajoutées sont **déclaratives**, elles décrivent une propriété de la stack. La borne de DEC-007 tient — le pivot ne classe toujours pas — et celle de DEC-006 aussi : chaque clause est bornée à son champ, et la seconde énonce explicitement quelle moitié le pivot **ne peut pas** connaître.

**L'hypothèse infirmée.** La part 4 en posait une troisième : *Anchor boundary* supposerait un runtime navigateur. Vérification faite, non — sa définition oppose « the product's real public boundary » à « staying in process », et `decision-matrix.md:66` énonce déjà **« Anchored does not mean "in a browser." The requirement is independence from the source of the error, not a specific tool »**. Le champ existe précisément pour qu'un pivot y positionne la frontière dans ses termes concrets. Rien à amender ; l'hypothèse est consignée comme réfutée plutôt que passée sous silence.

## Compatibility

**Additif sur la règle 1, contraignant sur la règle 2.**

- Règle 1 : la déclaration n'est due que lorsque la disjonction ne tient pas. `sc-js` et `sc-python` séparent leurs populations et restent conformes sans être touchés.
- Règle 2 : **rétroactive**. `sc-js` › *Coverage command* citait `@vitest/coverage-v8` dans une parenthèse décrivant le projet mesuré ; `sc-python` nommait `pytest-cov` sans commande de constat. Aucun des deux ne satisfaisait la clause. Les deux sont repris dans le même lot que l'amendement — le contrat ne fige pas avant.

Aucun champ n'est renommé ni retiré, aucun pivot ne devient illisible. DEC-004 §5 qualifie de majeur ce qui rend un pivot existant illisible ; ici deux pivots reçoivent une ligne chacun. D'où `overcode` en **mineure**.

## Consequences

- `docs/control.md` › *Le pivot* : deux puces ajoutées, sœurs de « un champ introuvable est absent ».
- `references/pivot-contract.md` : *Test file glob* porte la clause de non-disjonction ; *Coverage command* renvoie aux prérequis et au repli dégénéré ; section ***Prerequisites*** ajoutée.
- `actions/04-strengthen.md` : le repli statique reconnaît le prérequis absent, et refuse de tourner là où il ne discrimine pas.
- `actions/05-stats.md` : `density` gagne une variante *outillage absent de la machine*, qui ne route pas vers `03-configure`.
- `sc-js` et `sc-python` : une clause de détection de prérequis chacun.
- **Deux illustrations périmées retirées du contrat au passage** — « `sc-js` and `sc-python` ship one today » et « the only `testing` pivot the marketplace currently ships ». C'est la troisième fois que ce document acquiert un état du monde qui se périme ; le paragraphe qui interdisait la pratique la commettait lui-même.
