# Changelog — sc-php

## [0.10.1] — 2026-08-03

### Fixed — l'en-tête d'installation est dérivé de ce qui a été écrit

`sniff/02-install-pivots` n'avait qu'un bloc de sortie, en-tête `✅ pivots installed` compris. Une bibliothèque PHP ou un outil CLI, sans framework ni ORM, recevait donc « pivots installed » alors qu'aucun fichier n'était écrit — et le cas se rencontre d'autant plus ici que le plugin cible aussi bien des dépôts sans `composer.json` que des installations WordPress. La sortie se branche maintenant en trois cas : au moins un pivot écrit ou mis à jour · **rien à installer** (en-tête `✅ sc-php sniff — nothing to install`, verbatim) · tout déjà à jour.

## [0.10.0] — 2026-07-30

### Added — pivot `testing`, mesuré sur deux mondes PHP qui ne partagent presque rien

- **`skills/sniff/references/capabilities/tools/testing.md`** (nouveau) — quatrième implémenteur du contrat `plugins/overcode/skills/control/references/pivot-contract.md`, écrit **en anglais** comme les dix autres fichiers `capabilities/` du plugin, titres de sections repris verbatim des noms de champs, aucune table de correspondance due. Trois terrains en lecture seule, parce qu'une seule mesure aurait décrit un seul des deux mondes de cette stack : une boutique PrestaShop à neuf modules (PHP 8.4.11, PHPUnit 10.5.63, deux suites exécutées de bout en bout — 46 et 29 tests), une installation WordPress complète versionnée, et un dépôt WordPress dont la racine **est** `wp-content`.
- **L'unité de mesure n'est pas le dépôt, c'est le composant.** Mesuré : neuf modules sous `modules/`, chacun son dépôt git, son `composer.json`, son `vendor/` et son `phpunit.xml.dist` ; **aucune commande racine ne les exécute**. Une mesure lancée depuis la racine du projet rend *zéro test* sur un projet qui en porte 225. C'est la première fois qu'un pivot doit dire qu'un projet n'a pas de point d'entrée unique.
- **La couverture échoue en silence avec un code de retour 0.** Sans driver installé, `phpunit --coverage-clover` avertit, affiche `OK, but there were issues!`, **sort 0** et **n'écrit aucun fichier** — mesuré. Un consommateur qui lit le code de retour conclut au succès puis ne trouve pas le rapport. C'est le cas d'application le plus net de la clause de prérequis entrée au contrat en 4.2.0 (DEC-009) : la commande de constat est `php -m` / `extension_loaded()`, et l'absence de Xdebug ou de PCOV est une propriété de la machine, jamais un défaut du projet mesuré.
- **`phpdbg -qrr` ne fournit plus de couverture** — conseil très répandu, mesuré faux sur PHPUnit 10 : même avertissement, même code 0, aucun fichier.
- **Un `vendor/bin/phpunit` présent peut être mort.** Mesuré sur deux modules : le binaire existe et sort en `Class "PHPUnit\TextUI\Application" not found`, l'autoloader ayant été régénéré sans les dépendances de développement pendant que `vendor/phpunit/` restait sur le disque. Le constat fiable est `installed.json`, pas l'existence du fichier.
- **Un `composer.json` sans `require-dev` ne signale pas un composant sans tests** — même contre-signal que le `[dev-dependencies]` absent de `sc-rust`, mesuré ici sur un module dépouillé pour l'empaquetage qui porte 93 méthodes de test et un `phpunit.xml.dist`.
- **L'univers source WordPress est le contre-exemple du glob naïf** : 1640 fichiers `**/*.php` dont **86 appartiennent au projet** (5,2 %), le reste étant le cœur et des extensions tierces. Et le layout ne se déduit pas de la stack — deux dépôts WordPress mesurés, univers opposés, discriminant : la présence de `wp-includes/` à la racine.
- **L'E2E d'un projet PHP n'est ordinairement pas en PHP.** Mesuré sur les deux terrains web : Playwright piloté depuis `package.json`. Le champ le dit plutôt que de nommer un outil PHP qu'aucun terrain n'utilise.

## [0.9.0] — 2026-07-28

### Added — `builder-coverage` : le scan inverse

