# Workflow de plateforme — block theme (FSE)

Instancie les classes de cas agnostiques de `design:detail` sur un thème de blocs WordPress FSE. Squelette figé par `plugins/design/references/sc-pivot-contract.md § Workflow de plateforme`. `design` garde le QUOI ; ce fichier porte le COMMENT propre à la plateforme (dec-002).

## Case classes covered

`mockup-multipage` · `codebase-inherited` · `contract-drift` · `element-evolution` · `element-production` (`workflow-classes.md`). Pour chacune, ce workflow instancie nativement les phases `enforce` et `diffuse` et ajoute les phases `off-funnel` du cycle de vie d'un site à blocs.

## Prerequisites (capabilities)

- **Runtime conteneurisé** portant le CLI de la plateforme et sa base — sans lui, ni mesure ni import (`enforce` sur référence servie, `off-funnel` d'import).
- **Base de données distante** : une part du vocabulaire vit comme contenu stocké, pas dans les sources versionnées.
- **Accès shell distant** vers l'environnement de destination, pour la phase de déploiement.

Écrites comme capabilities : aucun hébergeur ni projet nommé.

## Phases

| Phase | input | output | verbe |
|---|---|---|---|
| Préparer l'environnement mesurable | contrat figé + runtime conteneurisé ; référence pas encore servie | instance servie, mesurable par l'oracle (précondition `harness`) | `off-funnel` |
| Enforcement natif | spec d'enforcement + preuve (markup de blocs, contenu stocké extrait) | linter PHP/WP idiomatique câblé + rapport de pivot | `enforce` |
| Rendu natif | spec de rendu (composant neutre + variantes) | block pattern + `theme.json` conformes au contrat | `diffuse` |
| Importer le contenu | patterns rendus, instances de référence | instances en base | `off-funnel` |
| Déployer et recetter | instances vérifiées | cible livrée, recette passée | `off-funnel` |

## Gates

Ce workflow **instancie** les gates du contrat, il n'en crée aucun :

- **Vocabulaire** — lint natif du markup de blocs et du contenu stocké extrait (`references/wordpress-lint-instances.md`).
- **Fidélité** — rendu mesuré par propriété à chaque breakpoint contre la référence servie.
- **Seuil de maturité** — un vert n'affirme la conformité qu'au seuil ; sous le seuil, le runner sort en 4.

Point d'application : le gate vocabulaire après la phase d'enforcement, le gate fidélité après le rendu et l'import.

## Out of scope

- Le contenu rédigé en base au-delà des instances de référence mesurées — hors de portée du gate, déclaré non réalisé, jamais passé en silence.
- Les liaisons de classe résolues à l'exécution — non lisibles par lint statique, déclarées `unrealized`.
- Toute garantie que le contrat ne connaît pas : aucun gate local n'est introduit ici.
