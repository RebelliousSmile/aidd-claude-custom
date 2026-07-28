# Wire-gates

## Rôle

Câbler les 4 gates dans le projet : import de la feuille de tokens, rules de génération, `success_condition` des plans, hook pre-commit auto-armé. Spécification complète de chaque point : `${CLAUDE_PLUGIN_ROOT}/skills/enforce/references/gate-wiring.md`.

## Prérequis

`01-build-linter` terminé : `run-gates.py`, `lint-core.mjs` et `gates.config.json` installés dans le projet, gate vert ou violations documentées.

## Processus

### Étape 1 — Identifier le périmètre

Lister les fichiers qui portent le vocabulaire du design system : markup statique, templates qui émettent du markup, composants du build. Ce périmètre s'écrit dans `gates.config.json § targets` — c'est là qu'il est lu, nulle part ailleurs.

Ce qui n'est pas un fichier du dépôt (feuilles de style, contenu stocké, configuration de plateforme) ne va pas dans `targets` : ces règles se déclarent en `usage.rules[]` avec leur type d'enforcement et sont réalisées par un pivot (`${CLAUDE_PLUGIN_ROOT}/references/enforcement-registry.md`).

### Étape 2 — Vérifier/câbler Gate 0 (import de la feuille de tokens)

Vérifier que les artefacts émis par `generate.py` sont chargés en tête, sans `:root` concurrent (`gate-wiring.md § Gate 0`). Déjà câblé par `adjust/02-freeze` ⇒ confirmer sans refaire. Sinon câbler, et signaler l'absence préexistante comme un finding si l'app avait ses propres variables.

### Étape 3 — Câbler Gate 1 (rules de génération)

**Projet avec rules Claude Code** : créer ou compléter `.claude/rules/08-design/01-enforce.md` :

```markdown
## Design system gate

Avant de générer du markup ou des classes :
- Lire `design/components.json` (classes) et `design/tokens.json` (valeurs) — n'utiliser QUE ce qui y est déclaré.
- Toute classe non déclarée dans `components.json` est une violation ; STOP avant de générer.
- Pour ajouter une classe : re-figer via `/design:adjust`, puis re-jouer `/design:enforce`.
```

**Projet sans rules Claude Code** : porter l'instruction dans le `SKILL.md` de `diffuse` (partie `requires:`).

### Étape 4 — Câbler Gate 2 (`success_condition`)

Ajouter la condition de `gate-wiring.md § Gate 2` au frontmatter de chaque plan touchant du markup. Une seule condition, quel que soit le nombre de cibles.

### Étape 5 — Câbler Gate 3 (pre-commit)

Créer `scripts/hooks/pre-commit` avec le contenu de `gate-wiring.md § Gate 3`, le rendre exécutable, ajouter le `postinstall` d'auto-armement.

Valider : introduire une violation dans une cible et vérifier que `git commit` est refusé.

### Étape 6 — Versionner et documenter

1. Committer `scripts/hooks/pre-commit`, `design/lint/gates.config.json` et l'auto-armement.
2. Documenter dans `design-system.md § Provenance` : "Gates enforce câblés le [date]".

## Sortie attendue

> Gates câblés :
> - Gate 0 (import) : déjà câblé par `adjust` / câblé maintenant — `:root` concurrents supprimés
> - Gate 1 (rules) : `.claude/rules/08-design/01-enforce.md` créé
> - Gate 2 (`success_condition`) : N plans mis à jour
> - Gate 3 (pre-commit) : `scripts/hooks/pre-commit` créé, auto-armement ajouté
>
> Test Gate 3 : commit avec violation → bloqué ✓
