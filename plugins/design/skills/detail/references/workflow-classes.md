# Classes de cas

Six classes, **exhaustives** sur la signature d'entrée (ce que le consommateur détient) croisée avec l'état du contrat (absent, brouillon, figé). Aucune ne recouvre une autre sur la même paire. Ensemble fermé : un terrain nouveau est une classe existante, ou un amendement à ce fichier — jamais une septième classe improvisée.

Déclarées une seule fois ici ; `02-route` les lit, aucun autre fichier ne les énumère. Les verbes de chaque séquence renvoient à `funnel-map.md` pour leur rôle ; ce fichier n'en répète pas le processus.

`harness` n'est pas une classe : c'est la **précondition** de toute classe dont la référence n'existe pas encore comme artefact mesurable ou dont le HTML n'est pas au format canonique. `route` l'énonce comme précondition de `mockup-multipage`, jamais comme une étape.

**Extension par un workflow de plateforme.** Chaque classe est agnostique. Quand le pivot correspondant est installé et la stack correspond, son workflow de plateforme (`sc-pivot-contract.md § Workflow de plateforme`) **étend** la classe : il instancie nativement les phases `enforce` et `diffuse` et ajoute **les phases `off-funnel` que sa table `## Phases` déclare**, chacune à la position qu'elle déclare. Ce fichier n'en énumère aucune : la liste vit dans le pivot, qui en est l'autorité, et toute énumération faite ici dérive dès qu'un pivot ajoute une phase. Pivot absent ou stack non correspondante → la classe seule, l'absence énoncée. La règle de résolution est portée par `02-route`.

---

## `mockup-multipage`

- **Signature d'entrée** : une référence visuelle de plusieurs pages fait autorité.
- **État du contrat** : absent.
- **Précondition** : la référence doit être mesurable et son HTML canonique ; sinon `harness` d'abord.
- **Séquence** : `define` (intake, fan-out copycat) → **checkpoint humain sur la table de correspondance** → `adjust` → `enforce` (vocabulaire + fidélité) → `diffuse`.
- **Checkpoint humain** : la table de correspondance avant figeage — rejet ⇒ retour à `define`.
- **Gate de sortie** : vocabulaire **et** fidélité verts au seuil de maturité.
- **Condition d'arrêt** : les deux gates verts au seuil, éléments diffusés.
- **Point d'extension** : `enforce`/`diffuse` natifs + phases off-funnel du pivot.

## `brief-only`

- **Signature d'entrée** : une intention écrite, aucun visuel.
- **État du contrat** : absent.
- **Séquence** : `define` (intake, construction) → `destructure` → `adjust` → `enforce` (vocabulaire ; fidélité seulement si une référence est produite plus tard) → `diffuse`.
- **Checkpoint humain** : la direction construite avant figeage.
- **Gate de sortie** : vocabulaire vert au seuil ; fidélité sans objet tant qu'aucune référence n'existe.
- **Condition d'arrêt** : gate vocabulaire vert au seuil ; si une référence est produite ensuite, ré-entrer par le gate de fidélité.
- **Point d'extension** : `enforce`/`diffuse` natifs + phases off-funnel du pivot.

## `codebase-inherited`

- **Signature d'entrée** : une source existe, aucun contrat.
- **État du contrat** : absent.
- **Séquence** : `destructure` autonome → `define` par extraction depuis le rendu → `adjust` → `enforce` → boucle de réconciliation.
- **Checkpoint humain** : le contrat extrait valide-t-il l'intention observée dans la source.
- **Gate de sortie** : vocabulaire vert au seuil sur la source réconciliée.
- **Condition d'arrêt** : la boucle s'arrête quand le contrat extrait linte la source sans violation, ou que les divergences restantes sont arbitrées.
- **Point d'extension** : `enforce` natif sur la source + phases off-funnel du pivot.

## `element-evolution`

- **Signature d'entrée** : un élément doit évoluer.
- **État du contrat** : figé.
- **Séquence** : `destructure` autonome → `adjust` re-figeage du delta → `enforce` re-dérivation → `diffuse`.
- **Checkpoint humain** : le delta avant re-figeage (bump de version).
- **Gate de sortie** : gate re-dérivé vert au seuil sur l'élément évolué.
- **Condition d'arrêt** : delta re-figé, gate re-dérivé vert, élément diffusé.
- **Point d'extension** : `enforce`/`diffuse` natifs + phases off-funnel du pivot.

## `contract-drift`

- **Signature d'entrée** : les instances divergent du contrat, ou le contrat a été re-figé.
- **État du contrat** : figé.
- **Séquence** : `adjust` delta si la divergence est arbitrée → `enforce` re-dérivation et lint des instances → boucle corriger / propager / re-linter.
- **Checkpoint humain** : arbitrage de la divergence — instance à corriger, ou contrat à ajuster.
- **Gate de sortie** : vocabulaire vert au seuil sur toutes les instances.
- **Condition d'arrêt** : la boucle s'arrête quand les instances re-lintent sans violation contre le contrat (re)figé.
- **Point d'extension** : `enforce` natif sur les instances + phases off-funnel du pivot.

## `element-production`

- **Signature d'entrée** : un élément doit être livré.
- **État du contrat** : figé, gates verts.
- **Séquence** : `diffuse` seul.
- **Checkpoint humain** : aucun imposé — le contrat fait déjà autorité.
- **Gate de sortie** : `diffuse` sort en 0 contre le gate `enforce`.
- **Condition d'arrêt** : élément produit, gate `enforce` toujours vert.
- **Point d'extension** : `diffuse` natif + phase off-funnel de déploiement du pivot.
