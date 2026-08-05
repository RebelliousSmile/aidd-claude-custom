# Plan — #14 : les sept pivots inertes, S8 fermée, et la garde qui empêche le défaut de revenir

## Context

Le run 3 de #13 a adjugé deux contrôles négatifs et fait apparaître, en les mesurant, un défaut qu'aucune ligne des deux suites ne visait : **sept pivots sont installés puis restent inertes vis-à-vis du consommateur que leur propre en-tête déclare**. Ce plan ferme ce qui ment à un utilisateur — les sept orphelins et S8 — et pose la garde mécanique qui empêche l'appariement de se rompre à nouveau. Les défauts de harnais (scission critères/registres, S1 non falsifiable, S3/S4 install, fixture *detection*) partent dans une issue séparée, planifiée après.

**Arbitrages tranchés par l'utilisateur** (2026-08-03) : orphelins → compléter les deux cartes · S8 → corriger **et** poser un contrôle négatif neuf dans le même lot · périmètre → la cible d'abord, le harnais ensuite.

## État mesuré à HEAD `2c96f2f` + arbre de travail #13

Relevé sur la **source** (`plugins/`), jamais sur le cache.

| Fait | Mesure |
|---|---|
| Lignes de `pivot-providers.md` | **33** — 17 `perf`, 15 `data`, 1 `ap` |
| Pivots `perf` sans slug dans la carte de `web-optimize` | **5** : `celery`, `drf`, `fastapi`, `httpx`, `vite` |
| Pivots `data` sans slug dans la carte de `data-optimize` | **2** : `datasets`, `sqlalchemy` |
| Ce que ces sept fichiers déclarent | `Loaded by web-optimize` / `Loaded by data-optimize`, en tête de fichier |
| `paths:` dans les 33 sources | présent partout — mécanisme **natif Claude Code**, documenté `sc-js/README.md:80` (« Claude Code (automatique, via `paths:`) — à chaque édition de fichier matchant ») |
| Marqueur d'exemple sur les corps *Case A* | **0 sur 4** installeurs `sniff` ; couverture illustrée `sc-php` 6/6 · `sc-rust` 3/4 · `sc-python` 4/9 · `sc-js` 3/13 |
| Garde « source qui ne résout pas → rendue manquante » | **0 sur 4** `sniff` · **4 occurrences** dans `sc-tiers/setup/actions/01-install.md` |
| Garde de build sur l'appariement carte ↔ table | **aucune** — `pivot-providers.md:83` le dit déjà pour l'unicité de la clé |
| `tools/eval/` | 4 scripts, chaînés par `pnpm test` : `consistency` · `harness` · `coverage` · `selftest` |
| `coverage.mjs:188` | compte les `*-scenarios.md` d'un `evals/` — un `*-runs.md` n'entrerait pas dans ce compte |

## Trois constats que le brouillon de #14 ne portait pas

1. **`paths:` n'est pas une route d'appariement, c'est un chargement parallèle.** Le brouillon écrivait « la seule route qui charge ces pivots est leur `paths:` », ce qui suggère une route concurrente de la carte. C'est autre chose : Claude Code charge la règle à l'édition d'un fichier matchant, **hors de tout run `*-optimize`**. Les sept pivots ne sont donc pas « atteints par une autre route » — ils sont **inatteignables par leur consommateur déclaré**, et leur en-tête affirme le contraire. Contradiction interne mesurable, plus dure que « route non déclarée ».

2. **La détection nomme déjà trois des sept ; c'est la carte qui ne suit pas.** `web-optimize` Step 1.1 lit les manifestes Python « → Django / Flask / **FastAPI** » et Step 1.3 liste `vite.config.ts` en témoin ; `data-optimize` Step 1.1 lit « → Django ORM, **SQLAlchemy**, motor, boto3 ». Trois fois le même schéma : le texte nomme la stack, la carte ne peut pas la servir. Ce n'est pas une omission de sept lignes, c'est une désynchronisation entre deux endroits du même fichier.

3. **Les sept ne sont pas de même nature, et les traiter uniformément referait le défaut.** Quatre sont des stacks (`fastapi`, `drf`, `sqlalchemy`, `datasets`) ; trois sont des **couches additives** qui coexistent avec n'importe quel backend — `vite.md` le dit dans son propre titre (« build tool, hybride avec n'importe quel backend »), `celery` est un worker, `httpx` un client HTTP sortant. Les verser dans une liste dont l'énoncé est « map to one (or more) of » ferait croire qu'un projet peut être *un projet Celery*. Le modèle hybride existe déjà (Step 1.4) mais il parle backend + frontend, jamais couche additive.