- **`actions/scripts/orphan-selectors.mjs`** (verdict `ORPHANS: N`, exit 1 si non nul). `01-scan` part du contenu en base et voit les classes utilisées sans pattern ; ce script part du CSS et liste les classes **déclarées sans aucun consommateur** dans le markup — templates, parts, patterns, rendus SSR, JS. Le cas visé est une famille CSS portée depuis une maquette dont le markup n'a jamais été écrit : le CSS est complet, personne ne le voit, et rien ne le signalait. Limite assumée et affichée plutôt que masquée par une heuristique — une classe assemblée à l'exécution (`"prefix-" . $i`) n'est pas détectée comme consommée, le script signale le fragment pour arbitrage manuel.

### Changed

- **Les titres `H1` des actions ne portent plus leur numéro** — `# Explain`, plus `# Action 01 — explain`. Le numéro vivait à trois endroits, il n'en occupe plus que deux : le nom de fichier et la table de `SKILL.md`, que le gate de cohérence du marketplace compare désormais. Changement transversal aux onze plugins, détaillé dans le journal du marketplace (3.4.0).

## [0.8.1] — 2026-07-27

### Fixed — discipline de sévérité (l'audit alimente des mutants)

Même correctif transversal que sc-css/sc-rust, transposé au PHP. `legacy/01-scan` et `improve` sont read-only mais `legacy/02-migrate` mute (écriture in-place). Correction **inline**, conditionnée à une propriété **mesurée**, jamais à une stack supposée. (Classe C — code mort indécidable — absente ici : le plugin ne prétend nulle part prouver du code mort au scan.)

- **(A) Verdict sur propriété supposée → mesurée.** Le détecteur DIP flaguait tout `new ClassName()` en présupposant un conteneur DI. Désormais : ne flaguer que l'instanciation d'un **service** (jamais un value object / DTO / exception / collection, où `new` est correct) **et** seulement si le projet **injecte déjà ailleurs** (mesuré). Sans conteneur DI, prescrire l'injection est un choix d'architecture → `info`, pas une violation (`sniff/references/capabilities/php/solid.md`, `improve/01-analyze.md`).
- **(B) Sévérité alimentant la mutation.** `02-migrate` appliquait les transformations CRITICAL/WARN après simple affichage d'un diff — or **un signal grep n'est pas une preuve et un diff n'est pas une confirmation**. Un signal *nom de fonction nu* peut viser un homonyme utilisateur, un import de namespace ou une méthode. Ajout d'une confirmation explicite par occurrence (ou par lot de même pattern) avant écriture ; doute non résolu → `Skipped (needs manual review)`, jamais réécrit (`legacy/02-migrate.md`).
- **(E) Le moteur d'analyse mal-juge les constructions qu'il recommande.** Les signaux `each(` et `split(` capturaient `$collection->each(...)` / `Str::split(...)` (Laravel/Doctrine, valides) → resserrés en `(?<![>:$\w])each\s*\(` / `split\s*\(`, jamais précédés de `->`/`::`/`$`. Et le détecteur OCP ne flague plus un `match ($enum)` exhaustif — sur un `enum` le compilateur impose l'exhaustivité, c'est la fermeture même (`legacy/01-scan.md`, `solid.md`, `improve/01-analyze.md`).

## v0.7.1 — 2026-07-25

### Fixed
- **Description du manifeste** (`plugin.json` + `marketplace.json`) — omettait les skills `log-analysis` et `bruno`. `log-analysis` (commit `37f792f`, 2026-05-27) avait été livrée sans jamais toucher `plugin.json` ni ce CHANGELOG : silencieusement non versionnée depuis sa création. `bruno` figure dans l'historique (v0.4.0) mais n'était jamais entré dans la phrase de description.

## v0.7.0 — 2026-07-25

### Reçu du pivot design (design 2.5.0 — verbe 0 `detail`)

