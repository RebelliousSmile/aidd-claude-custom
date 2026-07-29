# `control` — le modèle

> **Autorité.** Cette page porte le modèle ; `skills/control/` le réalise. En cas de divergence, c'est cette page qui fait foi et la skill qui est en retard.
>
> La page porte la règle et son **motif** ; la skill porte la règle et sa **procédure**. Aucune étape d'exécution ne remonte ici.

`control` gouverne une suite de tests : ce qui mérite d'exister, ce qui ne le mérite plus, ce qui manque et ce que le projet dit de lui-même. Elle **ne rédige aucun test** — elle décide, puis délègue à `aidd-dev:06-test`.

Elle porte `disable-model-invocation: true` : elle ne se déclenche jamais seule. C'est délibéré — une skill qui propose de supprimer des tests ne doit pas s'inviter.

## L'autorité classante

Tout le modèle tient dans un enchaînement, et il est **en série** : les domaines disent **ce qui compte**, la phase dit **quelle preuve elle en exige maintenant**. Le tier est ce qui **sort** de cet arbitrage — jamais ce qui le rend.

| | Décide | Ne décide jamais |
|---|---|---|
| **Domaines** | quelles parties du code comptent, et à quel niveau | quelle preuve est exigée, ni aucune exclusion |
| **Phase** | la preuve exigée et son plafond ; ce qui entre dans l'analyse — à condition de déclarer ce qu'elle écarte — et l'ordre de restitution | ce que signifie une donnée mesurée, ni aucune restriction silencieuse |
| **`control`** | ce qu'il a mesuré, et qu'il écrit sous sa propre autorité | la stratégie — phase, niveaux de domaine, plafonds : il applique celle qui est en vigueur, il ne l'établit jamais de sa propre autorité |

**L'autorité de classement est une seule, et c'est la phase.** Tout ce qui, ailleurs dans le modèle, mesure ou signale le fait sous la borne énoncée plus bas en règle transversale.

### La matrice `phase × niveau de domaine`

**L'axe n'est pas le domaine nommé, c'est son niveau.** Un axe indexé par nom ne serait pas énumérable : le catalogue de domaines est un plancher de détection et jamais l'inventaire, donc chaque domaine détecté exigerait une cellule inédite. Indexée par niveau, la matrice ne bouge pas quand un domaine apparaît — seule l'affectation de ce domaine à une colonne est nouvelle.

Chaque cellule porte **une preuve exigée et un plafond** :

| | critique | structurant | ordinaire | hors-domaine |
|---|---|---|---|---|
| `scaffolding` | ancrée, 1 | — | — | — |
| `hardening` | ancrée + interne, 2 | ancrée, 1 | — | — |
| `production` | ancrée nominale + dégradée, 3 | ancrée, 2 | interne, 6 | — |
| `sustaining` | ancrée, 4 | ancrée, 2 | interne, 6 | interne sur régression, 1 |

**Une preuve ancrée traverse la frontière publique du produit ; une preuve interne reste en processus.** L'exigence d'ancrage tient à l'indépendance vis-à-vis de la source de l'erreur : un test écrit par qui a écrit le code procède de la même compréhension, et rejoue le malentendu au lieu de l'attraper. Elle ne fonde jamais « ancré vaut mieux qu'interne » — un test ancré ne prouve que le chemin qu'il parcourt, et c'est exactement pourquoi un domaine critique en `production` exige le nominal **et** le dégradé, jamais un ancrage seul.

**L'unité du plafond est la preuve : un comportement établi sous la forme que la cellule exige** — ni un fichier, ni un cas de test. Plusieurs cas qui affirment les facettes d'un même comportement comptent pour une preuve.

**Une cellule `—` dit qu'à cette phase, ce niveau n'a aucune preuve exigée — et n'a donc aucun plafond.** Les deux vont ensemble : un plafond posé là où rien n'est exigé refuserait une preuve que la phase n'a jamais demandée, c'est-à-dire déciderait sur rien. Une cellule vide n'est pas un trou de la matrice, c'est une réponse.

`references/decision-matrix.md` en porte le **défaut générique**, et **le document du projet le surcharge** — sur le mécanisme de précédence déjà en place, celui-là même qui remplit le vocabulaire de sortie. Aucun dispositif nouveau : un projet qui écrit ses propres exigences par niveau les voit appliquées, un projet qui n'écrit rien tombe sur le défaut générique.

### Le classement intra-domaine

La matrice range une colonne ; **elle n'ordonne pas ce qu'il y a dedans.** Six critères de risque s'en chargent, et ils ne décident d'aucun régime :

| Critère | Ce qu'il mesure |
|---|---|
| **Consequence** | argent, autorisations, persistance, suppression — tout échec silencieux non évident pour l'utilisateur |
| **Branching** | nombre de branches non testées |
| **Churn** | fréquence des changements récents, et la part de ces commits qui étaient des correctifs |
| **Blast radius** | combien d'appelants en dépendent |
| **Absence de tout autre filet** | ni type, ni validation runtime, ni parcours e2e qui traverse déjà ce chemin |
| **Dépendance à un contrat externe** | SDK, conteneur de tags, client d'API sortant — ce qui casse sans qu'une ligne du dépôt bouge |

`churn` garde son nom anglais. Le terme est légèrement infidèle à ce qu'il mesure — il inclut la part de correctifs, pas seulement le volume de modification — mais il sert de renvoi entre trois fichiers de la skill, et le renommer coûterait plus qu'il ne clarifie.

Ce classement compare des **ordres, jamais des parts** : aucun pourcentage n'est produit.

### Le plafond

`01-write` sur un domaine saturé rend **`skip`**, motif « plafond atteint (n/n) — `<phase> × <niveau>` », et **trois sorties sont offertes** :

- déclarer la phase suivante ;
- retirer un test du domaine ;
- forcer, par une décision explicite et tracée.

**Le refus est franchissable, jamais un blocage dur** : la skill propose, l'utilisateur choisit. Et **il refuse un ajout, il n'exige jamais un retrait** — refuser ne fait que resserrer, exiger déciderait à la place du projet.

