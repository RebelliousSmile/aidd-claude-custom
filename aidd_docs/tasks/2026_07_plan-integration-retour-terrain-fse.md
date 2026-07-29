---
type: plan
statut: proposé
date: 2026-07-28
périmètre: design · sc-php · sc-css · sc-js
matériau: un journal d'intégration maquette → FSE, utilisé comme falsificateur
---

# Plan d'intégration multi-plugins — retour de terrain « maquette → site éditable »

## Ce que ce document est

Un terrain a exercé la chaîne `design` → pivots `sc-*` de bout en bout et a produit un journal de ses défauts. Ce journal n'est pas un plan : c'est un **falsificateur**. Chaque défaut y a été soumis à un test unique —

> **Quel skill a permis, induit, ou omis d'empêcher ce défaut ?**

Aucun skill nommable ⇒ imputation projet ⇒ écarté sans traitement. Un skill nommable ⇒ retenu, puis **généralisé en classe de cas** dépouillée de la plateforme, du projet et de tout nom de fichier de terrain. Ce qui ne survit pas à ce dépouillement descend au pivot correspondant ; ce qui n'y survit toujours pas part en quarantaine (`2026_07_quarantaine-retour-terrain-fse.md`).

Un terrain unique ne prouve aucune classe de cas. Il ne peut que la **réfuter**. Tout énoncé ci-dessous vaut donc par sa cohérence interne avec le contrat du plugin visé, pas par la fréquence observée.

## Forme des énoncés

Chaque item porte un **énoncé cible** : ce que le skill doit garantir, sans présumer quel fichier le portera. Cette forme est délibérée — elle survit à la refonte en cours de `design` et des pivots, et à l'arbitrage `design` ↔ pivot qui n'est pas tranché ici.

Deux natures, jamais confondues :

| Nature | Sens | Ce qu'on écrit |
|---|---|---|
| **manque** | le skill devrait garantir X et ne le garantit pas | un énoncé cible à implémenter |
| **opposable** | l'outil ne peut structurellement pas dire X | un énoncé que le plugin **déclare ne pas mesurer** |

Un opposable n'est pas une fonctionnalité reportée. C'est une limite publiée, qui rend illégitime de lire un vert comme une garantie qu'il ne porte pas.

Toute écriture ultérieure dans un skill passe par `aidd-context:03-context-generate`, sous-flux `skills`, règles R1–R9. Aucun énoncé destiné à `design` ne nomme de plateforme.

---

## A — Champ optique des gates

> **Classe de cas.** Un programme de vérification déclare le *périmètre* de ses gates (quels fichiers) sans déclarer leur *champ optique* (quelles propriétés du réel elles atteignent). Un vert est alors lu comme une garantie sur tout ce que le lecteur croit vérifié.

### ÉC-A1 — Un gate documentaire déclare qu'il ne lit aucune exécution
- **Énoncé.** Le programme déclare que ses gates lisent des documents et des rendus statiques, et qu'aucune ne constate qu'un élément interactif est relié à un comportement. Un composant syntaxiquement conforme et fonctionnellement inerte est un vert légitime du gate, jamais une conformité du produit.
- **Plugin.** `design`
- **Nature.** opposable
- **Imputation.** Le référentiel canonique des natures de gate énumère ce qui n'est pas couvert (rôles ARIA, fond appliqué, contraste du rendu, fichiers hors cibles) sans jamais y faire figurer le comportement. Le terrain a livré deux champs de filtre rendus conformes et morts, sous verdict fermé.

### ÉC-A2 — L'oracle de fidélité déclare son domaine de propriétés
- **Énoncé.** L'oracle publie la liste close des propriétés qu'il compare et énonce que toute propriété hors de cette liste n'est pas mesurée. Une divergence portant sur une propriété non listée ne peut pas être ouverte par l'oracle ; ce n'est ni une conformité ni un silence, c'est un hors-champ déclaré.
- **Plugin.** `design`
- **Nature.** opposable, avec un **manque** attenant : la liste doit être lisible depuis le rapport, pas seulement depuis le code de l'adaptateur.
- **Imputation.** Le comparateur s'arrête aux paddings, gaps, typographie et couleurs. Aucune propriété de boîte ni de flux (`margin*`, dimensions, `box-sizing`, `display`) n'y figure. Le terrain a passé sept verdicts fermés sur des vues dont l'aplomb était faux de plusieurs dizaines de pixels.

