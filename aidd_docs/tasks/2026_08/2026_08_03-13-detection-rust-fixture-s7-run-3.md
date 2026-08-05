# Plan — Issue #13 : la détection Rust, la fixture S7, et le run 3

## Context

La clôture de #11 a livré la quittance de pivot (DEC-010) et retiré neuf cibles fantômes, mais a laissé trois résidus qui ne vivaient que dans deux suites `behave` — c'est-à-dire nulle part où un backlog les relise. #13 leur a donné un porteur ; ce plan les ferme.

Le problème de fond n'est pas la quittance, qui est réparée : c'est la **détection**. Une stack Rust ne devient jamais applicable, donc aucune paire `source` / `pivot` n'est construite pour elle — et une paire jamais construite ne peut pas être bien rendue. S3 et S11 sont rouges **en amont** de ce qu'elles mesurent. Deux autres résidus s'y ajoutent : un barreau du modèle de provenance (*template*) qu'aucune fixture du parc n'exerce, et deux contrôles négatifs écrits et mesurés mais jamais jugés.

Résultat attendu : les deux suites tournent sur une détection qui existe, le barreau *template* est exercé pour la première fois, et un run 3 en contexte neuf note S8 et S12 — **en laissant des rouges**, qui sont la matière de #14.

**Arbitrages tranchés par l'utilisateur** (2026-08-03) : S7 → poser le fichier de fixture et élargir son critère · contenu → copier le fichier réel et écrire la divergence de version · `sc-tiers` → bump de patch, un eval expédie dans le plugin.

## État mesuré à HEAD `2c96f2f`

Relevé sur la **source** (`plugins/`), jamais sur le cache.

| Fait | Mesure |
|---|---|
| `Cargo.toml` dans `web-optimize/SKILL.md` | **0** |
| `Cargo.toml` dans `data-optimize/SKILL.md` | **2**, toutes deux au service du test monorepo (`:70`, `:74`) — jamais comme signal de stack |
| Entrées Rust dans les deux cartes de stacks | **0** sur 15 slugs (web, `:130-138`) et **0** sur 17 (data, `:141-144`) |
| Pivots Rust réellement fournis | **4** dans `pivot-providers.md` : `perf-pivots-axum.md`, `data-pivots-diesel.md`, `data-pivots-rusqlite.md`, `data-pivots-sqlx.md` |
| Garde monorepo `web-optimize` (`:79`) | `pnpm-workspace.yaml`, `turbo.json`, `nx.json`, `lerna.json` — **rien sur `Cargo.toml [workspace]`**, là où `data-optimize:74` le teste |
| `web-optimize/tests.md` ligne 1 | attend `nuxt3` — le correctif résidu-6 de #11 a renommé le slug en `nuxt` dans `SKILL.md` sans suivre ici |
| Position des `Cargo.toml` du parc | **jamais à la racine** : `lyremember/_code/app/rust-backend/` (prof. 2), `choix-narratifs/_code/engine/core\|harness\|wasm/` (prof. 3), `email-to-markdown/_code/app/` (prof. 1) |
| Fixture S7 — `email-to-markdown/_code/site` | Nuxt **^4.3.1** · `aidd_docs/templates/dev/` existe (5 fichiers, aucun `perf_checklist_*`) · réceptacle `.claude/rules/07-quality/` présent avec **`.gitkeep` seul** · dépôt git autonome, `aidd_docs/` non ignoré |
| Marqueur d'exemple sur les corps *Case A* | **0 sur 4** installeurs `sniff` |
| Versions | `overcode` 4.3.0 · `sc-tiers` 0.3.0 · marketplace 3.11.0 |

## Quatre constats que l'issue ne porte pas

