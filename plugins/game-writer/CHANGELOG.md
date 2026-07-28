# Changelog — game-writer

> Baseline établie le 2026-05-29 à partir de l'état courant. Détail : `git log -- plugins/game-writer plugins/gamedesign`.

## [1.0.1] — 2026-07-28

### Changed

- **Les titres `H1` des actions ne portent plus leur numéro** — `# Explain`, plus `# Action 01 — explain`. Le numéro vivait à trois endroits, il n'en occupe plus que deux : le nom de fichier et la table de `SKILL.md`, que le gate de cohérence du marketplace compare désormais. Changement transversal aux onze plugins, détaillé dans le journal du marketplace (3.4.0).

## [1.0.0] — 2026-06-13

### Changed
- **BREAKING** — plugin renommé `gamedesign` → `game-writer` ; les invocations passent de `/gamedesign:*` à `/game-writer:*`.
- Recentrage sur la **création de contenu** narratif. La partie technique (GDScript, moteur Godot) est désormais couverte par le nouveau plugin `sc-godot`.

## [0.2.0] — 2026-05-29 (baseline)

Game design pour le projet 8-MINE. Skills :

- `bank` — gère le registre de ressources (`bank.yml`) : init et challenge de la bank d'assets narrative.
- `dialogic-draft` — pipeline d'écriture séquentiel des timelines Dialogic (spec de scène, comportement PNJ, arcs, DTL).
- `dialogic-review` — revue/validation des timelines et du graphe narratif (précheck, persona, audit de graphe, gestion des nœuds).

## Antérieur
- Voir `git log -- plugins/gamedesign` pour l'historique complet.
