---
status: figé
version: 1.0.0
---

# Design system

## Provenance

Fixture de migration — classe de cas : **namespace de tokens de plateforme non possédé par le
contrat**. Le contrat est migré et valide (`release.json` présent, le linter ne sort plus en 3).
Son markup (`sample.html`) inline `var(--platform--accent)` : une propriété personnalisée qu'une
plateforme génère depuis sa propre couche de configuration, hors du `tokens.json` du contrat.

La Rule 2 (`token-reference`) du `lint-core.mjs` générique vérifie chaque `var(--…)` contre le
seul `tokens.json` et n'a, **par construction**, aucune notion de namespace de plateforme
externe. Elle sort donc en **1** sur `--platform--accent`, alors que le contrat ne revendique
légitimement pas ce token. Ce n'est pas une régression de vocabulaire : les classes BEM du
markup passent la Rule 1.

Résolution : la divergence est une **frontière attendue**, pas un bug à corriger dans le linter.
Déclarer les tokens de plateforme dans `tokens.json` pour verdir le run est refusé — le contrat
revendiquerait des tokens d'une autre couche. L'extension de couverture appartient à un pivot
`sc-<langage>:design-bridge`, jamais à une règle de `lint-core.mjs`. Le namespace est écrit
générique (`--platform--`), jamais lié à une plateforme nommée.

## Inventaire des composants

| Composant | Rôle |
|---|---|
| btn | action |
