---
name: project_status
description: Rapport de statut projet — audit, sécurité, plan d'action.
---
# Statut du projet — 2026-08-05

> Dépôt documentaire (marketplace de plugins Claude Code : `SKILL.md`, `actions/`, `references/`, `evals/`, `plugin.json`, `marketplace.json`). Pas de code applicatif → les axes ont été adaptés en conséquence. Chaque constat cite `fichier:ligne` vérifié dans la source (`plugins/`), jamais dans le cache installé.

## Résumé projet

| Métrique | Valeur |
|---|---|
| Branche | `main` |
| Tests | ✅ `pnpm test` — exit 0 (`tools/eval/consistency.mjs` + `harness.mjs` + `coverage.mjs` + `selftest.mjs`) |
| Détail tests | consistency : 11 plugins, manifestes/actions cohérents · harness : 5/5 projets fixtures conformes (dont 2 rejets attendus d'`invalid`) · coverage : 71 skills analysés, **0 problème bloquant**, 7 non vérifiables ⚠ (aucune action déclarée dans `SKILL.md`), 11 suites de routage absentes ○ (informatif) · selftest : 4/4 gardes OK |
| Couverture | N/A au sens lignes/branches/fonctions (dépôt Markdown) — substitut : couverture de routage `coverage.mjs` = 71/71 skills sans trou **bloquant** ; 17 skills sans `evals/` ni `tests.md` (cf. Audit) |
| Issues ouvertes | 4 (#8, #9, #12, #13 — remote `RebelliousSmile/my-claude-marketplace`) |
| Arbre de travail | 12 fichiers modifiés (non committés) + `aidd_docs/tasks/2026_08/` non suivi (2 fichiers) |

**État de l'arbre non committé** : correspond à l'exécution en cours des Phases 1/2/5 du plan `aidd_docs/tasks/2026_08/2026_08_03-13-detection-rust-fixture-s7-run-3.md` (issue #13) — détection Rust ajoutée dans `web-optimize/SKILL.md` et `data-optimize/SKILL.md`, suites `evals/pivot-provenance-scenarios.md` et `evals/pivot-install-scenarios.md` étendues, versions bumpées en cohérence (`overcode` 4.3.0→4.4.0, `web-tiers` 0.3.0→0.3.1, marketplace 3.11.0→3.12.0, dans le même diff que le contenu — conforme à la règle du dépôt). Rien n'a été committé ni poussé (conforme à la consigne du plan : « Ne rien committer ni pousser — déclenchement utilisateur »).

## Digest des tâches (`aidd_docs/tasks/`)

95 fichiers `.md` au total (dont 8 sous `audits/`, catégorie séparée — sorties de skill `taste`/`control`, pas des plans).

### Terminé (marqueur `.processed.md` / `.review.md` / `.review_functional.md`)
20 fichiers portent un marqueur de clôture explicite, dont les plus récents :
- `aidd_docs/tasks/2026_07/2026_07_30-10-pivots-testing-fournisseurs-master.processed.md` + 5 parts `.processed.md` — clôturé, source de `pivots-testing.md`
- `aidd_docs/tasks/2026_07/2026_07_28-control-refonte-phase-domaines-master.processed.md`
- `aidd_docs/tasks/2026_07/2026_07_25-design-harness-contract-2-0-alignment.processed.md`
- `aidd_docs/tasks/2026_07/2026_07_23-design-2-0-guarantees-alignment-master.processed.md`
- `aidd_docs/tasks/2026_07/2026_07_22-control-strengthen-action.processed.md`
- `aidd_docs/tasks/2026_06/2026_06_10-design-funnel-refactor-master.processed.md`
- `aidd_docs/tasks/2026_05/2026_05_28-sc-js-sveltekit-pivots.processed.md`

### En cours / pending (session active — non suivi git)
- `aidd_docs/tasks/2026_08/2026_08_03-13-detection-rust-fixture-s7-run-3.md` — plan de l'issue #13, en exécution partielle (cf. diff non committé ci-dessus ; Phases 3-4, la fixture Nuxt et le run 3 en contexte neuf, restent à faire)
- `aidd_docs/tasks/2026_08/2026_08_04-14-pivots-orphelins-s8-garde-appariement.md` — plan de l'issue **#14, qui n'existe pas encore sur GitHub** (le corps est rédigé, la création est une action sortante non déclenchée) ; ce plan lui-même dépend de la clôture du run 3 ci-dessus, pas encore joué
- `aidd_docs/tasks/2026_07_quarantaine-retour-terrain-fse.md` — frontmatter `statut: ouvert` (2026-07-28), 2 entrées actives (Q-01, Q-02+), en attente d'un second constat terrain avant remontée

### Incohérences de nommage relevées
1. **Convention `<yyyy_mm>/<yyyy_mm_dd>-slug.md` rompue par 2 fichiers** posés directement à la racine de `tasks/`, hors de tout sous-dossier mensuel, avec un préfixe mois-seul (pas de jour) : `aidd_docs/tasks/2026_07_plan-integration-retour-terrain-fse.md` et `aidd_docs/tasks/2026_07_quarantaine-retour-terrain-fse.md`. Le second porte un `statut:` en frontmatter que les autres fichiers de `tasks/` n'utilisent pas — mécanisme de suivi local à cette paire, non généralisé.
2. **Suffixe `.plan.md` isolé** : `aidd_docs/tasks/2026_06/2026_06_18-behave-skill-quality-framework.plan.md` est le seul fichier de tout `tasks/` à porter ce suffixe (les autres plans n'en portent aucun). Daté du 2026-06-18 (48 jours), sans marqueur de clôture — **stale** au sens de la consigne (>30 jours sans signal d'achèvement), probablement absorbé depuis par les cycles `control` (7 commits `fix(sc-*)` et 4 cycles `pivots-testing` postérieurs le couvrent vraisemblablement) mais rien ne le déclare formellement clos.
3. **Marqueur de clôture non appliqué de façon uniforme aux fichiers `-part-N`** : quand un plan multi-parties se clôt, seul le fichier `-master` reçoit `.processed`/`.review` — ses `-part-N` associés restent nommés sans marqueur (ex. les 7 `2026_07_23-design-2-0-guarantees-alignment-part-*.md` à côté de leur `-master.processed.md`). Lu isolément, un fichier `-part-N` est indiscernable d'un plan encore ouvert ; il faut retrouver son `-master` pour trancher. Deux lots plus anciens (mai) n'ont **aucun** marqueur, ni sur leur master ni sur leurs parts — `2026_05_28-sc-js-knowledge-provider-master.md` et `2026_05_28-sc-php-sniff-v0.4.0-master.md` — alors que leur contenu est empiriquement dépassé (`sc-php` est aujourd'hui en 0.10.1, loin du « v0.4.0 » visé par le second plan). Ce sont des complétions non déclarées, pas des tâches vivantes.

## Travail connu

- **Issues GitHub ouvertes (4)** : #13 (Rust detection/fixture S7/run 3, en cours — cf. ci-dessus), #12 (`overcode:control` — FAIL S17 + défauts de cible du run 8, ouverte 2026-07-30), #9 (gate `coverage.mjs` — 11 suites absentes, 7 non vérifiables, 4 dérives de préfixe, ERR-09 sans correspondance), #8 (design + sc-php — 3 manques « brownfield » révélés par un projet WP réel, ouverte depuis 2026-06-22 — la plus ancienne, aucun signal de traitement dans les commits récents)
- **#14 rédigée, pas créée** : `aidd_docs/tasks/2026_08/2026_08_04-14-pivots-orphelins-s8-garde-appariement.md` en attend la création sur GitHub, elle-même conditionnée à la clôture du run 3 de #13
- **TODO/FIXME dans `plugins/`** : aucune occurrence en tant que dette de code — les seules occurrences de `TODO`/`FIXME` dans `plugins/*.md` sont soit du **vocabulaire normalisé documenté à éviter** (`obs:extract-pdf` interdit explicitement `TODO`/`DONE` au profit de `pending`/`done`/`failed`, `plugins/obs/skills/extract-pdf/actions/01-setup.md:42`), soit des **détecteurs** que `overcode:taste`/`foresee` cherchent dans le code d'un projet cible (`plugins/overcode/skills/taste/actions/02-assess-code.md:93`, `plugins/overcode/skills/taste/assets/code-patterns.md:51`) — rien à traiter ici
- **1 TODO opérationnel réel** trouvé hors `plugins/` : `aidd_docs/tasks/2026_07_plan-integration-retour-terrain-fse.md:191` — `<!-- TODO(human) : classer les quinze énoncés en vagues d'intégration.` — marqueur de tâche humaine explicite, non résolu

## Constats d'audit

### Axe 1 — Liens `@../<chemin>.md` cassés (skills → assets/references)

Vérification exhaustive : 118 références `@../...md` collectées dans `plugins/`, chacune résolue relativement au dossier du fichier qui la porte, existence testée sur disque.

**1 lien cassé sur 118** :
- `plugins/overcode/skills/foresee/SKILL.md:34` — `` Read all adjacent context before scoring — never score in isolation. See `@../assets/context-map.md`. `` La cible réelle est `plugins/overcode/skills/foresee/assets/context-map.md` (fichier confirmé présent). Le lien pointe un cran trop haut, vers `plugins/overcode/skills/assets/context-map.md` (inexistant). Convention confirmée par 3 autres `SKILL.md` du dépôt qui référencent leurs propres `assets/` sans `../` (`plugins/sc-css/skills/audit/SKILL.md:33`, `plugins/overcode/skills/taste/SKILL.md:34`, `plugins/overcode/skills/behave/SKILL.md:46`, tous en `@assets/...`) : `foresee/SKILL.md` est l'unique exception, par erreur de frappe vraisemblable.

117 autres liens vérifiés résolvent correctement — pas de dérive systémique, un seul cas isolé.

### Axe 2 — Couverture `evals/`/`tests.md` par skill

Vérification exhaustive sur les 71 skills recensés par `coverage.mjs` (chaque `<plugin>/skills/<nom>/` avec un `SKILL.md`) : présence d'un dossier `evals/` OU d'un fichier `tests.md` à la racine du skill (les deux formats coexistent légitimement dans ce dépôt — `data-optimize` et `web-optimize` utilisent `tests.md`, la majorité `evals/`).

**17 skills sans aucun des deux**, répartis sur 3 plugins :
- `plugins/overcode/skills/{ap-optimize,baby,changelog,decompose,harvest,journey,reconcile-normative}/` (7)
- `plugins/sc-css/skills/{audit,design-bridge,improve,legacy,sniff,teach}/` (6 — **la totalité des skills du plugin**)
- `plugins/sc-php/skills/{audit,builder-coverage,design-bridge,setup}/` (4)

Fait à ne pas confondre avec ce constat : `sc-css` n'a délibérément **pas** de pivot `testing` (décision documentée dans `aidd_docs/memory/pivots-testing.md:15`, « décompte 2026-07-30 : 1 champ sur 10, 0 des 5 requis ») — mais ce champ concerne les pivots de stack fournis à `overcode:control`, un objet distinct des suites `evals/` qui testent le comportement des skills `sc-css` elles-mêmes. Les deux gaps sont réels et non liés : le second n'a aucune décision documentée équivalente.

## Constats de sécurité / intégrité

### Axe 1 — Chemins personnels codés en dur

Recherche `C:/Users/fxgui/...` dans `plugins/` (hors `CHANGELOG.md`, qui documente légitimement une correction passée).

**13 occurrences dans le skill `obs:mail`**, toutes vers `C:/Users/fxgui/Public/Notes/Thunderbird/` (racine de courrier personnelle) :
`plugins/obs/skills/mail/SKILL.md:5,21,74` · `plugins/obs/skills/mail/actions/01-scan.md:19,20,42` · `plugins/obs/skills/mail/actions/02-analyze.md:69` · `plugins/obs/skills/mail/actions/06-reply.md:83` · `plugins/obs/skills/mail/evals/mail-reply-scenarios.md:28,67` · `plugins/obs/skills/mail/evals/mail-scenarios.md:16,61,93`

Ce n'est **pas un secret** (pas de token/clé), mais c'est un chemin d'installation propre à la machine de l'auteur, codé en dur dans un skill distribué par le marketplace — tout utilisateur du plugin `obs` sur une autre machine (ou l'auteur lui-même sur un autre poste) verra `obs:mail` échouer silencieusement à trouver son répertoire. `plugins/obs/CHANGELOG.md:71` montre qu'un chemin en dur analogue (`Public/Notes/…`) a déjà été corrigé une fois dans `obs:tree`/`obs:project` (« fin du chemin mort … le vrai coffre est sous `Documents/` ») — `obs:mail` n'a pas reçu le même traitement et porte le même risque.

### Axe 2 — Commandes destructives non gardées dans les prompts d'action

Recherche `rm -rf|--force|force-push|reset --hard|git push.*-f|--no-verify|--no-gpg-sign|DROP TABLE|chmod 777` dans `plugins/**/*.md`.

**0 occurrence.** Aucune instruction d'action du dépôt ne prescrit de commande destructive non gardée. Vérifié également : aucun secret/clé/token en dur (`api[_-]?key|secret|token|password|bearer` grep sur `plugins/` — les seules occurrences sont du vocabulaire de domaine : « nonce », « access token » en tant que concept documenté, jamais de valeur) ; aucun appel réseau sortant vers un hôte externe non local dans les `actions/*.md` (les seuls `fetch`/`curl` trouvés visent `localhost:8888`/`localhost:3000` en fixtures de dev, `plugins/sc-js/skills/wp-blocks/actions/01-validate-roundtrip.md:13,79,99`).

## Quick wins (< 15 min chacun)

- [ ] Corriger `@../assets/context-map.md` → `@assets/context-map.md` dans `plugins/overcode/skills/foresee/SKILL.md:34` — 1 ligne, aligne sur la convention des 3 autres `SKILL.md` — source : Audit axe 1
- [ ] Créer l'issue #14 sur GitHub depuis le corps déjà rédigé dans `aidd_docs/tasks/2026_08/2026_08_04-14-pivots-orphelins-s8-garde-appariement.md` (le fichier le signale lui-même : « action sortante à déclencher ») — source : Digest tâches
- [ ] Renommer/déplacer les 2 fichiers racine `aidd_docs/tasks/2026_07_plan-integration-retour-terrain-fse.md` et `2026_07_quarantaine-retour-terrain-fse.md` sous `aidd_docs/tasks/2026_07/` pour respecter la convention `<yyyy_mm>/` (ou documenter explicitement pourquoi ils dérogent) — source : Digest tâches, incohérence #1
- [ ] Trancher le sort de `2026_06_18-behave-skill-quality-framework.plan.md` (stale, 48 jours) : marquer `.processed`/`.review` s'il est couvert par les cycles `control` postérieurs, ou le réactiver — source : Digest tâches, incohérence #2

## Plan à 7 jours (60 min/jour)

### J1 — Sécurité : chemin en dur `obs:mail` (60min)
- **Auditer les 13 occurrences de `C:/Users/fxgui/Public/Notes/Thunderbird/`** (~20min) et décider du mécanisme d'ancrage (variable d'environnement ? détection type `obs:tree` via l'ancre `Pro/` déjà en place pour `obs:project`, cf. `plugins/obs/skills/project/evals/project-scenarios.md:14`) `/obs:mail`
- **Appliquer le correctif sur `SKILL.md` + 3 `actions/`** (~30min)
- **Mettre à jour les 3 fichiers `evals/`** pour refléter le nouveau mécanisme d'ancrage (~10min)

### J2 — Quick wins + issue #14 (60min)
- Corriger `foresee/SKILL.md:34` (~5min)
- Renommer les 2 fichiers racine de `tasks/` (~5min)
- Trancher `2026_06_18-behave-skill-quality-framework.plan.md` (~15min)
- Créer l'issue #14 sur GitHub depuis le plan rédigé (~15min) `gh issue create`
- Marge : revue de #8 (ouverte depuis 44 jours, la plus ancienne, aucun signal récent) — évaluer si elle est toujours pertinente (~20min)

### J3 — Poursuite du plan #13 (60min)
- Reprendre `aidd_docs/tasks/2026_08/2026_08_03-13-detection-rust-fixture-s7-run-3.md` Phase 3 (fixture template `perf_checklist_nuxt.md`, hors dépôt marketplace) (~30min)
- Vérifier les 8 assertions automatisables de la section *Vérification* du plan (~30min) `pnpm test`

### J4 — Run 3 en contexte neuf (60min)
- Lancer les 2 subagents READ-ONLY prescrits par la Phase 4 du plan #13, un par suite (`pivot-provenance-scenarios.md`, `pivot-install-scenarios.md`) (~60min, probablement à cheval sur J4-J5 vu la consigne « contexte neuf, ne rien committer »)

### J5 — Clôture #13 + versions (60min)
- Dépouiller les registres du run 3, rédiger le corps final de #14 à partir de ce qui est adjugé (~30min)
- Vérifier cohérence des 3 bumps déjà en place dans l'arbre de travail (`overcode` 4.4.0, `web-tiers` 0.3.1, marketplace 3.12.0) contre le contenu final avant commit (~15min) `pnpm test`
- Committer la clôture de #13 (~15min) `git add && git commit`

### J6 — Couverture `evals/` : sc-css (60min)
- Poser une première suite `evals/` minimale sur au moins 1 des 6 skills `sc-css` sans couverture (candidat : `sniff`, le plus proche des suites déjà éprouvées côté `sc-js`/`sc-php`) (~60min) `/behave:scaffold`

### J7 — Couverture `evals/` : overcode + sc-php (60min)
- Traiter 1-2 skills parmi les 7 `overcode` et 4 `sc-php` non couverts, en priorisant ceux avec des `actions/` déjà stables (`changelog`, `decompose`) plutôt que ceux encore mouvants (~60min) `/behave:scaffold`
