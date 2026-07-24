# 01-build-linter

## Rôle

Installer `lint-core.mjs` dans le projet courant et vérifier qu'il tourne correctement sur le contrat figé.

## Prérequis

- `design/release.json` existe et déclare au moins `tokens.json`, `components.json` et `policies.json` (produits par `adjust`). Sans `release.json`, le contrat est au format 1.x : jouer `adjust/03-migrate` d'abord.
- Node.js ≥ 18 disponible dans l'environnement du projet.
- Python ≥ 3.9 si le projet peut avoir à migrer un contrat 1.x.

## Étape 1 — Créer le répertoire de lint

```
design/
  lint/
    lint-core.mjs        ← copie du cœur portable (source : ${CLAUDE_PLUGIN_ROOT}/skills/enforce/adapters/lint-core.mjs)
    migrate-contract.py  ← copie du script de migration (source : ${CLAUDE_PLUGIN_ROOT}/tools/migrate-contract.py)
    status.py            ← copie du calcul de statut (source : ${CLAUDE_PLUGIN_ROOT}/tools/status.py)
    .lintrc.json         ← config projet (chemins, préfixe BEM optionnel)
```

Créer `design/lint/` s'il n'existe pas.

## Étape 2 — Copier les trois fichiers

Copier `skills/enforce/adapters/lint-core.mjs`, `tools/migrate-contract.py` et `tools/status.py` depuis `${CLAUDE_PLUGIN_ROOT}` vers `design/lint/`, à plat.

Les trois voyagent ensemble : sur un contrat 1.x, `lint-core.mjs` sort en 3 et imprime la commande de migration, cherchée à côté de lui ; `migrate-contract.py` importe `status.py` en frère, seule implémentation du statut de maturité. Un fichier manquant fait sortir l'outil en 2 en le nommant — jamais un chemin mort ni une trace d'exception. Sans eux, la seule issue reste de rejouer `adjust/03-migrate` depuis le plugin.

Si le projet gère déjà Node avec un `package.json`, ajouter un script :

```json
{
  "scripts": {
    "lint:design": "node design/lint/lint-core.mjs --contract design"
  }
}
```

## Étape 3 — Créer `.lintrc.json`

`design/lint/.lintrc.json` n'est pas consommé directement par `lint-core.mjs` (qui lit ses règles depuis les artefacts déclarés par `release.json`, jamais depuis un fichier de config séparé) — c'est un **fichier de référence projet**, documentant pour les humains/CI quelles cibles linter et comment calibrer les sévérités du wiring (hook pre-commit, script CI). Il n'existe pas de `.lintrc.json` canonique dans ce plugin ; ce qui suit est le gabarit à créer dans le projet consommateur.

Deux profils selon le mode du contrat (`policies.json § mode`, cf. `${CLAUDE_PLUGIN_ROOT}/references/contract-schema.md`) :

**Profil `bem`** (wireframes HTML, templates WP FSE) :

```json
{
  "contractDir": "design",
  "targets": ["design/wireframes/**/*.html"],
  "severity": {
    "unknownClass": "error",
    "unknownToken": "error"
  }
}
```

**Profil `utility-first`** (aucune classe BEM dans le code, `usage` déclaré dans `policies.json`) :

```json
{
  "contractDir": "design",
  "targets": ["src/**/*.{vue,jsx,tsx,html}"],
  "severity": {
    "unknownToken": "error",
    "rawHexForbidden": "error",
    "colorNamespace": "error",
    "stateColourIcon": "pivot-only"
  }
}
```

- `contractDir` : chemin vers le répertoire contenant `release.json` et les artefacts qu'il déclare (relatif à la racine projet). C'est la valeur de `--contract` — la fournir toujours explicitement.
- `targets` : globs à linter par défaut (hook pre-commit, CI). En `utility-first`, les cibles doivent couvrir **tous** les fichiers de composants, pas seulement le HTML — sinon la majorité du code échappe au gate.
- `severity` : ne référencer ici que des règles réellement émises par `lint-core.mjs` (`${CLAUDE_PLUGIN_ROOT}/references/contract-schema.md § Dérivation des règles de lint`). `stateColourIcon` est la seule entrée `pivot-only` du gabarit : déclarée dans `usage.rules[]`, jamais émise par la baseline (cf. `references/sc-pivot-contract.md`).

## Étape 4 — Vérification de fonctionnement

Demander à l'utilisateur (ou exécuter si le contexte le permet) :

```bash
# Test baseline sur les wireframes existants
node design/lint/lint-core.mjs design/wireframes/<premier-fichier>.html --contract design
```

Si exit 0 → installation OK. Si exit 1 → des violations existent avant même de commencer ; les documenter et proposer de jouer `03-lint-instances` pour les résoudre.

Si aucun wireframe n'existe encore, utiliser les fixtures du plugin comme smoke test :

```bash
# Profil bem
node plugins/design/skills/enforce/adapters/lint-core.mjs \
  plugins/design/skills/enforce/fixtures/clean.html \
  --contract plugins/design/skills/enforce/fixtures

# Profil utility-first
node plugins/design/skills/enforce/adapters/lint-core.mjs \
  plugins/design/skills/enforce/fixtures/utility-clean.html \
  --contract plugins/design/skills/enforce/fixtures/utility
```

## Sortie attendue

> lint-core.mjs installé dans `design/lint/`. Config `.lintrc.json` créée.
> Smoke test : [OK / N erreurs trouvées].
> Prochaine étape : `/design:enforce` → 02-wire-gates.