Un plafond qui n'oppose rien n'en est pas un : ce serait un second signal à côté de la densité, et la phase n'aurait rien gagné.

**Le plafond classe, et il en a le droit.** Il transforme une sortie en `skip`, ce qui est un acte de classement. La première règle transversale — « l'instrument qui mesure ne peut pas trancher », énoncée plus bas — vise les instruments de **mesure** ; le plafond n'en est pas un, il est énoncé par la phase, devenue l'autorité classante. Sans cette phrase, les deux se lisent comme une contradiction, et c'est la règle transversale qui serait « corrigée » par le prochain lecteur.

**L'unité est un nombre de preuves, par domaine et par phase**, et c'est ce qui la met hors de portée de l'objection connue contre les caps absolus. Cette objection vise un cap *projet* — « pas plus de N tests » —, incapable de distinguer une grosse suite d'une grosse base de code. Un plafond par domaine et par phase n'a pas ce défaut : il est déjà relatif à une population identifiée et à un moment.

**Un plafond, jamais un plancher.** L'interdiction de seuil chiffré qui régnait jusqu'ici visait un plancher, lequel dégénère en cible dès qu'il est affiché. Un plafond ne peut pas devenir une cible : il ne peut être qu'atteint ou dépassé. L'interdiction tombe sans que son motif soit désavoué.

**L'expression du plafond en multiple de médiane est écartée.** Elle hériterait des cas dégénérés de la densité — pas de rapport de couverture, rapport sans données de branche, population insuffisante — et elle disparaîtrait en `scaffolding`, la phase où le plafond compte le plus.

### Ce qui nomme la sortie

Le tier nomme la forme de preuve produite. Ce qui le remplit, par ordre de précédence :

1. la stratégie de test documentée du projet — conventionnellement `aidd_docs/memory/testing.md` ;
2. `references/decision-matrix.md`, le défaut générique de la skill, sinon.

Le pivot `testing` du plugin de langage vient par-dessus : il apporte la mécanique propre à la stack, et son champ **`Anchor boundary`** dit **où passe, dans cette stack, la frontière entre une preuve ancrée et une preuve interne** — un émulateur qui n'ancre pas, un défaut de rendu que seul le navigateur réel établit, un handler de service appelable directement. Il raffine la **position** de cette frontière, jamais l'exigence : quelle preuve est due reste la cellule de la matrice, et le nom de sortie s'en déduit.

Un cas que rien ne tranche part sur **`contract`, l'ambiguïté signalée** — jamais sur `e2e` en silence. Le tier le plus cher ne se choisit pas par défaut.

## Les deux règles transversales

Deux bornes valent partout, et elles sont énoncées **une fois**. Le reste de la page les applique et les cite ; aucune section ne les réénonce à sa façon. Une borne réécrite à quatre endroits dérive à quatre vitesses, et c'est sa version la plus faible qui finit par faire jurisprudence.

### L'instrument qui mesure ne peut pas trancher

Ce qui mesure rapporte et priorise ; il ne classe pas, ne refuse pas, et ne change aucun nom de sortie. Cela couvre `05-stats`, la densité, les *Risk signals* du pivot et le rapport de couverture — et la liste n'a pas à être close, puisque la règle porte sur la **nature** de l'instrument et non sur son nom. Toute ligne de la skill qui donnerait un pouvoir de classement à un instrument de mesure est un **défaut, pas une exception**.

Le motif : une mesure décrit ce que le projet est déjà. Elle ignore la phase en vigueur et ce que le projet a déclaré compter, donc elle ne peut trancher qu'en se donnant un référent qu'elle n'a pas. Un instrument qui tranche est un **second lieu d'arbitrage**, tenu par ce qui est aveugle à l'enjeu — précisément le défaut que l'autorité classante unique supprime.

Le plafond n'est pas visé : il n'est pas un instrument de mesure, il est énoncé par la phase.

### Le pivot déclare ce qu'il fournit, jamais qui le consomme

Un champ de pivot porte un savoir de stack et la borne de ce savoir. Il ne nomme ni action, ni skill, ni consommateur.

Le motif : un champ qui nomme son consommateur s'attribue un **droit d'usage exclusif que le contrat ne lui donne pas**. Il fait entendre deux choses également fausses — qu'il n'a d'autorité que là, et qu'il a là toute autorité —, alors que le contrat appartient au consommateur, que plusieurs actions peuvent légitimement lire le même champ, et que la borne d'un champ ne dépend jamais de qui le lit. C'est aussi ce qui rend un pivot remplissable sans lire une seule action de `control`.

## Le pivot

**L'autorité d'un pivot ne se donne jamais en général : champ par champ.** Un champ dont la borne n'est pas énoncée n'a aucune autorité à étendre. C'est ce qui empêche « le pivot connaît la stack » de devenir « le pivot décide de la stack ».

- **Un champ introuvable est absent**, et son repli documenté s'applique. Jamais une erreur, jamais une invitation à le déduire d'une section voisine — déduire un champ, c'est se donner l'autorité qu'on n'a pas trouvée.
- **L'absence de pivot n'est pas une erreur**, et elle se dit. Les actions retombent sur les conventions du projet et déclarent que la résolution est non assistée.

Le partage est le même partout où le pivot intervient : `control` possède le critère générique, le pivot possède l'inventaire propre à la stack.

## Le document du projet

La stratégie de test du projet — conventionnellement `aidd_docs/memory/testing.md`. Elle appartient à la **skill de mémoire projet d'`aidd-context`**, et `control` ne fait que la lire : ce qu'il a à y faire inscrire passe par son propriétaire, par la délégation décrite plus bas. Le fichier que `control` écrit de sa propre main en est un autre — `testing-domains.md`, et `06-align` en est le seul écrivain.

