# Par où commencer

Cette page répond à « quelle séquence pour mon cas ». Le **pourquoi** de chaque pièce est dans [`concepts.md`](concepts.md) ; le détail d'exécution de chaque verbe vit dans son propre `SKILL.md`, cité ici, jamais recopié.

## La réponse courte

Invoquer la capacité `design:detail` dans l'hôte courant.

Le verbe 0 lit l'état de ton contrat et les pivots installés, classe ton intention, et émet la séquence exécutable avec ses checkpoints et ses gates. Il n'exécute rien de ce qu'il décrit — tu gardes la main sur chaque lancement.

Le reste de cette page est ce que `detail` te dirait, sous forme consultable.

## Les six classes de cas

Elles sont **exhaustives** sur la signature d'entrée (ce que tu détiens) croisée avec l'état du contrat (absent · brouillon · figé). Aucune ne recouvre une autre sur la même paire. Un terrain nouveau est l'une de ces six, ou un amendement à [`workflow-classes.md`](../skills/detail/references/workflow-classes.md) — jamais une septième improvisée.

### `mockup-multipage` — j'ai des maquettes de plusieurs pages

> Contrat absent · une référence visuelle multi-pages fait autorité.

```
[harness si la référence n'est pas mesurable]
  → define (intake + fan-out copycat)
  → ⏸ checkpoint humain : la table de correspondance
  → adjust → enforce (vocabulaire + fidélité) → diffuse
```

**Précondition** : la référence doit être *mesurable*. Un PDF ou un JPEG ne l'est pas — `harness` scaffolde alors le fichier HTML autonome que l'oracle sait piloter. C'est une précondition, pas une étape de la classe.

**Checkpoint** : la table de correspondance agrégée, avant figeage. Un rejet renvoie à `define`. Les conflits entre pages y sont remontés, pas arbitrés — l'arbitrage est le travail d'`adjust`.

**Sortie** : les deux gates verts au seuil de maturité.

### `brief-only` — j'ai une intention écrite, aucun visuel

> Contrat absent · un brief, un positionnement, une user story.

```
define (intake + construction) → destructure → adjust → enforce (vocabulaire) → diffuse
```

**Checkpoint** : la direction construite, avant figeage.

Le gate de fidélité est **sans objet** tant qu'aucune référence n'existe — il n'y a rien contre quoi mesurer. Si une maquette est produite plus tard, on ré-entre par ce gate.

C'est la classe où `destructure` compte le plus : sans visuel de référence, rien ne s'oppose naturellement au « plausible générique ».

### `codebase-inherited` — j'ai une source, aucun contrat

> Contrat absent · le code existe et fait foi de fait.

```
destructure (autonome) → define (extraction depuis le rendu) → adjust → enforce → boucle de réconciliation
```

L'ordre est inversé par rapport aux autres classes : on critique **avant** d'extraire, pour ne pas canoniser l'accident. `destructure` en mode standalone répond ici à « on a hérité de ce codebase, quel est l'état du design ».

**Checkpoint** : le contrat extrait valide-t-il l'intention observée dans la source ?

**Condition d'arrêt** : la boucle s'arrête quand le contrat extrait linte la source sans violation, ou que les divergences restantes sont arbitrées — pas quand la source est parfaite.

### `element-evolution` — un élément doit changer

> Contrat **figé** · un composant existant doit évoluer.

```
destructure (autonome) → adjust (re-figeage du delta) → enforce (re-dérivation) → diffuse
```

`adjust` est explicitement rejouable. Il ne rejoue que sur le **delta** : les composants et tokens non touchés sont conservés. La version est bumpée en mineur (ajout) ou en majeur (renommage, suppression).

**Checkpoint** : le delta avant re-figeage — c'est là qu'on assume le bump.

### `contract-drift` — les instances ont divergé

> Contrat **figé** · le code ne respecte plus le contrat, ou le contrat vient d'être re-figé.

```
adjust (delta, si la divergence est arbitrée) → enforce (re-dérivation + lint des instances)
  → boucle corriger / propager / re-linter
```

**Checkpoint** : l'arbitrage de la divergence. La question est toujours la même et elle n'a pas de réponse par défaut — *l'instance est-elle fautive, ou le contrat est-il en retard ?*

### `element-production` — je livre un élément

> Contrat **figé**, gates verts.

```
diffuse
```

Aucun checkpoint imposé : le contrat fait déjà autorité. C'est le régime de croisière — celui où le plugin cesse de coûter du temps.

## Parcours nominal, de zéro

Pour un projet neuf avec un brief, dans l'ordre :

```text
design:define          # poser la matière — tokens de travail, inventaire, charte brouillon
design:destructure     # challenger la direction avant de la figer
design:adjust          # arbitrer + figer le contrat
design:enforce         # dériver le linter, câbler les gates
design:diffuse <comp>  # produire, sous gate
```

Puis, en régime établi : invoquer `design:diffuse` pour chaque nouvel élément, et revenir à
`design:adjust` quand le contrat doit bouger.

## Les checkpoints humains

Trois moments où le plugin s'arrête et demande, plutôt que de trancher :

| Moment | Question posée | Pourquoi elle n'est pas automatisée |
|---|---|---|
| Table de correspondance (avant `adjust`) | ces contributions tokens/composants sont-elles justes ? | `copycat` propose et ne fige jamais ; les conflits inter-pages remontent bruts |
| Arbitrage `adjust` | quelle option gagne quand le motif dominant ne tranche pas ? | le motif dominant décide à ≥ 2/3 ; en deçà, c'est un choix de direction |
| Divergence `contract-drift` | corriger l'instance, ou ajuster le contrat ? | les deux réponses sont défendables et l'outil ne sait pas laquelle tu veux |

Le reste — dérivation des règles, mesure, calcul du statut — est déterministe et ne demande rien.

## Extension par un pivot `sc-*`

Chaque classe est **agnostique de la stack**. Quand le pivot correspondant est installé et que la stack correspond, son *workflow de plateforme* étend la classe : il instancie nativement les phases `enforce` et `diffuse` et ajoute ses phases hors-entonnoir (environnement, déploiement, recette).

Pivot absent ou stack non correspondante → la classe seule s'applique, et l'absence est énoncée plutôt que silencieuse. Le squelette de ces workflows est figé par [`sc-pivot-contract.md`](../references/sc-pivot-contract.md) ; ils vivent dans les pivots, pas ici.

## Le profil mobile-first

`define` propose — et n'impose pas — le profil `profile-mobile-first.md` : sept conventions (authoring mobile-first, enrichissement progressif, UX mobile-only, tokens sans magic number, composants à variantes, baseline a11y, iconographie sans emoji). Il s'installe dans `.claude/rules/08-design/` uniquement s'il est retenu.

## Voir aussi

- [`concepts.md`](concepts.md) — le modèle mental derrière ces séquences
- [`troubleshooting.md`](troubleshooting.md) — quand un gate sort en rouge
- [`workflow-classes.md`](../skills/detail/references/workflow-classes.md) — la déclaration normative des six classes
