# Refonte de `overcode:control` — la phase arbitre, les domaines portent

| Champ | Valeur |
|---|---|
| Date | 2026-07-28 |
| Cible | `plugins/overcode/skills/control/` + `plugins/overcode/docs/control.md` |
| Origine | audit `aidd_docs/tasks/audits/2026_07_code-quality_control.md` (santé **poor** — 3 critiques / 4 warnings / 2 mineurs) |
| Statut | **arbitré — planifiable** |
| Antécédents | `2026_07_21-control-skill-testing-pivot-hardening.md`, `2026_07_22-control-phase-governance-*`, `2026_07_27-control-ddd-alignment-*` |
| ADR touchés | DEC-004 (amendement requis), DEC-006 (contrainte de séquence) |
| Analyses liées | rapport shadow `…-shadow-report.md` (16 gaps) · [issue #10](https://github.com/RebelliousSmile/my-claude-marketplace/issues/10) (pivots) |

---

## 1. Objet

`control` doit **contrôler que l'application fonctionne, en portant son regard sur ce qui est important** — au lieu de produire une batterie de tests lourde et coûteuse à maintenir.

L'écart constaté : la skill décide aujourd'hui d'un tier (`contract` / `e2e` / `skip`) par une table qui ne sait rien de l'importance. Elle sait ce qu'un comportement *est*, jamais ce qu'il *vaut* pour ce projet à ce moment. Les quatre modulateurs greffés autour (phase, domaines, densité, *Risk signals*) corrigent ce défaut par pondération, sans jamais pouvoir le redresser : **aucun d'eux n'a le droit de classer.**

## 2. Diagnostic

### 2.1 Le mécanisme derrière l'hypothèse « e2e > contrat sur du code écrit par un agent »

Le pouvoir de détection d'un test tient à son **indépendance vis-à-vis de la source de l'erreur**. Quand un agent écrit à la fois le code et son test de contrat, les deux procèdent de la même compréhension : le test rejoue le malentendu au lieu de l'attraper. Un test qui traverse la frontière publique du produit ne partage pas cette origine — il est **ancré** ailleurs.

**Contre-argument conservé, il n'est pas réfuté** : un test ancré ne prouve que le chemin qu'il parcourt. Sur le paiement, il établit le cas nominal, pas le refus de carte ni la justesse du montant. L'hypothèse est vraie sur *la preuve que le chemin existe*, fausse sur *la discrimination des cas*. C'est pourquoi la matrice (§3.2) exige sur les domaines critiques **le nominal ET le dégradé**, jamais un ancrage seul.

### 2.2 Le défaut architectural

Quatre dispositifs se disputent la même fonction sans qu'aucun ne la détienne :

| Dispositif | Ce qu'il apporte | Ce qu'il ne peut pas |
|---|---|---|
| table des tiers | classe | ignorer l'importance |
| phase | pondère l'ordre | classer |
| domaines | ordonnent la lecture | classer |
| densité | signale | classer |
| *Risk signals* (pivot) | priorise | classer |

Résultat : la seule autorité classante est aussi la seule aveugle à l'enjeu. Empiler un cinquième critère n'y changerait rien — c'est l'architecture qu'il faut reprendre.

## 3. Architecture cible

### 3.1 La phase passe de pondérateur d'ordre à **régulateur d'exigence**

La phase est l'ADN de la skill : c'est elle qui évite une couverture excessive qui rendrait l'évolution des tests fastidieuse et ralentirait le développement. **Sa suppression n'est pas envisageable et ne doit jamais être reproposée.**

Elle gagne le droit de fixer un **plafond par domaine**. L'interdiction de seuil numérique de `SKILL.md:80` tombe : elle visait un *plancher*, qui dégénère en cible ; un *plafond* ne peut pas devenir une cible, il ne peut être qu'atteint ou dépassé.

### 3.2 La matrice **phase × niveau de domaine**

Elle remplace quatre dispositifs : la table des tiers comme autorité, la pondération par phase des six critères de risque, les deux axes de lecture, et la règle des quatre modulateurs.

**L'axe n'est pas le domaine nommé, c'est son niveau.** Un axe indexé par nom de domaine ne serait pas énumérable : le catalogue est un *plancher de détection*, donc le nombre de domaines est ouvert, et chaque nouveau domaine détecté exigerait une cellule inédite — le problème d'idempotence du scan (`A B C' D" E°`) remonté d'un cran, dans l'arbitrage cette fois.

**Trois niveaux, plus le hors-domaine.** `06-align` attribue le niveau en même temps que le nom.

|  | critique | structurant | ordinaire | hors-domaine |
|---|---|---|---|---|
| `scaffolding` | 1 preuve ancrée | — | — | — |
| `hardening` | ancrée + interne, 2 | 1 ancrée | — | — |
| `production` | ancrée nominale + dégradée, 3 | ancrée, 2 | interne, 2 | — |
| `sustaining` | ancrée, 4 | ancrée, 2 | interne, 2 | interne sur régression, 1 |

> **Les valeurs ci-dessus sont une proposition de départ, pas la décision.** Ce qui est arrêté, c'est la **forme** : 4 phases × 4 colonnes, cellule = *preuve exigée + plafond numérique*. Les valeurs se calibrent à la rédaction de `references/decision-matrix.md`.

`default` et `undetermined` prennent le régime le plus permissif, **en le disant** — l'un est une décision écrite du projet (DEC-006/D2), l'autre une question sans réponse, et la sortie doit les distinguer.

Conséquences directes :

- **le tier devient une sortie, pas une décision** — il nomme la forme de preuve produite, il ne la choisit plus ;
- **composants en série, non en parallèle** : les domaines d'abord (qu'est-ce qui compte ici), la phase ensuite (quelle preuve j'en exige maintenant) ;
- **les six critères de risque survivent** comme classement *intra*-domaine (`04-strengthen:51`) — ils ordonnent au sein d'une colonne, ils ne décident plus du régime ;
- **la matrice est stable sous ajout de domaine** : détecter F et G ne la touche pas, seule leur affectation à une colonne est nouvelle. §3.4 protégeait le scan ; ceci protège l'arbitrage.

**Emplacement** : `references/decision-matrix.md` comme défaut générique, **surchargeable par le document du projet**, sur le mécanisme de précédence déjà en place (`05-stats:42` — `authority : project doc <path> | generic default`). Aucun dispositif nouveau.

### 3.3 Le plafond **refuse un ajout**, jamais il n'exige un retrait

Un plafond qui n'oppose rien n'est pas un plafond : c'est un second signal à côté de la densité, et §3.1 serait vide.

- `01-write` sur un domaine au plafond rend **`skip`**, motif « plafond atteint (n/n) — `<phase> × <niveau>` », et offre trois sorties : déclarer la phase suivante, retirer un test du domaine, ou forcer par décision explicite tracée.
- **Refus franchissable, jamais blocage dur** — `05-stats:121` : la skill propose, l'utilisateur choisit.
- **Asymétrie ajouts / retraits**, exactement celle que DEC-006/D3 a déjà établie et motivée : refuser un ajout ne fait que resserrer, exiger un retrait déciderait à la place du projet.

**À écrire noir sur blanc, sinon ce sera lu comme une contradiction** : le plafond *classe* (il transforme un tier en `skip`). Ce n'est pas une violation de « l'instrument qui mesure ne peut pas trancher » — le plafond n'est pas un instrument de mesure, il est énoncé par la phase, **devenue l'autorité classante**.

**Unité : nombre de preuves, par domaine et par phase.** L'objection de `test-density.md:13` contre les caps absolus vise un cap *projet* (« pas plus de N tests »), incapable de distinguer une grosse suite d'une grosse base de code. Un plafond par domaine et par phase n'a pas ce défaut : il est déjà relatif à une population identifiée et à un moment. Une expression en multiple de médiane est écartée — elle hériterait des cas dégénérés de la densité et disparaîtrait en `scaffolding`, la phase où elle compte le plus.

### 3.4 L'**ancrage** est une propriété ; `contract` / `e2e` / `skip` restent les noms de sortie

La matrice exige une **preuve ancrée** ou une **preuve interne** ; la sortie continue de s'appeler `e2e` ou `contract`. On gagne la précision conceptuelle de §2.1 sans rupture de vocabulaire sur la skill, la page, cinq suites d'évals, le pivot `sc-js` et tout `testing.md` de projet existant.

**Ancré ne veut pas dire navigateur.** L'ancrage est la **frontière publique du produit**, et sa position dépend de la stack :

| Stack | Ce qui ancre |
|---|---|
| application web | le navigateur réel, parcours complet |
| API / service | la frontière HTTP réelle |
| CLI | l'invocation du binaire |
| bibliothèque | l'API publique consommée de l'extérieur |

C'est ce qui permet à la matrice de s'appliquer à `sc-rust`, `sc-python` ou une CLI sans exiger un runner E2E qui n'existe pas dans ces stacks.

### 3.5 Les domaines sont établis et écrits par `06-align`

Quasi-statiques : ils n'évoluent qu'à l'occasion de gros changements applicatifs.

**Production : catalogue de référence × scan du code**, où le catalogue est un **plancher de détection, jamais l'inventaire**. Il garantit qu'on ne rate pas `auth` ou `payment` ; il n'interdit à aucun domaine propre au projet d'exister.

- **Catalogue** : `references/domain-catalogue.md` — une douzaine de domaines transverses avec leur **niveau par défaut** (`auth` critique, `payment` critique, `notification` structurant…). Le niveau par défaut est une proposition, jamais une imposition.
- **Un domaine n'existe que confirmé par l'utilisateur.** `align` propose, il ne devine jamais seul. Sur une base sans conventions structurelles (monolithe procédural, thème WordPress), `align` rendra peu et le résidu sera large — **c'est un fait à rapporter, pas un échec à masquer.** C'est précisément ce que `05-stats:88` reproche au mode de défaillance actuel, où la zone ratée ressort comme « zone sans manque » au lieu de ressortir comme non couverte par le vocabulaire.
- **Artefact écrit** : `<projet>/aidd_docs/memory/testing-domains.md`. **`align` n'écrit pas dans `testing.md`**, qui reste à `aidd-context` — un fichier, un écrivain, pas de perte d'écriture possible.
- **Format des termes de résolution** : littéraux, insensibles à la casse, plus les chemins. **Pas de regex** — le fichier est édité à la main par le projet, et une regex y devient illisible puis fausse.

### 3.6 Idempotence par jugement matérialisé

Le problème posé : un scan à 50 % d'avancement trouve A B C D E ; un scan à 75 % doit rendre **A B C D E + F G**, jamais `A B C' D" E°`.

Solution — déplacer le non-déterminisme de l'exécution vers l'établissement : `align` juge **une fois** et fige son jugement en termes littéraux. Les passages suivants **appliquent** au lieu de re-résoudre ; seul le **résidu** (fichiers sans aucune correspondance) est scanné à neuf.

- appartenance **multiple** : un fichier peut relever de plusieurs domaines ;
- **capteurs de dérive** : résidu qui croît, termes devenus orphelins — **rapportés par `05-stats`, jamais appliqués**. La boucle se ferme ainsi : `stats` rapporte → l'utilisateur décide → `align` re-juge. Seuil de signalement : relatif, avec un plancher absolu (un résidu de 2 fichiers sur 8 n'est pas une dérive) ;
- **renommer est une opération explicite d'`align`**, jamais un effet de bord d'un scan.

