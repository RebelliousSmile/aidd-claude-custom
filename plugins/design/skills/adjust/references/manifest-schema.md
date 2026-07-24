# Manifest schema — `design/components.json`

`components.json` est l'artefact d'**anatomie** du contrat : la nomenclature déclarée des composants, et rien d'autre. Écrit par `adjust/02-freeze.md`, lu par `lint-core.mjs` (Règles 1 et 5) et par `config-gen.py` (cibles de mesure).

Les quatre autres fichiers du contrat, l'étiquetage des champs, la dérivation des règles de lint et la redistribution depuis un contrat 1.x : `${CLAUDE_PLUGIN_ROOT}/references/contract-schema.md`. Ce document ne traite que `components.json`.

## Structure

```json
{
  "$schema": "design/references/contract-schema#components",
  "components": {
    "<canonical-name>": {
      "base": "<BEM-block>",
      "elements":  { "<element-label>": "<BEM-element>" },
      "modifiers": { "<variant-label>": "<BEM-modifier>" },
      "backgrounds": ["<token.path>"],
      "a11y": { "role": "<ARIA-role>", "requires": ["<attribute>"] }
    }
  }
}
```

### Champs

Chaque champ est **exécutable** — un consommateur nommé le lit et en tire un effet vérifiable — ou **informationnel** — il documente une intention qu'aucun outil ne vérifie.

| Champ | Requis | Statut · consommateur | Description |
|-------|--------|-----------------------|-------------|
| `$schema` | oui | informationnel | Toujours `"design/references/contract-schema#components"` |
| `components` | oui en `bem` ; optionnel en `utility-first` | exécutable · `lint-core.mjs` Règles 1 et 5 | Map des composants canoniques |
| `components.<name>` | — | — | Clé = nom canonique en kebab-case |
| `.base` | oui | exécutable · `lint-core.mjs` Règle 1 · `config-gen.py` (cible racine) | Classe BEM block — source unique de la nomenclature |
| `.elements` | non | exécutable · `lint-core.mjs` Règles 1 et 5 · `config-gen.py` (une cible par élément) | Map `label → BEM-element` |
| `.modifiers` | non | exécutable · `lint-core.mjs` Règles 1 et 5 | Map `label → BEM-modifier` |
| `.backgrounds` | non | exécutable · `adjust/02-freeze.md` (existence du chemin, au figeage) | Chemins de tokens autorisés comme fond. Omis = pas de contrainte. Aucune règle de lint ne vérifie le fond réellement appliqué (Invariant 4) |
| `.a11y.role` | non | informationnel | Rôle ARIA attendu. Aucun consommateur ne le vérifie |
| `.a11y.requires` | non | informationnel | Attributs ARIA requis. Aucun consommateur ne les vérifie |

La version de cet artefact vit dans `release.json § artifacts["components.json"].version` — jamais ici.

## Invariants

Chaque invariant porte une étiquette : **exécutable** — un consommateur nommé le vérifie, à un moment nommé — ou **informationnel** — règle d'écriture, aucun consommateur ne la vérifie.

1. **Vocabulaire ouvert par défaut** — *exécutable · `lint-core.mjs` Règle 1, mode `bem` uniquement*. Une classe dont le **bloc est déclaré** mais dont l'élément/modificateur ne l'est pas est une `error`. Une classe dont le **bloc n'est pas déclaré** est traitée comme utilitaire et ignorée. Le vocabulaire ne se ferme que sous `--strict`, et seulement sur les classes de **forme BEM** (contenant `__` ou `--`) hors `policies.json § $utilityPrefixes` — elles deviennent alors des `warning`, jamais des `error`. Une classe utilitaire ordinaire (`flex`, `mt-4`) n'est jamais signalée, dans aucun mode.
2. **Pas de doublons** — *informationnel*. Deux composants ne peuvent pas partager le même `.base`.
3. **Concordance avec la charte** — *exécutable · `adjust/02-freeze.md § Étape 2 Règle 4`, au figeage seulement*. Chaque composant listé dans `design-system.md § Inventaire des composants` a une entrée ici, et réciproquement. Aucun lint ne re-vérifie cette concordance après le figeage.
4. **Backgrounds token-référencés** — *exécutable · `adjust/02-freeze.md § Étape 2 Règle 3`, au figeage seulement*. Chaque chemin de `.backgrounds` doit exister dans `tokens.json` ; un chemin absent bloque le figeage. `lint-core.mjs` ne porte aucune règle de fond : il ne lit pas `.backgrounds` et ne compare aucune couleur de conteneur.
5. **Contraste par thème** — *gap déclaré, non vérifié à cette version*. Pour une variante sombre dont `.backgrounds` liste un token surchargé dans un thème (`token-schema.md § Modes / themes`), le contraste WCAG AA texte/fond devrait être évalué contre la valeur **résolue dans le thème concerné**, jamais contre la valeur `default`. Aucun outil du plugin ne calcule ce ratio. La conformité contraste d'un contrat figé est **non établie**.
6. **Concordance avec le code réel (retrofit)** — *exécutable · `adjust/02-freeze.md § Étape 2bis`, au figeage, via `lint-core.mjs` Règles 1 et 4*. `components.json` doit concorder avec les classes/utilitaires réellement présents dans le code préexistant, pas seulement avec la prose de la charte (Invariant 3, concordance distincte). Mode-aware, always-on, auto-neutralisante en greenfield. Divergence **code → manifeste** : bloquante. Divergence **manifeste → code** (`--report-unused`) : jamais bloquante, ledger optionnel.

La parité de versions entre artefacts n'est plus un invariant : `release.json` déclare une version par artefact et un écart est une donnée (`contract-schema.md § Disparition de l'invariant 5`).

## Exemple

```json
{
  "$schema": "design/references/contract-schema#components",
  "components": {
    "btn": {
      "base": "btn",
      "elements": { "icon": "btn__icon", "label": "btn__label" },
      "modifiers": {
        "primary":   "btn--primary",
        "secondary": "btn--secondary",
        "ghost":     "btn--ghost"
      },
      "backgrounds": ["color.semantic.background", "color.semantic.surface", "color.brand.primary"],
      "a11y": { "role": "button", "requires": [] }
    },
    "card": {
      "base": "card",
      "elements": { "media": "card__media", "body": "card__body", "title": "card__title" },
      "modifiers": { "featured": "card--featured" },
      "backgrounds": ["color.semantic.surface"],
      "a11y": { "role": "article", "requires": ["aria-label"] }
    }
  }
}
```

## Déclenchement d'un re-figeage

Si `destructure` identifie une direction incompatible avec le manifeste actuel (`coût contrat: demande un re-figeage`) :

1. `/design:adjust` rejoue l'arbitrage sur le delta (nouvelles pistes uniquement).
2. `02-freeze.md` met à jour les artefacts touchés et bumpe leur version dans `release.json`.
3. `enforce` propage et re-lint.