### ÉC-A3 — Un oracle relatif déclare son angle mort symétrique
- **Énoncé.** Un oracle qui compare une implémentation à une référence déclare qu'il est aveugle à tout défaut identiquement présent des deux côtés. Il prouve la conformité à la référence, jamais la qualité de la référence. Corollaire opposable : toute porte absolue doit s'exécuter **sur la référence, avant** l'implémentation, sinon elle mesure un écart déjà consenti.
- **Plugin.** `design`
- **Nature.** opposable
- **Imputation.** Le référentiel des natures de gate distingue déjà référence interne et référence externe, mais n'énonce nulle part cette conséquence. Le terrain a mesuré un ratio de contraste conforme des deux côtés d'une comparaison, sur une paire non conforme dans l'absolu.

### ÉC-A4 — Le socle a un statut contractuel explicite
- **Énoncé.** Le contrat statue sur les règles qui ne sont ni une valeur nommée ni une anatomie de composant — remise à zéro, modèle de boîte, marges par défaut, héritages typographiques. Soit elles entrent dans un artefact du contrat, soit le programme déclare qu'elles en sont exclues et nomme qui les tient. Elles ne peuvent pas rester sans statut.
- **Plugin.** `design`
- **Nature.** manque
- **Imputation.** Les cinq verbes du entonnoir couvrent les valeurs et les anatomies. Le socle traverse les deux sans appartenir à aucun, donc échappe au figeage comme à l'enforcement, sans qu'aucun rapport ne le signale.

### ÉC-A5 — La stratégie de cascade constate l'ordre d'impression, pas seulement la topologie de layer
- **Énoncé.** Le réalisateur de feuilles de style constate l'**ordre effectif d'insertion** des feuilles dans le document rendu, en plus de la présence ou de l'absence de couches. À couches égales — y compris toutes deux absentes — la dernière feuille imprimée l'emporte à spécificité égale : émettre hors couche ne suffit pas si l'émission précède celle de l'hôte.
- **Plugin.** `sc-css`
- **Nature.** manque
- **Imputation.** La stratégie de couche du réceptacle traite « hôte layered » contre « hôte unlayered » et conclut, dans le second cas, à émettre hors couche. Elle ne mesure pas l'ordre d'impression, qui est le seul départage restant. Le terrain a exposé cent-dix règles perdant silencieusement contre l'hôte, toutes hors couche des deux côtés.

---

## B — Vert par vacuité

> **Classe de cas.** Une vérification qui n'a rien eu à lire retourne le même signal qu'une vérification qui a tout lu et tout validé. Le vert n'a pas de référent.

### ÉC-B1 — Toute vérification déclarative porte son compte de sujets
- **Énoncé.** Une vérification agrégée en verdict booléen expose, dans le même objet, le nombre de sujets effectivement examinés. Un verdict positif sur zéro sujet est refusé ou marqué non concluant ; il n'est jamais rendu indistinguable d'un verdict positif sur N sujets. La règle vaut pour toutes les vérifications du programme, pas pour celle qui a motivé son écriture.
- **Plugin.** `design`
- **Nature.** manque
- **Imputation.** Vérifié dans le source : le contrôle de contraste porte sa garde de vacuité et la commente explicitement ; le contrôle d'états, quelques dizaines de lignes plus loin, retourne « complet » pour un composant qui ne déclare aucun état. Le terrain a lu un vert d'états sur zéro déclaration parmi soixante-quatorze composants. La règle de méthode existait déjà et ne s'est pas propagée d'un contrôle au suivant.

### ÉC-B2 — Aucune paire n'est appariée hors déclaration
- **Énoncé.** Les paires soumises à un calcul de conformité sont exclusivement celles que le contrat déclare. Aucune heuristique de nommage ne construit une paire que le rendu n'associe pas. Un faux rouge coûte le même prix qu'un faux vert : il fait corriger ce qui n'était pas cassé et déplace l'attention hors des vraies violations.
- **Plugin.** `design`
- **Nature.** manque
- **Imputation.** Le terrain a obtenu un échec de contraste sur six paires alors que zéro composant en déclarait, ce qui implique un appariement produit hors déclaration.

---

## C — Périmètre, dénominateur, peuplement

> **Classe de cas.** Le périmètre d'un gate est ce qu'une commande énumère, jamais ce qu'une phrase affirme. Un ratio sans dénominateur explicite est une assertion. Un gate qui **fabrique lui-même** son univers de référence ne mesure plus rien d'opposable.