`05-stats:118` porte déjà le résidu et sa trace de dérive. L'architecture l'étend, elle ne l'invente pas.

### 3.7 Sans domaines établis : le régime hors-domaine s'applique

Un projet où `06-align` n'a jamais tourné n'est pas un cas particulier — **tout son code est hors-domaine, et la colonne existe déjà** dans la matrice. Chaque action annonce « aucun domaine établi, régime hors-domaine appliqué, lancez `06-align` ».

Le repli n'est pas un mécanisme de plus : c'est un cas du mécanisme. Il couvre aussi le premier contact avec un projet, qui est précisément ce que `05-stats` sert en tant que porte d'entrée.

Même règle pour un projet dont le `testing.md` est antérieur à la refonte : sa stratégie documentée garde son autorité sur ce qu'elle déclare (les tiers, un cap éventuel), et l'absence de niveaux de domaine déclarés le place en régime hors-domaine jusqu'à ce qu'`align` tourne.

### 3.8 `05-stats` reste la porte d'entrée et **ne conclut jamais**

Borne, à inscrire telle quelle : **« `stats` affiche ce qui est déclaré et ce qui est mesuré. Il ne produit rien qui soit déduit des deux. »**

Motif : un verdict du type « il y a un domaine sans sa preuve » est une *application de la matrice*, donc l'arbitrage de la phase. Le rendre dans `stats` créerait **deux lieux d'arbitrage** — exactement le défaut que la refonte supprime.

