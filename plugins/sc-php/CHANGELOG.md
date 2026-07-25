# Changelog — sc-php

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
