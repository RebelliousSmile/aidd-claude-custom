---
name: improve
description: >-
  Amélioration ciblée de l'architecture CSS existante : extraction vers custom properties,
  organisation en cascade layers, réduction de spécificité, modernisation syntaxique
  (nesting, :is()/:where()/has(), container queries). Travaille sur les findings d'audit
  ou sur une demande directe. Propose un plan avant d'éditer.
---

Read [host portability](../../references/host-portability.md) before resolving plugin files, invoking sibling skills, or persisting project guidance.

# sc-css:improve

Amélioration CSS ciblée — propose → valide → exécute.

## Actions disponibles

| # | Action | Rôle | Input |
|---|--------|------|-------|
| 01 | `analyze` | Lire le rapport audit ou inspecter la zone cible, prioriser les améliorations | rapport audit ou fichier CSS ciblé |
| 02 | `plan` | Proposer le plan de modifications (diff lisible) avant toute édition | output de analyze |

## Default flow

Séquentiel : `analyze` → `plan` → validation humaine → exécution.

## Périmètre par capability

### custom-properties
Extraire les valeurs littérales répétées (couleurs, espacements, typo) vers des déclarations `--custom-property` dans `:root`. Si un contrat design (`design/tokens.json`) est présent, aligner les noms sur la nomenclature du contrat (`--color-brand-primary`, `--space-4`, etc.) — les custom props CSS deviennent la réalisation du token.

### cascade-layers
**Conditionné à la topologie de layer _mesurée_ de l'hôte.** Ne s'applique que si l'hôte émet déjà ses styles en `@layer` (à constater dans la feuille rendue, pas à présumer) : enrôler du CSS dans une layer au sein d'un document dont l'essentiel reste hors layer prend un plancher pour un plafond — toute layer passe **sous** les déclarations *normales* non-layered, à spécificité quelconque. Quand l'hôte est unlayered, cette capability est **contre-indiquée** : elle ferait descendre le CSS sous les styles hôtes qu'il devait surcharger.
Quand elle s'applique : déclarer `@layer` en tête (reset, base, components, utilities, overrides), reclasser les règles dans la layer appropriée. Ne retirer un `!important` que s'il est **prouvablement redondant au vu de l'ordre réel des layers dans le document rendu** — jamais un `!important` qui hisse une règle au-dessus de styles hôtes hors layer.

### specificity
Remplacer les sélecteurs ID par classes, aplatir les chaînes trop profondes, retirer les qualificateurs superflus (`.btn.btn--primary` → `.btn--primary`). Utiliser `:where()` pour les sélecteurs réinitialisables à zéro-spécificité. **Attention** : baisser la spécificité d'une règle qui l'emporte *par spécificité* sur un style hôte concurrent change le rendu — vérifier qu'aucun override ne dépend de la spécificité actuelle avant d'aplatir.

### modernize
Introduire `:is()`, `:where()`, `:has()`, nesting natif, container queries — en respectant la cible de support navigateur du projet (`package.json → browserslist`).

## Règles

- Ne jamais éditer sans avoir soumis le plan à validation (action 02 d'abord).
- Conserver la sémantique exacte des règles — `improve` ne change pas le rendu visuel, seulement l'architecture.
- Si un contrat design est présent, tout token extrait en custom property doit être aligné sur la nomenclature du contrat.
- Signaler quand une amélioration change le rendu (ex. retrait d'un `!important` qui masquait un bug latent).
- Une capability conditionnée à la topologie (`cascade-layers`, `specificity`) ne s'exécute qu'**après constat** de cette topologie — l'hôte est-il layered ? un override dépend-il de la spécificité actuelle ? — jamais sur présomption. Un `error` de spécificité reçu de `audit` n'autorise pas la mutation si la condition n'est pas mesurée.
