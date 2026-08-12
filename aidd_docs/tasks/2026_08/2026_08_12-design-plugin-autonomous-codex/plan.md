---
name: design-plugin-autonomous-codex
status: implemented
---

# Refonte du plugin design

Rendre les sept skills `design` compatibles Codex, autonomes pour les usages précis et composables pour un cycle complet, tout en préservant le contrat 2.x et les interfaces publiques.

## Phases

1. Packaging Codex portable et prérequis AIDD — `phase-1.md`
2. Entrées autonomes des sept skills — `phase-2.md`
3. Hiérarchie P0/P1/P2 des contrôles — `phase-3.md`
4. Tests comportementaux et validation finale — `phase-4.md`

## Contraintes

- Conserver les noms `detail`, `define`, `destructure`, `adjust`, `enforce`, `diffuse`, `harness`.
- Conserver les cinq artefacts du contrat 2.x, `release.json`, les migrations et les interfaces `sc-*`.
- Le pipeline complet reste une recette, jamais un prérequis universel.
- Un mode sans contrat ne peut jamais affirmer la conformité.
- Conserver les codes de sortie publics `0/1/2/3/4`.

## Validation finale

```bash
python3 /home/tnn/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/design
for skill_dir in plugins/design/skills/*; do python3 /home/tnn/.codex/skills/.system/skill-creator/scripts/quick_validate.py "$skill_dir"; done
node tools/eval/consistency.mjs
node tools/eval/coverage.mjs
node tools/eval/design-behave.mjs
npm test
```

## Acceptation

- Le manifeste Codex et les sept skills passent leurs validateurs officiels.
- Aucun skill design ne reste à couverture non vérifiable.
- Chaque skill a un usage direct, un cas voisin refusé et une preuve qu'il ne déclenche pas le pipeline complet par défaut.
- Un cycle complet explicite reste correctement routé.
- Les contrôles P0/P1 bloquent ; les contrôles P2 avertissent sans invalider seuls le design.
- Les installations Codex exposent `aidd-context`, `aidd-dev`, `aidd-refine` et `design` dans une nouvelle session.
