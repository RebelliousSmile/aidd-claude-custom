---
name: master_plan
description: Refonte de overcode:control — la phase devient l'autorite classante par une matrice phase x niveau de domaine ; trois parts sequencees par DEC-006
---

# Master Plan: Refonte de `overcode:control` — la phase arbitre, les domaines portent

## Overview

- **Goal**: la phase cesse de ponderer un ordre et devient le **regulateur d'exigence** — une matrice `phase x niveau de domaine` fixe, par cellule, la preuve exigee et un plafond numerique ; le tier redevient un **nom de sortie** ; les domaines sont produits et figes par `06-align` ; le contrat pivot est reecrit en questionnaire et son champ mal nomme devient `Anchor boundary`.
- **Risk Score**: 8/10 — changement cassant d'une interface publique (+3, le contrat pivot est declare interface publique par DEC-004 §5), 5+ modules touches (+3), refactoring majeur (+2).
- **Branch**: `refactor/control-phase-domaines`
- **Demande source**: `aidd_docs/tasks/2026_07/2026_07_28-control-refonte-phase-domaines.md` (statut **arbitre — planifiable**). Le plan ne re-arbitre rien : il ordonne, il chiffre, il expose ce que la demande laisse ouvert.
- **Perimetre**: `plugins/overcode/docs/control.md` · `plugins/overcode/skills/control/**` · `plugins/sc-js/skills/sniff/references/capabilities/tools/testing.md` · `aidd_docs/internal/decisions/` · manifestes et changelogs. **En source (`plugins/<name>/`), jamais dans le cache.**
- **Hors perimetre**: tout le §7 de la demande — ecriture des cinq pivots `testing` manquants, verification de `sc-css/skills/sniff/actions/02-install-pivots.md`, mecanisme de distribution des pivots. Aucune decision du plan n'en depend.
- **Ne rien committer ni pousser.** Les bumps de version sont **prepares** par chaque part et poses avec le contenu au moment ou l'utilisateur demande le commit.

## Child Plans

| #   | Plan                                   | File                                                       | Status  | Validated |
| --- | -------------------------------------- | ---------------------------------------------------------- | ------- | --------- |
| 1   | La page fait foi, et l'ADR d'amendement | `./2026_07_28-control-refonte-phase-domaines-part-1.md`     | done    | [ ]       |
| 2   | Les suites `behave`, ecrites rouges     | `./2026_07_28-control-refonte-phase-domaines-part-2.md`     | done    | [ ]       |
| 3   | La skill rattrape la page               | `./2026_07_28-control-refonte-phase-domaines-part-3.md`     | in-progress | [ ]   |

<!-- Status values: pending, in-progress, done, blocked -->
<!-- RULE: Plan N+1 blocked until Plan N checkbox checked -->

**Part 3 reste `in-progress` au 2026-07-29, et une seule chose l'y tient** : sa phase 5 s'intitule « jusqu'au vert », et le run qui prouverait le vert n'a pas ete rejoue apres la passe de correction. Les six phases sont implementees, les huit suites portent un run date, les 22 lignes rouges ont leur cause racine tranchee et corrigee — mais l'etat mesure est anterieur aux correctifs. Le passage a `done` est conditionne au run de confirmation, plus a `overcode:behave 03-regress` contre la baseline. La colonne `Validated` reste vide pour les trois parts : aucune n'a ete validee par l'utilisateur.

## Ordre impose par DEC-006 — et pourquoi il n'est pas cosmetique

`docs/control.md` fait foi sur `skills/control/`. L'ordre **page -> suites rouges -> skill** est declare non cosmetique dans l'ADR :

> « `behave` teste des sorties, jamais la coherence entre deux documents normatifs. Une incoherence page/reference introduite par le mauvais bout n'aurait ete detectee par rien. »

Partage de charge, applique tel quel dans les trois parts :

| Artefact | Ce qu'il porte |
|---|---|
| `docs/control.md` | la regle **et son motif** |
| `skills/control/` | la regle **et sa procedure** |
| ADR (`aidd_docs/internal/decisions/`) | le **rationnel** |

Aucune etape de `## Process` ne remonte sur la page. **Critere de fin de chantier** : toutes les suites `behave` au vert, et aucune regle de `docs/control.md` sans contrepartie procedurale dans `skills/control/`. Les scenarios que la refonte rend caducs sont **reecrits, jamais supprimes en silence**.

## Etat de depart mesure

