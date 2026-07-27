---
name: master_plan
description: Master - aligner skills/control/ sur docs/control.md en DDD (la page fait autorite)
---

# Master Plan: `control` — alignement DDD sur `docs/control.md`

## Overview

- **Goal**: la page `plugins/overcode/docs/control.md` porte le modele complet et fait foi ; `skills/control/` le realise sans divergence, et chaque **regle** de la page est verifiee par une suite `overcode:behave` executee sur deux fixtures reelles.
- **Risk Score**: 8/10 (contrat public de skill modifie +3 ; 5+ fichiers normatifs touches +3 ; refactor normatif majeur +2)
- **Branch**: `docs/control-ddd-alignment`
- **Perimetre**: **chaque regle, jamais chaque etape.** Un invariant, une borne d'autorite, une precedence, une exclusivite, une arete de chainage, une ligne de tableau de parametres, un regime de confirmation = une unite de travail. Les etapes de `## Process` ne sont jamais l'objet du test ni de l'alignement.

## Child Plans

| #   | Plan                              | File            | Status  | Validated |
| --- | --------------------------------- | --------------- | ------- | --------- |
| 1   | Completer et arbitrer la page     | `./2026_07_27-control-ddd-alignment-part-1.md` | pending | [ ]       |
| 2   | Ecrire les suites `behave` rouges | `./2026_07_27-control-ddd-alignment-part-2.md` | blocked | [ ]       |
| 3   | Aligner la skill, passer au vert  | `./2026_07_27-control-ddd-alignment-part-3.md` | blocked | [ ]       |

<!-- RULE: Plan N+1 blocked until Plan N checkbox checked -->

## Ordre impose par le DDD

L'ordre n'est pas negociable et c'est ce qui distingue ce chantier d'une revue de coherence :

