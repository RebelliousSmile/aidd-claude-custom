---
name: plan
description: Part 2/3 - ecrire les suites behave qui echouent
objective: "sept suites behave couvrent regle par regle le modele de docs/control.md, sont executees sur les deux fixtures reelles, et le run initial consigne au moins un FAIL par defaut reel de la skill."
success_condition: "bash -c 'test $(ls plugins/overcode/skills/control/evals/*-scenarios.md | wc -l) -eq 7 && grep -lq \"run 1\" plugins/overcode/skills/control/evals/*-scenarios.md && grep -q \"FAIL\" plugins/overcode/skills/control/evals/*-scenarios.md'"
iteration: 0
created_at: "2026-07-27T15:22:58Z"
---

# Instruction: les suites de non-regression, ecrites rouges

## Feature

- **Summary**: Chaque regle de `docs/control.md` devient un scenario `behave`, groupe par famille de regles et non par action. Les suites sont ecrites **avant** l'alignement de la skill et executees telles quelles : le run initial doit reproduire les defauts connus (D1, D2, D3, B3, B5) sous forme de FAIL. Une suite ecrite apres le correctif ne prouve rien.
- **Stack**: `overcode:behave (SKILL.md + actions/02-run.md), suites Markdown, juges dry-run READ-ONLY`
- **Branch name**: `docs/control-ddd-alignment`
- **Parent Plan**: `2026_07_27-control-ddd-alignment-master.md`
- **Sequence**: `2 of 3`
- Confidence: 9/10
- Time to implement: ~1 session

## Architecture projection

### Files to create

- `plugins/overcode/skills/control/evals/authority-scenarios.md` - une seule autorite de classement, quatre modulateurs bornes
- `plugins/overcode/skills/control/evals/phase-scenarios.md` - resolution, provenance, `default` vs `undetermined`, `03-configure` hors modele
- `plugins/overcode/skills/control/evals/domains-scenarios.md` - qui declare quoi, priorise sans restreindre, terme non apparie rapporte
- `plugins/overcode/skills/control/evals/chaining-scenarios.md` - aretes du graphe comme contrat, exclusivite `scope`/`domain`, cas limites du classement
- `plugins/overcode/skills/control/evals/confirmations-scenarios.md` - regime un-par-un sur trois actes, l'unique lot borne et ses quatre composants
- `plugins/overcode/skills/control/evals/measurement-scenarios.md` - densite, plafond, pourcentage, lecture du rapport de couverture, frontieres externes
- `plugins/overcode/skills/control/evals/align-write-scenarios.md` - propriete et lecture seule du document, cinq natures d'ecart, fidelite d'ecriture

### Files to modify

- aucun. **Les blocs `## Test` des six actions restent intacts en phase 2** : ils sont la source des scenarios. Leur transformation en renvoi appartient a la part-3, apres que les suites ont prouve qu'elles tiennent.

### Files to delete

- aucun

## Applicable rules

| Tool   | Name | Path | Why it applies |
| ------ | ---- | ---- | -------------- |
| claude | plugins-marketplace | `C:\Users\fxgui\.claude\rules\plugins-marketplace.md` | ecrire dans `plugins/overcode/skills/control/evals/`, jamais dans le cache |
| claude | skill-writing-style | `C:\Users\fxgui\.claude\projects\C--Users-fxgui-Documents-LLM-Marketplace\memory\skill-writing-style.md` | les fixtures sont du materiau : leurs noms restent dans la suite, jamais dans la skill |
| plugin | behave harness | `plugins/overcode/skills/behave/references/harness-conventions.md` | dry-run READ-ONLY, reproduce-then-confirm, N/A vs FAIL, fixture peuplee |
| plugin | behave quality | `plugins/overcode/skills/behave/references/quality-grid.md` | grille 7 axes par scenario, detection des tests trop vagues ou trop larges |
| plugin | behave template | `plugins/overcode/skills/behave/assets/scenario-template.md` | squelette de suite impose |

## User Journey

```mermaid
---
title: Ecriture des suites rouges
---
flowchart TD
  Page["Page completee en part 1"]
  Extraction["Extraire les regles observables"]
  Tri["Trier observable ou statique"]
  Suites["Ecrire les sept suites"]
  Revue["behave 04-review sur chaque suite"]
  Run["behave 02-run sur les deux fixtures"]
  Verdict["Verdict du run initial"]
  Rouge["Au moins un FAIL consigne"]
  Faux["FAIL du a un test mal ecrit"]

  Page --> Extraction
  Extraction --> Tri
  Tri --> Suites
  Suites --> Revue
  Revue --> Run
  Run --> Verdict
  Verdict -- "defaut reel de la skill" --> Rouge
  Verdict -. "criteres trop vagues" .-> Faux
  Faux -.-> Suites
```

