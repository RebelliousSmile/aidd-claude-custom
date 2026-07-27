# `control` — le modèle

> **État.** Ce document a été écrit **en avance** de la skill, puis `skills/control/` a été aligné sur lui — `SKILL.md`, les deux références et les six actions. Les deux disent désormais la même chose ; en cas de divergence constatée, c'est la skill qui fait foi et cette page qui est en retard.

`control` gouverne une suite de tests : ce qui mérite d'exister, ce qui ne le mérite plus, ce qui manque et ce que le projet dit de lui-même. Elle **ne rédige aucun test** — elle décide, puis délègue à `aidd-dev:06-test`.

Elle porte `disable-model-invocation: true` : elle ne se déclenche jamais seule. C'est délibéré — une skill qui propose de supprimer des tests ne doit pas s'inviter.

## Les trois autorités

Tout le modèle tient dans une séparation : **trois autorités distinctes, qui ne se recouvrent jamais.**

| Autorité | Décide | Ne décide jamais |
|---|---|---|
| **Table des tiers** | le tier d'un test : `contract` · `e2e` · `skip` | rien d'autre |
| **Phase** | ce qui est analysé, comment c'est pondéré, dans quel ordre c'est restitué | aucun tier |
| **Domaines** | quelles parties du code sont sous contrôle en priorité | aucun tier, aucune exclusion |

C'est l'invariant central, et il est écrit à l'identique dans neuf endroits de la skill :

> **La phase priorise ; elle ne classe jamais un tier.** Un test est refusé sur un critère de tier, jamais « parce qu'on est en production ».

Le même énoncé borne les deux autres mécanismes de pondération — la densité, et les *Risk signals* du pivot. Trois modulateurs, une seule autorité de classement. Quand on lit une ligne de la skill qui semble donner un pouvoir de classement à autre chose que la table des tiers, c'est un défaut, pas une exception.

### Qui remplit la table des tiers

Par ordre de précédence :

1. la stratégie de test documentée du projet — conventionnellement `aidd_docs/memory/testing.md` ;
2. `references/decision-framework.md`, le défaut générique de la skill, sinon.

Le pivot `testing` du plugin de langage vient par-dessus : il apporte la mécanique propre à la stack, et **peut** raffiner un tier via ses *Tier thresholds* — mais seulement quand la frontière concernée reste locale ou émulée. Un pivot ne reclasse jamais un cas qui traverse une vraie frontière externe.

## La phase

La phase répond à une question que le dépôt ne peut pas trancher : **est-ce que quelqu'un s'en sert ?** Un dépôt montre ce qui a été construit ; il ne montre pas s'il y a des utilisateurs, et c'est le seul point sur lequel la phase se décide.

Elle n'est donc **jamais déduite**. Elle vient d'un argument explicite, d'une déclaration dans la documentation du projet, ou d'une question posée à l'utilisateur avant que quoi que ce soit ne soit classé ou proposé.

| Phase | La question binaire qui la définit |
|---|---|
| `scaffolding` | le modèle de domaine bouge-t-il encore ? |
| `hardening` | modèle figé, mais pas encore d'utilisateurs réels ? |
| `production` | des utilisateurs réels, et des données irremplaçables ? |
| `sustaining` | le nouveau code a-t-il cessé d'arriver ? |
| `default` | neutralité **choisie** et déclarée |
| `undetermined` | la question a été posée, elle est restée sans réponse |

Ce que la phase pilote concrètement : la pondération des six critères de risque, la lecture du rapport de couverture, l'ordre des tables produites, et — au moment d'un changement de phase — la qualification d'un lot de tests devenus obsolètes.

### Valeur et provenance sont deux axes

Chaque action rapporte **deux** lignes sur la phase, jamais fusionnées :

| Axe | Répond à | Valeurs |
|---|---|---|
| **valeur** | *quelle phase est en vigueur* | `scaffolding` · `hardening` · `production` · `sustaining` · `default` · `undetermined` |
| **provenance** | *d'où vient cette valeur* | `argument` · `declared <chemin>` · `answered` · `unanswered` |

La provenance est nommée par la paire `answered` / `unanswered` délibérément. L'appeler `undetermined` était le raccourci évident et le mauvais : `undetermined` est une **phase**, et le réutiliser comme provenance faisait dire au même mot *quelle phase* sur une ligne et *d'où elle vient* sur l'autre. La confusion restait invisible tant que les deux coïncidaient ; c'est `default` qui l'a rendue lisible, puisqu'un `default` arrivé par argument, par déclaration ou par une réponse orale sont trois situations qu'une ligne fusionnée ne sait pas distinguer.

