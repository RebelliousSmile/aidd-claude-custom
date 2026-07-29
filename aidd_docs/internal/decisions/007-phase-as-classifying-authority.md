# Decision: la phase devient l'autorité classante, et DEC-004 §4 est amendé

| Field   | Value |
|---------|-------|
| ID      | DEC-007 |
| Date    | 2026-07-28 |
| Feature | `overcode:control` — refonte : la phase arbitre, les domaines portent |
| Status  | Accepted |
| Antécédents | **DEC-004** — consommation d'un pivot `sc-*` par un autre plugin ; son §4 est amendé ici. **DEC-006** — `docs/control.md` fait foi sur `skills/control/`, et le partage page = règle + motif / skill = règle + procédure / ADR = rationnel |

## Context

### Le défaut architectural

Cinq dispositifs se disputent la même fonction sans qu'aucun ne la détienne :

| Dispositif | Ce qu'il apporte | Ce qu'il ne peut pas |
|---|---|---|
| table des tiers | classe | voir ce qui compte pour ce projet |
| phase | pondère l'ordre | classer |
| domaines | ordonnent la lecture | classer |
| densité | signale | classer |
| *Risk signals* (pivot) | priorise | classer |

La seule autorité classante est donc aussi la seule aveugle à l'enjeu : elle sait ce qu'un comportement **est**, jamais ce qu'il **vaut** pour ce projet à ce moment. Les quatre autres dispositifs ont été greffés autour pour corriger ce défaut par pondération ; aucun ne peut le redresser, faute du droit de classer. Empiler un cinquième critère n'y changerait rien — c'est l'attribution de l'autorité qu'il faut reprendre.

### Le mécanisme qui fonde l'exigence de preuve ancrée, et son contre-argument

Le pouvoir de détection d'un test tient à son **indépendance vis-à-vis de la source de l'erreur**. Quand un même agent écrit le code et son test interne, les deux procèdent de la même compréhension : le test rejoue le malentendu au lieu de l'attraper. Un test qui traverse la frontière publique du produit ne partage pas cette origine — il est **ancré** ailleurs.

**Contre-argument conservé, il n'est pas réfuté** : un test ancré ne prouve que le chemin qu'il parcourt. Sur un paiement, il établit le cas nominal, pas le refus de carte ni la justesse du montant. Le mécanisme est vrai sur *la preuve que le chemin existe*, faux sur *la discrimination des cas*.

Il fonde donc une exigence, jamais une préférence générale : sur un domaine critique, la matrice exige le nominal **et** le dégradé, jamais un ancrage seul. Une lecture qui en tirerait « ancré vaut mieux qu'interne » remplacerait une autorité aveugle par une autre.

## Decision

### 1 — La phase devient l'autorité classante, par une matrice `phase × niveau de domaine`

Les domaines disent ce qui compte, la phase dit quelle preuve elle en exige maintenant. Chaque cellule porte une **preuve exigée** et un **plafond numérique**. Ce qui est arrêté ici est la forme : 4 phases × 4 colonnes ; les valeurs se calibrent à la rédaction du défaut générique.

**L'axe est le niveau du domaine, jamais son nom.** Un axe indexé par nom n'est pas énumérable : le catalogue de domaines est un **plancher de détection**, jamais l'inventaire, donc le nombre de domaines est ouvert et chaque domaine détecté exigerait une cellule inédite. Ce serait le problème d'idempotence du scan remonté d'un cran — dans l'arbitrage cette fois, où il n'est plus rattrapable. Indexée par niveau, la matrice est stable sous ajout de domaine : détecter un domaine de plus ne la touche pas, seule son affectation à une colonne est nouvelle.

La phase n'est pas supprimable : elle est ce qui évite une couverture excessive, coûteuse à maintenir et ralentissant le développement. Le présent ADR lui donne le droit de classer ; il ne la met pas en cause.

### 2 — DEC-004 §4 est amendé : le principe survit, la désignation tombe

**Ce qui tombe** : la désignation de la table des tiers, puis du framework de décision générique, comme dépositaires de l'autorité de classement. Il n'y a plus de tier à raffiner — le tier n'est plus décidé, il est produit (voir *Consequences*).

