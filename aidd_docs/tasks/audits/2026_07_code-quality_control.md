---
name: audit
description: Audit code-quality de la skill overcode:control — cohérence normative et efficacité
argument-hint: N/A
---

# Codebase Audit: plugins/overcode/skills/control

La cohérence interne du modèle d'autorité est quasi parfaite ; c'est elle qui verrouille un biais structurel pro-`contract` que rien dans la skill n'a le droit de corriger, et qui rend la skill inopérante sur un projet dont la valeur se prouve en `e2e`.

- **Date**: 2026-07-28
- **Scope**: `plugins/overcode/skills/control/**` (SKILL.md, 6 actions, 4 références, 7 suites d'evals)
- **Health**: poor
- **Findings**: 3 critical, 4 warning, 2 minor

Health: `good` = no critical findings; `fair` = critical findings exist but are isolated and addressable; `poor` = systemic or widespread critical findings.

Justification du `poor` : le biais tier n'est pas localisé dans un fichier. Il est réparti sur la tier table (`decision-framework`), la borne du pivot (`pivot-contract`), le signalement (`05-stats`) et la contrainte de nombre (`test-density`), et chacune de ces pièces est individuellement défendable. C'est la définition d'un défaut systémique.

## Findings

One row per issue. Every row MUST cite a concrete `file:line`. Sort by severity (critical first). Read-only: an audit reports, it never edits code.

Severity (shared rubric across every audit pillar, so a full audit ranks consistently):
- 🔴 critical - exploitable security hole, data loss, or broken correctness. Fix now.
- 🟡 warning - real debt or risk that will bite later. Fix soon.
- 🟢 minor - nit or cleanup. Fix when convenient.

Effort: `S` (under 1h), `M` (under 1d), `L` (over 1d).
Category (the audit pillar, one of): `code-quality`, `architecture`, `security`, `dependencies`, `performance`, `tests`, `ui`.

| Sev | Category | Location | Issue | Suggested fix | Effort |
| --- | --- | --- | --- | --- | ------ |
| 🔴 | code-quality | `references/decision-framework.md:16` | Le biais pro-`contract` est **unidirectionnel et non corrigeable**. Le tie-break par défaut tombe sur `contract` au motif du coût (« favors under-provisioning e2e »), `pivot-contract.md:24` n'autorise un raffinement de tier que vers le local/émulé (donc e2e→contract, jamais l'inverse), et `05-stats.md:114` ne lève de flag de déséquilibre que dans un sens (« inverted pyramid »). Une suite 100 % `contract` sur un produit dont la valeur est un parcours ne déclenche rien. Comme `SKILL.md:77` interdit à tout modulateur de classer, aucune pièce de la skill n'a le droit de redresser ce biais. | Rendre le tie-break dépendant de **ce que le comportement prouve**, pas du coût du tier ; ouvrir la borne du pivot dans les deux sens (un pivot peut aussi remonter vers `e2e` quand le seam in-process n'a pas de pouvoir de détection) ; symétriser le flag de `05-stats` (« pyramide plate : le produit se prouve en parcours, la suite ne les couvre pas »). | L |
| 🔴 | code-quality | `references/test-density.md:6` | La contrainte de nombre par défaut **ne sait mesurer que le tier `contract`**. La densité s'appuie sur les *branch points* du rapport de couverture, or les tests e2e n'y contribuent presque rien au dénominateur et traversent des centaines de branches au numérateur. Le fichier ne dit nulle part si « test cases exercising f » inclut les cas e2e : les deux lectures possibles sont fausses (inclus → le signal est écrasé, exclus → la contrainte mesure une suite dont elle ignore la moitié). Les cas dégénérés (`:52-59`) couvrent l'absence de rapport, jamais l'inadéquation du tier. | Déclarer explicitement le tier sur lequel la densité est définie, et poser une contrainte de nombre distincte pour `e2e` (par frontière ou par parcours, pas par branche). Une contrainte muette sur la moitié de la suite est pire qu'absente : elle se présente comme « la » contrainte en vigueur (`SKILL.md:88`). | L |
| 🔴 | code-quality | `actions/01-write.md:31` | **Zone morte : le non-déterminisme n'a aucun tier.** Les trois tiers sont définis par la topologie de la frontière (I/O, browser, réseau), jamais par la nature de l'assertion. Un comportement agentique (appel LLM en production) traverse une vraie frontière externe → `e2e` par `decision-framework.md:14`, mais l'étape 3-bis le déclare **hors de portée des tests** et le renvoie au monitoring, « quel que soit le tier que la table lui assigne ». Sur un projet agentique, le cœur du produit est donc systématiquement classé non testable — alors que c'est exactement ce qu'un eval e2e prouve. Le cap « une frontière = un test » (`:33`) aggrave : un produit agentique a une frontière et toute sa valeur derrière. | Distinguer *frontière dont la disponibilité est hors contrôle* (→ monitoring, la règle actuelle) de *frontière dont la sortie est non déterministe mais dont le comportement est assertable statistiquement* (→ e2e/eval, avec sa propre borne de nombre). `SKILL.md:3` renvoie à `behave`, mais `behave` teste des skills prompt-driven, pas une application qui appelle un LLM : la passerelle n'existe dans aucun des deux sens. | L |
| 🟡 | code-quality | `references/phase-framework.md:153` | Le tier de la frontière externe est **fixé hors de la tier table** : « Provable in process, at `contract` tier » — répété à `actions/04-strengthen.md:58`. Or `SKILL.md:77` pose que « a line of this skill that appears to give classifying power to anything other than the tier table is a **defect, not an exception** ». La règle s'auto-qualifie. | Reformuler en critère de *ce qui est prouvable* sans nommer le tier, et laisser la table classer. | S |
| 🟡 | code-quality | `evals/authority-scenarios.md:39` | **Contradiction normative avec une eval en PASS.** S6 attend qu'une vraie frontière externe atterrisse en `e2e` (refus du raffinement du pivot), et le résultat est journalisé PASS à `:78`. `phase-framework.md:153` et `01-write.md:33` disent l'inverse : ce qui reste testable sur cette frontière l'est au tier `contract`, le reste part au monitoring. Deux normes coexistent, l'eval valide la seconde en citant la première. | Trancher, puis répercuter dans les trois emplacements. C'est le symptôme direct de la duplication normative (voir la ligne 🟢 ci-dessous). | M |
| 🟡 | code-quality | `actions/05-stats.md:114` | Le flag « inverted pyramid » route vers `02-audit`, **dont aucune heuristique ne peut qualifier un test e2e** : `actions/02-audit.md:29` définit *trivial* par « test body under 5 lines » et *getter/setter* par une assertion de propriété — trois critères écrits pour de l'unitaire. Le lot revient vide par construction. Ce raisonnement exact est écrit noir sur blanc à `actions/06-align.md:106` (« The heuristics of `02-audit` alone would produce an empty batch by construction ») et n'a jamais été appliqué ici. | Soit doter `02-audit` d'une heuristique de valeur propre au tier e2e (parcours redondant, assertion sur un état intermédiaire déjà couvert), soit retirer le routage et signaler sans router. | M |
| 🟡 | code-quality | `references/phase-framework.md:186` | **La phase sait ce qu'il faut prouver et n'a aucun moyen de le faire écrire.** En `production`, la phase déclare que la suite doit prouver « the client-facing acts — sign-in, registration, payment, booking » (`:45`) et attend l'ordre `domains → foundations`. Mais elle priorise sans classer : chaque gap remonté redescend dans `01-write`, où le decision order le rabat sur `contract` dès qu'un seam in-process existe. Le modèle d'autorité est formellement cohérent et son résultat contredit l'intention affichée de la moitié des phases. | Ne pas casser la borne d'autorité — la faire porter par la tier table : un critère de tier lisant l'axe (`foundations` vs `critical journeys`) classerait sans qu'aucun modulateur ne classe. | M |
| 🟢 | code-quality | `SKILL.md:80` | **Duplication normative sur 4 niveaux.** Les bornes d'autorité (« priorise, ne classe jamais ») sont réécrites en toutes lettres dans `SKILL.md:77-80`, `phase-framework.md:5`, `test-density.md:65` et `pivot-contract.md:25` ; le bloc *frontière externe* est triplé (`01-write.md:31-33`, `04-strengthen.md:56-60`, `phase-framework.md:145-164`), duplication assumée à `01-write.md:31`. Coût : toute évolution doit être répercutée en 3 ou 4 endroits — et la contradiction 🟡 ci-dessus est exactement une répercussion ratée. | Garder une seule formulation normative par règle, les autres emplacements y renvoyant. La règle est déjà présente à `SKILL.md:77` sous forme de règle de lecture : elle suffit. | M |
| 🟢 | code-quality | `actions/05-stats.md:60-63` | Le bloc `VOLUME` ne compte que `contract` et `e2e` et le split se fait « by the pivot's respective globs, else by the project's own directory convention » — donc par emplacement de fichier, jamais par ce que le test prouve. Sur une suite où les deux vivent au même endroit, ou sur un projet dont les evals ne portent pas de glob distinct, le split est silencieusement faux. L'approximation du *matching* densité est déclarée (`test-density.md:61`), celle du split de tier ne l'est pas. | Déclarer l'approximation du split au même titre que celle du matching, ou renoncer au split quand aucun glob ne le porte. | S |

