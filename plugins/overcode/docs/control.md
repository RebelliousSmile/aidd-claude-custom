# `control` — le modèle

> **Autorité.** Cette page porte le modèle ; `skills/control/` le réalise. En cas de divergence, c'est cette page qui fait foi et la skill qui est en retard.
>
> La page porte la règle et son **motif** ; la skill porte la règle et sa **procédure**. Aucune étape d'exécution ne remonte ici.

`control` gouverne une suite de tests : ce qui mérite d'exister, ce qui ne le mérite plus, ce qui manque et ce que le projet dit de lui-même. Elle **ne rédige aucun test** — elle décide, puis délègue à `aidd-dev:06-test`.

Elle porte `disable-model-invocation: true` : elle ne se déclenche jamais seule. C'est délibéré — une skill qui propose de supprimer des tests ne doit pas s'inviter.

## Les quatre autorités

Tout le modèle tient dans une séparation : **quatre autorités distinctes, qui ne se recouvrent jamais.**

| Autorité | Décide | Ne décide jamais |
|---|---|---|
| **Table des tiers** | le tier d'un test : `contract` · `e2e` · `skip` | rien d'autre |
| **Phase** | ce qui est analysé — à condition de déclarer ce qu'elle écarte —, comment c'est pondéré, dans quel ordre c'est restitué | aucun tier, aucune restriction silencieuse |
| **Domaines** | quelles parties du code sont sous contrôle en priorité | aucun tier, aucune exclusion |
| **`control`** | ce qu'il a mesuré — et qu'il écrit sous sa propre autorité | la stratégie : phase déclarée, vocabulaire de tiers, liste des domaines, contrainte de nombre — proposée, jamais appliquée |

C'est l'invariant central, et il est répété à l'identique partout où la skill déclare un mécanisme de pondération :

> **La phase priorise ; elle ne classe jamais un tier.** Un test est refusé sur un critère de tier, jamais « parce qu'on est en production ».

Le même énoncé borne les trois autres mécanismes de pondération — les domaines, la densité, et les *Risk signals* du pivot. **Quatre modulateurs, une seule autorité de classement.** Quand on lit une ligne de la skill qui semble donner un pouvoir de classement à autre chose que la table des tiers, c'est un défaut, pas une exception.

Les modulateurs et les autorités ne se comptent pas ensemble, et les deux listes ne se recoupent que sur deux entrées : la densité et les *Risk signals* pondèrent sans rien décider — pas de ligne dans le tableau ; `control` décide sans rien pondérer — ce n'est pas un modulateur. Seules la phase et les domaines figurent dans les deux.

### Qui remplit la table des tiers

Par ordre de précédence :

1. la stratégie de test documentée du projet — conventionnellement `aidd_docs/memory/testing.md` ;
2. `references/decision-framework.md`, le défaut générique de la skill, sinon.

Le pivot `testing` du plugin de langage vient par-dessus : il apporte la mécanique propre à la stack, et **peut** raffiner un tier via ses *Tier thresholds* — mais seulement quand la frontière concernée reste locale ou émulée. Un pivot ne reclasse jamais un cas qui traverse une vraie frontière externe.

Un cas que rien ne tranche part sur **`contract`, l'ambiguïté signalée** — jamais sur `e2e` en silence. Le tier le plus cher ne se choisit pas par défaut.

## Le pivot

**L'autorité d'un pivot ne se donne jamais en général : champ par champ.** Un champ dont la borne n'est pas énoncée n'a aucune autorité à étendre. C'est ce qui empêche « le pivot connaît la stack » de devenir « le pivot décide de la stack ».

- **Un champ introuvable est absent**, et son repli documenté s'applique. Jamais une erreur, jamais une invitation à le déduire d'une section voisine — déduire un champ, c'est se donner l'autorité qu'on n'a pas trouvée.
- **L'absence de pivot n'est pas une erreur**, et elle se dit. Les actions retombent sur les conventions du projet et déclarent que la résolution est non assistée.

Le partage est le même partout où le pivot intervient : `control` possède le critère générique, le pivot possède l'inventaire propre à la stack.

