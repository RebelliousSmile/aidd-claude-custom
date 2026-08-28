# web-tiers

*Règles de consommation de services SaaS tiers : Firebase, Klaviyo, GTM/Meta Pixel, Microsoft Clarity, PageSpeed Insights.*

Installe dans le projet les règles d'usage des SaaS tiers (quotas, sécurité, consentement, performance) et les data pivots associés, consommés par `data-optimize` (plugin `overcode`).

## Skills

| Skill | Déclencheur | Description |
|---|---|---|
| `setup` | `/web-tiers:setup` | Installe les règles de consommation SaaS dans `.claude/rules/` — install, verify (audit du code contre les règles), help (contexte d'intégration pour un service) |
| `cd` | `/web-tiers:cd local\|server\|automata` | Consomme un `deploy/contract.json` existant pour configurer SSH, Railway ou Heroku et générer une enveloppe GitHub/GitLab mince. Reprend la commande exacte, manuel par défaut, noms de secrets seulement. |

Couvre : Firestore (limites de requêtes, security rules, quotas), Auth listeners, Hosting (trailing slash, cache headers), Playwright + Firebase Auth, Klaviyo (subscribe 2 temps, 409→PATCH), GTM Consent Mode v2 + Meta Pixel, Microsoft Clarity (best-effort, consent-gated), PageSpeed Insights / Lighthouse (variance, métriques déterministes, checklist Nuxt 3). Data pivot : Firebase/Firestore uniquement.

## CD par cible

`web-tiers:cd` consomme une cible v2 déjà validée et ne possède aucune logique applicative. Il configure des faits fournisseur bornés pour SSH, Alwaysdata, Railway ou Heroku, et des enveloppes GitHub/GitLab minces avec ref immuable, garde de cycle de vie et concurrence par cible. Les valeurs secrètes, builds, migrations et synchronisations restent hors de ses fichiers.

## Licence

MIT — voir [LICENSE](../../LICENSE).
