# Changelog — sc-tiers

## [0.5.0] — 2026-08-28

- Contrat v2 par cible, profil Alwaysdata, enveloppes automata à ref immuable, garde distante et concurrence isolée.

## [0.4.0] — 2026-08-28

### Added

- Skill `cd` qui consomme la commande d'un contrat projet validé pour SSH, Railway, Heroku, GitHub Actions et GitLab CI.
- Adaptateurs minces, déclenchement manuel par défaut, propagation du code de sortie et déclaration des seuls noms de secrets.

> Baseline établie le 2026-05-29 à partir de l'état courant. Détail : `git log -- plugins/sc-tiers`.

## [0.3.2] — 2026-08-05

### Changed — `pivot-install-scenarios.md` : S8 est fermée, S9 la remplace comme rouge vivant

Comme en 0.3.1, aucune action, référence ou skill n'est touchée : le lot est entièrement dans la suite behave. **Run 4, juge en contexte neuf : 7 PASS · 0 FAIL sur les 7 lignes en décompte (S1, S3–S8).** S8 passe de **FAIL 4/4** à **PASS 4/4** — marqueur d'exemple à l'intérieur de la clôture *Case A* et contre-instruction au-dessus, sur les quatre installeurs `sniff`.

**S9 est ajoutée avant le run, pas après.** Fermer S8 laissait la famille *frozen output* sans rouge ; la famille *déclaration de source manquante* n'en avait plus depuis le correctif de S7 au run 2. S9 juge les **quatre** installeurs qui ne portent aucune branche pour une source **irrésoluble** — S1 juge le seul plugin qui la porte. Écrite et mesurée le 2026-08-05 (annexe datée), **hors décompte au run 4**, elle entre au run 5 : le cycle exact de S8, et la seule raison pour laquelle son verdict du run 3 valait quelque chose. Mesure d'origine : **0 branche sur 4**, 32/32 sources résolvant sur disque.

- **Le seul quasi-manqué est une branche de la mauvaise cible** : `If the target file does not exist → install` gouverne la **cible**, jamais la source. Le critère de S9 le dit en forme générique, sans citer la mesure — contrat `behave` 4.3.0.
- **Une clause a été posée puis retirée, et l'épisode est consigné.** Les quatre installeurs avaient brièvement reçu la branche manquante, dans la même vague d'édition qui fermait S8 — ce qui aurait rendu S9 verte à la naissance. *Une ligne écrite contre un défaut que son propre auteur vient de corriger mesure l'auteur, pas la cible.*
- **Le défaut que S9 nomme n'est pas corrigé, délibérément** : c'est le travail du cycle suivant.

### Fixed — deux frictions du run 3 appliquées, trois frictions du run 4 consignées sans correctif

- **Le juge du run 4 a lu l'annexe avant de noter, et c'est enregistré contre le run.** Un seul `Read` charge tout le fichier : critères, annexe et journal partagent un même document. Le juge l'a déclaré et a reconstruit chaque verdict depuis les sources primaires — atténuation, pas garantie. **Les verdicts de ce run sont plus faibles que ceux du run 3 d'exactement cela.** Deuxième run à buter sur le mur ; le remède est structurel — scinder le fichier — et c'est le premier point de l'issue de harnais, pas une instruction à répéter plus fort.
- **S3 : le comportement attendu de la ligne n'a pas été reproduit comme faux.** Le run 3 tenait que sur la fixture WordPress le texte annoncerait Laravel et Eloquent installés ; tracé cette fois contre `wp-2026`, `01-scan.md` n'arme jamais Laravel. Non reproduit ≠ réfuté — le juge a dû quitter le chemin de chargement déclaré pour le vérifier, ce qui est en soi le constat.
- **S4 ne discrimine toujours rien que S3 et S5 ne fassent** — troisième run consécutif où c'est écrit. **S7 passe, mais sa branche vit dans la prose de préambule, hors de la procédure numérotée qu'un agent exécute** : les deux lectures se défendent sur le texte actuel, ce qui est le défaut.

