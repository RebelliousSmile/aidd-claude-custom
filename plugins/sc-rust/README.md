# sc-rust

*Knowledge provider pour les stacks Rust (Axum, Actix-web) : détection de stack, audit, modernisation et enseignement par pivots.*

Détecte les crates du projet (`Cargo.toml`) et charge à la demande les pivots de capacité applicables. Les pivots perf/data alimentent `web-optimize` / `data-optimize` (plugin `overcode`).

## Skills

| Skill | Déclencheur | Description |
|---|---|---|
| `sniff` | `/sc-rust:sniff` | Détecte les crates depuis `Cargo.toml`, installe/met à jour uniquement les règles pertinentes |
| `audit` | `/sc-rust:audit` | Auditeur qualité Rust — détecte la stack via sniff puis délègue la revue avec les pivots applicables |
| `improve` | `/sc-rust:improve` | Analyse le code — opportunités d'idiomes Rust et de design patterns, plan d'amélioration |
| `legacy` | `/sc-rust:legacy` | Scanne le code pour patterns dépréciés / spécifiques à une édition, propose une migration |
| `log-analysis` | `/sc-rust:log-analysis` | Analyse les logs d'application Rust (local, Docker, prod SSH) — tail, parse-errors, search, summarize |
| `teach` | `/sc-rust:teach` | Enseigne le langage, l'ownership, les idiomes et les patterns de framework |

## Pivots

### Capability pivots — chargés à l'audit, non installés sur disque

| Signal de détection | Pivot |
|---|---|
| Tout projet Rust | `rust/idioms.md` |
| `pyo3` | `rust/pyo3.md` |
| `tauri` | `rust/tauri.md` |

### Pivots perf / data — installés dans `.claude/rules/07-quality/`

| Signal de détection | Pivot | Consommateur |
|---|---|---|
| `axum`, `actix-web` | `perf/axum.md` | `overcode:web-optimize` |
| `sqlx` · `diesel` · `rusqlite` | `data/sqlx.md` · `data/diesel.md` · `data/rusqlite.md` | `overcode:data-optimize` |

### Pivot de gouvernance `testing` — lu par un autre plugin

`sniff/references/capabilities/tools/testing.md` répond aux dix champs du contrat de pivot `testing` : runners, motifs de test, comptage, couverture, univers source, signaux de risque, frontière d'ancrage, pièges d'outillage, résolution de domaine, outil E2E. Il n'est ni installé sur disque ni chargé par un `paths:` — il est découvert par glob depuis le plugin qui en a besoin.

Ce que ce pivot **ne fait pas** : décider s'il faut écrire un test, ni quel niveau de preuve un cas mérite. Ses commandes et ses chiffres ont été relevés sur un crate binaire Win32 réel ; ce qui n'a pas pu être mesuré — répertoire `tests/`, doctests, outillage de couverture, code asynchrone — est signalé à l'endroit où il apparaît.

### Résumé

| Type | Où ça vit | Qui le charge | Quand |
|---|---|---|---|
| Capability pivot | Plugin uniquement | Claude Code (automatique, via `paths:`) | À chaque édition de fichier matchant |
| Perf / data pivot | `.claude/rules/07-quality/` | `web-optimize` / `data-optimize` (explicite) | Au lancement du skill |
| Pivot `testing` | Plugin uniquement | Tout consommateur du contrat de pivot (découverte par glob) | À chaque action de gouvernance de tests sur un projet Rust |

## Licence

MIT — voir [LICENSE](../../LICENSE).