- le bloc `VOLUME` (`contract : n / e2e : n / ratio`) devient un bloc **`DOMAINES exigé / trouvé`** ;
- le drapeau « pyramide inversée » (`05-stats:114`) est **supprimé sans remplacement** : routé vers `02-audit`, qui ne peut rien en faire. Il n'existait que parce que mesurer sans référent oblige à inventer un signal ; la matrice fournit le référent, le drapeau disparaît de lui-même ;
- la table `excluded` (`:23-25`, issue de DEC-006/D5) est **conservée** — elle est ce qui empêche la phase de restreindre en silence.

### 3.9 Deux règles transversales, énoncées une fois

1. **L'instrument qui mesure ne peut pas trancher.** (couvre `stats`, la densité, les *Risk signals* — remplace les quatre réécritures locales de la borne d'autorité)
2. **Le pivot déclare ce qu'il fournit, jamais qui le consomme.** (supprime le droit d'usage exclusif que *Risk signals* s'attribue en finissant par « Consumed by `strengthen` »)

### 3.10 *Tier thresholds* est **renommé, pas supprimé**

Vérification faite sur le seul pivot existant : `sc-js/.../tools/testing.md:86-104` remplit ce champ avec 19 lignes de savoir stack réel et vérifié — émulateur Firebase, mismatch d'hydratation Nuxt, handlers Nitro appelés directement.