- **On la désigne par son rôle, jamais par un numéro d'action figé.** Un numéro appartenant à une autre skill se périme au premier renommage.
- **Un document qui ne tranche aucun tier est traité comme absent** pour la décision de tier. La correspondance forcée s'applique alors : unit + integration → `contract`, end-to-end → `e2e`. Il y a **trois formes**, et dire laquelle on a rencontrée fait partie du rapport, car elles n'appellent pas la même suite :
  1. **absent** — il n'y a rien à lire ;
  2. **présent mais vide** — le template n'a pas été rempli ;
  3. **présent, rempli, et ne tranchant aucun tier** — il énumère des *types* de test, des outils, des conventions, sans jamais dire ce qui mérite un test. C'est la forme la plus trompeuse : elle a l'apparence d'une stratégie et n'en gouverne aucune, de sorte qu'un lecteur pressé la croit décisive. Ne jamais la confondre avec la deuxième — un template à remplir et un document à faire décider appellent des corrections opposées.
- **Non documenté se rapporte comme non documenté**, jamais comme « suit implicitement le défaut ». Le budget déclaré est alors nul — et ce n'est pas une absence de limite : le plafond de la matrice s'applique sans qu'aucun document ait à le dire. Ce qui manque est la surcharge, pas la contrainte.

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

Ce que la phase pilote concrètement : **la preuve exigée et son plafond, par niveau de domaine**, **quels fichiers entrent dans la lecture du rapport de couverture**, l'ordre des tables produites, et — au moment d'un changement de phase — la qualification d'un lot de tests devenus obsolètes.

### Borner en le disant

La phase peut réduire l'univers analysé. Elle ne peut pas le faire en silence : **tout fichier qu'elle écarte est listé, avec le motif de phase qui l'a écarté.**

C'est la seule forme de restriction que le modèle admet, et la raison est celle qui borne déjà les domaines : un faux positif coûte une ligne de bruit, un faux négatif silencieux coûte le manque que la skill existe pour empêcher. Une restriction déclarée n'est pas un faux négatif — c'est une décision qu'on peut relire et contester.

### Ce que la phase ne décide pas

**Ce qu'une donnée du rapport de couverture signifie ne change dans aucune phase.** Une absence du rapport vaut « non couvert » partout, quelle que soit la phase en vigueur.

La distinction est fine et elle porte tout le modèle : la phase décide **ce qui entre** dans la lecture et **comment le résultat se classe** ; elle ne décide jamais **ce que dit** ce qui a été lu. Une phase qui changerait le sens d'une absence trancherait une mesure, et aucune autorité de classement ne tranche de mesure. Le même fait se lit deux fois — en `scaffolding` une masse de fichiers jamais importés est l'état attendu et classe bas, en `sustaining` la même masse est le constat. Deux rangs, jamais deux faits.

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

**Les deux prennent le régime le plus permissif de la matrice : aucune preuve exigée, aucun plafond, sur aucune colonne.** Ce régime est **annoncé**, jamais silencieux : un arbitrage permissif qu'on ne dit pas est indiscernable d'un arbitrage qui n'a pas eu lieu.

Et la sortie les distingue, parce qu'ils ne sont pas la même chose : `default` est une **décision écrite du projet** — quelqu'un a choisi de ne pas être arbitré ; `undetermined` est une **question restée sans réponse** — personne n'a rien choisi. Ils diffèrent ensuite sur ce qui est observable :

| | `default` | `undetermined` |
|---|---|---|
| Origine | choix déclaré | question sans réponse |
| La question se repose | non, **une fois déclaré** | à chaque exécution |
| Lot de suppression | aucun | selon la phase réelle, une fois connue |
| Changement de phase | ne s'y applique pas | s'applique dès qu'une phase est déclarée |
| Régime de matrice | le plus permissif, **par décision** | le plus permissif, **faute de réponse** |

`default` est la réponse à un besoin précis : utiliser les actions sans biais de classement ni de suppression, **sans pour autant se faire redemander la phase à chaque fois**. C'est la différence entre « je ne veux pas être arbitré » et « je n'ai pas répondu ».

**Si `default` échappe à la bascule de phase, c'est par consentement, non par mécanique.** Un projet qui déclare `default` vient de poser une décision ; la faire suivre d'un lot de tests à qualifier obsolètes contredirait le choix à l'instant où il est pris. `undetermined` n'a rien décidé du tout : dès qu'une phase est déclarée, il bascule comme n'importe quelle autre.

## Les domaines

Un domaine est une part fonctionnelle du produit — `auth`, `payment`, `checkout` — résolue dans le code par des termes : `Login`, `Register`, `SessionGuard`. Il porte un **niveau**, et c'est ce niveau, jamais le nom, qui désigne sa colonne dans la matrice.

| Niveau | Ce qui l'y range |
|---|---|
| **critique** | un échec y coûte de l'argent, un accès, ou une donnée irremplaçable |
| **structurant** | un échec y interrompt un parcours entier, sans rien détruire |
| **ordinaire** | le reste de ce que le projet a nommé |
| **hors-domaine** | ce qu'aucun domaine n'apparie |

Le niveau qualifie **le domaine** ; les six critères de risque ordonnent **ce qu'il y a dedans**. Aucun des deux ne remplace l'autre : le premier fixe le régime exigé, les seconds fixent le tour de passage à l'intérieur. Leur nature diffère et c'est ce qui interdit de les confondre malgré des mots voisins — le niveau est un **jugement déclaré** sur un domaine, posé une fois et figé ; les critères sont des **observations** refaites sur des fichiers à chaque exécution, et à ce titre ils ne classent rien.

Les domaines sont **quasi-statiques** : ils ne bougent qu'à l'occasion d'un gros changement applicatif. C'est ce qui rend leur établissement rentable — un jugement posé une fois sert des dizaines d'exécutions.

### Qui produit quoi

`06-align` établit les domaines par **catalogue de référence × scan du code**, et **il attribue le niveau en même temps que le nom**. Un domaine nommé sans niveau ne désigne aucune colonne, donc n'exige rien : le déclarer ainsi reviendrait à le déclarer sans effet.

Le catalogue (`references/domain-catalogue.md`) est un **plancher de détection, jamais l'inventaire**. Il garantit qu'un `auth` ou un `payment` présent dans le code ne soit pas manqué ; il n'interdit à aucun domaine propre au projet d'exister, et le niveau qu'il porte est une proposition par défaut, jamais une imposition. Aucun domaine n'est universel — une bibliothèque, un outil en ligne de commande, un jeu n'ont ni authentification ni paiement — et c'est précisément pourquoi le catalogue **détecte** au lieu d'énumérer.

