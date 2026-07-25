# Action 04 — scaffold-symfony

Scaffold un projet Symfony + Docker Compose depuis zéro.

## Inputs

- `project_root` (doit être vide ou quasi-vide — voir action 01).
- Slug applicatif (nom de la base de données), version PHP cible, variante skeleton (`symfony/skeleton` API-only vs `symfony/website-skeleton` Twig+assets).

## Process

1. `composer create-project symfony/skeleton:"7.*" .` (ou `symfony/website-skeleton` si demandé — poser la question si non précisé).
2. Lire `references/docker-compose-symfony.md` et écrire `docker-compose.yml`, `docker/php.Dockerfile`, `docker/nginx.conf`, en substituant les placeholders.
3. Lire `references/compose-project-name-guard.md` et écrire `scripts/start.ps1` / `scripts/stop.ps1`, avec `{{START_COMMAND}}` = `docker compose up -d --build` et `{{STOP_COMMAND}}` = `docker compose down`.
4. Aligner `DATABASE_URL` dans `.env.local` (jamais committer ce fichier) sur la valeur du service `db` du docker-compose.
5. Ne PAS lancer `docker compose up` automatiquement — le confirmer à l'utilisateur.

## Outputs

```
docker-compose.yml
docker/php.Dockerfile
docker/nginx.conf
scripts/start.ps1
scripts/stop.ps1
.env.local
```

## Test

`pnpm run start` (ou exécution directe de `scripts/start.ps1`) démarre les conteneurs sans erreur de nom de projet Docker Compose, et `docker compose exec app php bin/console --version` répond.