- **`design-bridge/references/workflow-fse.md`** (nouveau) — ce pivot possède désormais le **workflow de plateforme FSE**, sous le squelette figé par `plugins/design/references/sc-pivot-contract.md § Workflow de plateforme` (cinq titres, déclaration de phase input/output/verbe, prérequis en capabilities). Il instancie les classes de cas agnostiques de `design:detail` sur un thème de blocs : phases `enforce`/`diffuse` natives + phases `off-funnel` (environnement conteneurisé, import en base, déploiement). `design:detail/02-route` l'étend à la classe quand ce pivot est installé et la stack correspond. Un workflow de plateforme est un COMMENT : il vit dans le pivot, jamais dans `design` (dec-002).
- **`design-bridge/SKILL.md`** — section « Workflow de plateforme (block theme / FSE) » + référence ajoutée.

## v0.6.0 — 2026-07-24

### Reçu du pivot design (design 2.2.0)

- **Obligation de report** (`design-bridge/SKILL.md`) — toute règle reçue en `Declared rules` est rendue au gate, réalisée ou non, au format `plugins/design/references/gate-config-schema.md § Rapport de pivot`. Cas fréquent ici : les règles de type `stored-content`. Le vocabulaire vit en base, hors du dépôt, et n'est lisible qu'après extraction — sans instance extraite la règle est `unrealized`, quel que soit l'état du code. Un `pass` y mentirait sur du contenu jamais ouvert.
- **`design-bridge/references/wordpress-lint-instances.md`** (reçu de `design`, ex-`design/skills/enforce/adapters/wordpress.md`) — réalisation des règles `stored-content` : extraction du contenu stocké en fichiers, lint, correction à la source, réécriture, re-lint.
- **`design-bridge/references/wordpress-pitfalls.md`** (reçu de `design`, ex-`design/references/wordpress-pitfalls.md`) — les pièges de plateforme appartiennent au réceptacle qui la sert, plus au cœur agnostique. Les références internes (`actions/02-render.md`, `SKILL.md`) pointent désormais sur `${CLAUDE_PLUGIN_ROOT}`.
- **`design-bridge/actions/01-realize-lint.md`** — écrit le rapport et le branche dans `gates.config.json § pivotReports` avec un `command`, au lieu d'étendre le hook pre-commit : le gate n'a qu'une commande, la même partout.

## v0.5.4 — 2026-06-26

### Changed
- `wordpress/fse-patterns.md` — carve-outs affinés après audit réel sur un thème bloc : (1) **formulaires** — WP core n'a pas de bloc form natif, donc `<form>`/`<input>`/`<select>` en HTML brut est légitime ; ne lever que la copie à fort churn (label submit, phrase de consentement/intro). (2) **Patterns `Inserter: no`** (showcases design-system, previews) — non édités par le client, exemptés de la règle tout-natif ; la règle se limite aux patterns insérables et porteurs de contenu. (3) **Nuance grammaire** — un `wp:list` à `<li>` nus (sans `wp:list-item`) est une **déprécation core auto-migrée**, pas un « invalid content » : nit de cohérence, pas une erreur.

## v0.5.3 — 2026-06-26

### Added
- Capability pivot `wordpress/fse-patterns.md` — conventions d'authoring des **block patterns FSE statiques** (`patterns/*.php`), framées en critères d'audit : texte client-éditable en blocs natifs (jamais piégé dans `wp:html`), neutralisation de l'injection de layout WP au passage en natif (`is-layout-flex:center`, `block-gap` ; bouton stylé sur `.wp-block-button__link`), CSS de bloc aussi en `add_editor_style()` (WYSIWYG éditeur), en-têtes complets + catégories enregistrées, slug ↔ nom de fichier sans doublon, grammaire de blocs valide. Scope = correction d'écriture + éditabilité, distinct du vocabulaire design (`design-bridge`) et des blocs SSR (`wordpress/ssr.md`). Note le pendant déterministe (linter de patterns en pre-commit, réalisé via `design:enforce` → `sc-php:design-bridge`).
- `sniff/01-scan.md` : Step 4c — détection d'un thème bloc (`theme.json`) avec dossier `patterns/` → émet le pivot ; câblé en Step 5a + exemple de manifeste WordPress (block theme).
- `audit/01-audit.md` : `wordpress/fse-patterns.md` ajouté à la structure de critères chargés à l'audit.

## v0.5.2 — 2026-06-19