## Risk register

| Risk | Impact | Mitigation |
| ---- | ------ | ---------- |
| Un FAIL vient d'un critere de passage mal ecrit, pas d'un defaut de la skill | On « corrige » la skill pour satisfaire un mauvais test, et on casse une regle juste | `behave 04-review` sur chaque suite **avant** le run initial ; checkpoint utilisateur sur chaque FAIL en fin de part |
| Un scenario teste une etape de `## Process` et non une regle | Le test devient fragile a toute reecriture de procedure et sort du perimetre valide | Chaque ligne de scenario cite la **regle de la page** qu'elle pin, par son titre de section ; une ligne sans regle citee est retiree |
| Les deux fixtures ne peuvent pas exercer certaines regles | Tentation d'inventer une fixture stub, interdite par le harnais | Marquer **N/A** et le consigner ; la limite est declaree dans le master, pas contournee |
| Le juge lit trop de fichiers et « voit » une borne que le chemin de chargement naturel ne montre pas | Un vrai defaut (B3) passe en PASS | Declarer, par scenario, le **chemin de chargement** exact du juge : `SKILL.md` + l'action + les references qu'elle nomme, rien de plus |
| Tout est teste en `behave`, y compris ce qui ne s'observe pas | Scenarios non decidables, verdicts arbitraires | Voir le tri ci-dessous : les regles meta passent par une passe de coherence documentaire, pas par un juge |

## Deux niveaux de verification, decides avant d'ecrire

Toutes les regles de la page ne sont pas observables sur un comportement. Le tri est explicite :

| Nature de la regle | Exemple | Verifiee par |
|---|---|---|
| **Observable** — un refus, un routage, un contenu de rapport, un ensemble d'ecritures prevues | « donnes ensemble, `scope` et `domain` arretent l'action » | `behave` |
| **Meta / redactionnelle** — une enonciation, un decompte, une borne qui doit figurer la ou le champ est defini | « quatre modulateurs, une seule autorite » ; « la borne des *Tier thresholds* doit etre a l'endroit ou le champ est defini » | passe de coherence documentaire en part-3, tracee dans le CHANGELOG |

Une regle meta mal placee peut neanmoins produire un defaut observable — c'est le cas de B3, teste en `behave` par un scenario qui borne le chemin de chargement du juge a `pivot-contract.md`.

## Implementation phases

### Phase 1: Cadrer les fixtures

> Une fixture non decrite rend tout verdict incontestable et donc inutile.

#### Tasks

1. Relever, pour chaque fixture, l'etat qui decide : chemin et taille du document de test, presence d'une suite, presence d'un lanceur e2e etabli, absence de phase declaree, absence de domaine declare, disponibilite d'un rapport de couverture.
2. Ecrire ce releve dans le bloc `Fixture / preconditions` de chacune des sept suites.
3. Lister les regles qu'aucune des deux fixtures ne peut exercer, et les marquer N/A par avance avec leur cause.

#### Fixtures

| Fixture | Chemin | Etat decisif |
|---|---|---|
| `app` | `C:\Users\fxgui\Documents\Perso\Projects\suddenly\_code\app` | `aidd_docs/memory/TESTING.md` — 85 lignes, **rempli mais non decisionnel** (types de tests, aucun critere de tier), a un chemin non conventionnel (majuscules) ; `tests/`, `pytest`, marqueur `e2e`, Playwright etabli ; aucune phase, aucun domaine |
| `ai-hub` | `C:\Users\fxgui\Documents\Perso\Projects\suddenly\_code\ai-hub` | `aidd_docs/memory/testing.md` — 14 lignes, **template generique intact** ; `tests/` + `tests/e2e/` ; aucune phase, aucun domaine |

Le couple discrimine la regle C5 : deux documents qui tombent tous deux dans « traite comme absent pour la decision de tier », a deux niveaux de remplissage — la skill doit **dire lequel des deux cas** elle a rencontre, et c'est verifiable.

#### Acceptance criteria

- [ ] Les sept suites nomment leur fixture et son etat decisif.
- [ ] Les regles non exercables par les deux fixtures sont listees avec leur cause, une fois pour toutes.
- [ ] Aucune fixture stub, aucun document invente.

### Phase 2: Ecrire les sept suites

> Une famille de regles par suite ; une regle par ligne ; jamais une etape.

#### Tasks

