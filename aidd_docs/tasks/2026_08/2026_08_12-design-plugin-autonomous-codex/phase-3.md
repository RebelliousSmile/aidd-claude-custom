---
status: done
---

# Phase 3 — Contrôles utiles

## Travail

- Définir P0 résultat réel, P1 cohérence contractuelle et P2 intégration de workflow.
- Rendre P0/P1 bloquants et P2 informatifs.
- Garder les codes de sortie existants et la barrière de maturité.
- Empêcher un contrôle vide ou hors périmètre de produire un vert.

## Acceptation

- La référence canonique et `enforce` portent la même classification.
- Le runner distingue violations bloquantes et avertissements P2 sans casser ses codes publics.
- Les fixtures prouvent P0/P1 rouge, P2 warning et absence de faux vert.
