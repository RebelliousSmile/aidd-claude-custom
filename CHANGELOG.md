# Changelog — my-claude-marketplace

Journal au niveau du marketplace : ajout/retrait de plugins et changements transverses. Les évolutions internes à un plugin sont dans son propre `CHANGELOG.md`.

Format inspiré de [Keep a Changelog](https://keepachangelog.com/). Versionnement du marketplace en SemVer (`marketplace.json`).

## [3.3.3] - 2026-07-27

### Fixed

- **`overcode` (3.9.1)** — numérotation des actions d'`alias` réalignée sur la table de `SKILL.md` : six fichiers sur dix résolvaient sur un mauvais numéro, dont deux revendiquant tous deux « Action 06 ». Origine : un trou en `07` laissé par la suppression de `07-aiddlegacy.md` en 3.1.1, jamais comblé. Aucun contrat cassé — les actions sont désignées par nom partout. Documentation de `control` : l'autorité entre `docs/control.md` et `skills/control/` est inversée (la page porte le modèle, la skill le réalise), et une quatrième autorité est énoncée — que la skill ne réalise pas encore.
- **Dérive silencieuse d'`index.json` sur six plugins** — `design`, `sc-css`, `sc-js`, `sc-php`, `sc-python` et `sc-rust` y portaient encore la version précédant les bumps de 3.3.2, alors que `plugin.json` et `marketplace.json` étaient à jour. Aucune version n'est bumpée ici : c'est le troisième manifeste qui rattrape. La cause est structurelle — `index.json` est le seul des trois qu'aucun consommateur ne lit à l'exécution (Claude Code se sert de `marketplace.json`), donc rien ne se casse quand il ment. `alias:bump-plugin` propage bien sur les trois depuis `overcode` 3.9.0, mais un bump fait à la main y échappe.
- **`~/.claude/rules/plugins-marketplace.md`** (hors dépôt, chargé à chaque session) — décrivait la marketplace sous son ancienne racine `aidd-overlay/`, nom abandonné en 3.0.0, et listait neuf plugins dont trois inexistants (`gamedesign`, `writing`, `obsidian`) et trois manquants (`design`, `sc-css`, `sc-godot`). Il annonçait notamment la skill `dig`, retirée en 3.3.0 — d'où un diagnostic de skill « manquante » qui ne portait sur rien. Reconstruit depuis `marketplace.json`, sans versions (elles dérivent). Règle ajoutée : la marketplace étant déclarée `source: directory` sur l'arbre de travail, une installation capture **ce qui est sur le disque**, commité ou non — un numéro de version identifie une intention, jamais un contenu.
- **`aidd_docs/memory/marketplace-v3.md`** — titré « état v3.0.0 » mais décrivant un état antérieur à la v3, avec onze versions fausses. Réécrit en « état courant », sans versions, et doté de deux registres de ce qui n'existe plus : plugins supprimés ou renommés, et skills supprimées.

## [3.3.2] - 2026-07-27

Entrée écrite rétroactivement : la version a été atteinte par deux apports — le commit `81c66dd` (correctifs `sc-*`) puis le merge `cc604e2` (overcode 3.9.0) — dont aucun ne l'a rédigée.

### Added

- **`overcode` (3.9.0)** — revue DDD de la skill `control` : le modèle a été écrit d'abord, puis la skill alignée dessus. Trois autorités séparées et énoncées comme telles, les **domaines** comme nouvelle dimension (le projet déclare lesquels existent, le pivot `sc-*` déclare comment les repérer — autorité découpée par nature de connaissance, donc sans arbitrage nécessaire), deux nouvelles phases (`default` et `undetermined`), et le graphe de chaînage des six actions promu en contrat. Quatre pages `docs/` créées (`concepts`, `workflow`, `aliases`, `control`). `alias:bump-plugin` propage désormais la version sur les **trois** manifestes au lieu de deux — la divergence que ça corrige ne se voyait qu'à l'installation.

### Fixed

- **Discipline de sévérité des audits, sur cinq plugins `sc-*`** — `sc-css` (0.3.2), `sc-js` (0.13.1), `sc-php` (0.8.1), `sc-python` (0.5.3), `sc-rust` (0.4.4). Même défaut transposé à chaque stack : une dimension d'audit présupposait une propriété du monde (un conteneur DI, un hôte en `@layer`, un plancher d'interpréteur, un runtime async, un module ESM) puis sur-affirmait la sévérité quand cette propriété était fausse. Le verdict est désormais conditionné à une propriété **mesurée** de la preuve, jamais à la plateforme supposée. L'enjeu est le chaînage : `audit` et `improve/01-analyze` sont read-only mais alimentent des actions **mutantes** (`legacy/02-migrate`, `aidd-dev:implement`), donc un faux verdict devient une réécriture. Toute indécidabilité est portée dans la **sévérité** (`info`), jamais dans une note que le pipeline ignore — et « code mort » n'est plus jamais affirmé au scan statique, seulement « non référencé dans les sources scannées ». Détail par plugin dans leurs CHANGELOG respectifs.
- **`design` (2.6.1)** — titres de section et phrases du README portaient des numéros de version (`(2.4.0)`, `(2.1.0)`, « Depuis 1.1.0 : … »). Retirés : l'historique est le rôle du CHANGELOG. Même correction dans `sc-js`, dont une section s'intitulait « Migration depuis 0.3.0 ».

