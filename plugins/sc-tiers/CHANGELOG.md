# Changelog — sc-tiers

> Baseline établie le 2026-05-29 à partir de l'état courant. Détail : `git log -- plugins/sc-tiers`.

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
