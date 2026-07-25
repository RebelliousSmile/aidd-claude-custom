---
name: detail
description: >
  Verbe 0 de l'entonnoir : le point d'entrée qui dit ce que font les verbes et quoi lancer.
  LECTURE SEULE sur tout artefact du contrat et sur la source du projet ; seul skill du plugin
  sans artefact de sortie. Deux actions sans recouvrement :
  (1) EXPLAIN — la carte, à la granularité demandée (entonnoir entier, un verbe, une action, un gate, un artefact).
  (2) ROUTE — classe une intention en classe de cas, lit l'état du contrat et les pivots installés,
  émet la séquence exécutable avec ses checkpoints et ses gates, étendue par le workflow de plateforme
  quand le pivot correspondant est là. N'exécute jamais un verbe qu'il décrit.
triggers:
  - "que fait ce plugin"
  - "explique l'entonnoir"
  - "quels sont les verbes du design"
  - "par quoi je commence"
  - "quelle séquence pour mon cas"
  - "detail"
requires:
  - "aucun artefact requis — `route` lit l'état du contrat s'il existe, `explain` fonctionne sans contrat"
references:
  - ${CLAUDE_PLUGIN_ROOT}/skills/detail/references/funnel-map.md
  - ${CLAUDE_PLUGIN_ROOT}/skills/detail/references/workflow-classes.md
  - ${CLAUDE_PLUGIN_ROOT}/references/sc-pivot-contract.md
---

# detail

## Rôle dans l'entonnoir

```
detail (0) → define → destructure → adjust (figé) → enforce (GATE) → diffuse
```

Verbe 0 : il ne fait avancer aucun contrat, il en donne la carte. Les six autres verbes plus `harness` produisent ou vérifient ; `detail` seul lit et restitue.

## Routage des actions

| Question du consommateur | Action | Ce qu'elle rend |
|---|---|---|
| *que fait ce plugin / ce verbe / ce gate* | `01-explain` | la carte, à la granularité demandée |
| *par quoi je commence / quelle séquence pour mon cas* | `02-route` | la classe de cas, sa séquence, ses checkpoints, ses gates |

La bascule est sur la nature de la question, pas sur un mot-clé : une demande **descriptive** (ce que c'est) va à `explain` ; une demande **prescriptive** (quoi lancer, sur mon terrain) va à `route`. Une intention qui ne porte sur ni l'un ni l'autre ne déclenche pas le skill.

## Règles transversales

- **Lecture seule.** `detail` n'écrit aucun artefact et ne modifie ni contrat ni source. C'est le seul skill du plugin sans sortie.
- **N'exécute pas ce qu'il décrit.** Il émet une séquence de verbes et s'arrête. Lancer `enforce` ou `diffuse` reste au consommateur ; `route` ne les invoque jamais.
- **Ne paraphrase pas un processus.** Le rôle et les entrées/sorties d'un verbe viennent de `funnel-map.md` ; son comment vit dans son propre `SKILL.md`, cité, jamais recopié (dec-001).
- **Ne corrige pas en silence.** Si la classe énoncée par le consommateur contredit l'état observé du contrat, `route` **signale** l'écart au lieu de le masquer.

## Références

- `${CLAUDE_PLUGIN_ROOT}/skills/detail/references/funnel-map.md` — la carte : un verbe par ligne, chacun avec son fichier autoritaire. Lue par `01-explain`.
- `${CLAUDE_PLUGIN_ROOT}/skills/detail/references/workflow-classes.md` — les six classes de cas. Lue par `02-route`.
- `${CLAUDE_PLUGIN_ROOT}/references/sc-pivot-contract.md` — squelette du workflow de plateforme et règle de résolution des pivots.