### ÉC-C1 — Un gate de couverture reçoit son univers, il ne le déduit pas
- **Énoncé.** L'ensemble des sujets à couvrir provient d'une source contractuelle externe au gate. Aucune heuristique appliquée au corpus mesuré ne peuple cet ensemble. Si le gate doit néanmoins inférer son univers, il imprime le critère d'inférence, l'effectif retenu **et l'effectif écarté par ce critère** — un verdict de complétude sans ces trois nombres est irrecevable.
- **Plugin.** `sc-php`
- **Nature.** manque
- **Imputation.** Vérifié dans le source : l'univers attendu est peuplé par un préfixe unique, auto-détecté comme « le préfixe personnalisé le plus fréquent ». La mécanique de comparaison est correcte — deux sources indépendantes — mais un projet à plusieurs préfixes voit son attendu amputé en amont sans trace. Le terrain a lu une couverture complète portant sur trois composants d'un ensemble d'au moins soixante-seize.
- **Dépendance.** La source contractuelle naturelle est l'artefact d'anatomie du contrat `design`. L'arbitrage attend la refonte.

### ÉC-C2 — Une configuration d'oracle est produite par vue, jamais par union
- **Énoncé.** Le générateur de configuration produit, pour chaque vue mesurée, les cibles présentes **dans cette vue**. Il ne projette pas l'union des cibles du projet sur chaque vue. Corollaire : l'oracle distingue trois états et ne les confond jamais — cible mesurée et conforme, cible absente de cette vue par construction, cible attendue et introuvable.
- **Plugin.** `design`
- **Nature.** manque
- **Imputation.** Le générateur produit une union appliquée page par page ; le terrain a mesuré environ trois quarts de cibles inertes par configuration. La garde de couverture existante compare des titres d'implémentation à des cibles mesurées **à l'intérieur d'une vue** ; rien n'énumère l'ensemble des vues à mesurer, donc rien ne détecte une vue jamais soumise.

### ÉC-C3 — Un réalisateur refuse un artefact hors de sa grammaire
- **Énoncé.** Un réalisateur déclare la grammaire des artefacts qu'il sait lire et **refuse** par un code de sortie distinct tout artefact hors de cette grammaire. Il ne produit jamais de violations en traitant un artefact d'une autre nature comme s'il était de la sienne. Symétriquement, la sélection des fichiers soumis au gate et la grammaire acceptée par le réalisateur sont énoncées au même endroit : un artefact qu'aucun réalisateur n'accepte est **non réalisé**, jamais conforme par absence de gate.
- **Plugin.** `design`
- **Nature.** manque
- **Imputation.** Le registre d'enforcement énonce déjà que le linter lit « un fichier de markup à la fois, en texte », et route les feuilles de style vers le pivot. Rien n'empêche pourtant de lui soumettre une feuille de style : le terrain en a tiré sept-cent-trente-huit violations qui n'en étaient pas, chaque valeur héritée de la plateforme étant lue comme un identifiant absent du vocabulaire. Dans le même mouvement, le filtre de pré-commit ne retenant que le markup, les feuilles n'étaient tenues par rien.

---

## D — Exemptions

> **Classe de cas.** Une exemption sans propriétaire ni échéance n'est pas une dette, c'est une décision de ne jamais corriger, écrite dans le vocabulaire du sursis.

### ÉC-D1 — Le schéma d'exemption porte le propriétaire et l'échéance
- **Énoncé.** Une exemption enregistrée porte, par contrainte de schéma et non par convention de prose, un propriétaire — nommé, ou explicitement non attribué — et une échéance. L'absence de propriétaire est une valeur déclarée, jamais un champ manquant : elle doit être comptable. Une règle de méthode non portée par le schéma est démentie par les fichiers du programme lui-même.
- **Plugin.** `design`
- **Nature.** manque
- **Imputation.** Vérifié dans le source : le schéma d'exemption ne comporte aucun champ de propriétaire, et l'échéance y est optionnelle avec la mention explicite « absente ⇒ pas d'expiration ». Le terrain a compté quarante-quatre exemptions pour un propriétaire réel, deux registres sur quatre n'ayant pas même le champ — pendant qu'un artefact publié du même programme affirmait la règle inverse.

---

## E — Normalisation

### ÉC-E1 — La normalisation couvre tous les domaines de valeur comparés
- **Énoncé.** Toute propriété comparée par l'oracle passe par une forme canonique propre à son domaine de valeur — couleurs, longueurs, familles typographiques, ordre des raccourcis. Normaliser n'est pas tolérer : la forme canonique est exacte, et une valeur qu'elle ne sait pas analyser retombe en comparaison stricte plutôt que d'être réputée égale.
- **Plugin.** `design`
- **Nature.** manque (partiel — un domaine sur quatre est traité)
- **Imputation.** Vérifié dans le source : la canonisation des couleurs est implémentée, testée, et documentée comme « forme canonique, pas tolérance ». Aucun autre domaine n'en dispose. Le terrain a nommé les trois autres comme posant exactement la même question.

---

## F — Prose contre exécutable

> **Classe de cas.** Le périmètre d'un gate se convertit silencieusement en périmètre de vérité, et la prose qui décrit une garantie diverge de l'exécutable qui la tient, sans qu'aucun mécanisme ne le constate.