Ce que ces règles décrivent n'est pas *quel tier*, c'est **où passe la frontière d'ancrage dans cette stack** :

- « un test contre l'émulateur reste `contract` » → l'émulateur n'ancre pas ;
- « un mismatch d'hydratation n'est prouvable qu'en `e2e` » → seul le navigateur réel ancre ;
- « une route Nitro est testable par appel direct au handler » → pas besoin d'ancrage.

**Le champ était mal nommé, pas inutile.** Il devient **`Anchor boundary`** — *où passe, dans cette stack, la frontière entre une preuve ancrée et une preuve interne*. Le contenu de `sc-js` est conservé tel quel, recadré sous le nouveau titre. Ce renommage est aussi ce qui rend le contrat exprimable pour `sc-rust` et les stacks sans navigateur (§3.4).

### 3.11 Rebranchements pivot

Analyse complète en [issue #10](https://github.com/RebelliousSmile/my-claude-marketplace/issues/10). Ce que la refonte doit traiter :

| Action | Champ à brancher | État actuel |
|---|---|---|
| `06-align` | *Domain resolution* | ne lit **aucun** pivot — c'est le trou le plus coûteux, `align` devient le producteur des domaines |
| `01-write` | *Risk signals* | `:33` traite les frontières externes en générique |
| `02-audit` | *Risk signals* | ignoré |
| `03-configure` | *Coverage command* | ignoré, alors que `test-density.md:55-56` lui route les deux cas dégénérés de couverture |

- **champ fantôme à supprimer** : `05-stats:106` « split contract vs e2e by the pivot's respective globs » — le contrat ne déclare qu'**un seul** `Test file glob` (`:20`). Deux *runners*, un seul glob ;
- **champ mort à trancher** : *Canonical E2E tool* (`:33`), lu par personne. Le brancher dans `03-configure:28` ou le supprimer ;
- le contrat est réécrit **en format questionnaire**, remplissable sans lire une seule action du consommateur. **Aucun champ ne nomme son consommateur.**

## 4. Ce qui disparaît

| Élément | Emplacement | Motif |
|---|---|---|
| `decision-framework.md` / table des tiers **comme autorité** | référence + 4 actions | remplacé par la matrice |
| tie-break par le coût | table des tiers | le coût n'est pas un critère d'importance |
| borne unidirectionnelle du pivot sur le tier | `pivot-contract.md:24` | il n'y a plus de tier à raffiner |
| globs contract/e2e fantômes | `05-stats:106` | champ inexistant |
| drapeau pyramide inversée | `05-stats:114` | sans destinataire capable d'agir |
| 4 réécritures locales de la borne d'autorité | actions | remplacées par §3.9 règle 1 |

**Cinq doctrines contredites, à réécrire et non à supprimer** : `SKILL.md:77`, `phase-framework.md:5`, `phase-framework.md:200` et `:207`, `06-align.md:81`.

`phase-framework.md:199-203` a **déjà** perdu son argument par analogie (DEC-006) ; sa justification propre reste à écrire. La refonte absorbe cette dette au lieu de la traiter séparément.

## 5. Contraintes de séquence — non négociables

### 5.1 DEC-006 impose l'ordre : page → évals → skill

`docs/control.md` fait foi sur `skills/control/`. L'ordre **page → suites `behave` rouges → skill** est déclaré non cosmétique dans l'ADR : *« `behave` teste des sorties, jamais la cohérence entre deux documents normatifs. Une incohérence page/référence introduite par le mauvais bout n'aurait été détectée par rien. »*

Partage de charge : **la page porte la règle et son motif ; la skill porte la règle et sa procédure ; l'ADR porte le rationnel.** Aucune étape de `## Process` ne remonte sur la page.

**Critère de fin de chantier** : toutes les suites `behave` au vert, et aucune règle de `docs/control.md` sans contrepartie procédurale dans `skills/control/`. Les scénarios que la refonte rend caducs sont réécrits, jamais supprimés en silence.

### 5.2 DEC-004 §4 est contredit — un amendement d'ADR est requis

DEC-004 §4 grave : *« L'autorité sur le tier reste à la stratégie du projet puis au framework de décision générique — un pivot ne peut la raffiner que sur une frontière restant locale/émulée. »*

**Ce qui survit** : §1 (découverte par glob), §2 (le contrat appartient au consommateur), §3 (une section par champ), et le **principe** de §4 — *le pivot priorise, il ne classe pas* — qui devient la règle transversale §3.9-1.
**Ce qui tombe** : la désignation de la table des tiers comme dépositaire de l'autorité de classement.

Le contrat étant déclaré **interface publique** par DEC-004 §5, l'ADR d'amendement est un livrable du plan. Le renommage `Tier thresholds` → `Anchor boundary` (§3.10) y est tracé, avec la correction de `sc-js` **dans le même commit** que le changement de contrat.

### 5.3 Contrainte marketplace

Bump de version et changement de contenu **atterrissent dans le même commit** ; aucune installation contre un arbre sale. Travail en source (`plugins/<name>/skills/`), jamais dans le cache.

## 6. Points résiduels — non bloquants

- **Calibrage des valeurs de la matrice** (§3.2) — la forme est arrêtée, les chiffres se posent à la rédaction de `references/decision-matrix.md`.
- **Contenu initial du catalogue de domaines** (§3.5) — la douzaine d'entrées transverses est à écrire.
- **Sort de *Canonical E2E tool*** (§3.11) — brancher ou supprimer.

## 7. Hors périmètre

Reporté explicitement **après** la refonte. **L'analyse complète des pivots — inventaire, carte de consommation champ par champ, quatre trous durs, champ fantôme, champ mort, cause racine, deux mécanismes de distribution — est consignée en [issue #10](https://github.com/RebelliousSmile/my-claude-marketplace/issues/10).**

- écriture des cinq pivots `testing` manquants — `sc-python` d'abord, **`sc-rust` tôt car il casse trois hypothèses du contrat**, puis `sc-php`, `sc-css`, `sc-godot` ;
- vérification de `sc-css/skills/sniff/actions/02-install-pivots.md` (jamais ouvert) ;
- **mécanisme de distribution des pivots** — lecture in-plugin contre installation dans `.claude/rules/07-quality/`. Chantier propre, dont aucune décision ci-dessus ne dépend.
