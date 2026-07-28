# Decision: `docs/control.md` fait autorité sur `skills/control/`, et les six divergences sont tranchées

| Field   | Value |
|---------|-------|
| ID      | DEC-006 |
| Date    | 2026-07-27 |
| Feature | `overcode` — alignement DDD de `control` : la page porte le modèle, la skill le réalise |
| Status  | Accepted |

## Context

`docs/control.md` a été écrite comme le modèle de la skill, mais un inventaire règle par règle en montre autre chose : sur 84 règles normatives, **41 figurent aux deux endroits, 6 sont plus faibles sur la page, 43 n'existent que dans `skills/control/`, et 6 se contredisent.**

Trois conséquences observées :

- **L'autorité était inversée dans les faits.** L'encart d'origine annonçait que la skill faisait foi. Une page qui décrit sans obliger devient un résumé, et un résumé se périme sans que rien ne le signale — c'est exactement ce qui est arrivé aux six règles affaiblies.
- **Une règle de `references/` peut fonder une règle voisine sans être une règle elle-même.** `phase-framework.md:201` justifie l'invariant des domaines par une analogie avec la phase (« same boundary as the phase, for the same reason »). Un inventaire règle par règle ne voit pas ce lien : il n'est une règle ni d'un côté ni de l'autre. Il n'a été découvert qu'au moment de trancher D5.
- **Deux fichiers d'action se contredisent en interne**, pas seulement avec la page — `02-audit` entre ses étapes 4 et 5, `06-align` entre son annonce d'exclusion totale et ce qu'il décrit ensuite.

## Decision

### 1 — La page fait foi, la skill est en retard

En cas de divergence, `docs/control.md` a raison par construction et `skills/control/` est un défaut à corriger. Le partage de charge qui rend cette autorité tenable :

| Porte | Quoi |
|---|---|
| la page | la règle et son **motif** |
| la skill | la règle et sa **procédure** |
| cet ADR | le **rationnel** des arbitrages, qui n'a sa place ni dans l'une ni dans l'autre |

Aucune étape de `## Process` ne remonte sur la page. Sans cette borne, la page redevient un doublon de la skill et la dérive est garantie au bump suivant.

### 2 — Les six arbitrages

| # | Divergence | Camp retenu | Motif |
|---|---|---|---|
| **D1** | `02-audit:34` admet un lot que l'utilisateur nomme ; `:35` et la page interdisent tout retrait sans confirmation individuelle | **la skill** | La page décrivait un absolu qu'aucune action n'applique. Ce que `:35` protège réellement, c'est que **la phase** ne change aucun régime de confirmation — pas l'interdiction du lot |
| **D2** | `06-align:99` exclut `default` **et** `undetermined` de toute bascule, puis décrit une demi-bascule | **la page** | `undetermined` bascule normalement dès qu'une phase est déclarée. `default` n'en est exclu ni par mécanique ni par neutralité, mais par **consentement** : c'est une décision écrite, et une bascule y contredirait le choix qui vient d'être posé |
| **D3** | `04-strengthen:71` admet un lot d'**ajouts** ; `:73` en encadre les effets | **la page** | Chaque ajout déplace l'arithmétique de la contrainte de nombre pour le suivant : un lot approuvé d'un bloc ne peut pas avoir été évalué contre une contrainte que le lot lui-même fait bouger. Une suppression n'a pas cette propriété — elle ne fait que desserrer. **L'asymétrie ajouts/suppressions est le motif, pas une incohérence** |
| **D4** | `scope` désigne deux ou trois univers selon l'action | **un seul univers** | Le code source **et les tests qui lui correspondent**, partout. Résolution **symétrique** du glob : un chemin tombant dans l'arbre de tests remonte vers sa source, et réciproquement. `scope=tests/legacy/` reste donc exprimable |
| **D5** | Le tableau des autorités donne à la phase « ce qui est analysé » ; la skill fait piloter l'univers par le glob source réduit par `scope` | **la page** | La phase borne l'univers — **à condition de lister ce qu'elle écarte** |
| **D5 bis** | `phase-framework.md:201` pose que la phase ne restreint pas, et en fait le précédent qui fonde l'invariant des domaines | **la page** | Ce que la référence interdit n'est pas la restriction, c'est la restriction **silencieuse** : « un faux négatif silencieux coûte le manque que la skill existe pour empêcher ». Une phase qui écarte en listant n'en produit aucun. L'analogie phase↔domaine tombe ; l'invariant des domaines, lui, reste — mais il devra désormais porter son motif propre |
| **D6** | La page fait piloter à la phase « la lecture du rapport de couverture » ; `04-strengthen:47` refuse explicitement toute variation de cette lecture | **la page, corrigée** | Le mot « lecture » recouvrait deux choses sans les distinguer. La phase décide **quels fichiers entrent** dans la lecture (c'est D5) et **comment le résultat se classe** ; elle ne décide jamais **ce qu'une donnée y signifie**. Une absence du rapport vaut « non couvert » dans toutes les phases, faute de quoi un modulateur trancherait une mesure |

**D4, D5, D6 sont des corrections de la page, pas des exceptions au principe d'autorité.** Une page qui fait foi doit pouvoir être corrigée sur le fond ; ce qu'elle ne peut pas, c'est perdre l'arbitrage par prescription parce que la skill a divergé sans que personne ne s'en aperçoive.

### 3 — La frontière `control` / `behave` est logée dans `workflow.md`

Le test comportemental des skills et des agents relève de `behave`. Cette règle (C43) décrit **quelle skill pour quelle situation**, ce qui est le rôle déclaré de `workflow.md` ; `control.md` décrit un modèle interne. Un seul emplacement, jamais les deux.

## Consequences

- **Deux régimes de confirmation coexistent, et l'asymétrie est délibérée.** Retirer admet un lot nommé par l'utilisateur ; ajouter reste ligne à ligne. La page doit énoncer le motif, sans quoi la règle se lit comme une incohérence et sera « corrigée » par le prochain lecteur.
- **`05-stats` gagne une table** — ce que la phase a écarté de l'univers, avec son compte. Sans elle, D5 devient la restriction silencieuse que D5 bis interdit.
- **`phase-framework.md:199-203` perd son argument par analogie.** La règle des domaines reste, sa justification doit être réécrite en propre.
- **Trois corrections attendues côté skill** (D1, D2, D3) ne touchent pas la page et sont reportées telles quelles en part-3.
- L'ordre page → suites `behave` rouges → skill n'est pas cosmétique : `behave` teste des sorties, jamais la cohérence entre deux documents normatifs. Une incohérence page/référence introduite par le mauvais bout n'aurait été détectée par rien.

## Alternatives rejetées

- **Laisser la skill faire foi et réduire la page à un résumé.** C'est l'état de départ. Il produit exactement la dérive constatée : 43 règles invisibles à qui lit la page, et six règles affaiblies que rien ne signale.
- **Remonter les 43 règles avec leur procédure.** Deux sources complètes à maintenir, donc une divergence garantie. La borne règle+motif / règle+procédure est ce qui rend la remontée soutenable.
- **Interdire à la phase de borner l'univers (D5, recommandation initiale).** Cohérent avec `phase-framework.md:201`, mais laissait le modèle sans détenteur du périmètre : ni la phase, ni les domaines, ni la table des tiers, ni `control` ne décidaient de l'univers analysé.
- **Faire changer à la phase le sens d'une absence de rapport (D6, camp de la page non corrigée).** Aurait fallu dire dans quelle phase une absence cesse de valoir « non couvert », et aurait fait trancher une mesure par un modulateur — la frontière sur laquelle tout le modèle repose.