**Ce qui survit** : §1 (découverte par glob, jamais par chemin en dur), §2 (le contrat appartient au consommateur, chaque champ optionnel avec son repli), §3 (une section par champ, un champ non localisé est traité comme absent), et le **principe** du §4 — *le pivot priorise, il ne classe pas* — promu **règle transversale** sous la forme « l'instrument qui mesure ne peut pas trancher », qui couvre du même coup `05-stats`, la densité et les *Risk signals*.

Motif de l'amendement plutôt que de la réécriture : ce que le §4 protégeait est intact, seule sa formulation nommait un dépositaire que la décision 1 remplace. **DEC-004 ne reçoit qu'un en-tête de statut** ; son corps reste ce qu'il était le 2026-07-22. Un ADR ne se réécrit pas après acceptation, sinon le motif de l'amendement devient illisible faute d'état antérieur à lui opposer.

### 3 — `Tier thresholds` du contrat de pivot devient `Anchor boundary`

Motif tiré du contenu réel du seul pivot existant, non d'une préférence de vocabulaire. Ce champ y porte du savoir de stack vérifié — émulateur, mismatch d'hydratation, handler serveur appelé directement — et ces règles ne disent pas *quel tier* : elles disent **où passe, dans cette stack, la frontière entre une preuve ancrée et une preuve interne**. « Un test contre l'émulateur reste interne » énonce que l'émulateur n'ancre pas ; « un mismatch d'hydratation n'est prouvable qu'en navigateur réel » énonce que seul le navigateur ancre.

Le champ était mal nommé, pas inutile : son contenu est conservé tel quel sous le nouveau titre. Le renommage est aussi ce qui rend le champ exprimable pour les stacks sans navigateur — CLI, bibliothèque, service — où « tier » n'avait pas de référent et où la frontière d'ancrage en a un.

**Conséquence de compatibilité, en toutes lettres.** DEC-004 §5 a déclaré le contrat de `control` **interface publique** : le modifier de façon incompatible casse les pivots existants. Le renommage est un tel changement. Un pivot tiers non mis à jour conserve un titre que le consommateur ne sait plus localiser, et DEC-004 §3 impose alors de traiter le champ comme **absent** — la stack perd son savoir d'ancrage sans qu'aucune erreur ne soit levée. La dégradation est silencieuse, ce qui est le pire mode de rupture pour une interface publique. D'où deux exigences, non négociables :

- le renommage vaut **changement majeur** pour `overcode`, acté au bump qui publie le contrat modifié ;
- la mise à jour du pivot `sc-js` atterrit **dans le même commit** que le changement de contrat — un commit intermédiaire où le contrat et le pivot divergent est un état publiable, donc un état qui sera publié.

### 4 — Le plafond refuse un ajout, il n'exige jamais un retrait

Sur un domaine au plafond, la production d'une preuve supplémentaire est refusée avec son motif chiffré ; aucune preuve existante n'est jamais désignée pour retrait.

Motif — la même asymétrie que DEC-006/D3, appliquée à l'autre bout du mécanisme : **refuser un ajout ne fait que resserrer, exiger un retrait déciderait à la place du projet.** Le refus reste franchissable : la skill propose, l'utilisateur choisit.

Motif de la forme *plafond* plutôt que *seuil* : l'interdiction de seuil numérique qui régnait jusqu'ici visait un **plancher**, lequel dégénère en cible dès qu'il est affiché. Un plafond ne peut pas devenir une cible — il ne peut être qu'atteint ou dépassé. L'interdiction tombe donc sans que son motif soit désavoué.

Motif de l'unité — **nombre de preuves, par domaine et par phase**. L'objection connue contre les caps absolus vise un cap *projet* (« pas plus de N tests »), incapable de distinguer une grosse suite d'une grosse base de code. Un plafond par domaine et par phase n'a pas ce défaut : il est déjà relatif à une population identifiée et à un moment.

Enfin, le plafond **classe** — il transforme une sortie en `skip`. Ce n'est pas une violation de la règle transversale de la décision 2 : celle-ci vise les instruments de **mesure**, et le plafond n'en est pas un. Il est énoncé par la phase, devenue l'autorité classante.

### Calibrage — deux valeurs s'écartent de la proposition de départ

La proposition de départ a été confrontée, cellule par cellule, à deux dépôts réels : un dépôt applicatif d'environ 80 fichiers de test avec rapport de couverture et zones fonctionnelles nettes, et un dépôt d'outillage d'environ 60 fichiers de test sans aucun rapport de couverture ni domaine établi.