## [0.3.1] — 2026-08-03

### Changed — `pivot-install-scenarios.md` : le contrôle négatif est jugé, et il est rouge

Aucune action, référence ou skill n'est touchée par cette version : le lot est entièrement dans la suite behave. La 0.3.0 avait ajouté **S8** — le corps illustré du bloc *Case A* des quatre installeurs `sniff` lu comme la liste à reproduire — en le laissant explicitement **non jugé**, faute de quoi un run 2 tout-vert aurait clos la famille *frozen output* sans qu'aucun rouge n'y survive.

**Run 3 (2026-08-03) : 6 PASS · 1 FAIL · 1 N/A sur 8**, juge en contexte neuf, auteur ni de la suite ni des correctifs. Le FAIL est S8, sur les quatre fichiers. **C'est le résultat attendu** : un run 3 qui aurait rendu 0 FAIL aurait jugé le contrôle négatif à côté.

- **Aucune des deux formes admises n'est présente** : pas de marqueur d'exemple dans un seul bloc *Case A*, et la clause existante dit l'inverse — `Pick the **header** by what actually happened`, le corps n'étant jamais mentionné.
- **Circonstance que le run 2 n'avait pas relevée** : la seule instruction de reproduction des quatre fichiers pointe dans le mauvais sens — **`Use this header verbatim`**, dans chaque *Case B*. Les fichiers posent une norme de copie littérale sur un bloc et ne posent jamais la contre-instruction sur l'autre.
- **Le classement d'exposition est révisé.** Le run 2 désignait `sc-rust` (corps à 75 %, qui *se lit* comme exhaustif) ; le run 3 mesure que `sc-php` à **6/6 l'est** — une copie littérale y est indiscernable d'une sortie dérivée, aucune ligne manquante ne la trahit, et sur la fixture WordPress de S3 cette copie affirme `perf-pivots-laravel.md (installed)` et `data-pivots-eloquent.md (installed)`. Les deux classements tiennent sur des axes différents : l'un sous-déclare, l'autre certifie faux. L'ordre des remèdes suit le second.

### Fixed — deux défauts de harnais dans la suite elle-même

- **S8 annonçait son verdict dans sa case *Pass criteria***, c'est-à-dire le défaut même que la révision précédente prétendait clore en retirant la colonne *Instruction pinned* — reparu deux colonnes plus à gauche, et sur la seule ligne que ce run devait adjuger de façon indépendante. Les mesures partent en appendice daté ; le critère ne décrit plus que ce qu'il faut chercher.
- **Le marqueur d'exemple n'était pas cadré.** Un grep non borné de l'ellipse remonte un résultat dans chacun des quatre fichiers — dans la prose des *Case B* et *C*, où l'ellipse tient lieu de chemin de fichier. Un juge s'arrêtant là note S8 verte partout, soit le verdict inverse du bon. La recherche est désormais bornée au bloc *Case A*.

Laissés ouverts délibérément : le fichier n'est pas scindé (critères / registres), l'*Expected behaviour* de S3 reste une assertion fausse sur la fixture qu'elle nomme, S4 duplique le critère de S5 — et **S8 reste rouge**, seul rouge vivant de sa famille : le fermer avant le run suivant répéterait ce que le run 2 a fait.

## [0.3.0] — 2026-08-03

### Removed — trois data pivots déclarés que le plugin n'a jamais contenus

`setup/01-install.md` déclarait quatre cibles de data pivots. Une seule avait un fichier source derrière. Les trois autres promettaient un remède qui ne s'installerait jamais :

- `.claude/rules/07-quality/data-pivots-supabase.md`
- `.claude/rules/07-quality/data-pivots-dynamodb.md`
- `.claude/rules/07-quality/data-pivots-hasura.md`

La `0.2.1` avait déjà retiré ces trois noms du `README.md` et de `marketplace.json` en constatant qu'ils n'existaient pas — mais elle avait laissé la **table d'installation**, c'est-à-dire le seul endroit où la fausse promesse était opérante. Le remède retenu est le retrait de la déclaration, l'autre branche (écrire les trois pivots) étant une décision produit qui n'a pas été prise.

