# Decision: borner un bloc généré par motif — une garantie bornée, et ses limites écrites

| Field   | Value |
|---------|-------|
| ID      | DEC-011 |
| Date    | 2026-08-25 |
| Feature | Synchronisation d'une section documentaire depuis une source externe (`overcode:alias/backlog`, issue #17) |
| Status  | Accepted |
| Antécédents | **DEC-006** — la page porte la règle et son motif, la skill la procédure : la présente décision porte le rationnel, `11-backlog.md` la procédure |

## Context

Une skill qui réécrit une section d'un document utilisateur doit décider **ce qu'elle a le droit d'écraser**. La borne initiale était positionnelle : du titre `## Backlog` jusqu'au prochain titre. Sans titre suivant, la plage court jusqu'à la fin du fichier et emporte tout contenu manuel placé après — silencieusement, à chaque synchronisation.

Une borne positionnelle ne connaît pas l'auteur des lignes qu'elle couvre. Elle est juste sur un document dont la section ne contient que du généré, et destructrice dès qu'un humain y ajoute quoi que ce soit — c'est-à-dire sur le cas d'usage même d'un document de projet.

## Decision

### 1. La borne est un motif, pas une position

Le **bloc généré** se définit par la forme de ses lignes, et le remplacement ne porte que sur lui : la première plage contiguë de lignes conformes, la reconnaissance s'arrêtant à la première ligne non conforme. Aucun titre ne borne quoi que ce soit. Hors de cette plage, la section est intouchée, y compris ce qui la suit jusqu'à la fin du fichier.

### 2. Le motif est ancré au dépôt, pas seulement à la forme

Une ligne de forme identique pointant vers **un autre dépôt** n'est jamais du généré : le motif inclut l'URL canonique du dépôt déclaré dans le frontmatter. Sans cet ancrage, une dépendance suivie chez un partenaire, écrite à la main dans la même forme, serait écrasée.

### 3. Absence de bloc → insertion en tête de section

Une section sans bloc généré reçoit le bloc **en tête**, le contenu manuel restant en place derrière. Il n'y a pas de troisième chemin : soit un bloc préexistant est remplacé, soit le bloc est inséré.

### 4. Les limites de la garantie sont écrites, pas implicites

Trois cas restent hors de portée du motif et sont énoncés comme tels dans la procédure :

- une ligne manuelle **identique** à une sortie de la skill est indiscernable, donc remplacée ;
- une telle ligne placée **avant** le vrai bloc capture la reconnaissance : le vrai bloc devient orphelin et se duplique à chaque synchronisation ;
- la ligne d'état vide est le seul motif **non ancré** au dépôt.

## Rationale

**Pourquoi le motif plutôt que des délimiteurs explicites.** Des marqueurs (`<!-- backlog:start -->`) donneraient une borne exacte et une garantie totale. Aucun document déjà synchronisé n'en porte : il faudrait soit une migration de tous les documents existants, soit un chemin de compatibilité qui retombe sur la reconnaissance par motif — donc écrire les deux mécanismes pour n'en garantir qu'un. Le motif seul est le mécanisme qui fonctionne sur le parc existant sans intervention.

**Pourquoi écrire les limites.** La formulation tentante — « un motif ne peut détruire que ce que la skill a écrit » — est fausse : il détruit ce qui **ressemble** à ce que la skill a écrit. Une garantie annoncée totale et bornée en fait ne se distingue d'une garantie bornée et annoncée comme telle que le jour où elle rate ; à ce moment, seule la seconde a prévenu.

### Ce que la décision ne fait pas

Elle ne fait pas de la skill l'autorité sur le contenu manuel de la section : elle borne son écriture, elle ne classe ni ne réordonne rien d'autre. Elle ne change pas les règles de création du document ni de la section quand ils n'existent pas.

## Compatibility

Correctif de comportement, sans changement de forme de sortie : un document dont la section ne contient que du généré rend exactement le même résultat qu'avant. Seuls les cas auparavant destructeurs changent — d'où un **patch**, `overcode` 4.6.0 → 4.6.1.

## Consequences

- `plugins/overcode/skills/alias/actions/11-backlog.md` — Step 4 rend le bloc seul, Step 5 porte la définition du bloc et le placement, Step 6 vérifie la préservation du non-généré.
- `plugins/overcode/skills/alias/evals/backlog-scenarios.md` — S1 exigeait le remplacement jusqu'au titre suivant, c'est-à-dire le défaut lui-même ; observables réécrits en effet préservé, S13–S16 ajoutés sans renumérotation (voir `aidd_docs/memory/behave-eval-method.md`).
- Deux fixtures neuves : document sans aucun titre `##`, et section à contenu manuel portant une ligne piège d'un autre dépôt.
- **Ouvert** : la suite `backlog-scenarios.md` est un harnais de rejeu raisonné, hors `pnpm test` ; S13–S16 n'ont pas encore de run.