### ÉC-F1 — Un pivot renvoie à la garantie amont, il ne la réénonce pas
- **Énoncé.** Un réceptacle de pivot ne reformule jamais ce que le plugin amont garantit ou ne garantit pas : il y renvoie. Une garantie amont réécrite dans le pivot devient fausse au premier changement de l'amont, sans qu'aucun gate ne le détecte, et oriente la conduite du pivot sur une version périmée du contrat.
- **Plugin.** `sc-css`, `sc-js`, `sc-php` (règle transverse des réceptacles)
- **Nature.** manque
- **Imputation.** Vérifié dans le source : la procédure d'audit d'un pivot justifie sa posture par « le plugin design déclare le contraste comme gap non vérifié ». Ce n'est plus vrai — l'amont le calcule au figeage. La règle du pivot reste bonne ; sa justification est périmée et invérifiable depuis le pivot.

### ÉC-F2 — Aucun renvoi à un réalisateur que le programme ne définit pas
- **Énoncé.** Une garantie déclarée assignée à un réalisateur nomme un réalisateur défini dans le programme ou dans un contrat qu'il référence. Un renvoi à une entité que le programme ne définit nulle part est une prétention de couverture sans support, et si cette entité vient d'un projet particulier, c'est en plus une contamination de plateforme dans un plugin agnostique.
- **Plugin.** `design`
- **Nature.** manque
- **Imputation.** Cinq fichiers du plugin assignent le contraste peint à une porte nommée, absente de toute définition du plugin ; ce nom provient du programme de gates d'un projet précis.

---

## G — Effet d'un figeage sur l'aval

### ÉC-G1 — Un figeage périme les rapports d'enforcement antérieurs
- **Énoncé.** Le figeage d'un contrat marque comme périmé tout rapport d'enforcement produit contre la version précédente. Un rapport dont la version de contrat ne correspond pas au sceau courant n'est ni vert ni rouge : il est **non applicable**, et le programme le dit au lieu de laisser le dernier vert connu faire office d'état courant.
- **Plugin.** `design`
- **Nature.** manque
- **Imputation.** Le terrain a produit un nouveau sceau majeur, en a lu le statut comme validé, et n'a jamais rejoué l'enforcement — les artefacts du contrat étant par ailleurs modifiés et non commités, donc installables tels quels.

---

## Récapitulatif

| # | Énoncé | Plugin | Nature | Dépend de la refonte |
|---|---|---|---|---|
| A1 | Gates documentaires, aucune exécution lue | `design` | opposable | non |
| A2 | Domaine de propriétés de l'oracle déclaré | `design` | opposable + manque | non |
| A3 | Angle mort symétrique de l'oracle relatif | `design` | opposable | non |
| A4 | Statut contractuel du socle | `design` | manque | **oui** |
| A5 | Ordre d'impression, pas seulement les couches | `sc-css` | manque | non |
| B1 | Compte de sujets sur toute vérification | `design` | manque | non |
| B2 | Aucune paire hors déclaration | `design` | manque | non |
| C1 | Univers reçu, jamais déduit | `sc-php` | manque | **oui** |
| C2 | Configuration par vue, pas par union | `design` | manque | non |
| C3 | Refus d'un artefact hors grammaire | `design` | manque | non |
| D1 | Propriétaire et échéance au schéma | `design` | manque | non |
| E1 | Normalisation sur tous les domaines | `design` | manque | non |
| F1 | Le pivot renvoie, ne réénonce pas | `sc-css` `sc-js` `sc-php` | manque | non |
| F2 | Aucun renvoi à un réalisateur indéfini | `design` | manque | non |
| G1 | Un figeage périme l'enforcement antérieur | `design` | manque | non |

Aucun item n'entraîne de modification de skill, de bump ni de commit à ce stade.

## Ordre d'attaque

<!-- TODO(human) : classer les quinze énoncés en vagues d'intégration.
     Contraintes connues : A4 et C1 attendent la refonte design ↔ pivots ;
     A1/A2/A3 sont des déclarations sans code et peuvent partir seules ;
     B1 et B2 touchent le même exécutable de figeage.
     Le reste est un arbitrage de valeur, pas une dérivation. -->

## Ce que ce plan ne fait pas

- Il n'arbitre pas ce qui revient à `design` et ce qui revient à un pivot pour A4 et C1 — la refonte en cours tranche.
- Il ne corrige rien dans le projet qui a fourni le matériau. Tout défaut d'exécution imputable à ce projet a été écarté sans traitement.
- Il ne mesure aucune fréquence. Les skills ayant évolué pendant l'exécution du terrain, deux retours ne sont jamais comparables à instrument constant.