| Fichier | Lignes | Sort |
|---|---|---|
| `plugins/overcode/docs/control.md` | 386 | reecrit en part-1 |
| `skills/control/SKILL.md` | 101 | `:77`, `:79`, `:80` reecrits en part-3 |
| `actions/01-write.md` | 45 | plafond, ancrage, pivot *Risk signals* |
| `actions/02-audit.md` | 40 | pivot *Risk signals* |
| `actions/03-configure.md` | 37 | pivot *Coverage command* (+ *Canonical E2E tool*, cf. arbitrage) |
| `actions/04-strengthen.md` | 80 | les six criteres deviennent un classement intra-domaine (`:51`) |
| `actions/05-stats.md` | 131 | `:106` et `:114` supprimes, bloc `VOLUME` -> `DOMAINES` |
| `actions/06-align.md` | 137 | devient le producteur des domaines, `:81` reecrit |
| `references/decision-framework.md` | 20 | perd son autorite (cf. arbitrage a trancher) |
| `references/phase-framework.md` | 232 | `:5`, `:199-203`, `:200`, `:207` reecrits |
| `references/pivot-contract.md` | 52 | reecrit en questionnaire, `:24` supprime |
| `references/test-density.md` | 71 | `:13` recadre (il vise un cap projet, pas un plafond par domaine) |
| `references/decision-matrix.md` | — | **nouveau** |
| `references/domain-catalogue.md` | — | **nouveau** |
| `evals/*-scenarios.md` | 7 fichiers, 883 lignes | reecrits en part-2, +1 suite |
| `plugins/sc-js/.../tools/testing.md` | 121 | `## Tier thresholds` (`:86-104`) -> `## Anchor boundary` |

Baseline `behave` relevee avant le chantier — c'est elle qui sert de temoin de non-regression :

| Suite | Dernier run | Verdict |
|---|---|---|
| `authority-scenarios.md` | 2 runs, 2026-07-28 | 12/12 PASS |
| `domains-scenarios.md` | run 4, 2026-07-28 | 8/9 PASS, S3 **N/A permanent** (limite de fixture), 5 frictions consignees |
| les cinq autres | 2026-07-27/28 | verts au terme du chantier DDD |

## Ce qui est arbitre, et ce qui reste a trancher

**Arbitre par la demande — le plan ne le rouvre pas** : la phase reste (sa suppression « ne doit jamais etre reproposee ») ; la forme de la matrice (4 phases x 4 colonnes, cellule = preuve exigee + plafond) ; le plafond refuse un ajout et n'exige jamais un retrait ; `contract`/`e2e`/`skip` survivent comme noms de sortie ; `align` ecrit `testing-domains.md` et jamais `testing.md` ; `stats` ne conclut jamais.

**Non bloquant, a poser pendant le chantier** (§6 de la demande) :

| Point | Ou il se pose | Position du plan |
|---|---|---|
| Calibrage des valeurs de la matrice | part-1 (la page les publie) puis part-3 (`decision-matrix.md`) | partir des valeurs de §3.2 et les **eprouver sur les deux fixtures** avant de les figer ; toute valeur changee est justifiee dans l'ADR, pas seulement dans le fichier |
| Contenu initial du catalogue de domaines | part-3 | une douzaine d'entrees transverses **plancher de detection** ; chaque entree = nom + niveau par defaut + termes litteraux ; aucune regex |
| Sort de *Canonical E2E tool* | part-3 | **le brancher** dans `03-configure` : l'action configure le runner, le champ est deja rempli chez `sc-js`, et supprimer un champ vrai pour cause de non-lecteur est le mauvais remede |

**Deux jugements que le plan pose et qui demandent l'accord de l'utilisateur au gate correspondant** :

1. **`references/decision-framework.md` est supprime, son contenu absorbe par `decision-matrix.md`.** La demande dit qu'il disparait « comme autorite ». Le conserver retrograde laisserait dans l'arbre une seconde table lisible comme classante — exactement le defaut que la refonte supprime. Ce qu'il faut sauver n'est pas la table mais la **definition des noms de sortie** (`contract`, `e2e`, `skip`), qui va dans `decision-matrix.md` a cote de la distinction preuve ancree / preuve interne. Gate : part-3, phase 1.
2. **Un domaine qui arrive en argument prend son niveau du catalogue ; absent du catalogue, l'action demande le niveau et ne devine pas.** La demande dit que `06-align` attribue le niveau en meme temps que le nom, et la regle etablie en 3.11.0 dit qu'un domaine est en vigueur des qu'il arrive en argument — l'intersection des deux n'est ecrite nulle part, et c'est elle qui rend la matrice testable sur les fixtures (voir ci-dessous). Gate : part-1, phase 3. Le jugement porte trois clauses indissociables, chacune fermant un trou que les deux premieres ouvrent :
   - **l'argument vaut confirmation.** « Un domaine n'existe que confirme » et « un domaine en argument est en vigueur » se contredisent si on ne dit pas sur quoi porte la confirmation : elle porte sur ce que le **scan propose**, pas sur ce que l'utilisateur a **ecrit lui-meme**. Redemander confirmerait deux fois la meme chose ;
   - **le niveau repondu n'est pas persiste.** Il vaut pour l'invocation, l'action l'annonce comme tel et propose `06-align` pour le figer. Sans cette clause, deux invocations peuvent recevoir deux reponses et poser deux plafonds sur le meme domaine — l'idempotence par jugement materialise tombe la ou elle est censee tenir ;
   - **`align` reste seul ecrivain de `testing-domains.md`.** La sortie de facilite serait de laisser l'action ecrire la reponse ; elle ferait deux ecrivains sur le fichier, la faute meme que la refonte corrige en interdisant `testing.md`.