1. Partir du squelette `behave/assets/scenario-template.md` pour chaque suite.
2. Reprendre les blocs `## Test` des six actions comme **source** : ce qu'ils affirment devient un scenario. Cinq des six affirment aujourd'hui des choses absentes de la page ; ces affirmations ne sont conservees que si la part-1 les a remontees.
3. Ajouter les scenarios pour les regles de la page qu'aucun bloc `## Test` n'affirme aujourd'hui (voir la table ci-dessous).
4. Pour chaque scenario : citer la section de la page qu'il pin, borner le chemin de chargement du juge, et privilegier un observable d'ecriture a un jugement de prose.

#### Repartition des suites

| Suite | Regles couvertes | Fixtures |
|---|---|---|
| `authority-scenarios.md` | la table des tiers seule classe ; la phase priorise sans classer ; la densite signale sans refuser et sans changer de tier ; un domaine ne retire rien ; les *Risk signals* du pivot priorisent sans classer ; **les *Tier thresholds* ne reclassent jamais un cas qui traverse une vraie frontiere externe (B3)** ; `control` ecrit ce qu'il a mesure et propose la strategie sans l'appliquer | les deux |
| `phase-scenarios.md` | jamais deduite ; question posee **avant** tout classement ; valeur et provenance sur deux lignes ; unique appariement force `unanswered` ⇔ `undetermined` ; `default` ne repose pas la question, `undetermined` si ; **bascule depuis `undetermined` des qu'une phase est declaree (D2)** ; argument valable pour l'execution seule, jamais ecrit ; divergence argument/declaration rapportee ; aucun seuil chiffre par phase ; `03-configure` ne prend ni `phase`, ni `domain`, ni `scope` | les deux |
| `domains-scenarios.md` | le projet declare lesquels, le pivot declare comment les reperer ; le pivot complete sans ecraser ; un domaine priorise et ne restreint pas ; le non apparie reste dans l'analyse **et est rapporte avec le terme qui a echoue** ; sans domaine declare, repli `critical journeys` ; les domaines se proposent en candidats, « aucun » est une reponse valide | les deux (aucun domaine declare des deux cotes : le repli et le rapport de terme sont les observables) |
| `chaining-scenarios.md` | `05-stats` route et **ne lance rien** ; aucun etat garde entre deux executions ; celui qui nomme passe la main, celui qui recoit ne recalcule pas ; `01-write` est le puits, et le passage est un a un avec reevaluation entre chaque ; `02-audit` n'a aucune arete vers `01-write` ; `03-configure` atteignable et terminale ; `scope` et `domain` ensemble → arret et explication ; aucun test trouve → aucun classement ; saturation → `scope` plus etroit, **jamais un `domain` comme remede** | les deux |
| `confirmations-scenarios.md` | un-par-un sur les trois actes : supprimer, appliquer un correctif de config, ecrire un test propose ; **`02-audit` n'admet aucun lot nomme (D1)** ; **`04-strengthen` non plus (D3)** ; l'unique exception, `06-align` sur bascule, avec ses quatre composants et son refus en bloc sans repli par item ; trois categories exclues de tout lot ; un lot vide est un resultat legitime ; la balance nette est un constat, jamais un objectif | les deux |
| `measurement-scenarios.md` | densite contre la mediane du projet, alerte a 3× ; un outlier pointe et ne qualifie jamais ; la densite n'est pas une cible ; un plafond declare l'emporte en tant que plafond, densite rapportee a cote ; `limit` ne vient que d'une limite de nombre ; un pourcentage n'est pas un budget ; **aucun pourcentage n'est produit (B5)** ; ordres, jamais parts ; `covered`/`total`, absence = non couvert, lecture identique dans toutes les phases ; le glob source pilote l'univers ; cas degeneres et leur ordre ; une frontiere externe vaut un test, « hors de portee du test » se renvoie a la supervision | les deux (`app` pour le rapport de couverture reel, `ai-hub` pour le cas `tests/e2e` deja parcouru) |
| `align-write-scenarios.md` | le document appartient a la skill de memoire projet, tout le monde le lit sauf `06-align` ; document en forme de template → traite comme absent, correspondance forcee, **dire lequel des deux cas** ; non documente ≠ suit implicitement le defaut ; cinq natures d'ecart, mesure au bloc des faits et reponse au bloc de strategie ; les deux blocs s'approuvent independamment ; ne jamais creer par defaut ; annoncer la voie d'ecriture, une synchro silencieuse n'est pas une synchro ; relire et comparer le fichier ecrit, rapporter la divergence sans la corriger ; ne jamais remplacer en silence ; hors bascule, cette action ne fait que decrire ; la phase s'ecrit en declaration, jamais en fait mesure | `ai-hub` (template intact) et `app` (rempli non decisionnel) — le contraste **est** l'observable |

#### Regles de la page qu'aucun bloc `## Test` n'affirme aujourd'hui