## Approche

### Phase 1 — Les sept slugs entrent, et la carte distingue deux natures

`plugins/overcode/skills/web-optimize/SKILL.md`
- Step 1.2 : `fastapi` et `drf` rejoignent la liste exclusive (`drf` documenté comme concaténant avec `django`, conformément à ce que `drf.md` écrit déjà de lui-même).
- Step 1.2, **bloc neuf** : les slugs **additifs** — `celery`, `httpx`, `vite` — s'ajoutent à une stack, ne la remplacent jamais, et n'en sont jamais l'unique valeur. Un projet Django + Celery rend `django` **et** `celery`.
- Step 1.1 : les manifestes Python mentionnent désormais `celery`, `httpx`, `djangorestframework` comme signaux de couche.
- Step 1.3 : témoins — `celery.py` / `tasks.py` + `CELERY_BROKER_URL` · `rest_framework` dans `INSTALLED_APPS` · `FastAPI()` dans `main.py` / `app.py` · `httpx` en dépendance. `vite.config.ts` y est **déjà**, sans slug pour l'accueillir : c'est le témoin qui attend sa carte, pas l'inverse.
- La note ⚠ *a stack slug is not a pivot filename* couvre les nouveaux : les cinq s'apparient à l'identique, ce qui est à écrire pour que l'absence de divergence soit un fait et non un oubli.

`plugins/overcode/skills/data-optimize/SKILL.md`
- Step 1.2 : `sqlalchemy` et `datasets` rejoignent la liste. `datasets` est nommé *HuggingFace datasets* — sans quoi le slug se confond avec un nom commun.
- Step 1.3 : `alembic/` + `models/` (SQLAlchemy) · `load_dataset(` + `datasets` en dépendance.
- La phrase existante « `diesel`, `sqlx` et `rusqlite` ont chacun une ligne » s'étend aux deux nouveaux.

`tests.md` des deux skills — une ligne par slug ajouté dans la matrice de détection.

**Vérification par appariement manuel** avant écriture : chaque slug ajouté est confronté à sa ligne de `pivot-providers.md`, dans les deux sens. Aucun nom deviné.

### Phase 2 — Une garde mécanique sur l'appariement, dans `tools/eval/`

Le remède de phase 1 est ponctuel : rien n'empêche le prochain pivot d'arriver orphelin. La garde le rend impossible silencieusement.

Nouveau contrôle dans `tools/eval/` (ajouté à la chaîne `pnpm test`) :
- **Sens 1, fatal** — tout pivot de `pivot-providers.md` a au moins un slug dans la carte de son consommateur. Un orphelin fait échouer le gate.
- **Sens 2, informatif** — tout slug de carte sans ligne dans la table est listé comme `no provider` **attendu** (`supabase`, `dynamodb`, `hasura`, `sequelize`, `sea-orm`, `rest-vanilla`, `rust-vanilla`, `other`, …). Non fatal : ces valeurs sont correctes depuis #11.
- **Unicité de la clé** — aucune stack revendiquée par deux plugins, ce que `pivot-providers.md:83` signale comme non gardé.

Parsing borné : la carte est extraite du bloc qui suit `Map to one (or more) of:` jusqu'à la ligne `⚠`, les identifiants étant ceux entre backticks. **Si le bloc n'est pas trouvé, le gate échoue bruyamment** — jamais un vert par parseur muet. C'est le seul terme du lot qui soit du code ; l'appariement `perf` ↔ `web-optimize`, `data` ↔ `data-optimize`, `ap` ↔ `ap-optimize` est la table de correspondance à écrire en dur, `seo` n'ayant aucun fournisseur.

### Phase 3 — S8 fermée sur les quatre installeurs

Sur les quatre `plugins/sc-{js,php,python,rust}/skills/sniff/actions/02-install-pivots.md` :
- **Marqueur d'exemple** dans chaque bloc *Case A*, sur le modèle éprouvé de `sc-tiers/setup/actions/01-install.md` (`… one line per target actually processed`).
- **Contre-instruction explicite**, qui manque là où `Use this header verbatim` existe en *Case B* : le corps de *Case A* est une illustration, l'énumération porte les cibles **réellement touchées**. Aujourd'hui les fichiers posent une norme de copie littérale sur un bloc et jamais son contraire sur l'autre.
- **`sc-php` en premier** : son corps illustré nomme 6 cibles sur 6, donc une copie littérale y est indiscernable d'une sortie dérivée — et sur la fixture WordPress de S3 elle affirme `perf-pivots-laravel.md (installed)` et `data-pivots-eloquent.md (installed)`. Puis `sc-rust`, `sc-python`, `sc-js`.