## Les fixtures — et le trou qu'elles laissent

| | `app` | `ai-hub` |
|---|---|---|
| Chemin | `C:\Users\fxgui\Documents\Perso\Projects\suddenly\_code\app` | `C:\Users\fxgui\Documents\Perso\Projects\suddenly\_code\ai-hub` |
| Document | `aidd_docs/memory/TESTING.md` (86 l.), chemin non conventionnel, **rempli mais non decisionnel**, declare un seuil de 80 % de couverture | `aidd_docs/memory/testing.md` (15 l.), **activement contredit par le depot** |
| Fichiers de test | 80 | 60 |
| Rapport de couverture | `.coverage` present | aucun |
| Phase declaree | aucune | aucune |
| Domaine declare | aucun | aucun |
| Matiere a domaines | reelle : `suddenly/fediverse_auth`, `suddenly/users`, `suddenly/messaging`, `suddenly/offers`, `suddenly/activitypub` | pauvre : depot d'outillage |

**Le trou** : la matrice s'indexe sur un **niveau de domaine**, et aucune des deux fixtures ne declare le moindre domaine. En lecture naive, toutes les cellules sauf la colonne hors-domaine seraient N/A — c'est-a-dire que le mecanisme central de la refonte serait non teste.

**L'echappatoire, et elle est reelle, pas un stub** : un domaine est en vigueur des qu'il arrive **en argument** (regle etablie en 3.11.0, `CHANGELOG` overcode). Un run `01-write ... domain=auth phase=production` sur `app` exerce donc la cellule `production x critique` sans rien ecrire dans la fixture, a condition que le niveau soit resolvable — d'ou le jugement 2 ci-dessus. `app` porte la matiere pour `auth` (critique), `payment`/`offers` (critique ou structurant selon le catalogue) et `messaging` (structurant) ; `ai-hub` reste la fixture du **regime hors-domaine** et du cas « aucun rapport de couverture ».

**L'axe phase s'exerce de la meme facon** : la phase est **posee en question** avant tout classement, donc un scenario en fixe la reponse dans ses preconditions. Ce qu'aucune fixture ne porte, c'est une phase *lue dans le projet* — pas la phase elle-meme. Les deux axes etant ainsi accessibles, la part 2 se donne un **plancher de couverture : 8 cellules sur 16, dont les quatre coins**, et nomme les cellules laissees dehors avec leur cause. Sans plancher ecrit, « chaque regle nouvelle a un scenario » se satisfait d'une seule cellule.

Ce qu'aucune fixture ne peut exercer, et qui sera marque N/A avec sa cause, jamais contourne par une fixture inventee :

- une **bascule de phase reelle** declaree par le projet (les deux sont sans phase) ;
- une **resolution de domaine depuis un `testing-domains.md` existant** — le fichier n'existe nulle part avant que `06-align` ne tourne ; seule sa **proposition** est observable en dry-run. La **capacite de lecture** des quatre actions consommatrices, elle, est observable : ce qui n'est pas exercable, c'est la lecture d'un fichier reel, pas l'existence du chemin de lecture ;
- la **derive** de residu entre deux passes d'`align` separees dans le temps.

## Versions et commits

Regle marketplace : bump et contenu **dans le meme commit**, aucune installation contre un arbre sale. Trois commits, trois bumps.

| Part | Contenu | overcode | sc-js | marketplace |
|---|---|---|---|---|
| 1 | page + DEC-007 | `3.11.1` -> **`3.12.0`** | — | `3.5.0` -> **`3.5.1`** |
| 2 | suites reecrites, rouges | -> **`3.12.1`** | — | -> **`3.5.2`** |
| 3 | skill + contrat pivot + `sc-js` | -> **`4.0.0`** | `0.13.2` -> **`0.14.0`** | -> **`3.6.0`** |

