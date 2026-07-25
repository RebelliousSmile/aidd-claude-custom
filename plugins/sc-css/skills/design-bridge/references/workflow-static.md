# Workflow de plateforme — feuilles de style seules (statique)

Instancie les classes de cas agnostiques de `design:detail` sur une cible sans runtime : custom properties CSS, feuilles de composants BEM, cascade layers. Squelette figé par `plugins/design/references/sc-pivot-contract.md § Workflow de plateforme`. `design` garde le QUOI ; ce fichier porte le COMMENT propre à la plateforme (dec-002).

## Case classes covered

`brief-only` · `mockup-multipage` · `contract-drift` · `element-evolution` · `element-production` (`workflow-classes.md`). Pour chacune, ce workflow instancie nativement `enforce` (sur les feuilles réellement chargées) et `diffuse` (feuilles générées depuis le contrat), et ajoute une phase `off-funnel` de mise en ligne.

## Prerequisites (capabilities)

- **Hôte statique** atteignable pour la phase de déploiement.
- Aucun runtime requis : la cible est servie telle quelle, sans exécution.

Écrites comme capabilities : aucun fournisseur, hébergeur ni projet nommé.

## Phases

| Phase | input | output | verbe |
|---|---|---|---|
| Servir la référence | contrat figé ; référence pas encore servie | page servie, mesurable par l'oracle (précondition `harness`) | `off-funnel` |
| Enforcement natif | spec d'enforcement portant des règles de type `stylesheet` | vérification native des feuilles chargées + rapport de pivot | `enforce` |
| Rendu natif | `tokens.json` + `components.json` | `tokens.css` (`:root`) + feuilles BEM par composant, sous cascade layers | `diffuse` |
| Déployer et recetter | feuilles vérifiées | cible livrée, recette passée | `off-funnel` |

## Gates

Ce workflow **instancie** les gates du contrat, il n'en crée aucun :

- **Vocabulaire** — chaque sélecteur correspond à un `.base`/`.elements.*`/`.modifiers.*` du manifeste ; chaque custom property à un token.
- **Fidélité** — rendu mesuré par propriété à chaque breakpoint contre la référence servie.
- **Seuil de maturité** — un vert n'affirme la conformité qu'au seuil ; sous le seuil, le runner sort en 4.

Point d'application : le gate vocabulaire après l'enforcement, le gate fidélité après le rendu.

## Out of scope

- Les feuilles applicatives hors des sources déclarées — hors de portée, déclarées non réalisées.
- Tout comportement dynamique : la plateforme statique n'exécute rien, aucune liaison à l'exécution n'existe.
- Toute garantie que le contrat ne connaît pas : aucun gate local n'est introduit ici.