1. **La détection seule ne ferme rien : les manifestes ne sont pas à la racine.** Ajouter `Cargo.toml` à la liste sans dire **jusqu'où chercher** laisse S3 et S11 rouges pour une seconde raison. Borne à écrire : `-maxdepth 3 -not -path '*/target/*'` — 3 suffit exactement pour atteindre `engine/core/Cargo.toml`.

2. **S11 est bloquée en amont par la garde monorepo.** `choix-narratifs` porte `pnpm-workspace.yaml` avec `packages: ["."]` : la halte se déclenche et n'offrira jamais `engine/`. Aligner la garde de `web-optimize` sur celle de `data-optimize` est **obligatoire**, pas cosmétique.

3. **La fixture de S7 est celle de S6, et leurs critères se contredisent sur l'axe `pivot`** — vérifié sur les lignes 49 et 50 de la suite. S6 exige `pivot : empty receptacle` (réceptacle présent, `.gitkeep` seul) ; S7 exige `pivot : not installed`. Poser le fichier rend S7 jugeable **et fausse** : une skill conforme y échouerait. Les deux axes sont orthogonaux — S6 lit le réceptacle, S7 lit le barreau atteint — donc **le critère de S7 s'élargit, la fixture ne bouge pas**.

4. **Fermer #13 ne rend pas les suites vertes, et c'est le résultat attendu.** Corriger S8 et S12 avant leur première notation détruirait le contrôle négatif que l'issue demande justement de faire juger. Le run 3 doit rendre au moins deux FAIL ; la clôture de #13 ouvre #14.

## Approche

### Phase 1 — La détection Rust existe dans les deux consommateurs

`plugins/overcode/skills/web-optimize/SKILL.md`
- Quick Start (`:78-80`) : sonde Rust (`axum`, `actix-web`, `rocket` dans les `Cargo.toml`) **et** garde monorepo alignée sur `data-optimize:74` (`grep -l '^\[workspace\]' Cargo.toml`).
- Step 1.1 : `Cargo.toml → crates web Rust`, avec la borne de profondeur explicite.
- Step 1.2 : entrées `rust-axum` et `rust-vanilla`. Écrire que `rust-vanilla` **rend une paire `no provider`** et n'ouvre aucune halte « la famille ne s'applique pas ».
- `:140` : ajouter `rust-axum → perf-pivots-axum.md` à la note *a stack slug is not a pivot filename*, qui existe déjà ici.
- Step 1.3 : témoins `Cargo.toml`, `Cargo.lock`, `src/main.rs`.

`plugins/overcode/skills/data-optimize/SKILL.md`
- Step 1.1 : `Cargo.toml → ORM Rust`, même borne.
- Step 1.2 : `rusqlite`, `sqlx`, `diesel` — les trois s'apparient à l'identique à leur `data-pivots-<slug>.md`.
- Step 1.2 : **ajouter la note « un slug n'est pas un nom de pivot »**, absente ici alors que la carte porte trois paires divergentes réelles (`laravel-eloquent` → `data-pivots-eloquent.md`, `graphql-apollo` et `graphql-urql` → `data-pivots-graphql.md`).
- Step 1.3 : témoins `diesel.toml`, `migrations/`.

`tests.md` des deux skills — lignes Rust dans la matrice ; côté web, corriger `nuxt3` → `nuxt` ligne 1.

**Vérifications** : chaque slug ajouté a soit une ligne dans `pivot-providers.md`, soit un `no provider` explicite — vérifié ligne à ligne, aucun nom deviné. La borne de profondeur est simulée à la main contre les **trois chemins réels** du parc.

### Phase 2 — S3, S4 et S11 mesurent ce qu'elles disent mesurer

`plugins/overcode/skills/web-optimize/evals/pivot-provenance-scenarios.md`
- **S3** et **S11** : critères reformulés sur la carte corrigée — manifeste lu, stack reconnue, paire construite. S11 mentionne que la halte monorepo doit désormais offrir `engine/`.
- **S4** : critère scindé en deux binaires — **(a)** la valeur émise est `no provider` ; **(b)** elle est atteinte par une entrée Rust reconnue, jamais par le fourre-tout `other`. Écrire que (a) sans (b) est un vert menteur, et pourquoi : le jour où `sc-rust` livre un second pivot `perf`, (a) reste vrai et (b) devient faux.
- Bloc *Two families* : consigner que la famille *detection* perd son seul rouge si S3 et S11 basculent — fait à déclarer au run 3, pas à compenser en inventant une ligne.

Contrainte de forme (contrat `behave` 4.3.0) : aucun verdict annoncé dans une cellule, aucun numéro de ligne contre un fichier mouvant — les citations vivent dans l'appendice daté.

### Phase 3 — Le barreau *template* devient exerçable

1. Copier `email-to-markdown/_code/app/aidd_docs/templates/dev/perf_checklist_nuxt.md` (234 l., réel, dérivé de PSI sur `jeveuxtravailler.com`) vers `email-to-markdown/_code/site/aidd_docs/templates/dev/`. Le fichier est aujourd'hui rangé dans un crate **Rust** : le déplacer corrige un mauvais rangement plutôt qu'il ne fabrique une fixture.
2. Élargir l'axe `pivot` de S7 : *un des trois états non-`installed`, cohérent avec l'état réel du réceptacle*. Le sujet de la ligne est l'axe `source` — le barreau *template* est atteint **et nommé** ; l'axe `pivot` ne doit qu'être non contradictoire.
3. Déclarer la fixture dans le bloc *Fixture / preconditions*, **divergence Nuxt 3 / Nuxt 4 écrite, pas tue** (les deux se rendent au slug `nuxt`, l'appariement tient).
4. Réécrire le bloc *S7's `N/A` is of another kind* : la dette est levée.

⚠ Écrire hors dépôt est un **provisionnement de fixture**, jamais une mutation de run : fait délibérément, hors de tout run de juge, committé dans `email-to-markdown/_code/site` (dépôt autonome, `aidd_docs/` non ignoré). Le réceptacle `.claude/rules/07-quality/` reste **inchangé** — vérifié par listing avec mtimes, jamais par `git status`.

### Phase 4 — Run 3, juge en contexte neuf

Deux subagents, **un par suite**, n'ayant écrit ni les suites ni les correctifs des phases 1-3 — sans quoi le défaut *juge = auteur* que le run 2 a clos se rouvre.

Consigne : dry-run READ-ONLY · sources lues dans `plugins/`, jamais dans le cache · **ne pas lire *Appendix* ni *Results log* avant notation** (six faux FAIL au run 2 par ce chemin) · tallier les deux familles à part.

- `pivot-provenance-scenarios.md` — 12 lignes, dont **S12 pour la première fois** et S3/S11 sur la détection.
- `pivot-install-scenarios.md` — 7 lignes actives, dont **S8 pour la première fois** (S2 archivée, non rejouée).

Chaque rapport devient un registre de run daté dans sa suite : table *Before / After / Δ*, désaccords, frictions, garde de non-mutation. Le registre est **append-only** — un run antérieur ne se recompte pas.

### Phase 5 — Versions, changelogs, mémoire, suite

`overcode` 4.3.0 → **4.4.0** (mineure, additive) · `sc-tiers` 0.3.0 → **0.3.1** · `.claude-plugin/marketplace.json` 3.11.0 → **3.12.0** avec les deux lignes de plugin. Bump et contenu dans le **même commit**, jamais d'install sur arbre sale.

`aidd_docs/memory/pivots-testing.md` : ce que ce cycle apprend — un critère de ligne peut passer par la mauvaise route ; un contrôle négatif se ferme, il ne se garde pas par confort.

Corps de **#14** rédigé à partir de ce que le run 3 a adjugé (attendu : marqueur d'exemple absent des 4 corps *Case A* ; route par frontmatter absente de la quittance).

Ce plan est archivé en `aidd_docs/tasks/2026_08/2026_08_03-13-detection-rust-fixture-s7-run-3.md`. **Ne rien committer ni pousser** — déclenchement utilisateur.

## Hors périmètre, délibérément

- **S8 et S12 ne sont pas corrigés.** Les corriger avant leur première notation détruit le contrôle négatif (constat 4).
- `supabase`, `dynamodb`, `hasura`, `sequelize` dans la carte `data-optimize` sans ligne dans `pivot-providers.md` : leur `no provider` est **correct** depuis le retrait de #11. Noté, pas traité.

## Vérification

**Automatisable** — chaque terme vérifié rouge à HEAD `2c96f2f` :

```
pnpm test
rg -q 'Cargo\.toml'  plugins/overcode/skills/web-optimize/SKILL.md
rg -q 'axum'         plugins/overcode/skills/web-optimize/SKILL.md
rg -q 'rusqlite'     plugins/overcode/skills/data-optimize/SKILL.md
rg -q 'Cargo\.toml'  plugins/overcode/skills/{web,data}-optimize/tests.md
! rg -q 'nuxt3'      plugins/overcode/skills/web-optimize/tests.md
test -f "C:/Users/fxgui/Documents/Perso/Projects/email-to-markdown/_code/site/aidd_docs/templates/dev/perf_checklist_nuxt.md"
rg -q '^### .*run 3' plugins/overcode/skills/web-optimize/evals/pivot-provenance-scenarios.md
rg -q '^### .*run 3' plugins/sc-tiers/skills/setup/evals/pivot-install-scenarios.md
```

Deux pièges de motif, évités : `rg -qi 'rust'` est **déjà vert** sur `web-optimize/SKILL.md` par *trustable* (`:248`) et *trusting* (`:289`) — d'où `Cargo\.toml` et `axum`. `run 3` nu est **déjà vert** dans les deux suites par la section *What a run 3 owes this suite* — d'où l'ancrage sur `^### .*run 3`.

**Simulation à la main** (le gate ne peut rien en dire) :
1. `web-optimize` sur `choix-narratifs/_code` — la halte monorepo offre désormais `engine/` ; le run rend **deux** paires, Astro et Rust, la seconde `no provider` par une entrée reconnue.
2. `data-optimize` sur `lyremember/_code/app` — `rust-backend/Cargo.toml:10` est lu, `(data, rusqlite)` devient applicable, la paire rend `pivot : not installed (sc-rust, /sc-rust:sniff)` cité verbatim de la table.
3. `web-optimize` sur `email-to-markdown/_code/site` — le barreau *template* est atteint sur `perf_checklist_nuxt.md`, la sortie porte `source : template …` **et** l'état réel du réceptacle sur l'axe `pivot`, sans contredire S6.

**Verdict du run 3 — non automatisable, et il ne vaut PAS 0 FAIL.** Différence décisive avec #11. Lu à l'œil dans les deux registres :
- aucune ligne non notée — S8 et S12 portent un verdict et sa cause ;
- S3 et S11 notées sur la détection, motivées par une mesure sur le texte corrigé et non par le fait que le plan les visait ;
- S7 porte PASS ou FAIL, plus N/A ;
- chaque N/A restant porte sa cause.

Un run 3 qui rendrait 0 FAIL aurait jugé les contrôles négatifs à côté.

## Risques

| Risque | Mitigation |
|---|---|
| Détection ajoutée mais manifestes en sous-dossier non atteints | Borne de profondeur écrite dans l'instruction, simulée contre les trois chemins réels avant d'écrire |
| La garde monorepo de `web-optimize` coupe avant Step 2 sur `choix-narratifs` | Alignement sur `data-optimize:74` — tâche explicite, pas un effet de bord |
| S7 devient jugeable et fausse (conflit d'axe avec S6) | Le critère s'élargit **dans le même lot** que la pose du fichier, jamais après |
| `rust-vanilla` déclenche une halte « famille ne s'applique pas » façon `ap-optimize` | Interdit explicitement : l'entrée rend une paire, elle n'arrête pas le run |
| Le juge lit l'appendice ou le registre avant de noter | Consigne explicite ; les deux suites le disent déjà dans *Decisive observables* |
| Le juge est l'auteur des correctifs | Deux subagents distincts, contexte neuf |
| Mutation accidentelle du parc | READ-ONLY ; aucune commande git dans `email-to-markdown/_code/app` (*dubious ownership*) ; non-mutation vérifiée par listing avec mtimes — `git status` est aveugle sur deux réceptacles |
| Le run 3 rend 2 FAIL et se lit comme une livraison ratée | Écrit noir sur blanc que 0 FAIL serait le mauvais résultat |