1. **La page d'abord.** Tant qu'une regle n'est pas ecrite sur la page, elle n'existe pas — meme si la skill l'applique deja. 43 regles vivent aujourd'hui uniquement dans la skill (categorie C de l'inventaire) : elles remontent sur la page ou elles disparaissent.
2. **Les tests ensuite, et ils doivent echouer.** Une suite ecrite apres l'alignement ne prouve rien. La phase 2 se termine sur un run `initial` rouge, consigne — c'est la preuve que la suite attrape le defaut.
3. **La skill en dernier.** Elle n'est modifiee que pour faire passer au vert une suite deja rouge. Toute modification de skill sans FAIL prealable est hors plan.

## Etat de depart mesure

Inventaire de divergence realise sur la page + `SKILL.md` + 6 actions + 4 references :

| Categorie | Volume | Traite en |
|---|---|---|
| **A** — regle sur la page, correctement realisee | 41 | rien a faire, sert de base de non-regression |
| **B** — sur la page, absente ou plus faible dans la skill | 6 | part-3 |
| **C** — dans la skill, absente de la page | 43 | part-1 |
| **D** — contradiction page / skill | 6 | part-1 (arbitrage) puis part-3 (application) |

Le volume de C sur A+C (43 sur 84) est le fait marquant : **la page ne porte aujourd'hui que la moitie du modele**. C'est cette moitie manquante que la phase 1 doit ecrire, sans quoi les phases 2 et 3 testeraient et aligneraient un modele incomplet.

## Les six arbitrages (gate de la part-1)

Aucune ligne de code ni de suite n'est ecrite avant que les six soient tranches par l'utilisateur. « La page fait foi » ne suffit pas : dans trois cas sur six, c'est la page qui a tort et c'est elle qu'il faut corriger.

| # | Sujet | Page | Skill | Recommandation |
|---|---|---|---|---|
| D1 | lot nomme par l'utilisateur dans `02-audit` | une seule exception au un-par-un, et c'est `06-align` | `02-audit` admet « ou via une selection groupee qu'il nomme » | **page gagne** — retirer le lot de `02-audit` |
| D2 | bascule depuis `undetermined` | s'applique des qu'une phase est declaree | `06-align` exclut `default` **et** `undetermined` de toute bascule | **page gagne** — seul `default` est exclu |
| D3 | lot nomme du cote des ajouts (`04-strengthen`) | confirmation par item | `04-strengthen` admet un lot nomme | **page gagne** — le lot se justifiait par le cout nul d'un test regenere, argument valide pour supprimer, pas pour creer |
| D4 | univers du `scope` de `05-stats` | binaire : suite de tests OU code source | troisieme univers : code source + tests qui lui correspondent | **skill gagne** — corriger la page : un instantane qui compte des tests doit borner des tests |
| D5 | la phase decide-t-elle « ce qui est analyse » | oui (tableau des autorites) | non — l'univers vient du glob source, reduit par `scope` | **skill gagne** — retirer « ce qui est analyse » de la ligne Phase |
| D6 | lecture du rapport de couverture | pilotee par la phase | l'absence d'un fichier se lit identiquement dans toutes les phases | **skill gagne** — la page porte la reserve : la phase pondere la lecture, elle ne change pas ce qu'une absence signifie |

D4, D5 et D6 sont des **corrections de la page**, pas des concessions a la skill : dans les trois cas la skill tient une borne que la page a formulee trop large. Les inscrire comme telles est la seule facon de conserver « la page fait foi » sans la rendre fausse.

## Les fixtures

Deux projets reels, jamais mutes (regime dry-run de `behave`) :

| Fixture | Chemin | Ce qu'elle donne |
|---|---|---|
| `app` | `C:\Users\fxgui\Documents\Perso\Projects\suddenly\_code\app` | document de test **rempli mais non decisionnel** (85 lignes, types de tests, aucun critere de tier), a un chemin non conventionnel (`aidd_docs/memory/TESTING.md`, majuscules) ; suite `pytest` avec marqueur `e2e`, Playwright etabli ; aucune phase, aucun domaine declares |
| `ai-hub` | `C:\Users\fxgui\Documents\Perso\Projects\suddenly\_code\ai-hub` | document de test **template generique intact** (14 lignes) au chemin conventionnel ; `tests/` + `tests/e2e/` ; aucune phase, aucun domaine declares |

Le couple est discriminant : les deux tombent dans la regle « document en forme de template → traite comme absent pour la decision de tier », mais a deux niveaux de remplissage differents, et la skill doit dire **lequel des deux cas** elle a rencontre. Le chemin en majuscules de `app` exerce en prime la resolution du document.

**Limite connue et assumee** : aucune des deux fixtures n'a « pas de document du tout ». Les regles qui en dependent (drapeau de strategie manquante de `05-stats`, refus de creation de `06-align`) seront marquees **N/A** et non PASS — `behave` interdit d'inventer une fixture stub pour les couvrir.

## Validation Protocol

1. Part-1 : page completee, 6 arbitrages tranches, ADR consigne.
2. [ ] Checkpoint 1 : l'utilisateur confirme que la page dit tout le modele et rien de faux.
3. Part-2 : 7 suites ecrites (une par famille de regles, jamais une par action), run `initial` execute sur les deux fixtures, **au moins un FAIL consigne**.
4. [ ] Checkpoint 2 : l'utilisateur confirme que chaque FAIL est un vrai defaut de la skill et non un test mal ecrit.
5. Part-3 : skill alignee, run `post-fix` vert, blocs `## Test` transformes en renvois, bump 3.10.0.
6. [ ] Final : `overcode:behave 03-regress` sur les 7 suites, aucun PASS→FAIL.

## Ce que `behave` ne peut pas juger

Toutes les regles ne sont pas observables sur un comportement. Quatre des six regles de categorie B (B1, B2, B4, B6) sont des **enonciations** — nommer un ensemble ferme, ne pas melanger deux decomptes, completer une enumeration, borner une autorite dans les deux sens. Elles se verifient a la lecture, une fois, en part-3, et se consignent au CHANGELOG. Les y forcer en scenarios produirait des verdicts arbitraires. Le tri est ecrit dans la part-2 et n'est pas negociable en cours de route.

## Estimations

- **Confidence**: 9/10
- **Duration**: 3 sessions (une par part)

### Evaluation de confiance

✓ L'inventaire de divergence est fait sur les onze fichiers de la skill, pas estime : 84 regles classees, 43 a remonter, 6 arbitrages nommes avec les deux formulations en regard.
✓ Les deux fixtures existent, sont peuplees, et le couple est discriminant sur la regle la plus subtile de la page (document en forme de template a deux niveaux de remplissage).
✓ Les trois `success_condition` sont des commandes reellement executables, verifiees rouges aujourd'hui — donc capables de basculer.
✓ L'ordre DDD est mecaniquement contraint : la part-3 interdit toute modification de skill qu'aucun FAIL ne designe, hors regles meta listees nommement.

✗ Le volume de la part-1 est le vrai risque : 43 regles remontees peuvent transformer la page en doublon de la skill. La borne « la page porte la regle et son motif, la skill porte la regle et sa procedure » tient, mais elle se verifie a l'oeil, pas par une commande.
✗ Les regles meta (B1, B2, B4, B6) echappent au harnais. Elles sont tracees et relues, jamais prouvees.
✗ « Pas de document du tout » n'est exercable par aucune des deux fixtures : deux regles resteront N/A tant que le couple de fixtures ne bouge pas.