**Un seul appariement est forcé** : `unanswered` ⇔ `undetermined`, les deux faces du même non-événement. Toutes les autres combinaisons sont libres — et c'est ce qui explique qu'un `default` *déclaré* ne déclenche aucun renvoi vers `06-align`, là où un `default` seulement *répondu* en déclenche un comme n'importe quelle autre réponse orale : dite à voix haute, écrite nulle part, elle sera redemandée au run suivant.

### `default` et `undetermined`

Les deux utilisent la pondération neutre. Ils diffèrent sur ce qui est observable :

| | `default` | `undetermined` |
|---|---|---|
| Origine | choix déclaré | question sans réponse |
| La question se repose | non, **une fois déclaré** | à chaque exécution |
| Lot de suppression | aucun | selon la phase réelle, une fois connue |
| Changement de phase | ne s'y applique pas | s'applique dès qu'une phase est déclarée |
| Ordre d'axes attendu | aucun — et c'est déclaré | aucun |

`default` est la réponse à un besoin précis : utiliser les actions sans biais de classement ni de suppression, **sans pour autant se faire redemander la phase à chaque fois**. C'est la différence entre « je ne veux pas de pondération » et « je n'ai pas répondu ».

## Les domaines

Un domaine est une part fonctionnelle du produit — `auth`, `paiement`, `checkout` — résolue dans le code par des termes : `Login`, `Register`, `SessionGuard`.

Les domaines dépendent des *core features* du projet. Il n'en existe aucun d'universel : une bibliothèque, un outil en ligne de commande, un jeu n'ont ni authentification ni paiement. La skill ne peut donc rien en proposer par défaut.

### Qui déclare quoi

| Connaissance | Détenteur | Pourquoi |
|---|---|---|
| **quels** domaines existent | le projet, dans son `testing.md` | personne d'autre ne le sait |
| **comment** les repérer dans cette stack | le pivot du plugin de langage | c'est de la convention de stack, et elle périme vite |

Séparés ainsi, ils ne peuvent pas se contredire — donc aucune règle d'arbitrage n'est nécessaire. Le pivot **complète** une déclaration incomplète du projet ; il n'écrase jamais une résolution que le projet a explicitement écrite sur son propre code.

C'est le même partage d'autorité que la skill applique déjà aux frontières externes : `control` possède le critère générique, le pivot possède l'inventaire.

### Le garde-fou

**Un domaine priorise, il ne restreint pas.** Ce qui n'est matché par aucun domaine reste dans l'analyse — il descend simplement dans l'ordre — et **il est rapporté**, avec le terme qui a échoué à le reconnaître.

La raison est concrète : chercher `Login` et `Register` trouve `LoginForm.tsx` et rate `SessionController`. Un faux négatif silencieux déclarerait hors périmètre un pan central du code sans que personne ne le voie. La trace évite ça — et elle sert une seconde fois, en alimentant la détection de dérive de `06-align`.

## Les axes de lecture

`control` lit une suite selon deux axes, et compare des **ordres**, jamais des parts. Aucun pourcentage n'est produit.

- **`foundations`** — invariants du modèle, validation, transformations partagées. Axe structurel.
- **les domaines** — axe fonctionnel, déclaré par le projet. En leur absence, `critical journeys` (actes visibles du client, opérations irréversibles, frontières externes) sert de repli générique et approximatif.

Le troisième bucket historique, `recent code`, a disparu : ce qu'il décrivait est le critère **`churn`**, qui existe déjà dans le classement par risque. Il n'a pas besoin d'exister deux fois.

### Les six critères de risque

C'est ce que `04-strengthen` pondère, repondéré par la phase :

| Critère | Ce qu'il mesure |
|---|---|
| **Consequence** | argent, autorisations, persistance, suppression — tout échec silencieux non évident pour l'utilisateur |
| **Branching** | nombre de branches non testées |
| **Churn** | fréquence des changements récents, et la part de ces commits qui étaient des correctifs |
| **Blast radius** | combien d'appelants en dépendent |
| **Absence de tout autre filet** | ni type, ni validation runtime, ni parcours e2e qui traverse déjà ce chemin |
| **Dépendance à un contrat externe** | SDK, conteneur de tags, client d'API sortant — ce qui casse sans qu'une ligne du dépôt bouge |

`churn` garde son nom anglais. Le terme est légèrement infidèle à ce qu'il mesure — il inclut la part de correctifs, pas seulement le volume de modification — mais il sert de renvoi entre trois fichiers de la skill, et le renommer coûterait plus qu'il ne clarifie.

## La densité, pas le compte

La contrainte de nombre de cette skill est une **densité** : les cas de test qui exercent un fichier, rapportés à ses points de branchement, lus **contre la médiane de la distribution du projet lui-même** — jamais contre un seuil absolu importé d'ailleurs. Alerte au-delà de 3× la médiane.

Deux règles la bornent, et elles ne bougent pas :

