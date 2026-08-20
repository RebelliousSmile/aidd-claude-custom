# Changelog — pdf

## [0.1.0] — 2026-08-20

### Added

- Plugin créé par extraction de `obs:extract-pdf`. Le skill est déplacé tel quel (actions, prompts, scripts, evals, agent) ; `references/domain-layout.md`, `references/bank-yml.md` et `references/host-portability.md` sont copiés depuis `obs` pour que les deux plugins restent installables indépendamment.
- Références repointées : `OBS_PLUGIN_ROOT` → `PDF_PLUGIN_ROOT`, `obs:extract-pdf` → `pdf:extract-pdf`, et les gloses « ancre `obs:tree` » remplacées par « ancre `Perso`/`Pro` » — le mécanisme est décrit dans `domain-layout.md` et ne dépend plus du plugin `obs`.

### Known issues

- `skills/extract-pdf/SKILL.md`, `actions/03-distribute.md` et `evals/extract-pdf-scenarios.md` renvoient encore à `references/jdr-layout.md`, absent depuis le retrait du plugin `ttrpg`. Référence morte héritée, non corrigée ici.