| Connaissance | Détenteur | Pourquoi |
|---|---|---|
| **quels** domaines existent, et à quel niveau | l'utilisateur, sur proposition d'`06-align` | personne d'autre ne sait ce qui compte dans ce produit |
| **comment** les repérer dans cette stack | le pivot du plugin de langage | c'est de la convention de stack, et elle périme vite |
| **où** le jugement est consigné | `06-align`, et lui seul | un fichier, un écrivain |

Séparés ainsi, ils ne peuvent pas se contredire — donc aucune règle d'arbitrage n'est nécessaire. Le pivot **complète** une résolution incomplète ; il n'écrase jamais une résolution que le projet a explicitement écrite sur son propre code.

**Un domaine n'existe que confirmé par l'utilisateur.** `align` propose, il ne consacre rien seul. Sur une base sans convention structurelle, il rendra peu et le résidu sera large : **c'est un fait à rapporter, pas un échec à masquer.** Une zone que le vocabulaire n'a pas atteinte et qu'on tait ressort comme une zone sans manque, ce qui est l'inverse exact de la vérité.

### Un domaine passé en argument

**La confirmation porte sur ce que la machine propose, jamais sur ce que l'utilisateur a écrit lui-même.** Un domaine sorti du scan n'existe que confirmé ; un domaine passé **en argument** est déjà une déclaration de l'utilisateur — **l'argument est la confirmation**, et redemander ferait confirmer deux fois la même chose. Les deux règles ne se contredisent pas : elles ne portent pas sur le même acte.

Ce qui reste à établir sur un domaine passé en argument n'est donc pas le domaine, c'est son **niveau** :

- **présent au catalogue** → il en prend le niveau, sans question ;
- **absent du catalogue** → l'action **demande** le niveau, et ne le devine pas. Deviner reviendrait à choisir un plafond à la place du projet.

**Le niveau répondu n'est pas persisté.** Il vaut pour l'invocation seule, l'action l'annonce comme tel, et propose `06-align` pour le figer. Sans cette borne, deux invocations peuvent recevoir deux réponses et poser deux plafonds sur le même domaine — l'idempotence par jugement matérialisé tomberait exactement là où elle est censée tenir.

**`06-align` reste le seul écrivain de `testing-domains.md`.** Laisser l'action consigner elle-même la réponse serait la sortie de facilité : elle ferait deux écrivains sur un même fichier, la faute même que l'interdit ci-dessous corrige.

### Ce qui est écrit, et sous quelle forme

L'artefact est `<projet>/aidd_docs/memory/testing-domains.md`.

**`align` n'écrit pas dans `testing.md`.** Ce document appartient à la skill de mémoire projet d'`aidd-context`, et ce que `control` a à y faire inscrire passe par son propriétaire. **Un fichier, un écrivain** : deux écrivains sur un fichier édité à la main perdent une écriture sans que rien ne le signale, et un document de stratégie est celui dont le contenu manuel a le plus de valeur. `testing-domains.md` obéit à la même règle, avec `06-align` pour écrivain.

**Les termes de résolution sont littéraux, insensibles à la casse, plus les chemins. Pas de regex.** Le fichier est édité à la main par le projet : une regex y devient illisible, puis fausse — et une correspondance fausse échoue en silence, ce que le garde-fou ci-dessous établit comme le pire mode de défaillance de ce mécanisme.

**Littéral veut dire sous-chaîne, et le nom du domaine est lui-même un de ses termes.** Deux précisions, parce que « littéral » seul ne fixe pas encore un ensemble : une lecture par égalité de jeton entière est tout aussi littérale et tout aussi sans regex, et elle résout un ensemble *différent* — `auth` n'apparierait alors rien dans `fediverse_auth`, dont le jeton est `fediverse_auth`. Or l'intérêt de fixer la règle est que **deux passages sur le même dépôt résolvent le même ensemble** ; une règle qui laisse ce choix ouvert coûte exactement ce qu'une regex coûterait. Et le nom compte comme terme parce qu'un catalogue liste ce que le nom seul raterait, jamais un jeu qui le remplace : `domain=auth` sur un projet dont le paquet s'appelle `fediverse_auth` n'apparierait rien de la liste de l'entrée `auth`.

**La surface de l'appariement est nommée : les chemins et les identifiants déclarés, jamais une occurrence quelconque dans le corps d'un fichier.** C'est la troisième précision du même ensemble, et elle est du même ordre que les deux précédentes — sur un dépôt réel, `Auth` apparie une dizaine de chemins et plusieurs dizaines de fichiers si l'on compte toute occurrence de texte, soit un facteur huit entre deux lectures que rien ne départage. Un domaine désigne du code dont le comportement relève d'une colonne ; un fichier qui *mentionne* un terme au passage — un import, un commentaire, une chaîne de log — n'en relève pas pour autant.

### L'idempotence par jugement matérialisé

Un scan qui rejoue son jugement à chaque exécution ne rend pas deux fois le même résultat : à mi-parcours il trouve A B C D E ; plus tard il doit rendre **A B C D E + F G**, jamais `A B C' D" E°`.

Le non-déterminisme se déplace donc de l'exécution vers l'établissement : **`align` juge une fois et fige son jugement en termes littéraux.** Les passages suivants **appliquent** au lieu de re-résoudre ; seul le **résidu** — ce qu'aucun terme n'apparie — est scanné à neuf.

- **L'appartenance multiple est admise** : un fichier peut relever de plusieurs domaines. Forcer l'exclusivité ferait trancher un cas réel par une règle arbitraire.
- **Les capteurs de dérive sont rapportés par `05-stats`, jamais appliqués** — résidu qui croît, termes devenus orphelins. La boucle passe par l'utilisateur : `stats` rapporte, l'utilisateur décide, `align` re-juge. Le seuil de signalement est **relatif, avec un plancher absolu** : un résidu de deux fichiers sur huit n'est pas une dérive.
- **Renommer est une opération explicite d'`align`**, jamais l'effet de bord d'un scan. Un renommage subi rebaptiserait un domaine que personne n'a demandé de rebaptiser, et le plafond suivrait le nouveau nom sans que rien ne le dise.

