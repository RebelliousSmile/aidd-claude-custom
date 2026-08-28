# Verify

Sanity checks post-scaffold. À exécuter après `02/03/04-scaffold-*` et, si câblé, après `05-wire-deploy`.

## Inputs

- `framework` résolu.
- `project_root`.

## Process

1. **Docker Compose up** : lancer `scripts/start.ps1` et confirmer que les conteneurs démarrent sans erreur de nom de projet (`references/pitfalls.md` #1).
2. **CLI applicative répond** :
   - WordPress → `pnpm wp core version` (wrapper `scripts/wp.ps1`, jamais `pnpm dlx @wordpress/env run cli wp` nu — voir `references/compose-project-name-guard.md`)
   - Laravel → `docker compose exec app php artisan --version`
   - Symfony → `docker compose exec app php bin/console --version`
3. **Le site rend quelque chose** — vérification distincte de la précédente, qui passe sur un site blanc :
   - WordPress → `pnpm wp theme status <slug>` doit rendre `Status: Active`, et la page d'accueil doit contenir `wp-site-blocks`. Un thème block dont les templates sont vides sert un HTTP 200 à zéro caractère : l'étape 2 ne le distingue pas d'un scaffold réussi.
   - Laravel / Symfony → la page d'accueil doit rendre la page de bienvenue du framework, pas seulement un code 200.
4. **Styles design front + éditeur (WordPress)** : la réponse front contient le handle
   `<slug>-design-css`, et `pnpm wp eval` confirme que `editor-styles` référence exactement
   `assets/css/design/index.css`. L'un sans l'autre est un échec.
5. **Si livraison câblée** : vérifier que `composer deploy:prod` correspond textuellement à `deploy/contract.json`, qu'une seule implémentation est possédée et que ses preflight, preuve et récupération sont déclarés. Ne jamais exécuter de transfert réel pendant cette vérification.
6. Rapporter un résumé pass/fail par vérification — jamais de "tout est bon" silencieux si une étape a été sautée (ex: pas de cible de déploiement configurée).

## Outputs

Résumé texte des vérifications, avec statut par étape.

## Test

Chaque vérification listée a un statut explicite (`ok`, `échec`, ou `non applicable` avec raison) — aucune étape non rapportée.