**Les cellules à preuve ancrée tiennent, et le calibrage le confirme plutôt qu'il ne le suppose.** Dans le dépôt applicatif, aucune preuve n'est ancrée au sens de la décision 3 : la totalité des tests de vue passent par le client de test en processus du framework, et le seul fichier portant `e2e` dans son nom déclare lui-même que ses cas simulent le réseau et que sa variante réelle est exclue de l'exécution par défaut. Un plafond de 1 à 4 preuves ancrées par domaine ne refuse donc aucun ajout légitime au premier usage : il mord là où l'ancrage devient redondant, et nulle part ailleurs.

**Les cellules à preuve interne ne tiennent pas à la valeur 2, et la donnée décisive n'est pas le sur-test.** L'objection évidente — des zones fonctionnelles ordinaires portant plus de cent cas — se retourne : un plafond largement dépassé sur une zone manifestement sur-testée est le verdict que la skill existe pour rendre, pas un défaut de calibrage. Ce qui réfute la valeur, c'est le cas opposé : dans le même dépôt, les **deux zones les plus étroites** — une messagerie, un cycle d'offres — portent chacune **six preuves internes** couvrant l'appariement canonique, le gating par réciprocité, l'idempotence de réception, l'expiration et les états de lecture. Aucune lecture ne qualifie cela de couverture excessive. Un plafond de 2 refuserait donc un ajout légitime sur la population la mieux tenue du dépôt, dès le premier usage, et sa seule sortie praticable serait le forçage — or un plafond dont le régime normal est d'être forcé n'est plus un plafond.

D'où **`production × ordinaire` et `sustaining × ordinaire` passent de 2 à 6**. Toutes les autres valeurs sont conservées.

**La colonne hors-domaine est confrontée et conservée à l'identique.** Le dépôt d'outillage porte plus de trois cents preuves internes et aucun domaine établi : tout y est hors-domaine. Aucune valeur ne rendrait ce plafond non saturé, et en chercher une serait se tromper de mécanisme — la sortie prévue pour ce cas n'est pas un chiffre plus haut, c'est l'établissement des domaines. Le refus y est structurel et son motif est exact ; il porte l'annonce du régime hors-domaine et le renvoi à l'action qui l'établit.

## Consequences

- **Le tier devient un nom de sortie.** `contract` / `e2e` / `skip` nomment la forme de preuve produite ; ils ne la choisissent plus. Le vocabulaire est conservé volontairement : la précision conceptuelle de l'ancrage s'obtient sans rupture sur la skill, la page, les suites d'évals, le pivot et tout document de stratégie de projet existant.
- **Les composants s'exécutent en série, non en parallèle** : les domaines d'abord — qu'est-ce qui compte ici —, la phase ensuite — quelle preuve j'en exige maintenant. La pondération simultanée de quatre modulateurs disparaît avec le défaut qu'elle compensait.
- **Les six critères de risque survivent comme classement *intra*-domaine** : ils ordonnent au sein d'une colonne, ils ne décident plus du régime.
- **`05-stats` ne conclut jamais.** Il affiche ce qui est déclaré et ce qui est mesuré ; il ne produit rien qui soit déduit des deux. Un verdict du type « il y a un domaine sans sa preuve » est une **application de la matrice**, donc l'arbitrage de la phase : le rendre dans `stats` recréerait un second lieu d'arbitrage, c'est-à-dire exactement le défaut que cette décision supprime.
- **DEC-004 porte désormais un en-tête d'amendement.** Toute lecture du §4 passe par le présent ADR ; aucune autre ligne de DEC-004 n'a bougé.
- **L'ordre imposé par DEC-006 est maintenu** : la page publie le modèle avant que la skill ne le réalise. L'écart page/skill qui en résulte est déclaré, pas subi.

## Alternatives rejetées

- **Supprimer la phase et ne garder que les domaines.** La phase est ce qui borne l'exigence dans le temps ; sans elle, un projet en amorçage se voit demander la couverture d'un projet en exploitation. Option définitivement close : elle ne doit pas être reproposée.
- **Ajouter un critère d'importance à la table des tiers.** Cinquième dispositif greffé sur le même défaut : l'autorité resterait à un instrument qui ne connaît que la forme du comportement.
- **Indexer la matrice par nom de domaine.** Donnerait des exigences plus fines, mais rendrait la matrice non énumérable et instable à chaque détection — le coût est porté par l'arbitrage, là où il n'est plus rattrapable.