- **`4.0.0` et pas `3.13.0`** : le contrat pivot est une **interface publique** (DEC-004 §5) et `Tier thresholds` -> `Anchor boundary` la casse. Un pivot tiers non mis a jour perd un champ. C'est la definition d'un majeur.
- `sc-js` en **mineur** (`0.x`) : le contenu est conserve, seul le titre de section change ; sur `0.x` un renommage de section n'est pas un majeur, mais l'entree de son `CHANGELOG` doit nommer le champ dans les deux titres pour qu'une recherche retrouve l'un par l'autre.
- Les parts 1 et 2 publient volontairement un etat ou **la page devance la skill**. C'est l'ordre DEC-006, pas un accident : l'entree de `CHANGELOG` de chacune le dit explicitement, sans quoi un lecteur y verra la contradiction que le chantier existe pour supprimer.
- `index.json` ne porte que `{id, name}` depuis la 3.4.0 — n'y remettre ni `version` ni `description` (garde `M3` de `tools/eval/consistency.mjs`).

## Validation Protocol

1. Executer la part 1. Verifier son `success_condition`, puis relire la page en entier d'une traite : une page reecrite par morceaux se contredit d'un bout a l'autre.
2. [ ] **Checkpoint 1** — l'utilisateur confirme : les valeurs de la matrice publiees sur la page, la formulation du plafond (il classe, et ce n'est pas une violation de la regle de mesure), DEC-007 tel qu'ecrit, et le jugement 2 (niveau d'un domaine passe en argument).
3. Debloquer la part 2. Ecrire les suites contre **la page**, jamais contre la skill. Lancer le run initial.
4. [ ] **Checkpoint 2** — l'utilisateur tranche **chaque FAIL** en « vrai defaut de la skill » ou « test a reecrire », et **chaque scenario declare caduc** en « reecrit » ou « retire, avec sa raison ». La part 3 ne demarre pas avant.
5. Debloquer la part 3. Aligner la skill, reecrire le contrat, corriger `sc-js`, poser les deux nouvelles references.
6. [ ] **Checkpoint 3** — les huit suites rejouees sur les deux fixtures : verdict au vert ou friction consignee et acceptee. `pnpm test` sort 0.
7. [ ] **Final** — passe de coherence documentaire page <-> skill : chaque regle de la page a une contrepartie procedurale, chaque enonce de la skill remonte a une regle de la page. Cette passe n'est pas jouable par `behave` (voir ci-dessous) ; elle est faite a la main et tracee dans le `CHANGELOG`.

## Ce que `behave` ne peut pas juger

Le tri est le meme qu'au chantier precedent, et il est decide avant d'ecrire :

| Nature de la regle | Exemple dans cette refonte | Verifiee par |
|---|---|---|
| **Observable** — un refus, un routage, un contenu de rapport, un ensemble d'ecritures prevues | `01-write` sur un domaine au plafond rend `skip` avec le motif « plafond atteint (n/n) — `<phase> x <niveau>` » | `behave` |
| **Meta / redactionnelle** — une enonciation, un decompte, une borne qui doit figurer la ou le champ est defini | « le pivot declare ce qu'il fournit, jamais qui le consomme » ; l'absence de tout consommateur nomme dans `pivot-contract.md` | passe de coherence documentaire, tracee dans le `CHANGELOG` |

Une regle meta mal placee peut malgre tout produire un defaut observable — c'est le cas de la borne d'ancrage : si `Anchor boundary` est defini sans dire ou passe la frontiere, un juge dont le chemin de chargement se limite au contrat classera de travers, et cela se voit.

## Estimations

- **Confidence**: 9/10
- **Duration**: 3 sessions, une par part, la part 3 etant la plus longue (13 fichiers touches + deux nouveaux + un pivot externe).

**Pourquoi 9 et pas 10** :

- ✓ la demande est arbitree, autoportante, et chaque ancre de ligne qu'elle cite a ete verifiee contre le fichier reel ;
- ✓ l'ordre de travail est impose par un ADR accepte, pas choisi par le plan ;
- ✓ la baseline `behave` est connue suite par suite, donc la non-regression est mesurable et non declarative ;
- ✓ le trou de fixture sur la matrice a une echappatoire **reelle** (domaine en argument), etablie par une regle deja publiee ;
- ✗ le calibrage des valeurs de la matrice est un jugement, pas un calcul : deux fixtures ne suffisent pas a le prouver, elles suffisent seulement a le rendre non absurde ;
- ✗ la part 2 produira un rouge massif — la skill entiere est en retard sur la page — et distinguer « vrai defaut » de « test mal ecrit » sur ce volume est le vrai risque du chantier, d'ou le checkpoint 2 item par item.
