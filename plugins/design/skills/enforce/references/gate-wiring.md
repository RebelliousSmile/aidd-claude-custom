# Gate wiring — les 4 points de câblage

`enforce` câble le gate à 4 endroits du projet. Chaque point est indépendant ; câbler un sous-ensemble reste valide.

## La commande unique

Les trois sites d'appel — poste local, hook pre-commit, CI — exécutent **exactement la même commande** :

```bash
python design/lint/run-gates.py --config design/lint/gates.config.json
```

Un site d'appel qui invoque `lint-core.mjs` directement contourne le runner : il ne voit que les règles de type `markup` et ne rapporte aucune règle non réalisée. Un run vert y signifie moins qu'ailleurs, sans le dire.

Contenu de la configuration : `${CLAUDE_PLUGIN_ROOT}/references/gate-config-schema.md`.

## Prérequis d'exécution

| Runtime | Rôle | Absent ⇒ |
|---|---|---|
| Python 3.10+ | démarre le runner | le gate ne démarre pas — y compris sur un projet sans une ligne de Python |
| Node.js 18+ | le runner invoque `lint-core.mjs` avec | exit 2 nommant Node, jamais 1 |

Énoncé ici une fois. Aucun autre document ne le redit ; ils pointent ici.

---

## Gate 0 — Import de la feuille de tokens dans l'app réelle

**Quand** : une fois, dès qu'`adjust` a figé le contrat et que `generate.py` a émis l'artefact de rôle `stylesheet`.

**Problème résolu** : sans ce point, l'artefact reste orphelin — l'app garde ses `:root` ad hoc, qui dérivent silencieusement de `tokens.json`. Aucun des gates 1-3 ne le détecte : ils lisent l'usage des classes et des tokens dans le markup produit, pas la présence de la source unique dans l'app.

**Câblage** : charger l'artefact `stylesheet` (et les autres rôles émis, s'il y en a) comme **première** feuille de style de l'app, avant toute feuille applicative, et supprimer toute déclaration `:root` concurrente. Le mécanisme dépend du consommateur, pas de la plateforme :

| Rôle consommateur | Mécanisme |
|---|---|
| `stylesheet` chargé statiquement | balise de lien en tête de document |
| `stylesheet source` / `build configuration` | import au point d'entrée du build |
| `platform token file` | déclaré par le pivot du runtime, en dépendance de tout style applicatif |

**Qui pose ce câblage** : `adjust/02-freeze` à la première écriture du contrat, ou `enforce/01-build-linter` si le contrat existe déjà sans import câblé — signaler alors l'absence comme un finding.

---

## Gate 1 — Rules de génération

**Quand** : tout verbe qui produit du markup consommant le vocabulaire du design system.

**Câblage** : les rules du projet, ou les gabarits de génération, portent une instruction explicite :

```
Avant de générer du markup :
1. Lire design/components.json — n'utiliser que les classes et tokens déclarés.
2. Vérifier que chaque classe produite est dans le manifeste.
3. Classe manquante ⇒ STOP, ne pas générer ; signaler la violation.
```

**Artefact** : `.claude/rules/08-design/` du projet consommateur, ou le `SKILL.md` de `diffuse`.

---

## Gate 2 — `success_condition` des plans

**Quand** : tout plan aidd-dev qui touche du markup, des templates ou du style lié au design system.

```yaml
success_condition: >
  python design/lint/run-gates.py --config design/lint/gates.config.json exits 0
```

Une seule condition quel que soit le nombre de cibles : le périmètre est dans la configuration, pas dans la ligne de commande. Le plan reste `blocked` tant que le gate est rouge.

---

## Gate 3 — Hook pre-commit

### 3a — Créer le hook

`scripts/hooks/pre-commit` :

```bash
#!/bin/sh
# Design-system gate. Same command as the local run and the CI job.
git diff --cached --name-only --diff-filter=ACM \
  | grep -qE '\.(html|astro|vue|jsx|tsx|svelte|css)$' || exit 0

python design/lint/run-gates.py --config design/lint/gates.config.json
```

Le filtre sur les fichiers indexés est un **court-circuit**, pas un périmètre : il évite de démarrer le gate sur un commit qui ne touche rien du design system. Quand il démarre, le gate porte sur la configuration entière — un commit ne peut pas casser une cible qu'il ne modifie pas et passer quand même.

`chmod +x scripts/hooks/pre-commit`

### 3b — Auto-armer

```bash
git config core.hooksPath scripts/hooks
```

Automatisable à l'installation des dépendances, via un script `postinstall` du gestionnaire de paquets qui rejoue cette commande.

### 3c — Versionnement

`scripts/hooks/pre-commit` est versionné. `core.hooksPath` est positionné par le `postinstall` — aucune manipulation manuelle.

---

## Résumé des artefacts à créer

| Gate | Artefact | Emplacement |
|------|----------|-------------|
| 0 — Import | artefact `stylesheet` chargé en tête, `:root` concurrents supprimés | App consommatrice |
| 1 — Rules | Instruction dans `.claude/rules/08-design/` ou `diffuse/SKILL.md` | Projet consommateur |
| 2 — success_condition | Frontmatter des plans concernés | Plans aidd-dev |
| 3 — pre-commit | `scripts/hooks/pre-commit` | Racine projet (versionné) |
| 3 — auto-armer | `postinstall` du gestionnaire de paquets | Racine projet |
| 3 — config | `git config core.hooksPath scripts/hooks` | Une fois par poste |