- **la densité signale et priorise ; elle ne refuse jamais, et ne change aucun tier** ;
- **elle n'est pas une cible** — proposer du travail dont la seule justification serait de rapprocher une densité de la médiane, c'est l'erreur du pourcentage de couverture portant un autre chiffre.

Et la règle mère, dont tout ceci découle :

> Le pourcentage de couverture est un symptôme, jamais une cible. Aucune action de cette skill ne propose un travail dont la seule justification serait de faire monter un chiffre de couverture.

C'est ce qui explique que la phase pondère et donne du sens, mais ne fixe jamais de seuil chiffré par phase. Un seuil transformerait le pourcentage en cible et ferait tomber la règle.

## Le chaînage

```
                        05-stats                point d'entrée
                     /     |    |    \
                    v      v    v     v
         03-configure  02-audit |  06-align
          (terminale)      ^    |    /   |
                           |    v   v    |
                           +- 04-strengthen
                                   |     |
                                   v     v
                                   01-write       puits
                                      |
                                      v
                             aidd-dev:06-test
```

Arête par arête, et rien d'autre n'est une arête : `05-stats` route vers les quatre actions qui agissent ; `04-strengthen` renvoie un fichier saturé vers `02-audit` ; `06-align` mobilise les motifs de `02-audit` et rejoue le classement de `04-strengthen` lors d'un changement de phase ; `04-strengthen` passe chaque manque confirmé à `01-write`, qui délègue à `aidd-dev:06-test`.

Trois propriétés portées par ce graphe :

- **`05-stats` est le point d'entrée.** C'est la seule action qui route vers quatre des cinq autres. Quand on ne sait pas par où commencer, on commence là.
- **`01-write` est le puits.** Tout nouveau test y entre, quelle que soit l'action qui l'a fait remonter. Aucune action n'écrit de test en contournant ce passage. **`02-audit` n'a aucune arête vers lui**, et ce n'est pas un oubli : un audit retire, il n'origine jamais un test.
- **`03-configure` est hors modèle.** Elle vérifie le câblage du tooling — un *gate* de couverture déclaré mais qu'aucun hook n'invoque, un seuil que sa propre configuration désactive en silence. Ces défauts sont vrais ou faux indépendamment de la phase et des domaines. Elle ne prend donc ni `phase`, ni `domain`, ni `scope`. Elle est **atteignable et terminale** : `05-stats` y route, elle ne route vers rien.

### La balance nette

`02-audit` retire, `04-strengthen` ajoute. La différence est un **constat, jamais un objectif** : aucune phase n'exige un solde négatif. `sustaining` s'attend à en avoir un, elle ne l'exige pas. Une suite qui ressort d'un changement de phase plus grosse qu'elle n'y est entrée n'est pas un échec.

## Les paramètres

| Action | `project_path` | `scope` | `domain` | `phase` | autre |
|---|---|---|---|---|---|
| `01-write` | requis | — | — | optionnel | `behavior` requis |
| `02-audit` | requis | suite de tests | optionnel | optionnel | — |
| `03-configure` | requis | — | — | — | — |
| `04-strengthen` | requis | code source | optionnel | optionnel | `top_n` (défaut 5) |
| `05-stats` | requis | code source | optionnel | optionnel | — |
| `06-align` | requis | code source | optionnel | optionnel | — |

Trois règles à retenir :

- **`scope` ne désigne pas le même univers partout.** Dans `02-audit` il limite la **suite de tests** ; dans les trois autres, le **code source**. Chaque action déclare sa cible dans son propre bloc d'entrée.
- **`scope` et `domain` sont exclusifs.** L'un est structurel (un chemin, un glob), l'autre sémantique (un nom de domaine). Si les deux sont fournis, la skill **s'arrête et le dit** — elle n'applique aucune précédence implicite.
- **`phase` en argument ne vaut que pour l'exécution en cours.** Il n'est jamais écrit dans le document du projet. Seule `06-align` transforme une réponse en déclaration, et seulement après validation.

## Les confirmations

Aucune suppression n'a lieu sans confirmation de la ligne concernée, une par une — la phase peut réordonner la table autant qu'elle veut, elle ne change pas ce régime.

L'unique exception est bornée : lors d'un **changement de phase**, `06-align` présente un lot caractérisé. Et même là, trois catégories de tests sont exclues de tout lot, quel que soit le changement — ceux qui couvrent une frontière externe, ceux qu'un critère de conséquence retient par ailleurs, et ceux qui sont le seul filet sur leur sujet.

Appartenir à un axe que la phase fait descendre n'est, en soi, jamais une raison de supprimer quoi que ce soit. Quand rien ne qualifie, le lot est vide — et un lot vide est un résultat légitime, rapporté comme tel.

## Voir aussi

- [`workflow.md`](workflow.md) — quelle skill pour quelle situation
- [`concepts.md`](concepts.md) — le modèle des pivots et les frontières entre skills