A ecrire de zero, ce sont les trous de couverture les plus surs :

- les deux lignes valeur/provenance de la phase et l'appariement force ;
- `scope` et `domain` ensemble → arret ;
- un domaine priorise, ne restreint pas, et le terme non apparie est rapporte ;
- l'exception de lot bornee, ses trois categories exclues, la legitimite d'un lot vide — le bloc `## Test` de `06-align` n'exerce aujourd'hui **aucune** bascule de phase ;
- la balance nette est un constat, jamais un objectif ;
- des ordres, jamais des parts, aucun pourcentage produit ;
- `03-configure` ne prend ni `phase`, ni `domain`, ni `scope`.

#### Acceptance criteria

- [ ] Les sept fichiers existent dans `plugins/overcode/skills/control/evals/`, au squelette du template.
- [ ] Chaque scenario cite la section de `docs/control.md` qu'il pin.
- [ ] Chaque scenario declare le chemin de chargement du juge.
- [ ] Les sept trous de couverture listes ci-dessus ont chacun au moins un scenario.
- [ ] Aucun scenario ne pin une etape de `## Process`.

### Phase 3: Revue de qualite avant execution

> Une suite rouge de mauvaise qualite produit un verdict rouge inutilisable.

#### Tasks

1. Lancer `overcode:behave 04-review` sur chaque suite, cible = `skills/control/SKILL.md`.
2. Corriger les scenarios notes trop vagues ou trop larges par la grille 7 axes.
3. Verifier la passe de couverture : chaque famille de regles de la page a au moins un scenario.

#### Acceptance criteria

- [ ] Les sept revues sont produites et leurs remarques bloquantes traitees.
- [ ] Aucun scenario ne reste note rouge sur l'axe « critere decidable ».

### Phase 4: Run initial, et il doit etre rouge

> C'est le run qui prouve que les suites attrapent quelque chose.

#### Tasks

1. `overcode:behave 02-run <suite> <fixture>` pour les sept suites sur les deux fixtures.
2. Consigner chaque run dans le `Results log` de sa suite, au format impose, en nommant la fixture et son etat.
3. Pour chaque FAIL : nommer l'instruction manquante ou contradictoire (fichier + section). Pour chaque N/A : nommer la precondition absente de la fixture.
4. Presenter a l'utilisateur le tableau des FAIL et faire trancher, un par un, « vrai defaut » ou « test a reecrire ».

#### FAIL attendus au run initial

Si l'un de ces cinq ressort PASS, c'est la suite qu'il faut suspecter avant la skill :

| Attendu | Defaut vise | Ou il vit |
|---|---|---|
| FAIL | `02-audit` accepte un lot nomme par l'utilisateur (D1) | `actions/02-audit.md` |
| FAIL | `06-align` exclut `undetermined` de toute bascule, contre la page (D2) | `actions/06-align.md` |
| FAIL | `04-strengthen` accepte un lot nomme du cote des ajouts (D3) | `actions/04-strengthen.md` |
| FAIL | *Tier thresholds* defini sans sa borne la ou le champ est defini (B3) | `references/pivot-contract.md` |
| FAIL | un pourcentage est produit alors que la page dit qu'aucun ne l'est (B5) | `actions/04-strengthen.md` · `actions/05-stats.md` |

#### Acceptance criteria

- [ ] Les sept suites portent un `Results log` avec un run `initial` date, la fixture nommee, un tableau de verdicts et un tally.
- [ ] Au moins un FAIL est consigne, et chaque FAIL cite l'instruction fautive par fichier et section.
- [ ] Chaque N/A cite la precondition de fixture absente ; aucun N/A n'est compte comme PASS.
- [ ] L'utilisateur a tranche chaque FAIL en « vrai defaut » ou « test a reecrire » — la part-3 ne demarre pas avant.

## Amendments

<!-- AI-initiated changes during implementation. Each entry is prefixed with 🤖. -->

## Log

<!-- APPEND ONLY. One entry per step attempt. Never rewrite. -->

## Validation flow demonstration

1. `ls plugins/overcode/skills/control/evals/` : sept fichiers `*-scenarios.md`.
2. Ouvrir `confirmations-scenarios.md` : le scenario D1 decrit une demande de suppression groupee et attend un refus de grouper, en citant `## Les confirmations`.
3. Ouvrir le `Results log` de la meme suite : un run `initial` date, fixture `app` nommee avec son etat, et le FAIL D1 avec `actions/02-audit.md` cite.
4. Verifier qu'aucun fichier des deux fixtures n'a change : `git -C <fixture> status` propre, ou horodatages inchanges si la fixture n'est pas un depot.
