# 03-realize-lint (sc-css)

## Rôle

Réaliser les règles de type `stylesheet` du spec d'enforcement : celles dont la preuve est **les feuilles de style réellement chargées par le projet**, sélecteurs compris. Ni le markup ni le graphe de source ne la portent — c'est pourquoi le cœur portable ne peut pas les couvrir.

## Input attendu

Le spec d'enforcement de `design:enforce/04-pivot`, dont :

- `Declared rules` — les règles routées ici, id et description verbatim.
- `Token paths` — les chemins de tokens, seule autorité de valeur.
- `Enforcement target` — les sources de style déclarées.
- `Report path` — où écrire le rapport.

## Étape 1 — Délimiter les sources de style

Le périmètre est celui des **feuilles chargées**, pas celui des feuilles produites depuis le contrat. Une feuille applicative qui n'est pas dans les sources déclarées est hors de portée : sa dérive ne sera pas vue.

| Origine | Dans le périmètre |
|---|---|
| feuilles produites depuis le contrat (`01-realize-tokens`, `02-realize-components`) | oui — dérivées, donc conformes par construction, mais vérifiées quand même |
| feuilles applicatives déclarées dans `Enforcement target` | oui |
| feuille applicative non déclarée | non — la règle est `unrealized` sur cette surface |
| style injecté à l'exécution | non — la preuve n'existe pas avant l'exécution |

## Étape 2 — Réaliser les règles

Matérialiser chaque règle de `Declared rules` dans l'outillage natif du projet (`stylelint` si présent, sinon un script Node autonome).

Deux vérifications reviennent systématiquement, et se dérivent du spec sans liste codée en dur :

- Toute valeur littérale là où un token existe est une violation — la valeur doit passer par sa custom property.
- Tout `var(--…)` référencé résout un chemin de `Token paths`. Une custom property inconnue est un token fantôme, pas une valeur.

Un second `:root` redéclarant une custom property du contrat est le cas le plus destructeur : la cascade rend la dérive invisible dans le markup, qui reste littéralement conforme.

## Étape 3 — Écrire le rapport et le brancher au gate

Format : `plugins/design/references/gate-config-schema.md § Rapport de pivot`. Une entrée par règle de `Declared rules`.

| Règle | Statut à écrire |
|---|---|
| réalisée, aucune violation sur les sources déclarées | `pass` |
| réalisée, violations trouvées | `fail` + une entrée `violations` par occurrence, fichier et sélecteur nommés |
| surface hors périmètre, ou outillage absent | `unrealized` |

Puis déclarer le rapport dans la configuration du gate :

```json
{
  "pivotReports": [
    { "path": "reports/design-css.json", "command": ["pnpm", "lint:design:css"] }
  ]
}
```

Avec `command`, le runner relance la vérification avant de lire — un rapport périmé devient impossible.

## Sortie attendue

> Règles `stylesheet` réalisées : \<ids\> — sources couvertes : \<liste\>.
> Non réalisées : \<ids + raison\> (feuilles hors périmètre, style injecté à l'exécution).
> Rapport écrit à `<Report path>`, branché dans `gates.config.json § pivotReports`.
>
> Retour à design:enforce — gate CSS opérationnel.