## [3.3.1] - 2026-07-25

### Fixed

- **`sc-php` (0.7.1)** — description du manifeste (`plugin.json` + `marketplace.json`) omettait les skills `log-analysis` et `bruno`. `log-analysis` avait été livrée le 2026-05-27 (commit `37f792f`) sans jamais toucher `plugin.json` ni le CHANGELOG du plugin — non versionnée depuis sa création. `bruno` figurait dans l'historique du CHANGELOG mais jamais dans la phrase de description. Découvert après coup, en vérifiant une suspicion de l'utilisateur sur les data pivots Eloquent/Doctrine (ceux-ci se sont avérés réels et implémentés — le vrai trou était ailleurs dans la même description).

## [3.3.0] - 2026-07-25

### Added

- **`overcode` (3.8.0)** — skill `baby` : explique, réécrit ou compare un sujet en langage simple et progressif, sans jargon non défini.
- **`sc-css` (0.3.1)** — `README.md` créé (n'en avait jamais eu) et ajouté à l'index et à la table de référence rapide du README racine ; ses six skills (`sniff`, `audit`, `improve`, `legacy`, `teach`, `design-bridge`) étaient jusqu'ici invisibles depuis la documentation du marketplace bien qu'installables.

### Removed

- **`overcode` (3.8.0)** — skill `dig` (quiz interactif /20) retirée : supplantée pour l'explication passive par le output style natif Learning (blocs ★ Insight). Sa capacité de rappel actif noté n'a pas d'équivalent.

### Fixed

- **Dérive de README vs état réellement livré**, sur quatre plugins dont le `plugin.json`/`CHANGELOG` étaient déjà à jour mais dont le `README.md` avait pris du retard :
  - `design` — la ligne `harness` ne mentionnait pas le flag `--contract` (2.6.0).
  - `obs` — les lignes `tree`, `filler` et `mail` omettaient respectivement `judge`/`destinations`, `index`/`synthesize`, et l'action `reply`.
  - `sc-js` — affirmait à tort que Svelte/SvelteKit n'étaient "pas encore" supportés ; `design-bridge` ne mentionnait pas le workflow de plateforme SPA.
  - `sc-php` — `design-bridge` ne mentionnait pas le workflow de plateforme FSE.
- **`sc-tiers` (0.2.1)** — `README.md` et `marketplace.json` affirmaient des data pivots Supabase/DynamoDB/Hasura qui n'ont jamais été implémentés (seul un pivot Firebase/Firestore existe). Fausse mention présente depuis l'entrée baseline du CHANGELOG du plugin, non corrigée pour préserver l'historique.
- **`sc-python`** — CHANGELOG comblé pour les versions `0.5.0`/`0.5.1`/`0.5.2`, bumpées sans entrée documentée. Un écart résiduel est noté dans le CHANGELOG du plugin : le commit `315a499` (2026-05-31) a ajouté du contenu après le bump `0.5.2` sans bumper à son tour — non corrigé ici, faute de version taguée à lui attribuer.

## [3.2.0] - 2026-07-22

### Added

- **Consommation cross-plugin d'un pivot `sc-*`** (`DEC-004`) — premier cas d'un pivot lu par un plugin **autre** que le sien : `sc-js/tools/testing.md` (0.10.0) est découvert **par glob** et consommé par `overcode:control` (3.3.0), qui détient le contrat (`references/pivot-contract.md`). Champs optionnels à repli documenté, titres de section alignés sur le contrat, et frontière d'autorité explicite — un pivot priorise un classement, il ne décide jamais d'un tier. Tout futur pivot `testing` (`sc-php`, `sc-python`…) s'y conforme sans modifier `control`.
- La résolution de racine du pivot accepte la **racine source** (`plugins/<plugin>/`) quand le consommateur tourne contre le dépôt marketplace — sans quoi aucun pivot n'est testable avant publication, les versions étant épinglées à l'installation.

### Fixed

- **Dérive de `marketplace.json`** — le manifeste annonçait encore `overcode` 3.1.5 et `sc-js` 0.8.0 alors que les plugins étaient publiés en 3.2.0 / 0.9.0, et la description d'`overcode` ignorait la skill `control`. Version du marketplace réalignée sur ce CHANGELOG (elle indiquait 3.0.0 pour une entrée 3.1.0 existante).

## [3.1.0] - 2026-06-13

### Added

- **Infra de test `tools/eval/`** (Node, zéro dépendance) — trois couches : `harness.mjs` (conformité structurelle d'un projet brief→output + invariants de portabilité + invariant plateau), `coverage.mjs` (chaque action *routable* a ≥1 scénario, tous plugins) et `behavioral/` (spec + rubrique LLM-juge à la demande). 4 fixtures golden + spec comportementale.
- **`writing` (1.1.0)** — boucle de review convergente + **PLATEAU** (`Δ < 1.0`), artefact `chapter-NN-scores.md`, routes de triage vers `tone-finder:improve` / `persona:train` (`references/review-loop.md`).

### Changed

- **Contrat brief resserré** : `_brief/personas/` et `_brief/output-styles/` exigent ≥3 entrées distinctes (`writing` 1.1.0 + `obsidian` 0.14.0).

### Fixed

- **`obsidian` (0.15.0)** — `rules-keeper/evals/scenarios.json` réparé (ids d'action périmés) ; dérive de version + description corrigée dans `index.json` (obsidian 0.11.0 → 0.15.0).

> `obsidian` 0.15.0 inclut aussi la formalisation de la convention `Pro/Projets` dans `tree` (`references/tree-convention.md`) — détail dans `plugins/obsidian/CHANGELOG.md`.

## [3.0.0] - 2026-06-13

### Added

- **Plugin `writing`** (1.0.0) — production éditoriale à partir d'un brief : documentation pro (`specification`, `technical-document`, `user-guide`) + craft narratif (`toc`, `write`, `tone-finder`, `persona`, `review`, `storyboard`, `upgrade`). Fusion de `doc-writer` + `rpg-writer`.
- **Plugin `game-writer`** (1.0.0) — contenu narratif jeu vidéo (bank, dialogic-draft, dialogic-review) ; remplace `gamedesign` (renommé).
- **Plugin `sc-godot`** (0.1.0) — coquille Godot/GDScript ; pendant technique de `game-writer`.
- **`obsidian`** (0.13.0) — skill `tree` (organiseur Documents/ piloté par cache) ; skill `brief` (construit `_brief/` autosuffisant) ; 8 skills JDR migrés vers domaines locaux autonomes (`R = <jeu>`, résolution via `_savoir/`) ; réf `jdr-layout.md`.

### Changed

- **Séparation des responsabilités** : `obsidian` assemble les intrants (`brief`, `forge`, `research`, `lore-extract`, `rules-keeper`, `extract-pdf`) ; `writing` produit à partir du brief — sans remonter vers `R` ni `bank.yml`.
- **`obsidian` — modèle JDR autonome (BREAKING)** : abandon de `tnn-jdr` / `~/.jdr.yaml` / variable globale `<vault>`. Savoir durable en `R/_savoir/{systeme,subsystems,univers}/{canon,mj}/` ; campagnes en `R/_campagnes/<c>/<AAAA>/<MM>/` ; résolution locale via marqueur `_savoir/`.

### Removed ⚠ BREAKING

- **Plugin `doc-writer`** — fusionné dans `writing`. Les déclencheurs `/doc-writer:*` sont inactifs.
- **Plugin `rpg-writer`** — fusionné : craft narratif → `writing`, skills JDR + assemblage intrants → `obsidian`. Les déclencheurs `/rpg-writer:*` sont inactifs.
- **Plugin `gamedesign`** — renommé `game-writer`. Les déclencheurs `/gamedesign:*` sont inactifs.
- **`obsidian`** — agents `claude-code-optimizer-jdr` et `documentation-architect-jdr` supprimés (obsolètes).

## [2.0.0] - 2026-06-11

### Added

- **Plugin `design`** (1.0.0) — entonnoir 5 verbes `define → destructure → adjust → enforce → diffuse` avec contrat 3 couches (tokens W3C · manifeste composants · charte prose), linter portable `lint-core.mjs` dérivé du contrat, 3 gates (règles génération, success_condition, pre-commit auto-armé), et pivot hybride vers `sc-php:design-bridge` / `sc-js:design-bridge`.
- **`sc-php`** (0.5.0) — skill `design-bridge` : réceptacle pivot design — linter PHP natif + block patterns WP FSE dérivés du contrat.
- **`sc-js`** (0.7.0) — skill `design-bridge` : réceptacle pivot design — règle ESLint/Biome + composant Vue 3 SFC ou React TypeScript dérivés du contrat.
- **`aidd-overlay`** (2.1.x) — skill `seo-optimize` ; alias `weeklyemail` ; endtask auto-détecte le numéro d'issue depuis 5 sources.
- **Plugin `doc-writer`** (0.1.0) — rédaction professionnelle : `user-guide`, `technical-document`, `specification`.
- **`LICENSE`** (MIT), **`CONTRIBUTING.md`** et ce **`CHANGELOG.md`** à la racine.

### Changed

- **`obsidian`** (0.10.0) — `solo-mc` enrichi (narrateur-agent, oracle agent, grille décisionnelle, substitution compagnon) ; `pc` avec questionnaire de background par genre (mapping GROG).
- **`rpg-writer`** (0.10.0) — migration vers vault layout par jeu ; pipeline canon/MJ ; extract-pdf préserve le brut.
- **`sc-python`** (0.5.2) — modèle pivot v0.5.0 (8 nouveaux pivots, catégorie AP protocol, refonte sniff).
- **`sc-js`** (0.6.8→0.7.0) — perf-vanilla : couverture img-src-dynamic + passive listeners.

### Removed ⚠ BREAKING

- **`design`** — 9 skills supprimés : `setup`, `from-reference`, `from-brief`, `wireframe`, `component`, `audit`, `diagnose`, `refactor`, `export-wordpress`. Tous les déclencheurs `/design:<skill>` correspondants sont inactifs. Voir `plugins/design/CHANGELOG.md` pour la correspondance legacy → 5 verbes.
- **Plugin `hermes`** — retiré du marketplace. La skill `solo-mc` est portée par `obsidian:solo-mc` (Claude Code).

### Fixed

- **`aidd-overlay`** (2.1.4) — endtask : auto-détection numéro d'issue depuis branche, frontmatter, commits.
- **`design`** — skill `doctor` renommé `diagnose` pour éviter la collision avec `/doctor` natif de Claude Code.
- **`sc-python`** — corrections AP protocol (ap-optimize audit v2 + v3).

## [1.0.0] - (unreleased)

### Added

- **Plugin `design`** (0.2.0) — design system mobile-first et responsive : intakes `from-reference` / `from-brief`, tokens W3C (DTCG) + adaptateurs CSS/Tailwind générés, wireframes HTML vivants, composants réutilisables à options, `audit` de conformité, `doctor` + `refactor` pour le code en production, et `export-wordpress` (`theme.json` v3 + block patterns). Règle « jamais d'émoticons » et décision du trio palette/typo/icônes en priorité.

## [1.0.0-initial]

- État initial du marketplace : `aidd-overlay`, `gamedesign`, `writing`, `sc-js`, `sc-php`, `sc-python`, `sc-rust`, `sc-tiers`, `obsidian`.