### Added
- Capability pivot `wordpress/ssr.md` — conventions d'authoring de blocs dynamiques (SSR `render_callback`/`render.php`), framées en critères d'audit : attributs de bloc additifs (ne pas casser les insertions sérialisées), `wp_kses_post` vs `esc_html`/echo brut pour le HTML inline dynamique, agrégats/compteurs calculés côté serveur (pas en dur, garde N+1), édition de la source `blocks/` vs build `build/` régénéré, et navigation SSR (liens + routes réelles) vs show/hide JS. Distinct du pivot perf (`perf/wordpress.md`) et de `design-bridge` (markup/design).
- `sniff/01-scan.md` : pivot câblé en Step 5a (capability pivots, condition « WordPress détecté ») + exemple de manifeste WordPress.
- `audit/01-audit.md` : `wordpress/ssr.md` ajouté à la structure de critères chargés à l'audit.

## v0.5.1 — 2026-06-16

### Added
- `design-bridge/SKILL.md` : section "Cascade CSS : presets `has-*-font-size` et `!important`" — routes (remove-override, counter-`!important`, réalignement `theme.json`). Contenu déplacé depuis `design/enforce/adapters/wordpress.md` : `design` doit rester stack-agnostique.

## v0.4.8 — 2026-05-29

### Changed
- `sniff/01-scan.md`: refactorise la readiness des skills — supprime la section `Skills support` séparée (systématiquement omise en 7 passes) et intègre les lignes `→ /skill : STATUS` directement dans chaque sous-bloc du Pivot manifeste (après capability pivots, perf pivots, data pivots). Supprime Step 8 et la closing gate.

## v0.4.7 — 2026-05-29

### Fixed
- `sniff/01-scan.md`: ajoute une closing gate avant `→ Proceed` — le modèle doit explicitement vérifier la présence du bloc `Skills support` et l'écrire s'il est absent.

## v0.4.6 — 2026-05-29

### Fixed
- `sniff/01-scan.md`: déplace `Skills support` après `Gaps`, en dernière position avant `→ Proceed` — le modèle sautait la section quand elle était intercalée entre deux sections qu'il génère naturellement.

## v0.4.5 — 2026-05-29

### Fixed
- `sniff/01-scan.md` Step 8: ajoute deux exemples concrets (vanilla PHP et Laravel+Eloquent) pour la section `Skills support` — le modèle sautait la section quand tous les pivots étaient NOT-APPLICABLE, faute d'exemple couvrant ce cas.

## v0.4.4 — 2026-05-29

### Fixed
- `sniff/01-scan.md`: ajoute Step 8 comme étape de traitement explicite pour la section `Skills support` — le modèle l'omettait car elle n'apparaissait que dans le template de sortie, jamais dans le processus.

## v0.4.3 — 2026-05-29

### Fixed
- `sniff/01-scan.md`: déplace la contrainte de format plain-text en tête du fichier, avant le processus, pour éviter que le modèle ne choisisse les tables markdown avant d'atteindre la section Output.
- `sniff/SKILL.md`: ajoute l'interdiction des tables markdown dans les règles transversales.

## v0.4.2 — 2026-05-29

### Added
- README.md — per-plugin documentation covering all six skills and their pivot model.

### Changed
- `improve` now loads capability pivots (`solid.md`, `eloquent.md`, `doctrine.md`) during analysis to surface stack-specific anti-patterns.

### Fixed
- `sniff/01-scan.md` output constraints: prohibit markdown tables, enforce plain-text format, mark **Skills support** section as mandatory.

## v0.4.0 — 2026-05-28

### Breaking changes
- Removed `setup` skill. Use `/sc-php:sniff` instead; it detects the stack and installs only the applicable pivots.
- Renamed sniff action `sync` to `install-pivots` (aligns with sc-js v0.4.0).

### Added
- New `/sc-php:audit` skill — delegates PHP code review to `aidd-dev:reviewer` using capability pivots as criteria.
- Two-tier pivot model: capability pivots (`php/solid.md`, `testing/bruno.md`) loaded at audit time; perf/data pivots installed to `.claude/rules/07-quality/`.
- References resolved via `${CLAUDE_PLUGIN_ROOT}` at runtime (cross-plugin convention).

### Changed
- `bruno` skill conventions moved to the sniff capability pivot store; `bruno/SKILL.md` updated to point to the new location.