## Le document du projet

La stratégie de test du projet — conventionnellement `aidd_docs/memory/testing.md`. Elle appartient à la **skill de mémoire projet d'`aidd-context`** ; `control` ne fait que la lire, à une exception près : `06-align`, et seulement après validation.

- **On la désigne par son rôle, jamais par un numéro d'action figé.** Un numéro appartenant à une autre skill se périme au premier renommage.
- **Un document qui ne tranche aucun tier est traité comme absent** pour la décision de tier. La correspondance forcée s'applique alors : unit + integration → `contract`, end-to-end → `e2e`. Il y a **trois formes**, et dire laquelle on a rencontrée fait partie du rapport, car elles n'appellent pas la même suite :
  1. **absent** — il n'y a rien à lire ;
  2. **présent mais vide** — le template n'a pas été rempli ;
  3. **présent, rempli, et ne tranchant aucun tier** — il énumère des *types* de test, des outils, des conventions, sans jamais dire ce qui mérite un test. C'est la forme la plus trompeuse : elle a l'apparence d'une stratégie et n'en gouverne aucune, de sorte qu'un lecteur pressé la croit décisive. Ne jamais la confondre avec la deuxième — un template à remplir et un document à faire décider appellent des corrections opposées.
- **Non documenté se rapporte comme non documenté**, jamais comme « suit implicitement le défaut ». Le budget est alors structurellement nul : sans limite écrite, il n'y a pas de limite à consommer.

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

Ce que la phase pilote concrètement : la pondération des six critères de risque, **quels fichiers entrent dans la lecture du rapport de couverture**, l'ordre des tables produites, et — au moment d'un changement de phase — la qualification d'un lot de tests devenus obsolètes.

### Borner en le disant

La phase peut réduire l'univers analysé. Elle ne peut pas le faire en silence : **tout fichier qu'elle écarte est listé, avec le motif de phase qui l'a écarté.**

C'est la seule forme de restriction que le modèle admet, et la raison est celle qui borne déjà les domaines : un faux positif coûte une ligne de bruit, un faux négatif silencieux coûte le manque que la skill existe pour empêcher. Une restriction déclarée n'est pas un faux négatif — c'est une décision qu'on peut relire et contester.

### Ce que la phase ne décide pas

**Ce qu'une donnée du rapport de couverture signifie ne change dans aucune phase.** Une absence du rapport vaut « non couvert » partout, quelle que soit la phase en vigueur.

La distinction est fine et elle porte tout le modèle : la phase décide **ce qui entre** dans la lecture et **comment le résultat se classe** ; elle ne décide jamais **ce que dit** ce qui a été lu. Une phase qui changerait le sens d'une absence trancherait une mesure, et un modulateur ne tranche pas de mesure. Le même fait se lit deux fois — en `scaffolding` une masse de fichiers jamais importés est l'état attendu et classe bas, en `sustaining` la même masse est le constat. Deux rangs, jamais deux faits.

### Valeur et provenance sont deux axes

Chaque action rapporte **deux** lignes sur la phase, jamais fusionnées :

| Axe | Répond à | Valeurs |
|---|---|---|
| **valeur** | *quelle phase est en vigueur* | `scaffolding` · `hardening` · `production` · `sustaining` · `default` · `undetermined` |
| **provenance** | *d'où vient cette valeur* | `argument` · `declared <chemin>` · `answered` · `unanswered` |

La provenance est nommée par la paire `answered` / `unanswered` délibérément. L'appeler `undetermined` était le raccourci évident et le mauvais : `undetermined` est une **phase**, et le réutiliser comme provenance faisait dire au même mot *quelle phase* sur une ligne et *d'où elle vient* sur l'autre. La confusion restait invisible tant que les deux coïncidaient ; c'est `default` qui l'a rendue lisible, puisqu'un `default` arrivé par argument, par déclaration ou par une réponse orale sont trois situations qu'une ligne fusionnée ne sait pas distinguer.

