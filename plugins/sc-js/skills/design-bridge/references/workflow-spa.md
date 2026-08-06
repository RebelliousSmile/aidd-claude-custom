# Workflow de plateforme — application à composants (SPA)

Instancie les classes de cas agnostiques de `design:detail` sur une application à composants (SFC Vue, composant React). Squelette figé par `plugins/design/references/sc-pivot-contract.md § Workflow de plateforme`. `design` garde le QUOI ; ce fichier porte le COMMENT propre à la plateforme (dec-002).

## Case classes covered

`mockup-multipage` · `brief-only` · `contract-drift` · `element-evolution` · `element-production` (`workflow-classes.md`). Pour chacune, ce workflow instancie nativement `enforce` et `diffuse` et ajoute les phases `off-funnel` de build et de mise en ligne.

## Prerequisites (capabilities)

- **Runtime de build** exécutant le bundler et le serveur de développement — pour servir la référence à mesurer et produire les artefacts.
- **Hôte de mise en ligne** (statique ou applicatif) atteignable pour la phase de déploiement.

Écrites comme capabilities : aucun fournisseur, hébergeur ni projet nommé.

## Phases

| Phase | input | output | verbe | position |
|---|---|---|---|---|
| Servir la référence | contrat figé + runtime de build ; référence pas encore servie | vue servie, mesurable par l'oracle (précondition `harness`) | `off-funnel` | `avant define` |
| Enforcement natif | spec d'enforcement + preuve (fichiers de composants) | règle de lint idiomatique câblée au pre-commit + rapport de pivot | `enforce` | `—` |
| Rendu natif | spec de rendu (composant neutre + variantes) | composant SFC/idiomatique consommant `tokens.css` | `diffuse` | `—` |
| Build | composants rendus | bundle de production | `off-funnel` | `après diffuse` |
| Déployer et recetter | bundle vérifié | cible livrée, recette passée | `off-funnel` | `fin` |

## Gates

Ce workflow **instancie** les gates du contrat, il n'en crée aucun :

- **Vocabulaire** — lint natif des classes littérales des composants (les liaisons dynamiques restent hors de portée, déclarées `unrealized`).
- **Fidélité** — rendu mesuré par propriété à chaque breakpoint contre la référence servie.
- **Seuil de maturité** — un vert n'affirme la conformité qu'au seuil ; sous le seuil, le runner sort en 4.

Point d'application : le gate vocabulaire après l'enforcement, le gate fidélité après le rendu, avant le build.

## Out of scope

- Les liaisons de classe calculées à l'exécution (`:class`, chaînes assemblées) — non réalisables par AST, déclarées `unrealized`.
- Les feuilles de style applicatives hors des sources déclarées — hors de portée du gate.
- Toute garantie que le contrat ne connaît pas : aucun gate local n'est introduit ici.
