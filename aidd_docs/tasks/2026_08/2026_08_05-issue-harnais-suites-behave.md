# Issue à créer — Harnais des deux suites behave « pivots »

> **Corps rédigé, non créé.** La création sur GitHub est une action sortante à déclencher par l'utilisateur, comme celle de #14. Le numéro sera attribué à la création ; les renvois ci-dessous citent #11, #13 et #14 par leur numéro de plan.
>
> Titre proposé : **Harnais — scinder les suites behave « pivots » et fermer onze dettes de méthode**
> Étiquettes proposées : `harness`, `behave`, `pivots`

## Contexte

Deux suites behave couvrent les pivots `.claude/rules/07-quality/` :

- `plugins/web-tiers/skills/setup/evals/pivot-install-scenarios.md` — l'installation (9 lignes, S1–S9)
- `plugins/overcode/skills/web-optimize/evals/pivot-provenance-scenarios.md` — la quittance et la détection (12 lignes, S1–S12)

Quatre runs ont eu lieu (2026-07-30, 2026-08-03 ×2, 2026-08-05). Les correctifs qu'ils ont produits sont livrés. **Ce qui suit est ce que les runs ont trouvé sur le harnais lui-même et que personne n'a corrigé** — chaque point est daté, mesuré, et adossé au registre de la suite concernée.

État à l'ouverture : install **7 PASS / 0 FAIL** en décompte (S9 hors décompte, mesurée FAIL 4/4, entre au run 5) · provenance **11 PASS / 1 FAIL / 0 N/A** (S12 rouge vivant, voulu).

---

## 1. Scinder critères et registres — **le seul point bloquant**

La règle « ne lis pas l'appendice ni le journal avant de noter » existe depuis le run 1. **Elle est structurellement inapplicable** : critères, annexe et journal de résultats partagent un fichier, et un seul `Read` charge le tout. Le juge ouvre les critères, il ouvre les réponses.

**Mesuré deux fois le même jour, sur les deux suites, par deux juges indépendants en contexte neuf** (run 4, 2026-08-05). Les deux l'ont déclaré plutôt que de prétendre s'être conformés, et ont reconstruit leurs verdicts depuis les sources primaires. C'est une atténuation, pas la garantie que la règle existe pour donner : **les verdicts du run 4 sont plus faibles que ceux du run 3 d'exactement cela.**

Le remède n'est pas d'écrire l'instruction plus fort. Proposition :

- `…-scenarios.md` — préconditions, lignes, critères. **Ce que le juge lit.**
- `…-scenarios.results.md` — annexe des mesures datées + journal des runs. **Ce que le juge n'ouvre qu'après avoir rendu.**

Les deux suites, dans le même lot. Le reste de cette issue est jugeable sans ce point ; ce point ne l'est par rien d'autre.

## 2. Lignes non falsifiables ou auto-contradictoires

| Suite | Ligne | Défaut | Constaté |
|---|---|---|---|
| install | **S4** | Après le resserrement du run 3, son critère est mot pour mot celui de S3 et de S5. Rien n'y dépend de `rusqlite`, de `lyremember`, ni de Rust — elle rendrait le même verdict **sans fixture**. | runs 3 **et** 4 (troisième écriture consécutive) |
| install | **S3** | Le *comportement attendu* affirme quelque chose de faux sur sa propre fixture selon le run 3 ; le run 4 n'a **pas pu le reproduire** (`01-scan.md:16,32` n'arme jamais Laravel sur `wp-2026`). Non reproduit ≠ réfuté : le juge a dû quitter le chemin de chargement déclaré pour le vérifier, ce qui est le constat. | runs 3 et 4 |
| install | **S7** | La branche « référence manquante » est en `:20`, dans la prose *Closed path list*, **hors** de la garde numérotée `:39-47` qu'un agent exécute réellement. Lecture stricte → FAIL ; lecture large → PASS. Les deux se défendent sur le texte actuel, ce qui **est** le défaut. | run 4 |
| provenance | **S1** | Non falsifiable : elle exige une valeur tout en déléguant la route à une autre ligne, alors que l'apparition de la valeur dépend de la route. **De plus, sa justification a péri sans que la ligne bouge** — le run 3 la tenait pour structurellement inatteignable (`datasets` absent de la carte) ; #14 a ajouté `datasets`, et le verdict ne survit plus que pour une raison de fixture. | runs 3 et 4 |
| provenance | **S8** | À moitié mesurée depuis le run 3 : demande un changement de fixture, pas de formulation. | runs 3 et 4 |
| provenance | **S11** | La ligne se contredit : sa *Situation* place `pnpm-workspace.yaml` à la racine, ses *Pass criteria* affirment qu'aucun marqueur n'est en profondeur 0. Sur disque les deux sont vraies **de marqueurs différents** (`pnpm-workspace.yaml` profondeur 0, `engine/Cargo.toml` profondeur 2). Le run 3 ne l'avait pas vu. | run 4 |
| provenance | **S3** | Deux prémisses fausses sans effet sur le verdict : le réceptacle porte **4** fichiers, pas 2 ; `lyremember-app/package.json` ne déclare aucun SDK data JS, donc le mode d'échec décrit n'est pas disponible sur cette fixture. | run 4 |