**Un seul appariement est forcé** : `unanswered` ⇔ `undetermined`, les deux faces du même non-événement. Toutes les autres combinaisons sont libres — et c'est ce qui explique qu'un `default` *déclaré* ne déclenche aucun renvoi vers `06-align`, là où un `default` seulement *répondu* en déclenche un comme n'importe quelle autre réponse orale : dite à voix haute, écrite nulle part, elle sera redemandée au run suivant.

**Quand l'argument et la déclaration divergent, la divergence est rapportée et l'argument l'emporte — pour l'exécution en cours seulement.** Une surcharge ponctuelle ne réécrit pas en silence ce que le projet a écrit. La phase est un attribut **du projet**, surchargeable sur un `scope` explicitement demandé ; il n'existe aucune découpe automatique par zone, faute d'une source de vérité fiable pour en produire une.

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

**Si `default` échappe à la bascule de phase, c'est par consentement, non par mécanique.** Un projet qui déclare `default` vient de poser une décision ; la faire suivre d'un lot de tests à qualifier obsolètes contredirait le choix à l'instant où il est pris. `undetermined` n'a rien décidé du tout : dès qu'une phase est déclarée, il bascule comme n'importe quelle autre.

## Les domaines

Un domaine est une part fonctionnelle du produit — `auth`, `paiement`, `checkout` — résolue dans le code par des termes : `Login`, `Register`, `SessionGuard`.

Les domaines dépendent des *core features* du projet. Il n'en existe aucun d'universel : une bibliothèque, un outil en ligne de commande, un jeu n'ont ni authentification ni paiement. La skill ne peut donc rien en proposer par défaut.

### Qui déclare quoi

| Connaissance | Détenteur | Pourquoi |
|---|---|---|
| **quels** domaines existent | le projet, dans son `testing.md` | personne d'autre ne le sait |
| **comment** les repérer dans cette stack | le pivot du plugin de langage | c'est de la convention de stack, et elle périme vite |

Séparés ainsi, ils ne peuvent pas se contredire — donc aucune règle d'arbitrage n'est nécessaire. Le pivot **complète** une déclaration incomplète du projet ; il n'écrase jamais une résolution que le projet a explicitement écrite sur son propre code.

### Le garde-fou

**Un domaine priorise, il ne restreint pas** — et contrairement à la phase, il ne restreint pas *du tout*, pas même en le déclarant.

La différence tient à la nature des deux : une phase écarte par **règle**, et une règle se relit. Un domaine écarte par **correspondance de terme**, et une correspondance échoue silencieusement. Chercher `Login` et `Register` trouve `LoginForm.tsx` et rate `SessionController` — la zone ratée ne ressort pas comme écartée, elle ressort comme une zone sans manque, ce qui est l'inverse exact de la vérité. Une exclusion par domaine serait donc invisible par construction.

Ce qui n'est matché par aucun domaine reste donc dans l'analyse — il descend simplement dans l'ordre — et **il est rapporté**, avec le terme qui a échoué à le reconnaître. La trace sert une seconde fois, en alimentant la détection de dérive de `06-align`.

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

### Densité et plafond ne se remplacent pas

**Un plafond de nombre déclaré par le projet l'emporte — en tant que plafond.** La densité est rapportée à côté, jamais à sa place : un plafond dit *combien*, une densité dit *si c'est au bon endroit*. Les deux réponses sont utiles et aucune ne contient l'autre.

**`limit` ne vient que d'une limite de nombre de tests explicite.** Un pourcentage de couverture n'est pas un budget et ne le devient jamais — le convertir en budget serait la transformation en cible que la règle mère interdit.

### Ce qu'un outlier dit, et ce qu'il ne dit pas

Un outlier admet **deux lectures, à discriminer avant d'en émettre une** :

- le fichier est dans le dernier décile de points de branchement → c'est un **signal de refactoring**, et **cette skill n'en propose aucun** ;
- sinon → beaucoup de cas sur peu de logique, c'est un sujet pour `02-audit`.