### Phase 4 — Le contrôle négatif qui remplace S8 dans sa famille

Fermer S8 sans rien poser reproduirait exactement ce que le run 2 a fait : une famille *frozen output* tout en vert, qui n'établit plus qu'un défaut **nouveau** serait attrapé.

Ligne neuve dans `plugins/sc-tiers/skills/setup/evals/pivot-install-scenarios.md` — **rouge sur une mesure, pas sur une hypothèse** : la garde « une source qui ne résout pas est rendue **manquante**, jamais écrite » existe dans `sc-tiers` (4 occurrences) et dans **aucun** des quatre `sniff` (0/4). C'est le correctif de la 0.3.0 appliqué à un seul plugin sur cinq : les quatre autres peuvent annoncer `(installed)` pour un fichier que le plugin ne contient pas.

Conforme à la méthode : la ligne est **écrite et mesurée maintenant, non talliée au run 4**, et entre au run 5. C'est ce cycle exact qui a fait de S8 un verdict indépendant.

Contrainte de forme (contrat `behave` 4.3.0) : aucun verdict annoncé dans une cellule, aucune mesure récitée dans le critère — elles vivent dans l'appendice daté.

### Phase 5 — Run 4, juges en contexte neuf

Deux subagents, un par suite, n'ayant écrit ni les suites ni les correctifs des phases 1-4.

Consigne : dry-run READ-ONLY · sources lues dans `plugins/`, jamais dans le cache · **ne pas lire *Appendix* ni *Results log* avant notation** · tallier les deux familles à part · la ligne neuve de phase 4 est **hors tally**.

