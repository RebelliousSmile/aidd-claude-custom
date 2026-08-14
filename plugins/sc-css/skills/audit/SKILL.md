---
name: audit
description: >-
  Audit CSS multi-dimensionnel : spécificité (guerres de cascade), code mort
  (sélecteurs inutilisés, règles inaccessibles), magic numbers (valeurs littérales
  hors tokens), couverture a11y (contrastes, focus visible, réduction de mouvement),
  opportunités modernes (has(), container queries, nesting, subgrid). Read-only :
  identifie et classe les problèmes, n'édite jamais le code.
---

Read [host portability](../../references/host-portability.md) before resolving plugin files, invoking sibling skills, or persisting project guidance.

# sc-css:audit

Audit CSS read-only — détecte, classe, priorise.

## Dimensions d'audit

| # | Dimension | Ce qu'on cherche |
|---|-----------|-----------------|
| 01 | `specificity` | `!important` selon la topologie de layer **mesurée** (porteur → `info`, jamais `error`), ID / profondeur (`warning`, sélecteurs possédés seulement), conflits de cascade — spécificité calculée en honorant `:where()` / `:is()` / `:has()` |
| 02 | `dead-code` | Sélecteurs **non-référencés dans les sources scannées** (jamais « mort » : classes composées / stockées / runtime invisibles au scan), `@keyframes` non référencées |
| 03 | `magic-numbers` | Littéraux hors `var(--)` rapprochés **par rôle** avec **tolérance de proximité** (`ΔE ≤ 2` couleurs · `±1px`/`±3 %` espacement) — `warning` si == ou dans le rayon d'un token (uniformité), `info` hors rayon (légitime) ; **jamais `error`** (proximité ≠ faute prouvée) |
| 04 | `a11y` | Contraste WCAG **quand les couleurs sont résolues et appariées** (sinon `info: non calculable`), focus et `prefers-reduced-motion` résolus contre la cascade globale |
| 05 | `modern-opportunities` | Constructions remplaçables par `has()`, `:is()`, `:where()`, container queries, nesting natif, subgrid |

## Routing

- Audit ciblé (`sc-css:audit specificity`) → une seule dimension.
- Audit complet (`sc-css:audit`) → toutes les dimensions, un rapport fusionné.

## Format du rapport

Fichier `aidd_docs/tasks/audits/<yyyy>_<mm>_css.md` (une seule passe), template `@assets/audit-template.md`.

Chaque finding : sévérité (`error`/`warning`/`info`) · dimension · `file:line` · problème · suggestion de fix · effort (`xs`/`s`/`m`/`l`).

## Règles

- Read-only : aucune modification de fichier.
- Ne pas inventer des findings pour une dimension non applicable (ex. pas de `:focus-visible` à auditer si aucune interaction JS).
- **Cet audit read-only alimente `improve` / `legacy`, qui mutent.** Réserver `error` au prouvable ; porter toute indécidabilité dans la **sévérité** (`info`), jamais dans une note de bas de finding que le pipeline ignore. Un `error` faux ici devient une casse réelle en aval.
- **Distinguer « hors périmètre / hors contrat » (`info`, peut être légitime) de « contredit le contrat » (`error`).** Le premier n'est pas une violation.
- Le code mort ne se prouve pas par scan statique : émettre « non-référencé dans les sources scannées » (glob listé), jamais « mort ».
- Conditionner tout verdict à une propriété **mesurée** de la preuve (topologie de layer, surface de classes, résolution des couleurs), jamais à une propriété supposée de la plateforme.
