# Manifest schema — `design/components.json`

`components.json` est l'artefact d'**anatomie** du contrat : la nomenclature déclarée des composants, et rien d'autre. Écrit par `adjust/02-freeze.md`, lu par `lint-core.mjs` (Règles 1 et 5) et par `config-gen.py` (cibles de mesure).

Les quatre autres fichiers du contrat, l'étiquetage des champs, la dérivation des règles de lint et la redistribution depuis un contrat 1.x : `${DESIGN_PLUGIN_ROOT}/references/contract-schema.md`. Ce document ne traite que `components.json`.

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
      "foregrounds": ["<token.path>"],
      "a11y": { "role": "<ARIA-role>", "requires": ["<attribute>"] },
      "states": { "disabled": <bool>, "error": <bool>, "focus": <bool> }
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
| `.backgrounds` | non | exécutable · `adjust/02-freeze.md` (existence du chemin, au figeage) · `adapters/a11y/contrast.py` (côté fond de chaque paire déclarée) | Chemins de tokens autorisés comme fond. Omis = pas de contrainte. Aucune règle de lint ne vérifie le fond réellement appliqué (Invariant 4) |
| `.foregrounds` | non | exécutable · `adjust/02-freeze.md` (existence du chemin, au figeage) · `adapters/a11y/contrast.py` (côté texte de chaque paire déclarée) | Chemins de tokens **portant du texte** sur ces fonds. Un chemin quelconque sous `color.*` — `color.brand.primary` est aussi légitime que `color.semantic.text`. C'est la seule déclaration qui dit un **usage** ; sans elle le contrôle de contraste retombe sur une heuristique de nom et n'apparie que `color.semantic` (Invariant 8) |
| `.a11y.role` | non | exécutable · pivot (`markup`) | Rôle ARIA attendu. Non calculable au figeage ; réalisé par un pivot de markup (`references/enforcement-registry.md`) |
| `.a11y.requires` | non | exécutable · pivot (`markup`) | Attributs ARIA requis. Même réalisateur que `role` |
| `.states` | non | exécutable · `tools/status.py` (contrôle d'états au figeage) | Présence déclarative des états interactifs. Trois clés booléennes fermées — `disabled`, `error`, `focus` : `true` = le composant présente l'état, `false` = il l'omet intentionnellement. Objet omis = composant statique. Objet **partiel** (une clé manquante) = gap `states` (§ Invariant 8) |

La version de cet artefact vit dans `release.json § artifacts["components.json"].version` — jamais ici.

## Invariants

Chaque invariant porte une étiquette : **exécutable** — un consommateur nommé le vérifie, à un moment nommé — ou **informationnel** — règle d'écriture, aucun consommateur ne la vérifie.

1. **Vocabulaire ouvert par défaut** — *exécutable · `lint-core.mjs` Règle 1, mode `bem` uniquement*. **Énoncé canonique : tout document qui affirme quelque chose sur l'ouverture du vocabulaire renvoie ici et ne le réécrit pas.** Une classe dont le **bloc est déclaré** mais dont l'élément/modificateur ne l'est pas est une `error`. Une classe dont le **bloc n'est pas déclaré** est traitée comme utilitaire et ignorée. Le vocabulaire ne se ferme que sous `--strict`, et seulement sur les classes de **forme BEM** (contenant `__` ou `--`) hors `policies.json § $utilityPrefixes` — elles deviennent alors des `warning`, jamais des `error`. Une classe utilitaire ordinaire (`flex`, `mt-4`) n'est jamais signalée, dans aucun mode.
2. **Pas de doublons** — *informationnel*. Deux composants ne peuvent pas partager le même `.base`.
3. **Concordance avec la charte** — *exécutable · `adjust/02-freeze.md § Étape 2 Règle 4`, au figeage seulement*. Chaque composant listé dans `design-system.md § Inventaire des composants` a une entrée ici, et réciproquement. Aucun lint ne re-vérifie cette concordance après le figeage.
4. **Fonds et avant-plans token-référencés** — *exécutable · `adjust/02-freeze.md § Étape 2 Règle 3`, au figeage seulement*. Chaque chemin de `.backgrounds` et de `.foregrounds` doit exister dans `tokens.json` ; un chemin absent bloque le figeage. `lint-core.mjs` n'en porte aucune règle : il ne lit ni l'un ni l'autre et ne compare aucune couleur de conteneur.
5. **Contraste par thème** — *exécutable · `adjust/02-freeze.md`, au figeage, via `adapters/a11y/contrast.py`*. Le contraste WCAG AA texte/fond est calculé depuis les valeurs de tokens **résolues dans chaque thème** (`token-schema.md § Modes / themes`), jamais contre la seule valeur `default`. Les paires viennent d'abord de `.foregrounds` × `.backgrounds` **par composant** — la seule source qui connaisse un usage — et à défaut d'une heuristique de nom bornée à `color.semantic`, jamais l'inverse. Le résultat est enregistré dans `release.json § checks.contrast` et pèse sur le statut de maturité (`contract-schema.md § Statut de maturité`) ; une paire qui échoue est un gap `contrast`. Ce contrôle ne lit aucun markup : il n'établit pas que le fond est réellement appliqué (Invariant 4), seulement que les valeurs déclarées contrastent.
6. **Concordance avec le code réel (retrofit)** — *exécutable · `adjust/02-freeze.md § Étape 2bis`, au figeage, via `lint-core.mjs` Règles 1 et 4*. `components.json` doit concorder avec les classes/utilitaires réellement présents dans le code préexistant, pas seulement avec la prose de la charte (Invariant 3, concordance distincte). Mode-aware, always-on, auto-neutralisante en greenfield. Divergence **code → manifeste** : bloquante. Divergence **manifeste → code** (`--report-unused`) : jamais bloquante, ledger optionnel.
7. **Rien à comparer n'est pas un contrat conforme** — *exécutable · `adjust/02-freeze.md`, au figeage, via `adapters/a11y/contrast.py` (exit 3)*. Un contrat dont aucun composant ne déclare `.foregrounds` et dont aucun nom ne matche un rôle sous `color.semantic` ne produit **aucune paire** : le contrôle de contraste sort exit 3 et le figeage **est refusé**. C'est le seul point a11y qui refuse ; il ne porte pas sur un contraste insuffisant — celui-là reste un gap plafonnant (Invariant 5) — mais sur un vocabulaire hors de portée du contrôle, qui est un défaut de conception du contrat et non un écart mesuré. La sortie se lève en déclarant les paires, jamais en renommant des tokens pour plaire à l'heuristique.
8. **Présence déclarative des états** — *exécutable · `adjust/02-freeze.md`, au figeage, via `tools/status.py`*. Le contrôle lit `.states` **par composant** et rapporte sa présence, sans inspecter aucun markup. Une déclaration `.states` doit être complète — les trois clés `disabled`/`error`/`focus` présentes ; une déclaration partielle est un gap `states`. Le figeage vérifie que l'état interactif est déclarativement rendu compte (présent ou intentionnellement omis), jamais qu'il est réellement implémenté dans le rendu — cet aspect relève du pivot de markup, côté HOW (dec-002).

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
      "foregrounds": ["color.semantic.text", "color.semantic.on-brand"],
      "a11y": { "role": "button", "requires": [] },
      "states": { "disabled": true, "error": false, "focus": true }
    },
    "card": {
      "base": "card",
      "elements": { "media": "card__media", "body": "card__body", "title": "card__title" },
      "modifiers": { "featured": "card--featured" },
      "backgrounds": ["color.semantic.surface"],
      "foregrounds": ["color.semantic.text", "color.brand.accent"],
      "a11y": { "role": "article", "requires": ["aria-label"] }
    }
  }
}
```

## Déclenchement d'un re-figeage

Si `destructure` identifie une direction incompatible avec le manifeste actuel (`coût contrat: demande un re-figeage`) :

1. Invoquer `design:adjust` rejoue l'arbitrage sur le delta (nouvelles pistes uniquement).
2. `02-freeze.md` met à jour les artefacts touchés et bumpe leur version dans `release.json`.
3. `enforce` propage et re-lint.