**Ce que ces sept lignes ont en commun** : leur verdict est juste, leur texte ne l'est plus. Une ligne dont la formulation ne tient plus rend un vert qui n'atteste rien — c'est le même mécanisme que la colonne *Instruction pinned* retirée en #11, un cran plus bas.

## 3. Une famille verte ne discrimine plus

La famille **détection** de la suite provenance est **2/2 verte** et n'a reçu **aucun contrôle négatif** ce cycle. C'est exactement la forme que la famille *frozen output* de l'autre suite avait atteinte au run 2, et qui avait justifié S8. La suite provenance entre au run 5 avec `S12` comme unique rouge vivant et une sous-famille incapable d'échouer.

**À faire avant le run 5** : écrire et mesurer un contrôle négatif de la famille *détection*, hors décompte au run 5, en décompte au run 6. Cycle fixe — toute autre chronologie rend un verdict sans valeur (cf. #14, la clause posée puis retirée sur les quatre installeurs).

**Fixture manquante que ce contrôle demande** : un **crate Rust sans framework, dans un dépôt polyglotte non-workspace**. Le parc actuel ne porte que des cas où la sonde Rust est soit armée par un framework (`rust-axum`), soit dans un workspace (`engine/Cargo.toml`). Le barreau « stack Rust reconnue, non servie » (`rust-vanilla`) n'est exercé que par `email-to-markdown/_code/app` (S4), dont la cohabitation avec une autre stack **dans la même racine de détection** reste à établir — c'est précisément ce que la fixture neuve doit rendre indiscutable. Poser la fixture **hors de tout run** et **élargir le critère dans le même lot** — les trois précautions de #13 s'appliquent telles quelles : copier jamais déplacer, ne pas toucher au réceptacle, déclarer la pose dans la suite.

## 4. Le parc de fixtures n'est pas gelé, et ses exclusions ne sont pas dites

- **Non gelé** : un `Cargo.toml` du parc a bougé le jour du run 3, par un développement sans rapport. Une ancre `fichier:ligne` posée dans un bloc de préconditions n'est garantie qu'à l'instant où on la lit. Deux options — figer une copie du parc, ou remplacer les ancres par des invariants vérifiables au run.
- **Exclusions muettes** : `load_dataset(` matche à l'intérieur de `venv/`. La suite ne dit nulle part qu'**un hit dans une dépendance vendorisée n'est pas un signal de stack** ; le juge du run 4 a dû l'exclure à la main. À écrire dans les préconditions communes, avec `node_modules/`, `vendor/`, `target/`, `venv/`.

## 5. La couverture retirée n'est suivie nulle part

Tous les verts d'une suite d'honnêteté s'obtiennent aussi **par retrait** : « toute source déclarée résout sur disque » se satisfait en publiant la source *ou* en supprimant la déclaration, et les correctifs de #11 ont choisi le retrait — `web-tiers` 12 → 9 cibles, `sc-css` 6 → 0. C'est légitime et voulu. Mais rien ne trace ce qui a été retiré, donc un run ultérieur lira ces PASS comme un progrès de couverture.

Slugs actuellement **`no provider`** et jamais suivis : `supabase`, `dynamodb`, `hasura`, `sequelize`, `sea-orm`, `rest-vanilla` côté data · `rust-vanilla` côté perf · les **six** de `sc-css`. Certains sont des décisions (`sc-css`, cf. `pivots-testing.md`), d'autres des dettes — et rien ne les distingue aujourd'hui. Une liste datée, avec le motif par ligne, suffit.

---

## Ce qui n'est **pas** dans cette issue

- **S9 (install) reste FAIL, délibérément.** Les quatre installeurs `sniff` ne portent aucune branche pour une source irrésoluble : c'est le défaut que S9 nomme, et le travail d'un cycle produit, pas du harnais. Le corriger ici referait la faute rattrapée en #14.
- **S12 (provenance) reste FAIL, délibérément.** Unique rouge vivant de sa suite.
- Les correctifs de #14 (cartes élargies, `pivot-map.mjs`, S8 fermée) sont livrés et hors périmètre.

## Estimation

Le point 1 est l'unité coûteuse : deux fichiers à scinder, chacun ~200 lignes dont un journal de quatre runs à déplacer sans perdre les dates. **1 à 2 sessions** pour le point 1 seul ; **2 à 3 sessions** pour l'ensemble, le point 2 étant sept réécritures de lignes indépendantes et le point 3 un contrôle négatif à mesurer avant écriture.