### Le garde-fou

**Un domaine priorise, il ne restreint pas** — et contrairement à la phase, il ne restreint pas *du tout*, pas même en le déclarant.

La différence tient à la nature des deux : une phase écarte par **règle**, et une règle se relit. Un domaine écarte par **correspondance de terme**, et une correspondance échoue silencieusement. Chercher `Login` et `Register` trouve `LoginForm.tsx` et rate `SessionController` — la zone ratée ne ressort pas comme écartée, elle ressort comme une zone sans manque, ce qui est l'inverse exact de la vérité. Une exclusion par domaine serait donc invisible par construction.

**Et la déclarer ne la sauverait pas.** Ce qu'une phase écarte, elle l'écarte sur un motif qui porte **sur le code** — un motif se relit, se conteste, se corrige. Ce qu'un domaine écarterait, il l'écarterait pour absence de correspondance : un motif qui ne dit rien du code et tout du vocabulaire employé pour le chercher. Écarter là-dessus reviendrait à transformer une **ignorance en décision**, et aucune déclaration ne répare cela — déclarer une ignorance ne la lève pas. L'invariant tient donc sur son mécanisme propre ; il n'emprunte rien à la borne de la phase.

Ce qui n'est matché par aucun domaine reste donc dans l'analyse — il descend simplement dans l'ordre — et **il est rapporté**, avec le terme qui a échoué à le reconnaître. La trace sert une seconde fois : elle alimente le résidu, dont `05-stats` rapporte la dérive et sur lequel `align` re-juge.

### Le régime hors-domaine

Un projet où `06-align` n'a jamais tourné n'est pas un cas particulier : **tout son code est hors-domaine, et la colonne existe déjà.** Ce n'est pas un repli — un repli serait un mécanisme de plus, à maintenir en parallèle et à faire diverger — **c'est une colonne de la matrice**, lue comme les trois autres. Hors-domaine n'est pas hors analyse : le garde-fou vaut ici comme ailleurs.

**Aucun repli générique ne se substitue à un domaine absent** — pas de liste de parcours critiques tenue à côté, pas d'inventaire par défaut. Ce qu'un tel repli couvrirait est déjà cette colonne, et deux dispositifs pour un même cas finissent par ne plus dire la même chose. Ce que le catalogue apporte n'est pas un repli mais une **proposition** : il fait exister des domaines, il n'en tient pas lieu.

**Chaque action l'annonce** : « aucun domaine établi, régime hors-domaine appliqué ». Sans cette annonce, l'absence d'exigence se lit comme une exigence satisfaite. Le renvoi à `06-align` accompagne l'annonce tant que la question n'a pas été posée ; il tombe quand « aucun domaine » est la réponse consignée du projet — renvoyer là vers l'action qui vient de répondre redemanderait ce qui est déjà décidé.

Même régime pour un projet dont la stratégie documentée est antérieure à ce modèle : **elle garde son autorité sur ce qu'elle déclare** — les noms de sortie, un plafond de nombre éventuel — et l'absence de niveaux de domaine déclarés le place en régime hors-domaine jusqu'à ce qu'`align` tourne. Ce qui a été écrit ne cesse pas de valoir ; ce qui ne l'a jamais été ne se devine pas.

## L'ancrage

L'ancrage est une **propriété de la preuve**, et la frontière publique du produit n'est pas au même endroit selon la stack :

| Stack | Ce qui ancre |
|---|---|
| application web | le navigateur réel, parcours complet |
| API / service | la frontière HTTP réelle |
| CLI | l'invocation du binaire |
| bibliothèque | l'API publique consommée de l'extérieur |

**Ancré ne veut pas dire navigateur.** L'exigence porte sur l'indépendance vis-à-vis de la source de l'erreur, pas sur un outil — c'est ce qui permet à la matrice de s'appliquer à une stack dépourvue de runner e2e sans exiger qu'elle s'en dote.

Cette table porte le **critère générique** et rien de plus ; l'inventaire de la stack réelle appartient au champ `Anchor boundary` du pivot, qui dit où la frontière tombe pour ses outils. Le partage est celui de tout pivot, et les deux ne peuvent donc pas se contredire.

`contract`, `e2e` et `skip` restent les **noms de sortie**. La matrice exige une preuve ancrée ou une preuve interne ; ce qui sort continue de s'appeler comme avant. La précision est conceptuelle et ne casse le vocabulaire de personne — ni celui de la skill, ni celui des suites d'évals, ni celui d'un `testing.md` de projet déjà écrit.

## La densité, pas le compte

La contrainte de nombre de cette skill est une **densité** : les cas de test qui exercent un fichier, rapportés à ses points de branchement, lus **contre la médiane de la distribution du projet lui-même** — jamais contre un seuil absolu importé d'ailleurs. Alerte au-delà de 3× la médiane.

Deux règles la bornent, et elles ne bougent pas :

- **la densité signale et priorise ; elle ne classe rien, ne refuse rien, et ne change aucun tier** — la première règle transversale, appliquée ici, et rien de plus ;
- **elle n'est pas une cible** — proposer du travail dont la seule justification serait de rapprocher une densité de la médiane, c'est l'erreur du pourcentage de couverture portant un autre chiffre.

Et la règle mère, dont tout ceci découle :

> Le pourcentage de couverture est un symptôme, jamais une cible. Aucune action de cette skill ne propose un travail dont la seule justification serait de faire monter un chiffre de couverture.

Ce que cette règle interdit est un **plancher** : un chiffre à atteindre devient la cible qu'aucune donnée de couverture ne mérite d'être, et il le devient le jour où on l'affiche. Elle n'a jamais visé le plafond de la matrice, qui n'ordonne aucun travail — il n'en refuse que.

### Densité et plafond ne se remplacent pas

