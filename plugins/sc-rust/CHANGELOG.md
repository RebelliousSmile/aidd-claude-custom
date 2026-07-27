# Changelog — sc-rust

> Baseline établie le 2026-05-29 à partir de l'état courant ; transitions récentes reprises de l'historique git. Détail antérieur : `git log -- plugins/sc-rust`.

## [0.4.4] — 2026-07-27

### Fixed — discipline de sévérité (l'audit alimente des mutants)

Même correctif transversal que sc-css, transposé au Rust : chaque signal présupposait une propriété du monde puis sur-affirmait la sévérité quand elle était fausse. `audit`/`improve`/`legacy/01-scan` sont read-only mais alimentent `legacy/02-migrate` (mutant, écriture in-place) — un faux verdict devient une mutation destructrice. Correction **inline**, conditionnée à une propriété **mesurée** (signature de fonction, `Cargo.toml`, attribut d'enum), jamais à une stack supposée.

- **(A) Verdict sur propriété supposée → mesurée.** Les règles async/erreurs typées ne nomment plus `tokio`/`thiserror`/`anyhow` par défaut : elles ne s'appliquent qu'aux crates **déclarées dans `Cargo.toml`** ; le défaut runtime-agnostique reste à gauche de la flèche, les noms de crates à droite sont illustratifs (`improve/01-analyze.md`, `sniff/references/capabilities/rust/idioms.md`).
- **(B) Sévérité alimentant la mutation — la seule classe qui casse pour de vrai.** `Arc<Mutex<T>>` écrit une seule fois au démarrage est une propriété **runtime**, absente du scan statique → `info` question, jamais un finding qui pilote le retrait du lock (mauvaise supposition = *data race que le compilateur ne rattrape pas*, contrairement aux fixes async qui sont grep-prouvables et vérifiés à la compilation) (`improve/01-analyze.md § Concurrency`).
- **(C) « Code mort » indécidable au scan statique.** `extern "C"` (souvent un export FFI/cdylib sans appelant intra-crate) et `extern crate` ne sont plus « à retirer » : émission de « non-référencé dans les sources scannées — vérifier l'absence de consommateur FFI/cdylib avant retrait » (`legacy/01-scan.md`).
- **(E) Le moteur d'analyse mal-juge les constructions qu'il recommande.** `\.unwrap\(\)` est un **signal, pas un verdict** : défaut seulement si la fonction retourne `Result`/`Option` **et** l'appel est réellement faillible ; exemption des cas idiomatiques-infaillibles (`write!` vers `String`, regex depuis `const`, `Mutex::lock` poison-only) → `warning`, jamais `HIGH`. `match err { _ => … }` : n'enjoindre d'énumérer les variantes **que si l'enum n'est pas `#[non_exhaustive]`** (`io::Error`/`sqlx::Error`/`rusqlite::Error` exigent le `_` — le retirer produit du code qui ne compile pas) (`improve/01-analyze.md § Error handling`, `legacy/01-scan.md`, `idioms.md`).

## [0.4.3] — 2026-05-29 (baseline)

Knowledge provider Rust (Axum, Actix-web). Skills : `sniff`, `audit`, `improve`, `legacy`, `log-analysis`, `teach`.

### Added
- Capability pivot **Tauri** (IPC, state, async, sécurité, chemins) — bump 0.4.2 → 0.4.3.
- `improve` : Step 1.5 — chargement des capability pivots pour les anti-patterns spécifiques à la stack.

## [0.4.1]
- `legacy` : ajout de `references/` (patterns dépréciés / spécifiques à une édition).

## [0.4.0]
- Alignement sur le modèle sc-php v0.4.0 : sniff à deux niveaux (pivot model), skill `audit` déléguant la revue, evals. Bump 0.3.0 → 0.4.0.

## Antérieur
- Voir `git log -- plugins/sc-rust` pour l'historique complet.
