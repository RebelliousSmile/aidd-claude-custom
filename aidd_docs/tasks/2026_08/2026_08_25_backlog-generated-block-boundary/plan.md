---
objective: "L'alias backlog ne remplace que les lignes qu'il a lui-même produites pour le dépôt déclaré et préserve byte-for-byte tout autre contenu de la section `## Backlog`."
status: in-progress
---

<!-- Fill or omit these sections; never add, rename, or reorder one. -->

# Plan: Borner le remplacement de `## Backlog` aux lignes générées

## Overview

| Field      | Value                                                                                            |
| ---------- | ------------------------------------------------------------------------------------------------ |
| **Goal**   | Remplacer la borne « prochain titre `#`/`##` » par une borne « bloc généré » dans `alias backlog` |
| **Source** | Issue GitHub [#17](https://github.com/RebelliousSmile/my-claude-marketplace/issues/17)           |

## Phases

| #   | Phase                                       | File                         |
| --- | ------------------------------------------- | ---------------------------- |
| 1   | Norme : bloc généré comme zone de remplacement | [`phase-1.md`](./phase-1.md) |
| 2   | Alignement des évals et du changelog         | [`phase-2.md`](./phase-2.md) |

La phase 1 laisse volontairement le scénario S1 des évals en contradiction avec la nouvelle borne ; la phase 2 la lève. Un état intermédiaire entre les deux phases n'est pas une régression.

## Resources

| Source                                                                | Verified                                                                                                     |
| --------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| [Issue #17](https://github.com/RebelliousSmile/my-claude-marketplace/issues/17) | Fournit la modification normative attendue : motifs du bloc généré, insertion en tête de section, suppression de la borne par titre. |

## Decisions

| Decision                                                                             | Why                                                                                                                                    |
| ------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------- |
| La zone de remplacement est définie par les motifs produits par la skill, pas par la structure du document | Une borne structurelle (titre suivant, fin de fichier) capture arbitrairement du contenu utilisateur ; une borne par motif limite le remplacement à des lignes que la skill sait produire. |
| Le motif de ligne générée est resserré au dépôt courant : URL du lien dérivée du `git_repo` résolu, et numéro de l'URL identique au `#<numéro>` affiché | Une reconnaissance par forme seule écraserait une ligne manuelle citant une issue d'un autre dépôt ; l'ancrage au dépôt résolu réduit la collision au seul cas d'une ligne manuelle imitant exactement la sortie de la skill pour ce dépôt. |
| Le bloc généré s'insère en tête de section quand la section existe sans bloc          | Position déterministe et idempotente : la resynchronisation suivante retrouve le bloc au même endroit sans déplacer le contenu manuel.   |
| Délimiteurs explicites (`<!-- backlog:start -->` / `<!-- backlog:end -->`) écartés     | Ils donneraient une garantie totale, mais aucun document déjà synchronisé ne les porte : leur adoption exigerait une migration manuelle de chaque document, ou une première passe qui devine la zone — soit le problème que ce plan corrige. Limites assumées en contrepartie, documentées dans l'action : une ligne manuelle strictement identique à une sortie de la skill pour le dépôt courant est remplacée, et si elle précède le bloc réel celui-ci se duplique à chaque synchronisation. |