**Ce ne sont pas deux mesures rivales : ce n'est pas la même nature de chose.** La densité est une **observation faite sur une population** — elle décrit ce que le projet est déjà, et ce qui décrit n'exige rien. Le plafond est une **exigence énoncée par la phase** — il ne décrit rien, et il vaut avant que la moindre donnée soit lue. C'est pourquoi l'un signale sans jamais classer, et l'autre classe sans jamais mesurer.

**Il n'y a qu'un plafond en vigueur à la fois** : celui de la matrice, ou celui que le document du projet déclare à sa place. C'est le mécanisme de précédence déjà en place, jamais une seconde notion de plafond. La densité est rapportée à côté, jamais à sa place : un plafond dit *combien*, une densité dit *si c'est au bon endroit*. Les deux réponses sont utiles et aucune ne contient l'autre.

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

## Ce que la mesure rend

> `stats` affiche ce qui est déclaré et ce qui est mesuré. Il ne produit rien qui soit déduit des deux.

Un verdict du type « il y a un domaine sans sa preuve » est une **application de la matrice**, donc l'arbitrage de la phase. Le rendre dans l'instantané créerait **deux lieux d'arbitrage** — le défaut même que l'autorité classante unique existe pour supprimer. Afficher l'exigence à côté du constat n'est pas déduire : le lecteur conclut, l'instrument non.

C'est ce que porte le bloc **`DOMAINES exigé / trouvé`** — par domaine en vigueur, la preuve que la matrice exige à la phase en vigueur, et celle que la suite porte. Deux colonnes, et aucune troisième qui les soustraie.

Il tient la place du compte par tier — `contract : n / e2e : n / ratio` —, qui posait la même question sans rien pour la trancher. **Aucun drapeau ne compare les formes de preuve entre elles** : un signal tiré du rapport entre deux tiers n'existait que parce que mesurer sans référent oblige à en inventer un. La matrice fournit le référent ; le signal tombe sans remplacement, et il n'avait de toute façon aucun destinataire capable d'en faire quelque chose.

**La table `excluded` reste, et elle est ce qui empêche la phase de restreindre en silence** : tout fichier écarté y figure avec le motif de phase qui l'a écarté. Sans elle, borner en le disant n'est qu'une intention — une restriction qu'on ne lit nulle part est indiscernable d'une restriction qui n'a pas eu lieu.

## Les frontières externes

Écrire ce qu'un test prouve ici, et ce qu'il ne prouve pas, est ce qui empêche le critère de fabriquer de la fausse assurance.

**Prouvable en processus, au tier `contract`, sans appeler le fournisseur :**

- que la charge utile construite est celle que le code croit envoyer — champs, types, unités, identifiant réellement utilisé ;
- que le **chemin dégradé** se comporte correctement quand le fournisseur renvoie une erreur, un schéma inattendu, ou rien.

**Non prouvable par la suite : que le fournisseur accepte encore cette charge utile.** Cela demande un appel réel, lent, soumis à quota, qui n'a pas sa place dans une suite qui garde chaque boucle de validation. C'est **déclaré hors de portée du test** et renvoyé à la supervision — jamais transformé en test proposé.

**Une frontière vaut un test par défaut**, le chemin dégradé. La charge utile en gagne un second seulement quand elle porte une donnée à conséquence vérifiable en processus : un montant, un identifiant de commande, un statut d'autorisation, un consentement. Un pixel de mesure n'en porte aucune. C'est une **borne par frontière, pas un quota** — une intégration peut légitimement ne rien recevoir. Elle n'est pas le plafond de la matrice et ne s'y ajoute pas : le plafond compte les preuves d'un domaine à une phase, cette borne dit ce qu'une frontière externe vaut de tests. Deux objets comptés, deux règles ; « il n'y a qu'un plafond en vigueur à la fois » vise le premier.

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
- **La liste d'exclusions est explicite dans la sortie** : code non classifiable déclaré par le pivot, tout ce que l'arbitrage de la phase classe `skip`, chemins déjà parcourus en e2e.

## Ce que `06-align` écrit

`06-align` est la seule action qui écrit — `testing-domains.md` sous sa propre plume, la stratégie du projet par délégation à son propriétaire — et la seule qui transforme une réponse orale en déclaration.

**Cinq natures d'écart**, une par écart, et la distinction est ce qui tient les deux blocs séparés :

| Nature | Ce que c'est | Bloc |
|---|---|---|
| **Fait manquant** | vrai du projet, absent du document | faits |
| **Fait périmé** | énoncé dans le document, plus vrai du projet | faits |
| **Décision manquante** | rien ne tranche ce que la skill est pourtant forcée de trancher à chaque exécution | stratégie |
| **Domaine non résolu** | un domaine déclaré ne résout aucun fichier | **les deux** |
| **Zone non déclarée** | une part du code qu'aucun domaine n'apparie — le résidu | **les deux** |

Pour les deux mixtes : la **mesure** va au bloc des faits, la **réponse** au bloc de stratégie — et une fois validée, cette réponse se consigne **là où le jugement de domaine vit**, `testing-domains.md`. Le document du projet reçoit ce qu'il a à décider, jamais la liste que `control` en a tirée : un fichier, un écrivain, et la liste des domaines a le sien. C'est ce découpage qui empêche la skill d'écrire une décision sous sa propre autorité. Une décision manquante n'est pas un défaut du document — c'est la question qu'on ne lui a pas encore posée. Et **une zone non déclarée n'est pas un défaut en soi** : un projet déclare légitimement les seuls domaines qu'il veut prioriser.

Les règles d'écriture, toutes bornées :

