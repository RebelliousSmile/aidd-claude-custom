# Pivot

## Rôle

Identifier le ou les langages dans lesquels la cible doit exister. Pour chaque langage, si un
`sc-<langage>:design-bridge` est installé, émettre une instance du spec de rendu (cf
`${DESIGN_PLUGIN_ROOT}/references/sc-pivot-contract.md`) et lui relayer. Sinon, utiliser la baseline
`${DESIGN_PLUGIN_ROOT}/skills/diffuse/adapters/html-css.md` pour l'artefact manquant et le signaler.

## Prérequis

- Spec neutre complète (issue de `01-define-element`).
- Langage de la cible identifié (précisé par `02-render`).

## Étape 1 — Mapper le langage vers le réceptacle

Le routage se fait sur le langage, jamais sur le nom du framework ou de la plateforme : un même réceptacle sert toutes les cibles qui s'écrivent dans son langage. Une cible peut produire plusieurs lignes ; elles donnent plusieurs specs simples, jamais un spec composite.

| Langage de l'artefact | Réceptacle | Statut |
|---|---|---|
| Feuilles de style seules | `/sc-css:design-bridge` | disponible |
| JavaScript / TypeScript (composants, templates compilés) | `/sc-js:design-bridge` | disponible |
| PHP (templates, gabarits) | `/sc-php:design-bridge` | disponible |
| WordPress FSE (`php-fse-block`) | `/sc-php:design-bridge` pour pattern + binding de plateforme **et** `/sc-css:design-bridge` pour tokens + composants génériques | disponibles |
| Python (gabarits) | `sc-python:design-bridge` | non implémenté |
| Rust (gabarits) | `sc-rust:design-bridge` | non implémenté |
| HTML+CSS pur | baseline (pas de pivot) | — |

## Étape 2a — Pour chaque sc-* disponible : émettre un spec de rendu

Construire le spec de rendu depuis la spec neutre, selon le format de `${DESIGN_PLUGIN_ROOT}/references/sc-pivot-contract.md § Spec de rendu` :

```
## Design render spec

Source: design/tokens.json + design/components.json
Version: <release.json § designSystem.version>

### Component to render
Name: <canonical-name>
Base: <.base>
Elements:
  <label>: <BEM-element>
  ...
Modifiers:
  <label>: <BEM-modifier>
  ...
Backgrounds: [<token.path>, ...]
a11y: { role: <role>, requires: [<attr>, ...] }

### Variants to produce
<liste des variantes de la spec neutre ou "toutes">

### Render target
Language: <langage de l'artefact>
Output dir: <design/components/<canonical-name>/ ou autre cible précisée>

### Request
[Texte du contrat de pivot — § Spec de rendu]
```

Puis appeler `/sc-<langage>:design-bridge` avec ce spec en contexte. Pour WordPress FSE, émettre deux
fois le format ci-dessus :

1. `Language: php-fse-block` vers `sc-php`, qui retourne la pattern et, si nécessaire,
   `fse-bindings.css` dans son propre chemin ;
2. `Language: css-stylesheet` vers `sc-css`, qui retourne tokens, composants génériques et point
   d'entrée dans des chemins distincts de ceux de `sc-php`.

Les deux retours sont attendus avant l'étape 3. `sc-css` ne génère pas `fse-bindings.css`, mais cette
feuille chargée rejoint ensuite son périmètre d'enforcement.

Les contraintes propres à la plateforme du réceptacle — classes générées par elle, outillage d'accès à son magasin de contenu, propagation de ses copies — appartiennent au réceptacle et sont documentées chez lui. `03-pivot` ne les transporte pas : il émet un spec que n'importe quel réceptacle sait lire. Toute contrainte qui doit gouverner le rendu se déclare **dans le contrat** (manifeste ou `policies.json`), où elle vaut pour toutes les cibles, jamais dans le spec d'une seule.

## Étape 2b — Si un réceptacle attendu est absent : baseline + signal

Utiliser `${DESIGN_PLUGIN_ROOT}/skills/diffuse/adapters/html-css.md` et informer :

```
Pivot non disponible pour <langage> : sc-<langage>:design-bridge n'est pas installé.
Rendu assuré par la baseline HTML+CSS (portable, universel).
Pour un rendu natif idiomatique en <langage>, installer `sc-<langage>` et invoquer de nouveau
`design:diffuse` dans l'hôte courant.
```

La baseline est fonctionnelle — ce n'est pas une erreur, seulement une dégradation gracieuse. Sur une
cible multi-réceptacle, elle ne remplace que l'artefact manquant et la sortie reste `non intégrée` : le
succès d'un autre réceptacle ne transforme pas une livraison partielle en intégration native complète.

## Étape 3 — Confirmer le gate

Que le rendu vienne d'un ou plusieurs pivots, ou de la baseline, `02-render` impose le gate enforce sur
toutes les sorties. `03-pivot` ne clôture pas lui-même — il agrège les retours, vérifie que leurs chemins
ne se chevauchent pas, puis remet la main à `02-render` pour le lint final.

Si le rendu du pivot sort en exit 1, corriger en appliquant uniquement des classes et tokens du manifeste, puis re-linter.

## Sortie attendue

**Avec pivot** :
> Specs de rendu émis : <réceptacle → langage → output dir>.
> Fichiers retournés : <réceptacle → fichiers, sans chevauchement>.
> Retours agrégés → gate enforce en cours.

**Sans pivot** :
> Baseline HTML+CSS — aucun `sc-<langage>` installé pour <langage>.
> → Rendu via `adapters/html-css.md`, gate enforce en cours.