**Un outlier est un fichier à regarder, jamais un verdict rendu sur lui.** L'angle mort est connu et déclaré : la discrimination pilotée par la donnée n'entre pas au dénominateur, de sorte qu'un fichier dont chaque cas exerce une alternative distincte que le compteur ne voit pas ressort comme un outlier tout en étant sain.

### Les cas dégénérés, et leur ordre

L'ordre compte : **le fait le plus extérieur se rapporte une fois**, et il rend les autres sans objet.

1. **Aucun test du tout.** Un projet sans test n'a pas non plus de rapport de couverture ; mener avec le rapport suggérerait que le câbler est ce qui le sépare d'une densité. Ce n'est pas le cas.
2. **Aucun rapport de couverture.** Il n'y a alors **pas de dénominateur**, et la densité n'est pas calculée — ni approximée, ni remplacée par un compte de lignes. Rapporter *non mesurable, et pourquoi*, en nommant `03-configure` comme ce qui change cela. Un ratio inventé sur un dénominateur manquant est pire que la mesure absente qu'il remplace.
3. **Rapport présent, données de branche absentes.** La configuration la plus répandue en pratique : la couverture tourne en mode ligne, le suivi de branches n'a jamais été activé. Il y a donc un rapport et pas de dénominateur — le cas 2 ne s'applique pas, et rapporter « aucun rapport » serait faux. Ne pas recalculer les points de branchement : ils viennent du rapport ou la densité n'est pas calculée. Rapporter *rapport en mode ligne, densité non mesurable*, et nommer `03-configure` — la correction tient à un drapeau du lanceur, ce qui n'est pas la même conversation que câbler la couverture depuis zéro.
4. **Population insuffisante.** Ni médiane, ni outlier.

Dans tous les cas, **déclarer la règle de correspondance utilisée et le nombre de fichiers qu'elle n'a pas appariés**.

## Les bornes de mesure

Trois bornes, et aucune ne dépend de la phase.

- **L'univers classifiable vient du glob source du pivot.** Le rapport de couverture ne définit jamais l'univers ; il l'enrichit d'un détail de branches. `scope` le réduit ; `domain` non — et c'est toute la raison pour laquelle ce sont deux paramètres distincts.
- **Raisonner sur `covered`/`total`, jamais sur un pourcentage seul.** Un fichier sans branche rapporte 100 % de couverture de branches tout en étant entièrement non testé.
- **Un fichier présent au glob et absent du rapport est non couvert, pas inexistant.** Les rapports omettent couramment les fichiers qu'aucun test n'importe — c'est-à-dire exactement la population la plus exposée. Traiter l'absence comme de la couverture masquerait précisément les manques que la skill cherche.

## Les frontières externes

Écrire ce qu'un test prouve ici, et ce qu'il ne prouve pas, est ce qui empêche le critère de fabriquer de la fausse assurance.

**Prouvable en processus, au tier `contract`, sans appeler le fournisseur :**

- que la charge utile construite est celle que le code croit envoyer — champs, types, unités, identifiant réellement utilisé ;
- que le **chemin dégradé** se comporte correctement quand le fournisseur renvoie une erreur, un schéma inattendu, ou rien.

**Non prouvable par la suite : que le fournisseur accepte encore cette charge utile.** Cela demande un appel réel, lent, soumis à quota, qui n'a pas sa place dans une suite qui garde chaque boucle de validation. C'est **déclaré hors de portée du test** et renvoyé à la supervision — jamais transformé en test proposé.

**Une frontière vaut un test par défaut**, le chemin dégradé. La charge utile en gagne un second seulement quand elle porte une donnée à conséquence vérifiable en processus : un montant, un identifiant de commande, un statut d'autorisation, un consentement. Un pixel de mesure n'en porte aucune. C'est un **plafond par frontière, pas un quota** — une intégration peut légitimement ne rien recevoir.

## Ce qui qualifie un retrait

Trois heuristiques, et rien d'autre ne qualifie :

- **doublon** — affirme le même comportement qu'un test déjà présent dans la suite ;
- **trivial** — corps sous cinq lignes **et** n'affirmant qu'une garantie du framework ou une affectation sans branche ;
- **getter/setter seul** — affirme seulement qu'une propriété a été écrite ou lue.

