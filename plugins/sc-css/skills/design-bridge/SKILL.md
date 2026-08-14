---
name: design-bridge
description: >-
  Réceptacle du pivot design pour la couche CSS, seule ou intégrée à une stack mixte. Reçoit le contrat design
  (tokens.json + components.json) émis par design:enforce ou design:diffuse, et produit :
  (1) un fichier de custom properties CSS (tokens → :root) ; (2) des stylesheets de
  composants BEM (components.json → .block, .block__element, .block--modifier) avec
  cascade layers. Jamais invoqué directement — appelé via le pivot design:enforce/04-pivot
  ou design:diffuse/03-pivot quand la cible demande des feuilles CSS.
---

Read [host portability](../../references/host-portability.md) before resolving plugin files, invoking sibling skills, or persisting project guidance.

# sc-css:design-bridge

## Rôle

Réceptacle côté CSS du pivot design. **design garde le QUOI** (contrat = tokens + manifeste) ; **sc-css:design-bridge fait le COMMENT** (custom properties + stylesheets BEM + layers).

## Prérequis

Le spec de pivot doit être présent en contexte, émis par :
- `design:enforce/04-pivot` → spec d'enforcement (quelles classes doivent exister, quels tokens référencés)
- `design:diffuse/03-pivot` → spec de rendu (composant neutre + variantes)

Lire `plugins/design/references/sc-pivot-contract.md` pour le format attendu.

## Actions disponibles

| # | Action | Déclencheur | Output |
|---|--------|-------------|--------|
| 01 | `realize-tokens` | spec reçu de enforce ou diffuse, `tokens.json` présent | `<Output dir>/tokens.css` (`:root { --token-path: value; }`) |
| 02 | `realize-components` | spec reçu, `components.json` présent | `<Output dir>/<component>.css` + point d'entrée |
| 03 | `realize-lint` | spec d'enforcement portant des règles de type `stylesheet` | vérification native + rapport de pivot branché au gate |

## Règle de dérivation stricte

Les fichiers produits **dérivent du contrat** — ils n'inventent pas de règles ni de sélecteurs.

- `realize-tokens` : chaque custom property correspond à un token dans `tokens.json`. Nommage : chemin de token en kebab-case (`color.brand.primary` → `--color-brand-primary`).
- `realize-components` : chaque sélecteur correspond à un `.base`, `.elements.*`, ou `.modifiers.*` du manifeste. Aucune classe inventée.

## Format produit

### `realize-tokens` → `design/css/tokens.css`

```css
/* Généré par sc-css:design-bridge depuis design/tokens.json — ne pas éditer manuellement */
@layer design.tokens {
  :root {
    /* color.brand */
    --color-brand-primary: #1a56db;
    --color-brand-secondary: #0e9f6e;

    /* font.size */
    --font-size-sm: 0.875rem;
    --font-size-base: 1rem;
    --font-size-lg: 1.125rem;

    /* space */
    --space-1: 0.25rem;
    --space-2: 0.5rem;
    /* … */
  }
}
```

### `realize-components` → `design/css/<component>.css`

```css
/* Généré par sc-css:design-bridge depuis design/components.json — ne pas éditer manuellement */
@layer design.components {
  .hero {
    background-color: var(--color-semantic-background);
    padding-block: var(--space-16);
  }

  .hero__eyebrow {
    font-size: var(--font-size-sm);
    font-weight: var(--font-weight-medium);
    color: var(--color-brand-primary);
    letter-spacing: 0.12em;
  }

  .hero__headline {
    font-size: var(--font-size-display);
    line-height: var(--line-height-tight);
  }

  .hero--dark {
    background-color: var(--color-neutral-900);
    color: var(--color-neutral-0);
  }
}
```

## Stratégie de layer — conditionnée à la topologie de l'hôte

L'enveloppe `@layer design.tokens` / `@layer design.components` **suppose un hôte layered**. Dans un document dont l'hôte émet ses styles hors layer (à constater par mesure de la feuille rendue, pas à présumer), toute la couche composants pivotée passe **sous** les styles hôtes : la cascade *normale* classe le non-layered en dernier — donc prioritaire — à spécificité quelconque. Le système réalisé perdrait alors silencieusement, propriété par propriété, sur chaque élément que l'hôte style aussi.

- **Hôte layered** (mesuré) : émettre en `@layer`, et le fichier d'entrée déclare l'ordre — la layer de l'hôte devant celle du design :
  ```css
  @layer design.tokens, design.components, project.overrides;
  ```
- **Hôte unlayered** (mesuré) : émettre les règles composants **hors layer**. `project.overrides` ne sauve pas — une layer, même déclarée dernière, reste sous tout le non-layered de l'hôte.
- Les **tokens** (`:root { --… }`) sont saufs dans les deux cas tant que les noms ne collisionnent pas avec ceux de l'hôte (espaces de noms disjoints) : le risque porte sur les **règles composants**, pas sur la résolution `var()`.

sc-css:design-bridge constate la topologie, émet selon la stratégie retenue, signale l'absence du fichier d'entrée et propose sa création.

Dans une stack mixte, `Output dir` vient du spec et peut viser les assets publics d'un thème. Le point
d'entrée charge, dans cet ordre, `tokens.css`, les feuilles composants, puis tout adapter de plateforme
nommé par le retour du réceptacle de plateforme. L'adapter reste produit par ce dernier ; sc-css ne le
réécrit pas et le contrôle comme toute autre feuille réellement chargée.

Sur FSE, transmettre au câblage de fidélité la liste exacte des feuilles composants contrôlées et de
`fse-bindings.css`. Le linter prouve leurs déclarations ; `measure.py` prouve séparément qu'elles gagnent
sur le front et dans l'éditeur à chaque breakpoint.

## Obligation de report

Toute règle reçue en `Declared rules` est **rendue au gate**, réalisée ou non. Le rapport s'écrit au `Report path` du spec, au format `plugins/design/references/gate-config-schema.md § Rapport de pivot`.

Une règle que ce réceptacle ne couvre pas s'écrit en `status: "unrealized"`. Sans elle, une règle hors de portée et une règle oubliée laissent la même trace — aucune — et le gate ne peut que les confondre.

Le cas fréquent ici : les règles de type `stylesheet`. Elles portent sur les feuilles réellement chargées, pas sur celles produites depuis le contrat. Une feuille applicative hors des sources déclarées est hors de portée — non réalisée, pas conforme.

## Workflow de plateforme (feuilles de style seules / statique)

Ce pivot **possède** le workflow de plateforme statique : `${SC_CSS_PLUGIN_ROOT}/skills/design-bridge/references/workflow-static.md`. Il instancie les classes de cas agnostiques de `design:detail` sur une cible sans runtime, sous le squelette figé par `sc-pivot-contract.md § Workflow de plateforme`. `design:detail/02-route` l'étend à la classe quand ce pivot est installé et la stack correspond.

## Références

- `plugins/design/references/sc-pivot-contract.md` — format des specs reçus et squelette de workflow de plateforme
- `${SC_CSS_PLUGIN_ROOT}/skills/design-bridge/references/workflow-static.md` — workflow de plateforme statique (classes de cas instanciées sur feuilles de style seules)
- `plugins/design/references/gate-config-schema.md` — format du rapport à écrire
- `plugins/design/references/token-schema.md` — structure tokens.json
- `plugins/design/skills/adjust/references/manifest-schema.md` — structure components.json
