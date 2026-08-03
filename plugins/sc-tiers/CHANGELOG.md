# Changelog — sc-tiers

> Baseline établie le 2026-05-29 à partir de l'état courant. Détail : `git log -- plugins/sc-tiers`.

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