**Le nombre de lignes seul ne qualifie jamais.** Un test court qui affirme une vraie transformation entrée → sortie est la forme idéale d'un test `contract` ; il n'est pas trivial pour être court.

**Un outlier de densité pointe cette action vers un fichier ; il ne remplit jamais une ligne de son tableau.** Une densité haute est une raison de **regarder**, et à elle seule jamais une raison **trouvée** : il faut qu'une des trois heuristiques tienne. Un fichier examiné sur ce signal et blanchi **est rapporté comme examiné et blanchi** — un outlier silencieusement abandonné se lit comme un outlier que personne n'a ouvert.

## Les cas limites du classement

- **Aucun fichier de test trouvé** → aucun classement. Classer l'arbre source entier nierait la contrainte de nombre et ferait de cette skill la campagne de masse qu'elle existe pour éviter. Un constat, un renvoi au document de stratégie — ou à son absence — et on s'arrête.
- **Saturation** — quand les manques qualifiés dépassent largement `top_n` : rapporter le total, dire que le classement ne peut pas être pertinent sur une population de cette taille, et proposer un `scope` plus étroit sur lequel l'utilisateur puisse réellement agir. **Ne jamais proposer un `domain` comme remède** : il réordonne la même population et la laisse exactement aussi grande — une saturation à laquelle on répondrait par un tableau qui a seulement l'air plus court.
- **Renforcer une assertion existante plutôt que créer un fichier**, chaque fois que les deux répondent au même manque.
- **La liste d'exclusions est explicite dans la sortie** : code non classifiable déclaré par le pivot, tout ce que la table des tiers classe `skip`, chemins déjà parcourus en e2e.

## Ce que `06-align` écrit

`06-align` est la seule action qui écrit dans le document du projet, et la seule qui transforme une réponse orale en déclaration.

**Cinq natures d'écart**, une par écart, et la distinction est ce qui tient les deux blocs séparés :

| Nature | Ce que c'est | Bloc |
|---|---|---|
| **Fait manquant** | vrai du projet, absent du document | faits |
| **Fait périmé** | énoncé dans le document, plus vrai du projet | faits |
| **Décision manquante** | rien ne tranche ce que la skill est pourtant forcée de trancher à chaque exécution | stratégie |
| **Domaine non résolu** | un domaine déclaré ne résout aucun fichier | **les deux** |
| **Zone non déclarée** | une part du code qu'aucun domaine ne couvre, ni le repli générique | **les deux** |

Pour les deux mixtes : la **mesure** va au bloc des faits, la **réponse** au bloc de stratégie. C'est ce découpage qui empêche la skill d'écrire une décision sous sa propre autorité. Une décision manquante n'est pas un défaut du document — c'est la question qu'on ne lui a pas encore posée. Et **une zone non déclarée n'est pas un défaut en soi** : un projet déclare légitimement les seuls domaines qu'il veut prioriser.

Les règles d'écriture, toutes bornées :

- **Les deux blocs s'approuvent indépendamment.** Refuser la stratégie ne retire pas les faits, et réciproquement.
- **Document absent** → produire l'audit quand même, puis offrir le choix explicite de créer ou de s'abstenir. **Jamais créer par défaut** : un projet qui n'a jamais écrit de stratégie de test a peut-être décidé exactement cela.
- **La voie d'écriture est annoncée.** Déléguer à la skill de mémoire projet quand elle est installée — résolue par son rôle, abordée par son étape de cadrage. **Une synchro silencieuse n'est pas une synchro réussie** : dire la voie prise, et ce qu'elle ne fait pas.
- **Fidélité.** Le texte approuvé est transmis comme **contenu littéral**, puis le fichier écrit est relu et comparé ligne à ligne. Toute divergence est **rapportée et jamais corrigée sur place** — c'est le document d'un autre plugin, et le réécrire en silence recréerait le problème que la délégation évite.
- **Ajouter est le défaut.** Une section existante n'est remplacée qu'après diff montré et remplacement explicitement validé : un paragraphe écrit à la main est le contenu le plus précieux du fichier, précisément parce qu'aucun outil ne l'a produit.
- **Hors bascule de phase, cette action ne propose aucun test, ne classe aucun manque, ne supprime rien.**
- **La phase s'écrit comme déclaration du projet, jamais comme fait mesuré.** Écrite comme un fait, toute exécution ultérieure la lirait comme une autorité, et la question ne serait plus jamais posée.
- **« Aucun domaine » est une réponse valide** et se consigne. Les domaines se proposent **en candidats**, jamais en inventaire découvert.
- **Proposer la médiane mesurée du projet plutôt qu'un nombre inventé.** Si le projet veut un plafond, énoncer les deux pour qu'il choisisse contre l'alternative.