- **Les deux blocs s'approuvent indépendamment.** Refuser la stratégie ne retire pas les faits, et réciproquement.
- **Document absent** → produire l'audit quand même, puis offrir le choix explicite de créer ou de s'abstenir. **Jamais créer par défaut** : un projet qui n'a jamais écrit de stratégie de test a peut-être décidé exactement cela.
- **La voie d'écriture est annoncée.** Déléguer à la skill de mémoire projet quand elle est installée — résolue par son rôle, abordée par son étape de cadrage. **Une synchro silencieuse n'est pas une synchro réussie** : dire la voie prise, et ce qu'elle ne fait pas.
- **Fidélité.** Ce qui est écrit dans le fichier doit être **identique** au texte approuvé — le texte circule comme contenu littéral, jamais comme consigne à reformuler. Toute divergence est **rapportée et jamais corrigée sur place** : c'est le document d'un autre plugin, et le réécrire en silence recréerait le problème que la délégation évite.
- **Ajouter est le défaut.** Une section existante n'est remplacée qu'après diff montré et remplacement explicitement validé : un paragraphe écrit à la main est le contenu le plus précieux du fichier, précisément parce qu'aucun outil ne l'a produit.
- **Hors bascule de phase, cette action ne propose aucun test, ne classe aucun manque, ne supprime rien.**
- **La phase s'écrit comme déclaration du projet, jamais comme fait mesuré.** Écrite comme un fait, toute exécution ultérieure la lirait comme une autorité, et la question ne serait plus jamais posée.
- **« Aucun domaine » est une réponse valide** et se consigne. Le projet passe alors en **régime hors-domaine**, qui est une colonne de la matrice et non un repli — il ne perd donc aucun arbitrage, il en prend un autre. Les domaines se proposent **en candidats**, jamais en inventaire découvert.
- **Trois objets sortent, en trois lignes, jamais fondus en un chiffre.** Le **plafond de la cellule** est le nombre fixe que la matrice énonce : il ne se propose pas, il s'énonce, il est en vigueur quoi que ce bloc propose, et **jamais en multiple de médiane** — l'expression en médiane est écartée plus haut, et pour les mêmes raisons. Ce qui **se propose** ici est la **densité mesurée du projet** : elle observe une population, elle ne refuse rien, et **elle n'est jamais nommée cap**. Le **cap du projet** n'existe que si le projet le déclare — sa décision, et un cap déclaré l'emporte sur la proposition — et il se déclare alors **en nombre, jamais en multiple de médiane** : un multiple ferait bouger le refus avec la population même qu'il borne. Aucun nombre n'est inventé à la place de l'un des trois. *Cette entrée disait jusqu'au 29/07/2026 « un plafond se propose en nombre, jamais en multiple de médiane », un seul objet là où il y en a trois : elle laissait lire l'interdiction du multiple comme portant sur ce que l'action propose, alors qu'elle porte sur le cap déclaré et sur le plafond de cellule, et que ce qui est proposé n'est pas un cap du tout. La règle qui les tient séparés est plus haut, `Densité et plafond ne se remplacent pas` ; c'est ici qu'elle manquait.*

## La configuration

`03-configure` vérifie le câblage de l'outillage, et ses vérifications sont **agnostiques** — des faits, jamais des opinions de style :

- le *gate* déclaré est-il réellement invoqué ;
- la commande de couverture tourne-t-elle **indépendamment du gate** — une commande qui ne s'exécute qu'au sein du gate ne peut pas servir à lire la couverture d'un projet qui échoue au gate, c'est-à-dire exactement quand la lire compte ;
- la couverture tourne-t-elle **en mode ligne, le suivi de branche jamais activé** — c'est la configuration la plus répandue de toutes, et la seule chose qui sépare le projet d'une densité mesurable. Un rapport qui existe sans donnée de branche n'est **pas** un rapport manquant, et ne se rapporte pas comme tel ;
- le lanceur e2e établi est-il canonique ;
- le schéma de configuration est-il structurellement valide.

**Un passage qui ne trouve rien le dit en toutes lettres, et dit ce qu'il a cherché** — le nombre de contrôles joués, et **séparément** ceux qui ne l'ont pas été faute de pivot. Une table vide se lit comme un plantage, comme une absence de fichier de configuration et comme un pivot manquant, qui appellent trois suites différentes. Nommer les contrôles non joués importe plus que nommer ceux qui passent : un piège propre à la stack que personne n'a vérifié est précisément ce que cette action existe pour attraper, et son absence est invisible tant qu'elle n'est pas dite.

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
- **`control` ne garde aucun état entre deux exécutions.** Tout ce qui doit survivre à une exécution passe par `06-align`, après validation.

### La balance nette

`02-audit` retire, `04-strengthen` ajoute. La différence est un **constat, jamais un objectif** : aucune phase n'exige un solde négatif. `sustaining` s'attend à en avoir un, elle ne l'exige pas. Une suite qui ressort d'un changement de phase plus grosse qu'elle n'y est entrée n'est pas un échec.

**Ni l'une ni l'autre n'est un quota.** Aucune des deux n'a de nombre à atteindre, dans un sens ou dans l'autre.

**`04-strengthen` ne repropose pas un test sur un chemin que `02-audit` vient de faire retirer**, sauf changement du risque démontré. Sans cette borne, les deux actions se renvoient la balle sur le même fichier d'une exécution à l'autre. Sur une session où les deux tournent, **l'effet net est rapporté**.

## Les paramètres

| Action | `project_path` | `scope` | `domain` | `phase` | autre |
|---|---|---|---|---|---|
| `01-write` | requis | — | optionnel | optionnel | `behavior` requis |
| `02-audit` | requis | code + tests liés | optionnel | optionnel | — |
| `03-configure` | requis | — | — | — | — |
| `04-strengthen` | requis | code + tests liés | optionnel | optionnel | `top_n` (défaut 5) |
| `05-stats` | requis | code + tests liés | optionnel | optionnel | — |
| `06-align` | requis | code + tests liés | optionnel | optionnel | — |

Cinq règles à retenir :

