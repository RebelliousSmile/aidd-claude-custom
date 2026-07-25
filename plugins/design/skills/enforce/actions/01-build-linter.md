# 01-build-linter

## Rôle

Installer le gate dans le projet courant — runner d'agrégation, cœur portable, périmètre — et vérifier qu'il tourne sur le contrat figé.

## Prérequis

- `design/release.json` existe et déclare au moins `tokens.json`, `components.json` et `policies.json` (produits par `adjust`). Sans `release.json`, le contrat est au format 1.x : jouer `adjust/03-migrate` d'abord.
- Runtimes : `${CLAUDE_PLUGIN_ROOT}/skills/enforce/references/gate-wiring.md § Prérequis d'exécution`.

## Étape 1 — Créer le répertoire de lint

```
design/
  lint/
    run-gates.py         ← runner d'agrégation (source : ${CLAUDE_PLUGIN_ROOT}/tools/run-gates.py)
    lint-core.mjs        ← cœur portable (source : ${CLAUDE_PLUGIN_ROOT}/skills/enforce/adapters/lint-core.mjs)
    migrate-contract.py  ← script de migration (source : ${CLAUDE_PLUGIN_ROOT}/tools/migrate-contract.py)
    status.py            ← calcul du statut de maturité (source : ${CLAUDE_PLUGIN_ROOT}/tools/status.py)
    gates.config.json    ← périmètre du gate (schéma : ${CLAUDE_PLUGIN_ROOT}/references/gate-config-schema.md)
```

Créer `design/lint/` s'il n'existe pas.

## Étape 2 — Copier les quatre fichiers

Copier `tools/run-gates.py`, `skills/enforce/adapters/lint-core.mjs`, `tools/migrate-contract.py` et `tools/status.py` depuis `${CLAUDE_PLUGIN_ROOT}` vers `design/lint/`, à plat.

Ils voyagent ensemble : `run-gates.py` invoque `lint-core.mjs` en frère ; sur un contrat 1.x, les deux sortent en 3 et impriment la commande de migration, cherchée à côté d'eux ; `migrate-contract.py` importe `status.py` en frère, seule implémentation du statut de maturité. Un fichier manquant fait sortir l'outil en 2 en le nommant — jamais un chemin mort ni une trace d'exception.

Si le projet a un gestionnaire de paquets, ajouter un script pointant sur la commande unique de `references/gate-wiring.md § La commande unique` :

```json
{
  "scripts": {
    "lint:design": "python design/lint/run-gates.py --config design/lint/gates.config.json"
  }
}
```

## Étape 3 — Créer `gates.config.json`

C'est le **seul** endroit où le périmètre du gate est déclaré, et il est exécutable : ce qui n'y figure pas n'est pas linté. Champ par champ : `${CLAUDE_PLUGIN_ROOT}/references/gate-config-schema.md`.

Les deux modes de contrat (`policies.json § mode`) ne diffèrent que par `targets` :

**Mode `bem`** — le vocabulaire porte sur les noms de classe, donc sur le markup :

```json
{
  "$schema": "design/references/gate-config-schema",
  "contract": "..",
  "linter": "lint-core.mjs",
  "targets": ["../wireframes/**/*.html"]
}
```

**Mode `utility-first`** — le vocabulaire porte sur l'usage des tokens : couvrir **tous** les fichiers de composants, pas seulement le markup statique, sinon la majorité du code échappe au gate :

```json
{
  "$schema": "design/references/gate-config-schema",
  "contract": "..",
  "linter": "lint-core.mjs",
  "targets": ["../../src/**/*.{vue,jsx,tsx,html}"]
}
```

Les chemins sont relatifs au fichier de configuration lui-même.

## Étape 4 — Vérification de fonctionnement

```bash
python design/lint/run-gates.py --config design/lint/gates.config.json
```

| Exit | Lecture | Suite |
|---|---|---|
| 0 | installation OK, aucune violation | `02-wire-gates` |
| 1 | des violations préexistent | les documenter, proposer `03-lint-instances` |
| 2 | runtime ou configuration | le message nomme ce qui manque (`references/gate-wiring.md § Prérequis d'exécution`) |
| 3 | contrat 1.x | `adjust/03-migrate` d'abord |

Le rapport liste aussi les règles **non réalisées** : déclarées, sans réalisateur disponible. Elles ne rougissent pas le gate et ne doivent pas être lues comme vérifiées.

Si aucune cible du projet n'existe encore, smoke test sur les fixtures du plugin :

```bash
python plugins/design/tools/run-gates.py --config plugins/design/skills/enforce/fixtures/gates.clean.config.json
```

## Sortie attendue

> `run-gates.py` + `lint-core.mjs` installés dans `design/lint/`, `gates.config.json` créé (N cibles).
> Gate : [exit 0 / N violations] · règles non réalisées : [liste ou aucune].
> Prochaine étape : `/design:enforce` → 02-wire-gates.