## La configuration

`03-configure` vérifie le câblage de l'outillage, et ses vérifications sont **agnostiques** — des faits, jamais des opinions de style :

- le *gate* déclaré est-il réellement invoqué ;
- le lanceur e2e établi est-il canonique ;
- le schéma de configuration est-il structurellement valide.

**Ne jamais proposer de remplacer l'outil e2e établi** — seulement des correctifs à sa configuration. Le choix d'un outil est une décision de projet, pas un défaut de câblage.

**Pas de `scope` ici**, et ce n'est pas un oubli : un `scope` ne servirait qu'à masquer un *gate* cassé en pointant ailleurs.

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
- **`03-configure` est hors modèle.** Ce qu'elle vérifie est vrai ou faux indépendamment de la phase et des domaines. Elle ne prend donc ni `phase`, ni `domain`, ni `scope`. Elle est **atteignable et terminale** : `05-stats` y route, elle ne route vers rien.

### Le contrat de chaînage

**Une route est un contrat : celui qui nomme passe la main, celui qui reçoit ne recalcule pas.** Deux sources de vérité pour la même mesure divergent, et celle qui diverge en silence est celle que personne ne relance.

- **`05-stats` n'écrit rien et ne propose rien.** Suggérer l'action qui traiterait un constat est permis ; la lancer, non.
- **Un drapeau nomme l'action qui le traite**, et ne rapporte que ce que l'instantané prouve. Le drapeau de domaine non résolu rapporte le terme **et les deux lectures** — orthographe divergente, ou domaine inexistant — et n'en tranche aucune.
- **`control` ne garde aucun état entre deux exécutions.** Tout ce qui doit survivre à une exécution est écrit dans le document du projet, par `06-align`, après validation.

### La balance nette

`02-audit` retire, `04-strengthen` ajoute. La différence est un **constat, jamais un objectif** : aucune phase n'exige un solde négatif. `sustaining` s'attend à en avoir un, elle ne l'exige pas. Une suite qui ressort d'un changement de phase plus grosse qu'elle n'y est entrée n'est pas un échec.

**Ni l'une ni l'autre n'est un quota.** Aucune des deux n'a de nombre à atteindre, dans un sens ou dans l'autre.

**`04-strengthen` ne repropose pas un test sur un chemin que `02-audit` vient de faire retirer**, sauf changement du risque démontré. Sans cette borne, les deux actions se renvoient la balle sur le même fichier d'une exécution à l'autre. Sur une session où les deux tournent, **l'effet net est rapporté**.

## Les paramètres

| Action | `project_path` | `scope` | `domain` | `phase` | autre |
|---|---|---|---|---|---|
| `01-write` | requis | — | — | optionnel | `behavior` requis |
| `02-audit` | requis | code + tests liés | optionnel | optionnel | — |
| `03-configure` | requis | — | — | — | — |
| `04-strengthen` | requis | code + tests liés | optionnel | optionnel | `top_n` (défaut 5) |
| `05-stats` | requis | code + tests liés | optionnel | optionnel | — |
| `06-align` | requis | code + tests liés | optionnel | optionnel | — |

Trois règles à retenir :

