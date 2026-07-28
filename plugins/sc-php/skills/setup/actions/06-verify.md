# Verify

Sanity checks post-scaffold. À exécuter après `02/03/04-scaffold-*` et, si câblé, après `05-wire-deploy`.

## Inputs

- `framework` résolu.
- `project_root`.

## Process

1. **Docker Compose up** : lancer `scripts/start.ps1` et confirmer que les conteneurs démarrent sans erreur de nom de projet (`references/pitfalls.md` #1).
2. **CLI applicative répond** :
   - WordPress → `pnpm dlx @wordpress/env run cli wp core version`
   - Laravel → `docker compose exec app php artisan --version`
   - Symfony → `docker compose exec app php bin/console --version`
3. **Si déploiement câblé** : `pnpm deploy <cible> --no-db` en dry-run mental (vérifier que `deploy-targets.mjs` contient bien la cible, ne pas exécuter de vrai transfert sans confirmation explicite de l'utilisateur si la cible est une cible réelle et non un exemple).
4. Rapporter un résumé pass/fail par vérification — jamais de "tout est bon" silencieux si une étape a été sautée (ex: pas de cible de déploiement configurée).

## Outputs

Résumé texte des vérifications, avec statut par étape.

## Test

Chaque vérification listée a un statut explicite (`ok`, `échec`, ou `non applicable` avec raison) — aucune étape non rapportée.