- `pivot-provenance-scenarios.md` — 12 lignes. Attendu : S12 **reste rouge** (ce lot ne traite pas la route `paths:`, et le dire d'avance évite de lire son rouge comme une régression), S3/S11 tenues sur une carte élargie.
- `pivot-install-scenarios.md` — 7 lignes actives, dont **S8 pour la première fois après correctif**.

Chaque rapport devient un registre daté en append : table *Before / After / Δ*, désaccords, frictions, garde de non-mutation.

### Phase 6 — Versions, changelogs, mémoire, suite

`overcode` **4.4.0 → 4.5.0** (mineure : cartes élargies + garde neuve) · `sc-js`, `sc-php`, `sc-python`, `sc-rust` **bump de patch chacun** (le correctif *Case A* touche un fichier d'action par plugin) · `sc-tiers` **0.3.1 → 0.3.2** (ligne de suite) · `.claude-plugin/marketplace.json` **3.12.0 → 3.13.0** avec les six lignes de plugin. Bump et contenu dans le **même commit**, jamais d'install sur arbre sale.

`aidd_docs/memory/pivots-testing.md` : ce que ce cycle apprend — un fichier peut déclarer son propre consommateur et lui être inatteignable ; une désynchronisation interne à un fichier se corrige par une garde, pas par une passe.

**Issue de harnais** rédigée à partir de ce que le run 4 laisse : scission critères/registres, S1 non falsifiable, S8 provenance à moitié exercé, *Expected behaviour* de S3 (install) faux, S4 (install) qui duplique S5, fixture *detection* neuve (crate Rust sans framework dans un dépôt polyglotte **non**-workspace), couverture retirée non suivie (`supabase`, `dynamodb`, `hasura`, les six de `sc-css`), parc de fixtures non gelé.

**Ne rien committer ni pousser** — déclenchement utilisateur. **#14 n'existe pas encore sur GitHub** : son corps est rédigé, sa création est une action sortante à déclencher.

## Hors périmètre, délibérément

- **S12 n'est pas corrigé.** Le chargement par `paths:` est un mécanisme Claude Code, pas une route de la quittance : le traiter demande de décider ce que la quittance doit dire d'un fichier chargé hors d'elle. Décision produit, pas correctif — et le fermer ici retirerait à la famille *receipt* son seul rouge vivant.
- **Les défauts de harnais** (arbitrage utilisateur : la cible d'abord).
- **Les slugs sans fournisseur** (`supabase`, `dynamodb`, `hasura`, `sequelize`, `sea-orm`) : leur `no provider` est **correct**. La garde de phase 2 les liste, ne les compte pas comme défauts.

## Vérification

**Automatisable** — chaque terme vérifié rouge avant le lot :

```
pnpm test
rg -q 'fastapi'    plugins/overcode/skills/web-optimize/SKILL.md
rg -q '`celery`'   plugins/overcode/skills/web-optimize/SKILL.md
rg -q '`vite`'     plugins/overcode/skills/web-optimize/SKILL.md
rg -q 'sqlalchemy' plugins/overcode/skills/data-optimize/SKILL.md
rg -q 'datasets'   plugins/overcode/skills/data-optimize/SKILL.md
for p in sc-js sc-php sc-python sc-rust; do
  rg -q 'one line per target actually processed' plugins/$p/skills/sniff/actions/02-install-pivots.md
done
rg -q '^### .*run 4' plugins/overcode/skills/web-optimize/evals/pivot-provenance-scenarios.md
rg -q '^### .*run 4' plugins/sc-tiers/skills/setup/evals/pivot-install-scenarios.md
```

Piège de motif évité : `rg -q 'vite'` est **déjà vert** sur `web-optimize/SKILL.md` par le témoin `vite.config.ts` de Step 1.3 — d'où l'ancrage sur le slug entre backticks. Même raison pour `celery`, absent, et `fastapi`, **déjà présent** en Step 1.1 : ce terme-là ne vaut que couplé à la garde de phase 2, seule à distinguer *nommé* de *apparié*.

**Le terme décisif est la garde elle-même** : après phase 1, `pnpm test` doit passer avec **0 orphelin** ; avant phase 1, la même garde doit en signaler **7**. Écrire la garde avant le correctif, la voir rouge à 7, puis verte à 0.

**Simulation à la main** (le gate ne peut rien en dire) :
1. `web-optimize` sur un Django + Celery + httpx — la sortie rend **trois** slugs, la stack et deux couches, et trois paires de quittance.
2. `data-optimize` sur un projet FastAPI + SQLAlchemy — `(data, sqlalchemy)` devient applicable, la paire rend `installed` ou `not installed (sc-python, /sc-python:sniff)` cité verbatim de la table, jamais `no provider`.
3. Un installeur `sniff` dont une source manque — la sortie rend la cible **manquante**, ce qu'aucun des quatre ne fait aujourd'hui, et c'est précisément le rouge que la ligne neuve conserve.

**Verdict du run 4 — non automatisable.** Lu à l'œil dans les deux registres :
- S8 verte, motivée par le texte corrigé et non par le fait que le lot la visait ;
- S12 **toujours rouge**, avec sa cause inchangée — un run 4 qui la rendrait verte sans que rien n'ait été écrit sur la route `paths:` aurait mal jugé ;
- la ligne neuve **hors tally**, sa mesure au registre ;
- chaque N/A restant porte sa cause.

## Risques

| Risque | Mitigation |
|---|---|
| Les trois slugs additifs sont lus comme exclusifs → un projet rendu « Celery » | Bloc séparé, énoncé explicite : ils s'ajoutent, ne sont jamais l'unique valeur |
| Le parseur de la garde ne trouve pas le bloc et rend vert | Échec bruyant sur bloc introuvable — écrit avant le correctif, vu rouge à 7 |
| La garde fige la forme de la carte, qui devient intouchable | Le motif d'ancrage (`Map to one (or more) of:` … `⚠`) est celui déjà partagé par les deux fichiers ; toute autre skill est hors garde |
| Fermer S8 vide sa famille de tout rouge | Phase 4 pose le remplaçant **dans le même lot**, mesuré 0/4 |
| La ligne neuve est talliée au run 4 et perd son indépendance | Hors tally, consigne explicite au juge — le cycle exact qui a rendu S8 fiable |
| Six bumps de version, un contenu oublié quelque part | Bump et contenu dans le même commit ; `pnpm test` après chaque plugin touché |
| Le juge lit l'appendice ou le registre avant de noter | Consigne explicite ; les deux suites le disent déjà dans *Decisive observables* |
| S12 rouge au run 4 se lit comme une régression du lot | Écrit noir sur blanc dans la consigne du juge **et** dans le hors-périmètre |