- **`scope` désigne un seul univers, partout : le code source et les tests qui lui correspondent.** La résolution est **symétrique** — un chemin qui tombe dans l'arbre de tests remonte vers la source correspondante, un chemin qui tombe dans la source descend vers ses tests, et l'univers est la paire dans les deux cas. `scope=tests/legacy/` reste donc exprimable, et aucune action n'a d'univers à part.
- **`scope` et `domain` sont exclusifs.** L'un est structurel (un chemin, un glob), l'autre sémantique (un nom de domaine). Si les deux sont fournis, la skill **s'arrête et le dit** — elle n'applique aucune précédence implicite.
- **`phase` en argument ne vaut que pour l'exécution en cours.** Il n'est jamais écrit dans le document du projet. Seule `06-align` transforme une réponse en déclaration, et seulement après validation.

## Les confirmations

Le régime de confirmation couvre **trois actes**, pas un : supprimer un test, appliquer un correctif de configuration, écrire un test proposé.

Le défaut est la confirmation **ligne à ligne**. Ce que rien ne change, c'est que **la phase n'a aucun effet sur ce régime** : elle peut réordonner la table autant qu'elle veut, elle ne fait passer aucune ligne.

Deux assouplissements existent, et ils ne sont pas symétriques.

### Un lot que l'utilisateur nomme lui-même — pour les retraits seulement

Un utilisateur peut désigner un lot de son propre chef et le confirmer d'un bloc. **Cela vaut pour les retraits, jamais pour les ajouts.**

L'asymétrie a un motif, et il n'est pas la prudence : **chaque ajout déplace l'arithmétique de la contrainte de nombre pour le suivant.** Un lot d'ajouts approuvé d'un bloc ne peut donc pas avoir été évalué contre une contrainte que le lot lui-même fait bouger. Un retrait n'a pas cette propriété — il ne fait que desserrer la contrainte, et ce qui est approuvé le reste.

C'est de ce motif que découle la forme : les lignes confirmées passent **une à une**, la contrainte de nombre réévaluée entre chaque. Le **total est annoncé avant la première**, pour que l'utilisateur sache dans quoi il entre — annoncer un total n'est pas le faire approuver.

### Le lot de bascule de phase

Lors d'un **changement de phase**, `06-align` présente un lot caractérisé. **Le consentement porte sur une règle, pas sur un défilement** : à l'échelle où un lot se justifie, plusieurs centaines de lignes ne sont pas plus lisibles qu'un compteur.

Un lot se compose de **quatre choses, toutes requises** :

1. son **critère de sélection**, en une phrase — ce que tous ses membres ont en commun ;
2. le **compte par motif de rejet** ;
3. un **échantillon représentatif**, montré à l'écran ;
4. le chemin d'un fichier portant la **liste exhaustive**, écrite **avant** que la question soit posée, et proposée à la lecture explicitement.

**Le refus est en bloc, inconditionnel, et ne déclenche aucun repli** — en particulier pas de confirmation par item, qui contournerait le refus un test à la fois.

**L'ensemble sortant repose sur deux motifs et exige les deux** : les heuristiques de `02-audit`, et la qualification `phase-obsolete`. Les heuristiques seules produiraient un lot vide par construction — un test de forme de modèle écrit en `scaffolding` n'est ni un doublon, ni trivial, ni un getter.

Sont exclus de tout lot, quel que soit le changement : les tests couvrant une frontière externe, ceux qu'un critère de conséquence retient par ailleurs, ceux qui sont le seul filet sur leur sujet, et tout test **qu'aucun des deux motifs ne qualifie**.

Appartenir à un axe que la phase fait descendre n'est, en soi, jamais une raison de supprimer quoi que ce soit — pas davantage que de se trouver hors de tout domaine déclaré, qui pondère un classement et ne qualifie aucun retrait. Quand rien ne qualifie, le lot est vide — et un lot vide est un résultat légitime, rapporté comme tel, jamais habillé en lot creux.

## Voir aussi

- [`workflow.md`](workflow.md) — quelle skill pour quelle situation
- [`concepts.md`](concepts.md) — le modèle des pivots et les frontières entre skills