- **`scope` désigne un seul univers, partout : le code source et les tests qui lui correspondent.** La résolution est **symétrique** — un chemin qui tombe dans l'arbre de tests remonte vers la source correspondante, un chemin qui tombe dans la source descend vers ses tests, et l'univers est la paire dans les deux cas. `scope=tests/legacy/` reste donc exprimable, et aucune action n'a d'univers à part.
- **`scope` et `domain` sont exclusifs.** L'un est structurel (un chemin, un glob), l'autre sémantique (un nom de domaine). Si les deux sont fournis, la skill **s'arrête et le dit** — elle n'applique aucune précédence implicite.
- **`phase` en argument ne vaut que pour l'exécution en cours.** Il n'est jamais écrit dans le document du projet. Seule `06-align` transforme une réponse en déclaration, et seulement après validation.
- **`domain` prend un seul nom, jamais une liste.** Aucune action n'en parse plusieurs, et ce n'est pas une limite d'implémentation : deux domaines passés ensemble désigneraient deux colonnes de la matrice, donc deux plafonds et deux formes de preuve, sans que rien ne dise laquelle arbitre. L'appartenance multiple d'un *fichier* reste admise — elle s'établit dans le registre, pas dans un argument. Un projet qui veut lire deux domaines lit deux exécutions.
- **`domain` sur `01-write` ne désigne aucun univers de fichiers, il désigne une colonne.** L'action juge un comportement et ne produit aucune table à réordonner ; ce qu'elle a besoin de savoir est la cellule dont elle relève, donc le niveau du domaine visé. Sans ce paramètre, le plafond serait inapplicable partout où le comportement à écrire ne se rattache pas déjà à un domaine résolu.

## Les confirmations

Le régime de confirmation couvre **trois actes**, pas un : supprimer un test, appliquer un correctif de configuration, écrire un test proposé.

Le défaut est la confirmation **ligne à ligne**. Ce que rien ne change, c'est que **la phase n'a aucun effet sur ce régime** : elle peut réordonner la table autant qu'elle veut, elle ne fait passer aucune ligne.

Deux assouplissements existent, et ils ne sont pas symétriques.

### Un lot que l'utilisateur nomme lui-même

Un utilisateur peut désigner un lot de son propre chef et le confirmer d'un bloc. **Pour les retraits, toujours ; pour les ajouts, dans la limite de la marge.**

L'asymétrie a un motif, et il n'est pas la prudence : **chaque ajout déplace l'arithmétique de la contrainte de nombre pour le suivant.** Un lot approuvé d'un bloc ne peut pas avoir été évalué contre une contrainte que le lot lui-même fait bouger. Un retrait n'a pas cette propriété — il ne fait que desserrer la contrainte, et ce qui est approuvé le reste.

**Ce motif distingue deux contraintes, et il ne mord que sur l'une.** Le cap projet est une densité — la médiane mesurée du projet — et chaque ajout la déplace : on ne compte pas d'avance contre une cible qui bouge à chaque pas. Le plafond de la cellule `phase × niveau` est un nombre fixe, et un nombre fixe se compte d'avance.

D'où la forme : **un lot d'ajouts est recevable tant qu'il tient entièrement dans la marge restante de chaque cellule qu'il touche.** Aucun de ses membres n'a alors été approuvé contre une contrainte qu'un autre lui fait franchir — la condition du motif n'est pas réunie, et l'interdit n'a plus de fondement. Au-delà de la marge, les lignes passent **une à une**, la contrainte réévaluée entre chaque. La règle dégrade d'elle-même : plus la cellule se remplit, plus le lot admis rétrécit, et à saturation il ne reste que le passage ligne à ligne.

Le **total est annoncé avant la première ligne**, lot ou pas, pour que l'utilisateur sache dans quoi il entre — annoncer un total n'est pas le faire approuver. La **marge est annoncée avec lui** : un lot refusé pour dépassement dit de combien il dépasse, sans quoi l'utilisateur ne peut que le représenter au hasard.

### Le lot de bascule de phase

Lors d'un **changement de phase**, `06-align` présente un lot caractérisé. **Le consentement porte sur une règle, pas sur un défilement** : à l'échelle où un lot se justifie, plusieurs centaines de lignes ne sont pas plus lisibles qu'un compteur.

Un lot se compose de **quatre choses, toutes requises** :

1. son **critère de sélection**, en une phrase — ce que tous ses membres ont en commun ;
2. le **compte par motif de rejet** ;
3. un **échantillon représentatif**, montré à l'écran ;
4. la **liste exhaustive**, montrée **en toutes lettres dans le même tour** — jamais un chemin qui en tiendrait lieu.

**Le quatrième point ne contredit pas le troisième, il le complète.** L'échantillon est ce qui se lit ; la liste exhaustive est ce sur quoi on peut revenir. Un chemin à la place de la liste transforme le contenu en promesse : au moment où la question est posée, l'utilisateur consent sans que rien de ce qu'il approuve ne lui ait été montré, et le fichier peut aussi bien ne pas exister encore. La liste est **aussi** écrite dans un fichier **avant** que la question soit posée, pour qu'un refus ou une interruption laisse une trace durable de ce qui a été proposé — mais ce fichier n'est pas ce que l'utilisateur lit pour consentir.

**Le refus est en bloc, inconditionnel, et ne déclenche aucun repli** — en particulier pas de confirmation par item, qui contournerait le refus un test à la fois.

**L'ensemble sortant repose sur deux motifs et exige les deux** : les heuristiques de `02-audit`, et la qualification `phase-obsolete`. Les heuristiques seules produiraient un lot vide par construction — un test de forme de modèle écrit en `scaffolding` n'est ni un doublon, ni trivial, ni un getter.

Sont exclus de tout lot, quel que soit le changement : les tests couvrant une frontière externe, ceux qu'un critère de conséquence retient par ailleurs, ceux qui sont le seul filet sur leur sujet, et tout test **que l'un des deux motifs ne qualifie pas**.

**Une cellule sans exigence ne qualifie aucun retrait.** Qu'à cette phase, ce niveau n'exige aucune preuve ne dit rien de ce qui existe déjà — pas davantage que de se trouver hors de tout domaine, qui fait descendre dans l'ordre et ne qualifie rien. Quand rien ne qualifie, le lot est vide — et un lot vide est un résultat légitime, rapporté comme tel, jamais habillé en lot creux.

## Voir aussi

- [`workflow.md`](workflow.md) — quelle skill pour quelle situation
- [`concepts.md`](concepts.md) — le modèle des pivots et les frontières entre skills
- `skills/control/references/decision-matrix.md` — le défaut générique de la matrice, que le document du projet surcharge, et la définition des noms de sortie à côté de la distinction preuve ancrée / preuve interne
- `skills/control/references/domain-catalogue.md` — le plancher de détection des domaines et leur niveau proposé