## Top actions (ranked by impact)

Highest impact first. Each action names the finding rows it resolves and, when a fix is wanted, the act-skill to hand off to (refactor, test, impeccable - the audit itself never edits code).

1. **Reconnaître un quatrième tier, ou une deuxième dimension au tier.** Résout les lignes 🔴 `01-write.md:31` et 🟡 `phase-framework.md:186`. Les trois tiers actuels classent par *topologie de frontière* ; il manque l'axe *pouvoir de détection de l'assertion*. C'est ce qui manque pour qu'un comportement agentique, un parcours client et une transformation pure ne se disputent pas la même case. À traiter en amont de tout le reste : les lignes 2 et 3 en dépendent.
2. **Symétriser le biais tier.** Résout la ligne 🔴 `decision-framework.md:16`. Trois points d'entrée : le tie-break de l'étape 4, la borne unidirectionnelle du pivot (`pivot-contract.md:24`), le flag unidirectionnel de `05-stats.md:114`. Le raisonnement de coût qui justifie aujourd'hui le tie-break est valable sur une app CRUD et faux sur un projet agentique, où l'e2e est le seul tier qui prouve quelque chose : il doit devenir un paramètre du projet, pas une constante de la skill.
3. **Définir la contrainte de nombre du tier `e2e`.** Résout la ligne 🔴 `test-density.md:6`. La densité par branch point restera juste pour `contract` ; il faut son pendant e2e (par frontière, par parcours critique) et une déclaration explicite du périmètre de chacune — sans quoi `SKILL.md:88` continue de présenter comme « la » contrainte en vigueur une mesure aveugle à la moitié de la suite.
4. **Purger la duplication normative avant de corriger quoi que ce soit d'autre.** Résout la ligne 🟢 `SKILL.md:80` et prévient la récidive de la ligne 🟡 `authority-scenarios.md:39`. Corriger le biais tier sur une base triplée produira une nouvelle contradiction ; l'historique en fournit déjà un cas.
5. **Réparer le routage du flag de déséquilibre.** Résout la ligne 🟡 `05-stats.md:114`. Correctif local, indépendant des quatre premiers.

Aucune de ces actions n'est un correctif de code : la cible est un corpus normatif. Passer la main à `overcode:reconcile-normative` pour les lignes 4 et 🟡 `authority-scenarios.md:39`, à une réécriture manuelle arbitrée pour les lignes 1 à 3.

## Coverage

Proves each pillar was examined. A pillar with no findings is still scanned and listed here. A pillar that could not be examined (missing tool or runtime) is listed under Skipped with the reason - never silently dropped.

- **Scanned**: code-quality
- **Skipped**: architecture, security, dependencies, performance, tests, ui — audit mono-pilier explicitement demandé (cohérence et efficacité d'une skill markdown). Les six autres piliers n'ont pas de prise sur un corpus normatif sans runtime : pas de surface d'exécution, pas de dépendances, pas de chemin chaud, pas d'UI. Le pilier `tests` est le seul discutable — les 7 suites d'evals ont été lues, mais en tant que source de vérité normative (elles ont produit la ligne 🟡 `authority-scenarios.md:39`), pas en tant qu'objet d'un audit de couverture.
