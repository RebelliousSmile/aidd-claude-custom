---
status: figé
version: 1.0.0
---

# Design system

## Provenance

Fixture de migration — classe de cas : **aucune cible oracle**. Le manifeste déclare son
`mode` et un jeu de composants non vide, mais aucun composant ne porte de clé `oracle` et il
n'y a pas d'`oracle` de niveau contrat. La migration écrit `components.json`, `policies.json`
et `release.json`, et **n'écrit pas d'`oracle.json`** : un contrat sans cible de mesure n'a pas
de face oracle, dont l'unique lecteur est l'adaptateur `measure`, jamais le linter. Le linter
et `generate.py --check` sortent en 0 sur le contrat migré, sans `oracle.json`.

## Inventaire des composants

| Composant | Rôle |
|---|---|
| btn | action |