**Conséquence pour un projet** : `data-optimize` sur une stack Supabase, DynamoDB ou Hasura ne rendra plus `not installed` avec `/sc-tiers:setup` en remède — il rendra `no provider`, ce qui est vrai. Aucun projet ne perd de fichier : ces trois n'ont jamais été écrits nulle part.

### Fixed — la sortie rend ce qui a été écrit, pas ce que la table liste

Le bloc de sortie annonçait `12 files written` en dur et énumérait les douze cibles déclarées, quel que soit le nombre de fichiers réellement écrits. Un run qui n'écrivait rien rendait donc le même rapport qu'un run complet.

- Le compte est dérivé (`<n> files written`), l'énumération porte les cibles **effectivement touchées**, avec leur issue (`written` / `skipped — identical`), et un marqueur d'exemple empêche de recopier la liste comme si elle était la sortie.
- Une source qui ne résout pas est rendue **manquante**, jamais écrite. Si toutes manquent, l'en-tête est `❌ sc-tiers rules — nothing written` : « installé » n'est plus prononçable à vide.

### Added

- `skills/setup/evals/pivot-install-scenarios.md` — 8 scénarios behave sur l'honnêteté des installeurs de la marketplace, registre append-only. Run 1 (2026-07-31) : 1 PASS / 6 FAIL. Run 2 (2026-08-03), sur le code corrigé : 6 PASS / 1 N/A.

  Le run 2 tout-vert a lui-même produit le défaut suivant : la suite ne prouvait plus rien d'un défaut *nouveau*. D'où **S8, contrôle négatif non encore jugé** — le bloc de sortie *Case A* des quatre installeurs `sniff` (`sc-js`, `sc-php`, `sc-python`, `sc-rust`) lu à côté de celui de `setup`. Mesure : **0 des 4** porte le marqueur d'exemple de `01-install.md:42`, celui qui empêche de recopier un corps illustré comme si c'était la liste des fichiers écrits ; la couverture du corps illustré va de 6/6 (`sc-php`) à 3/13 (`sc-js`). La suite perd par ailleurs sa colonne *Instruction pinned* (les citations partent en appendice daté) conformément au contrat `behave` 4.3.0.

## [0.2.2] — 2026-07-28

### Changed

- **Les titres `H1` des actions ne portent plus leur numéro** — `# Explain`, plus `# Action 01 — explain`. Le numéro vivait à trois endroits, il n'en occupe plus que deux : le nom de fichier et la table de `SKILL.md`, que le gate de cohérence du marketplace compare désormais. Changement transversal aux onze plugins, détaillé dans le journal du marketplace (3.4.0).

## [0.2.1] — 2026-07-25

### Fixed
- **`README.md` et `marketplace.json`** — retirait la mention de data pivots Supabase, DynamoDB et Hasura : ces trois n'ont jamais existé dans le plugin, seul un data pivot Firebase/Firestore (`skills/setup/references/08-data-pivots-firebase.md`) est réellement implémenté. La fausse mention datait de l'entrée baseline `0.2.0` ci-dessous, non corrigée pour préserver l'historique.

## [0.2.0] — 2026-05-29 (baseline)

Règles de consommation de SaaS tiers. Skill unique : `setup` (actions install / verify / help).

Couverture : Firebase (Firestore query limits, security rules, quotas, Auth listeners, Hosting trailing slash & cache, Playwright Firebase auth), Klaviyo (subscribe 2 temps, 409→PATCH), GTM Consent Mode v2 + Meta Pixel, Microsoft Clarity (best-effort, consent-gated, E2E), PageSpeed Insights / Lighthouse (variance, métriques déterministes, checklist Nuxt 3). Data pivots : Supabase, DynamoDB, Hasura, Firebase.

## Antérieur
- Voir `git log -- plugins/sc-tiers` pour l'historique complet.
